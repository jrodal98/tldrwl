#!/usr/bin/env python3
# www.jrodal.com

import re
import logging
import bs4
import aiohttp
from typing import Pattern, Set

from tldrwl.transformers.transformer import Transformer


class WebpageTransformer(Transformer):
    _pattern: Pattern[str] = re.compile(
        r"^(?:http|ftp)s?://"  # http:// or https://
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # noqa domain
        r"localhost|"  # localhost...
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
        r"(?::\d+)?"  # optional port
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )

    def __init__(self, url: str) -> None:
        super().__init__()
        self._url = url
        self._logger = logging.getLogger(__name__)

    @classmethod
    def extract_urls(cls, text: str) -> Set[str]:
        urls: Set[str] = set()
        for word in text.split():
            url = cls._pattern.search(word)
            if url:
                urls.add(url.group())
        return urls

    @classmethod
    def is_url(cls, text: str) -> bool:
        return cls._pattern.match(text) is not None

    async def get_text(self) -> str:
        self._logger.debug(f"Getting page text for {self._url}")
        async with aiohttp.ClientSession() as session:
            async with session.get(self._url) as response:
                response.raise_for_status()
                soup = bs4.BeautifulSoup(await response.text(), "html.parser")
                page_text = soup.get_text()
                self._logger.debug(f"Done getting page text for {self._url}")
                return page_text
