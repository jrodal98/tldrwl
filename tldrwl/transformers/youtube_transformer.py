#!/usr/bin/env python3
# www.jrodal.com

import logging
import re
from typing import Optional, Pattern

from youtube_transcript_api import YouTubeTranscriptApi  # pyright: ignore
from youtube_transcript_api.formatters import TextFormatter  # pyright: ignore

from tldrwl.transformers.transformer import Transformer

from tldrwl.exception import TldrwlVideoUrlParsingException
from tldrwl.transformers.webpage_transformer import WebpageTransformer


class YoutubeTransformer(Transformer):
    _pattern: Pattern[str] = re.compile(
        r"(?:[?&]v=|\/embed\/|\/1\/|\/v\/|https:\/\/(?:www\.)?youtu\.be\/)([^&\n?#]+)"
    )

    def __init__(self, url: str) -> None:
        super().__init__()
        self._url = url
        self._logger = logging.getLogger(__name__)

    @classmethod
    def is_youtube_url(cls, url: str) -> bool:
        return WebpageTransformer.is_url(url) and cls.get_video_id(url) is not None

    @classmethod
    def get_video_id(cls, url: str) -> Optional[str]:
        match = cls._pattern.search(url)
        if match:
            return match.group(1)
        return None

    async def get_text(self) -> str:
        video_id = self.get_video_id(self._url)
        if not video_id:
            raise TldrwlVideoUrlParsingException.make_error(video_url=self._url)
        self._logger.debug(f"Getting transcript for {video_id}")
        transcript = YouTubeTranscriptApi.get_transcript(video_id)  # type: ignore
        self._logger.debug(f"Done getting transcript for {video_id}")
        return TextFormatter().format_transcript(transcript)  # type: ignore
