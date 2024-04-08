#!/usr/bin/env python3
# www.jrodal.com

import re

from openai import AsyncOpenAI
from tldrwl.summarizers.text_summarizer import TextSummarizer

from tldrwl.ai_interface import Summary

aclient = AsyncOpenAI()


class ChatCompletionsTextSummarizer(TextSummarizer):
    MAX_TOKEN_RESPONSE = 1500

    async def _query_openai(self, text: str, max_tokens: int) -> Summary:
        prompt = self._prompt_string.format(text)
        completion = await aclient.chat.completions.create(
            model=self._model.value,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
        )
        output_text = completion.choices[0].message.content
        prompt_tokens = completion.usage.prompt_tokens  # type: ignore
        completion_tokens = completion.usage.completion_tokens  # type: ignore

        self._logger.debug(f"{prompt_tokens=}, {completion_tokens=}")

        summary = re.sub(r"\s+", " ", output_text.strip())  # type: ignore
        return Summary(
            text=summary,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            model=self._model,
        )
