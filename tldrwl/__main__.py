#!/usr/bin/env python3
# www.jrodal.com

import argparse
import asyncio

from tldrwl.summarize import Summarizer
from tldrwl.logger import init_logging
from tldrwl.summarizers.chat_completions_text_summarizer import (
    ChatCompletionsTextSummarizer,
)
from tldrwl.ai_interface import Model


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
    parser.add_argument(
        "--model",
        type=Model,
        choices=list(Model),
        default=None,
        help="Model to use for summarization",
    )
    args = parser.parse_args()

    init_logging(
        disable_logging=args.disable_logging,
        verbose_logging=args.verbose_logging,
        very_verbose_logging=args.very_verbose_logging,
    )

    text_summarizer = ChatCompletionsTextSummarizer(model=args.model)

    summary = await Summarizer(text_summarizer=text_summarizer).summarize_async(
        args.input
    )
    print(f"Summary: {summary.text}")
    print(f"Estimated cost (usd): ${summary.estimated_cost_usd:.4f}")


if __name__ == "__main__":
    asyncio.run(main())
