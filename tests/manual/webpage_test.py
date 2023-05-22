#!/usr/bin/env python3
# www.jrodal.com

import asyncio
import time
from tldrwl.summarize import Summarizer

# import logging
#
# logging.basicConfig(level=logging.DEBUG)

webpage = "https://www.jrodal.com/posts/how-to-deploy-rocket-rust-web-app-on-vps/"


def main_sync() -> None:
    summary = Summarizer().summarize_sync(webpage)

    print(summary)
    print(f"{summary.estimated_cost_usd=}")


async def main_async() -> None:
    summary = await Summarizer().summarize_async(webpage)

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
