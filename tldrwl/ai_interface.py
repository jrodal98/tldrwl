#!/usr/bin/env python3
# www.jrodal.com

from abc import ABC, abstractmethod
import asyncio
from dataclasses import dataclass
from enum import Enum

from tldrwl.exception import TldrwlAsyncioRunInEventLoop, TldrwlException
from tldrwl.register import Register


class Model(Enum):
    GPT35TURBO = "gpt-3.5-turbo"

    @property
    def cost_per_1000_tokens(self) -> float:
        if self is self.GPT35TURBO:
            return 0.002
        else:
            return 0


@dataclass
class Summary:
    text: str
    num_tokens: int
    model: Model

    @property
    def estimated_cost_usd(self) -> float:
        return self.num_tokens * self.model.cost_per_1000_tokens * (1 / 1000)


class AiInterface(ABC):
    @abstractmethod
    async def _summarize_async(self, text: str) -> Summary:
        pass

    def summarize_sync(self, text: str) -> Summary:
        try:
            return asyncio.run(self.summarize_async(text))
        except RuntimeError as e:
            if "asyncio.run() cannot be called from a running event loop" in str(e):
                raise TldrwlAsyncioRunInEventLoop.make_error(str(e)) from e
            else:
                raise

    async def summarize_async(self, text: str) -> Summary:
        if not Register.is_registered():
            Register.register()
        try:
            return await self._summarize_async(text)
        except TldrwlException:
            raise
        except Exception as e:
            raise TldrwlException(msg=str(e), cause="n/a", remediation="n/a") from e
