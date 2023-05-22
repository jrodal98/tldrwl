#!/usr/bin/env python3
# www.jrodal.com

import asyncio
import time
from tldrwl.summarize_webpage import WebpageSummarizer

import logging

logging.basicConfig(level=logging.DEBUG)

webpage = "https://en.wikipedia.org/wiki/ChatGPT"


def main_sync() -> None:
    summary = WebpageSummarizer().summarize_webpage(webpage)

    print(summary)
    print(f"{summary.estimated_cost_usd=}")


async def main_async() -> None:
    summary = await WebpageSummarizer().summarize_webpage_async(webpage)

    print(summary)
    print(f"{summary.estimated_cost_usd=}")


async def main() -> None:
    start = time.time()
    print("Running async")
    await main_async()
    end = time.time()
    print(f"Finished async in {end - start}s")

    start = time.time()
    print("Running sync")
    main_sync()
    end = time.time()
    print(f"Finished sync in {end - start}s")


if __name__ == "__main__":
    asyncio.run(main())
