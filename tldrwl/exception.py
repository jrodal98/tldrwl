#!/usr/bin/env python3
# www.jrodal.com


class TldrwlException(Exception):
    def __init__(
        self,
        *,
        msg: str,
        cause: str,
        remediation: str,
    ) -> None:
        super().__init__(
            "\n".join(
                (
                    msg,
                    f"Cause: {cause}",
                    f"Remediation: {remediation}",
                ),
            )
        )


class TldrwlRegisterException(TldrwlException):
    @classmethod
    def make_error(cls, *, field: str, env_var: str) -> "TldrwlRegisterException":
        return cls(
            msg=f"Failed to register {field}",
            cause=f"Environment variable {env_var} is not set.",
            remediation=f"Set {env_var} before running script.",
        )


class TldrwlVideoUrlParsingException(TldrwlException):
    @classmethod
    def make_error(cls, *, video_url: str) -> "TldrwlVideoUrlParsingException":
        return cls(
            msg=f"Failed to parse {video_url=}",
            cause="Url may be invalid or regex pattern is not comprehensive",
            remediation="Fix url if it's broken, maybe switch to more common format",
        )


class TldrwlAsyncioRunInEventLoop(TldrwlException):
    @classmethod
    def make_error(cls, msg: str) -> "TldrwlAsyncioRunInEventLoop":
        return cls(
            msg=msg,
            cause="You tried to run sync code from inside an async loop",
            remediation="Use the .summarize_async APIS, not .summarize_sync",
        )


class TldrwlRateLimitError(TldrwlException):
    @classmethod
    def make_error(cls, msg: str) -> "TldrwlRateLimitError":
        return cls(
            msg=msg,
            cause="OpenAI rate limited you",
            remediation="See this page for more information: https://platform.openai.com/docs/guides/rate-limits",
        )


class TldrwlNoSummaryError(TldrwlException):
    pass
