#!/usr/bin/env python3
# www.jrodal.com

import logging
import bs4
import requests
import aiohttp

from .ai_interface import AiInterface
from .summarize_text import TextSummarizer, TextSummary


class WebpageSummarizer(AiInterface):
    def __init__(self) -> None:
        super().__init__()
        self._text_summarizer = TextSummarizer()
        self._logger = logging.getLogger(__name__)

    def _get_page_text(self, url: str) -> str:
        self._logger.debug(f"Getting page text for {url}")
        response = requests.get(url)
        response.raise_for_status()
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        page_text = soup.get_text()
        self._logger.debug(f"Done getting page text for {url}")
        return page_text

    async def _get_page_text_async(self, url: str) -> str:
        self._logger.debug(f"Getting page text for {url}")
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                soup = bs4.BeautifulSoup(await response.text(), "html.parser")
                page_text = soup.get_text()
                self._logger.debug(f"Done getting page text for {url}")
                return page_text

    async def summarize_webpage_async(self, url: str) -> TextSummary:
        page_text = await self._get_page_text_async(url)
        return await self._text_summarizer.summarize_text_async(page_text)

    def summarize_webpage(self, url: str) -> TextSummary:
        page_text = self._get_page_text(url)
        return self._text_summarizer.summarize_text(page_text)
