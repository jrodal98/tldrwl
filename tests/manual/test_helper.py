#!/usr/bin/env python3
# www.jrodal.com

import time
import asyncio
from tldrwl.logger import init_logging
from tldrwl.summarize import Summarizer
from tldrwl.summarizers.chat_completions_text_summarizer import (
    ChatCompletionsTextSummarizer,
)


def main_sync(text: str) -> None:
    print("Sync test")
    start = time.time()
    text_summarizer = ChatCompletionsTextSummarizer()

    summary = Summarizer(text_summarizer=text_summarizer).summarize_sync(text)
    end = time.time()

    print(summary)
    print(f"{summary.estimated_cost_usd=}")
    print(f"runtime: {end - start:.4f}s")


async def main_async(text: str) -> None:
    print("Async test")
    start = time.time()
    text_summarizer = ChatCompletionsTextSummarizer()
    summary = await Summarizer(text_summarizer=text_summarizer).summarize_async(text)
    end = time.time()

    print(summary)
    print(f"{summary.estimated_cost_usd=}")
    print(f"runtime: {end - start:.4f}s")


def run_tests(text: str, include_sync: bool = False) -> None:
    init_logging(verbose_logging=True)
    asyncio.run(main_async(text))
    if include_sync:
        main_sync(text)
