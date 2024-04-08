#!/usr/bin/env python3
# www.jrodal.com

import logging
import asyncio

from typing import Optional

from tldrwl.ai_interface import AiInterface, Summary
from tldrwl.summarizers.text_summarizer import TextSummarizer
from tldrwl.summarizers.chat_completions_text_summarizer import ChatCompletionsTextSummarizer
from tldrwl.transformers.webpage_transformer import WebpageTransformer
from tldrwl.transformers.youtube_transformer import YoutubeTransformer


class Summarizer(AiInterface):
    def __init__(self, *, text_summarizer: Optional[TextSummarizer] = None) -> None:
        super().__init__()
        self._logger = logging.getLogger(__name__)
        self._summarizer = text_summarizer or ChatCompletionsTextSummarizer()

    async def _transform_text(self, text: str) -> str:
        if YoutubeTransformer.is_youtube_url(text):
            self._logger.debug(f"Using YoutubeSummarizer on {text}")
            return await YoutubeTransformer(text).get_text()
        elif WebpageTransformer.is_url(text):
            self._logger.debug(f"Using WebpageSummarizer on {text}")
            return await WebpageTransformer(text).get_text()
        elif len(text) < 500:
            self._logger.debug("Text is short... searching for urls")
            urls = WebpageTransformer.extract_urls(text)
            transformed = await asyncio.gather(
                *[self._transform_text(url) for url in urls]
            )
            # TODO: exact text replacement for edge-case scenarios like this:
            # https://www.jrodal.com/
            # https://www.jrodal.com/posts/how-to-deploy-rocket-rust-web-app-on-vps/
            for url, transform in zip(urls, transformed):
                self._logger.debug(f"Injecting content from {url}")
                text = text.replace(url, transform)
            return text

        else:
            self._logger.debug("Applying no further transformations to text")
            return text

    async def _summarize_async(self, text: str) -> Summary:
        transformed_text = await self._transform_text(text)
        return await self._summarizer.summarize_async(transformed_text)
