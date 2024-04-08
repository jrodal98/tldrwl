#!/usr/bin/env python3
# www.jrodal.com

from abc import abstractmethod
import asyncio
import logging
import textwrap
from typing import List

import openai

from tldrwl.ai_interface import AiInterface, Model, Summary
from tldrwl.exception import TldrwlNoSummaryError, TldrwlRateLimitError


class TextSummarizer(AiInterface):
    MAX_TOKEN_RESPONSE: int = 1500
    MAX_TOKEN_INPUT: int = 250

    def __init__(
        self,
        *,
        model: Model | None = None,
        prompt_string: str = "Write a detailed summary of the following:\n\n{}\n",
        chunk_size: int = 12000,
        max_num_chunks: int = 10,
    ) -> None:
        super().__init__()
        self._model = model or Model.default_model()
        self._prompt_string = prompt_string
        self._chunk_size = chunk_size
        self._max_num_chunks = max_num_chunks
        self._logger = logging.getLogger(__name__)

    @abstractmethod
    async def _query_openai(self, text: str, max_tokens: int) -> Summary:
        pass

    async def _summarize_chunk_async(self, chunk: str, max_tokens: int) -> Summary:
        for _ in range(0, 3):
            try:
                return await self._query_openai(chunk, max_tokens)
            except openai.RateLimitError:  # pyright: ignore
                retry_interval = 3
                self._logger.debug(
                    f"Rate limited by openai - resting for {retry_interval}s"
                )
                await asyncio.sleep(retry_interval)

        raise TldrwlRateLimitError.make_error("Rate limited after 3 attempts")

    def _get_chunks(self, text: str) -> List[str]:
        text_length = len(text)
        self._logger.debug(f"{text_length=}")

        chunks = textwrap.wrap(text, self._chunk_size)[: self._max_num_chunks]
        num_chunks = len(chunks)
        self._logger.debug(f"{num_chunks=}")

        return chunks

    async def _summarize_async(self, text: str) -> Summary:
        chunks = self._get_chunks(text)
        summaries = await asyncio.gather(
            *[
                self._summarize_chunk_async(chunk, max_tokens=self.MAX_TOKEN_INPUT)
                for chunk in chunks
            ]
        )
        if len(summaries) == 0:
            raise TldrwlNoSummaryError(
                msg=f"No summary was generatd for {text}",
                cause="I don't know",
                remediation="I don't know",
            )
        elif len(summaries) == 1:
            return summaries[0]
        else:
            final_input = " ".join(s.text for s in summaries)
            # TODO: recursively summarize if it is still too big instead
            # of hoping that this will work - maybe catch this exception?
            # noqa openai.error.InvalidRequestError: This model's maximum context length is 4097 tokens. However, you requested 4612 tokens (3112 in the messages, 1500 in the completion). Please reduce the length of the messages or completion.
            final_summary = await self._summarize_chunk_async(
                final_input, max_tokens=self.MAX_TOKEN_RESPONSE
            )
            return Summary(
                text=final_summary.text,
                prompt_tokens=final_summary.prompt_tokens
                + sum(s.prompt_tokens for s in summaries),
                completion_tokens=final_summary.completion_tokens
                + sum(s.completion_tokens for s in summaries),
                model=self._model,
            )
