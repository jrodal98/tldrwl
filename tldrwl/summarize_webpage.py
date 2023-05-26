#!/usr/bin/env python3
# www.jrodal.com

import re
import logging
import bs4
import aiohttp
from typing import Pattern

from .ai_interface import AiInterface, Summary
from .summarize_text import TextSummarizer


class WebpageSummarizer(AiInterface):
    _pattern: Pattern[str] = re.compile(
        r"^(?:http|ftp)s?://"  # http:// or https://
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # noqa domain
        r"localhost|"  # localhost...
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
        r"(?::\d+)?"  # optional port
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )

    def __init__(self) -> None:
        super().__init__()
        self._text_summarizer = TextSummarizer()
        self._logger = logging.getLogger(__name__)

    @classmethod
    def is_url(cls, text: str) -> bool:
        return cls._pattern.match(text) is not None

    async def _get_page_text_async(self, url: str) -> str:
        self._logger.debug(f"Getting page text for {url}")
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                soup = bs4.BeautifulSoup(await response.text(), "html.parser")
                page_text = soup.get_text()
                self._logger.debug(f"Done getting page text for {url}")
                return page_text

    async def _summarize_async(self, text: str) -> Summary:
        page_text = await self._get_page_text_async(text)
        return await self._text_summarizer.summarize_async(page_text)
