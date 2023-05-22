#!/usr/bin/env python3
# www.jrodal.com


from dataclasses import dataclass
import re
import textwrap
from typing import List

import openai

from ai_interface import AiInterface


@dataclass
class TextSummary:
    final_summary: str
    chunk_summaries: List[str]


class TextSummarizer(AiInterface):
    def __init__(
        self,
        *,
        model: str = "text-davinci-003",
        prompt_string: str = "Write a detailed summary of the following:\n\n{}\n"
    ) -> None:
        self.model = model
        self.prompt_string = prompt_string

    def _summarize_chunk(self, chunk: str, max_tokens: int = 256) -> str:
        prompt = self.prompt_string.format(chunk)

        response = openai.Completion.create(  # type: ignore
            model="text-davinci-003", prompt=prompt, max_tokens=max_tokens
        )
        summary = re.sub(r"\s+", " ", response.choices[0].text.strip())  # type: ignore
        return summary

    def summarize_text(self, text: str) -> TextSummary:
        text_length = len(text)

        # This is done to reduce overall amount of API calls
        chunk_size = 4000 if text_length >= 25000 else 2000

        # Wrap the transcript in chunks of characters
        chunks = textwrap.wrap(text, chunk_size)

        summaries = [self._summarize_chunk(chunk) for chunk in chunks]
        final_summary = self._summarize_chunk(" ".join(summaries), max_tokens=2056)

        return TextSummary(final_summary=final_summary, chunk_summaries=summaries)
