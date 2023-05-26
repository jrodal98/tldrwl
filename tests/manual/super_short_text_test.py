#!/usr/bin/env python3
# www.jrodal.com

import asyncio
from tldrwl.summarize import Summarizer

text = "Test input"


def main_sync() -> None:
    print("Sync test")
    summary = Summarizer().summarize_sync(text)

    print(summary)
    print(f"{summary.estimated_cost_usd=}")


async def main_async() -> None:
    print("Async test")
    summary = await Summarizer().summarize_async(text)

    print(summary)
    print(f"{summary.estimated_cost_usd=}")


if __name__ == "__main__":
    asyncio.run(main_async())
    main_sync()
