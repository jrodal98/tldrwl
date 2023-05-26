#!/usr/bin/env python3
# www.jrodal.com

import asyncio
from tldrwl.summarize import Summarizer

webpage = "https://www.jrodal.com/posts/how-to-deploy-rocket-rust-web-app-on-vps/"


def main_sync() -> None:
    print("Sync")
    summary = Summarizer().summarize_sync(webpage)

    print(summary)
    print(f"{summary.estimated_cost_usd=}")


async def main_async() -> None:
    print("Async")
    summary = await Summarizer().summarize_async(webpage)

    print(summary)
    print(f"{summary.estimated_cost_usd=}")


if __name__ == "__main__":
    asyncio.run(main_async())
    main_sync()
