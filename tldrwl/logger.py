#!/usr/bin/env python3
# www.jrodal.com

import logging
import argparse


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


def init_logging(args: argparse.Namespace) -> None:
    if args.disable_logging:
        return

    log_level = logging.INFO
    if args.verbose_logging or args.very_verbose_logging:
        log_level = logging.DEBUG

    logging.basicConfig(level=log_level)  # or any other desired logging configuration

    for handler in logging.root.handlers:
        handler.addFilter(VerboseFilter(very_verbose_logging=args.very_verbose_logging))
