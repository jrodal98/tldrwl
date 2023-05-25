#!/usr/bin/env python3
# www.jrodal.com

import argparse
import asyncio

from tldrwl.summarize import Summarizer  # pyright: ignore
from tldrwl.logger import init_logging  # pyright: ignore


async def main():
    parser = argparse.ArgumentParser(description="Input (Text or URL to summarize)")
    parser.add_argument("input", type=str, help="Input (Text or URL to summarize)")
    parser.add_argument(
        "--disable-logging", action="store_true", help="Turn logging off"
    )
    parser.add_argument(
        "--verbose-logging", action="store_true", help="verbose logging (tldrwl debug)"
    )
    parser.add_argument(
        "--very-verbose-logging",
        action="store_true",
        help="very verbose logging (include third party logs)",
    )
    args = parser.parse_args()

    init_logging(args)

    summary = await Summarizer().summarize_async(args.input)
    print(f"Summary: {summary.text}")
    print(f"Estimated cost (usd): ${summary.estimated_cost_usd:.4f}")


if __name__ == "__main__":
    asyncio.run(main())
