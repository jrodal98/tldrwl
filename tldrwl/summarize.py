#!/usr/bin/env python3
# www.jrodal.com

import logging

from .ai_interface import AiInterface, Summary
from .gpt_35_turbo_text_summarizer import Gpt35TurboTextSummarizer
from .summarize_webpage import WebpageSummarizer
from .summarize_youtube import YoutubeSummarizer


class Summarizer(AiInterface):
    def __init__(self) -> None:
        super().__init__()
        self._logger = logging.getLogger(__name__)

    def get_summarizer(self, text: str) -> AiInterface:
        if YoutubeSummarizer.get_video_id(text):
            self._logger.debug("Using YoutubeSummarizer")
            return YoutubeSummarizer()
        elif WebpageSummarizer.is_url(text):
            self._logger.debug("Using WebpageSummarizer")
            return WebpageSummarizer()
        else:
            self._logger.debug("Using Gpt35TurboTextSummarizer")
            return Gpt35TurboTextSummarizer()

    async def _summarize_async(self, text: str) -> Summary:
        summarizer = self.get_summarizer(text)
        return await summarizer.summarize_async(text)
