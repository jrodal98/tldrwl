#!/usr/bin/env python3
# www.jrodal.com

import asyncio
import time
from tldrwl.summarize_youtube import YoutubeSummarizer

import logging

logging.basicConfig(level=logging.DEBUG)

yt_video = "https://www.youtube.com/watch?v=6E3-MRnh8TQ"


def main_sync() -> None:
    summary = YoutubeSummarizer().summarize_video(yt_video)

    print(summary)
    print(f"{summary.estimated_cost_usd=}")


async def main_async() -> None:
    summary = await YoutubeSummarizer().summarize_video_async(yt_video)

    print(summary)
    print(f"{summary.estimated_cost_usd=}")


async def main() -> None:
    start = time.time()
    print("Running async")
    await main_async()
    end = time.time()
    print(f"Finished async in {end - start}s")

    # start = time.time()
    # print("Running sync")
    # main_sync()
    # end = time.time()
    # print(f"Finished sync in {end - start}s")


if __name__ == "__main__":
    asyncio.run(main())
