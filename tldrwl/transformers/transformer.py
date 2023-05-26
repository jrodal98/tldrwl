#!/usr/bin/env python3
# www.jrodal.com

from abc import ABC, abstractmethod


class Transformer(ABC):
    @abstractmethod
    async def get_text(self) -> str:
        pass
