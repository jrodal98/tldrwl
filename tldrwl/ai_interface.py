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
    GPT4 = "gpt-4"

    @property
    def cost_per_1000_prompt_tokens(self) -> float:
        if self is self.GPT35TURBO:
            return 0.0005
        elif self is self.GPT4:
            return 0.03
        else:
            return 0

    @property
    def cost_per_1000_completion_tokens(self) -> float:
        if self is self.GPT35TURBO:
            return 0.0015
        elif self is self.GPT4:
            return 0.06
        else:
            return 0

    @classmethod
    def default_model(cls) -> "Model":
        return cls.GPT35TURBO


@dataclass
class Summary:
    text: str
    prompt_tokens: int
    completion_tokens: int
    model: Model

    @property
    def estimated_cost_usd(self) -> float:
        return (
            (self.prompt_tokens * self.model.cost_per_1000_prompt_tokens)
            + (self.completion_tokens * self.model.cost_per_1000_completion_tokens)
        ) * (1 / 1000)


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
