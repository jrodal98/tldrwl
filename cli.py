#!/usr/bin/env python3
# www.jrodal.com

import argparse
import asyncio
import logging

from tldrwl.summarize import Summarizer


class VerboseFilter(logging.Filter):
    def __init__(self, name: str = "", very_verbose_logging: bool = False) -> None:
        super().__init__(name)
        self.very_verbose_logging = very_verbose_logging

    def filter(self, record: logging.LogRecord):
        return (
            record.name.startswith("tldrwl")
            or record.levelno != logging.DEBUG
            or self.very_verbose_logging
        )


def _init_logging(args: argparse.Namespace) -> None:
    if args.disable_logging:
        return

    log_level = logging.INFO
    if args.verbose_logging or args.very_verbose_logging:
        log_level = logging.DEBUG

    logging.basicConfig(level=log_level)  # or any other desired logging configuration

    for handler in logging.root.handlers:
        handler.addFilter(VerboseFilter(very_verbose_logging=args.very_verbose_logging))


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

    _init_logging(args)

    summary = await Summarizer().summarize_async(args.input)
    print(f"Summary: {summary.text}")
    print(f"Estimated cost (usd): ${summary.estimated_cost_usd:.4f}")


if __name__ == "__main__":
    asyncio.run(main())
