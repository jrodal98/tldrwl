#!/usr/bin/env python3
# www.jrodal.com

import asyncio
from tldrwl.summarize import Summarizer

yt_video = "https://www.youtube.com/watch?v=--khbXchTeE"


def main_sync() -> None:
    print("Sync")
    summary = Summarizer().summarize_sync(yt_video)

    print(summary)
    print(f"{summary.estimated_cost_usd=}")


async def main_async() -> None:
    print("Async")
    summary = await Summarizer().summarize_async(yt_video)

    print(summary)
    print(f"{summary.estimated_cost_usd=}")


if __name__ == "__main__":
    asyncio.run(main_async())
    main_sync()
