#!/usr/bin/env python3
# www.jrodal.com

import re

import openai

from tldrwl.summarizers.text_summarizer import TextSummarizer

from tldrwl.ai_interface import Summary


class Gpt35TurboTextSummarizer(TextSummarizer):
    MAX_TOKEN_RESPONSE = 1500

    async def _query_openai(self, text: str, max_tokens: int) -> Summary:
        prompt = self._prompt_string.format(text)
        response = await openai.ChatCompletion.acreate(  # type: ignore
            model=self._model.value,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
        )
        output_text = response["choices"][0]["message"]["content"]  # type: ignore
        num_tokens = response["usage"]["total_tokens"]  # type: ignore
        self._logger.debug(f"{num_tokens=}")

        summary = re.sub(r"\s+", " ", output_text.strip())  # type: ignore
        return Summary(
            text=summary,
            num_tokens=num_tokens,  # type: ignore
            model=self._model,
        )
