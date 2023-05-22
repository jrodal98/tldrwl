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
