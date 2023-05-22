#!/usr/bin/env python3
# www.jrodal.com

import asyncio
from dataclasses import dataclass
from enum import Enum
import logging
import re
import textwrap

import openai
from typing import List, Dict, Any

from .ai_interface import AiInterface


class Model(Enum):
    GPT35TURBO = "gpt-3.5-turbo"

    @property
    def cost_per_1000_tokens(self) -> float:
        if self is self.GPT35TURBO:
            return 0.002
        else:
            return 0


@dataclass
class TextSummary:
    summary: str
    num_tokens: int
    model: Model

    @property
    def estimated_cost_usd(self) -> float:
        return self.num_tokens * self.model.cost_per_1000_tokens * (1 / 1000)


class TextSummarizer(AiInterface):
    def __init__(
        self,
        *,
        model: Model = Model.GPT35TURBO,
        prompt_string: str = "Write a detailed summary of the following:\n\n{}\n",
        chunk_size: int = 8000,
        max_num_chunks: int = 15,
    ) -> None:
        self._model = model
        self._prompt_string = prompt_string
        self._chunk_size = chunk_size
        self._max_num_chunks = max_num_chunks
        self._logger = logging.getLogger(__name__)

    def _response_to_text_summary(self, response: Dict[str, Any]) -> TextSummary:
        output_text = response["choices"][0]["message"]["content"]  # type: ignore
        num_tokens = response["usage"]["total_tokens"]  # type: ignore
        self._logger.debug(f"{num_tokens=}")

        summary = re.sub(r"\s+", " ", output_text.strip())  # type: ignore
        return TextSummary(
            summary=summary,
            num_tokens=num_tokens,  # type: ignore
            model=self._model,
        )

    async def _summarize_chunk_async(self, chunk: str, max_tokens: int) -> TextSummary:
        prompt = self._prompt_string.format(chunk)

        response = await openai.ChatCompletion.acreate(  # type: ignore
            model=self._model.value,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
        )

        return self._response_to_text_summary(response)  # type: ignore

    def _summarize_chunk(self, chunk: str, max_tokens: int) -> TextSummary:
        prompt = self._prompt_string.format(chunk)

        response = openai.ChatCompletion.create(  # type: ignore
            model=self._model.value,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
        )
        return self._response_to_text_summary(response)  # type: ignore

    def _get_chunks(self, text: str) -> List[str]:
        text_length = len(text)
        self._logger.debug(f"{text_length=}")

        chunks = textwrap.wrap(text, self._chunk_size)[: self._max_num_chunks]
        num_chunks = len(chunks)
        self._logger.debug(f"{num_chunks=}")

        return chunks

    async def summarize_text_async(self, text: str) -> TextSummary:
        chunks = self._get_chunks(text)
        summaries = await asyncio.gather(
            *[self._summarize_chunk_async(chunk, max_tokens=250) for chunk in chunks]
        )
        if len(summaries) == 0:
            return TextSummary(summary="", num_tokens=0, model=self._model)
        elif len(summaries) == 1:
            return summaries[0]
        else:
            final_input = " ".join(s.summary for s in summaries)
            final_summary = await self._summarize_chunk_async(
                final_input, max_tokens=2000
            )
            return TextSummary(
                summary=final_summary.summary,
                num_tokens=final_summary.num_tokens
                + sum(s.num_tokens for s in summaries),
                model=self._model,
            )

    def summarize_text(self, text: str) -> TextSummary:
        chunks = self._get_chunks(text)

        summaries = [self._summarize_chunk(chunk, max_tokens=250) for chunk in chunks]
        if len(summaries) == 0:
            return TextSummary(summary="", num_tokens=0, model=self._model)
        elif len(summaries) == 1:
            return summaries[0]
        else:
            final_input = " ".join(s.summary for s in summaries)
            final_summary = self._summarize_chunk(final_input, max_tokens=2000)
            return TextSummary(
                summary=final_summary.summary,
                num_tokens=final_summary.num_tokens
                + sum(s.num_tokens for s in summaries),
                model=self._model,
            )
