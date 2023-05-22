#!/usr/bin/env python3
# www.jrodal.com

from abc import ABC, abstractmethod
from dataclasses import dataclass
from .register import Register
from enum import Enum


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
    def __init_subclass__(cls) -> None:
        if not Register.is_registered():
            Register.register()

    @abstractmethod
    def summarize_sync(self, text: str) -> Summary:
        pass

    @abstractmethod
    async def summarize_async(self, text: str) -> Summary:
        pass
