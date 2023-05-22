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
    def make_error(cls, *, field: str, env_var: str) -> "TldrwlException":
        return cls(
            msg=f"Failed to register {field}",
            cause=f"Environment variable {env_var} is not set.",
            remediation="Set {env_var} before running script.",
        )
