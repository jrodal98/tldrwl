#!/usr/bin/env python3
# www.jrodal.com


import os
import openai

from tldrwl.exception import TldrwlRegisterException


class Register:
    _registered: bool = False

    @classmethod
    def is_registered(cls) -> bool:
        return cls._registered

    @classmethod
    def register(
        cls,
        openai_api_key_env_var: str = "OPENAI_API_KEY",
    ) -> None:
        openai_api_key = os.getenv(openai_api_key_env_var)
        if not openai_api_key:
            raise TldrwlRegisterException.make_error(
                field="openai api key", env_var=openai_api_key_env_var
            )
        openai.api_key = openai_api_key

        cls._registered = True
