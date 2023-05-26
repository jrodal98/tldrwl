#!/usr/bin/env python3
# www.jrodal.com

import asyncio
import logging
import re
import textwrap

import openai
from typing import List, Dict, Any

from .ai_interface import AiInterface, Model, Summary

MAX_TOKEN_RESPONSE = 1500


class TextSummarizer(AiInterface):
    def __init__(
        self,
        *,
        model: Model = Model.GPT35TURBO,
        prompt_string: str = "Write a detailed summary of the following:\n\n{}\n",
        chunk_size: int = 12000,
        max_num_chunks: int = 10,
    ) -> None:
        super().__init__()
        self._model = model
        self._prompt_string = prompt_string
        self._chunk_size = chunk_size
        self._max_num_chunks = max_num_chunks
        self._logger = logging.getLogger(__name__)

    def _response_to_text_summary(self, response: Dict[str, Any]) -> Summary:
        output_text = response["choices"][0]["message"]["content"]  # type: ignore
        num_tokens = response["usage"]["total_tokens"]  # type: ignore
        self._logger.debug(f"{num_tokens=}")

        summary = re.sub(r"\s+", " ", output_text.strip())  # type: ignore
        return Summary(
            text=summary,
            num_tokens=num_tokens,  # type: ignore
            model=self._model,
        )

    async def _summarize_chunk_async(self, chunk: str, max_tokens: int) -> Summary:
        prompt = self._prompt_string.format(chunk)

        for _ in range(0, 3):
            try:
                response = await openai.ChatCompletion.acreate(  # type: ignore
                    model=self._model.value,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens,
                )
                return self._response_to_text_summary(response)  # type: ignore
            except openai.error.RateLimitError:  # pyright: ignore
                retry_interval = 3
                self._logger.debug(
                    f"Rate limited by openai - resting for {retry_interval}s"
                )
                await asyncio.sleep(retry_interval)

        return Summary(text="", num_tokens=0, model=self._model)

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
            *[self._summarize_chunk_async(chunk, max_tokens=250) for chunk in chunks]
        )
        if len(summaries) == 0:
            return Summary(text="", num_tokens=0, model=self._model)
        elif len(summaries) == 1:
            return summaries[0]
        else:
            final_input = " ".join(s.text for s in summaries)
            # TODO: recursively summarize if it is still too big instead
            # of hoping that this will work - maybe catch this exception?
            # noqa openai.error.InvalidRequestError: This model's maximum context length is 4097 tokens. However, you requested 4612 tokens (3112 in the messages, 1500 in the completion). Please reduce the length of the messages or completion.
            final_summary = await self._summarize_chunk_async(
                final_input, max_tokens=MAX_TOKEN_RESPONSE
            )
            return Summary(
                text=final_summary.text,
                num_tokens=final_summary.num_tokens
                + sum(s.num_tokens for s in summaries),
                model=self._model,
            )
