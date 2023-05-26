#!/usr/bin/env python3
# www.jrodal.com

import logging

from .ai_interface import AiInterface, Summary
from .gpt_35_turbo_text_summarizer import Gpt35TurboTextSummarizer
from .webpage_transformer import WebpageTransformer
from .youtube_transformer import YoutubeTransformer


class Summarizer(AiInterface):
    def __init__(self) -> None:
        super().__init__()
        self._logger = logging.getLogger(__name__)
        self._summarizer = Gpt35TurboTextSummarizer()

    async def _transform_text(self, text: str) -> str:
        if YoutubeTransformer.get_video_id(text):
            self._logger.debug("Using YoutubeSummarizer")
            return await YoutubeTransformer(text).get_text()
        elif WebpageTransformer.is_url(text):
            self._logger.debug("Using WebpageSummarizer")
            return await WebpageTransformer(text).get_text()
        else:
            self._logger.debug("Applying no transformations to text")
            return text

    async def _summarize_async(self, text: str) -> Summary:
        transformed_text = await self._transform_text(text)
        return await self._summarizer.summarize_async(transformed_text)
