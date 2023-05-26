#!/usr/bin/env python3
# www.jrodal.com

import re

import openai

from tldrwl.ai_interface import Model, Summary
from tldrwl.summarizers.text_summarizer import TextSummarizer


class TextAda001TextSummarizer(TextSummarizer):
    MAX_TOKEN_RESPONSE = 750
    MAX_TOKEN_INPUT = 125

    def __init__(
        self,
        *,
        model: Model = Model.TEXTADA001,
        prompt_string: str = "Write a detailed summary of the following:\n\n{}\n",
        chunk_size: int = 6000,
        max_num_chunks: int = 10,
    ) -> None:
        super().__init__(
            model=model,
            prompt_string=prompt_string,
            chunk_size=chunk_size,
            max_num_chunks=max_num_chunks,
        )

    async def _query_openai(self, text: str, max_tokens: int) -> Summary:
        prompt = self._prompt_string.format(text)
        response = openai.Completion.create(  # type: ignore
            model=self._model.value, prompt=prompt, max_tokens=max_tokens
        )
        output_text = response.choices[0].text.strip()  # type: ignore
        num_tokens = response["usage"]["total_tokens"]  # type: ignore
        self._logger.debug(f"{num_tokens=}")

        summary = re.sub(r"\s+", " ", output_text.strip())  # type: ignore
        return Summary(
            text=summary,
            num_tokens=num_tokens,  # type: ignore
            model=self._model,
        )
