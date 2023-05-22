#!/usr/bin/env python3
# www.jrodal.com


from .register import Register


class AiInterface:
    def __init_subclass__(cls) -> None:
        if not Register.is_registered():
            Register.register()
