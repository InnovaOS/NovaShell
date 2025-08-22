from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional

class Status(str, Enum):
    OK = "ok"
    WARN = "warn"
    ERROR = "error"

@dataclass(slots=True)
class CommandResult:
    """Canonical return object for all handlers and dispatcher.

    Attributes
    ----------
    status: Status     # OK/WARN/ERROR
    message: str       # human-friendly summary
    data: Any          # optional structured payload
    hint: Optional[str]# optional next-step guidance
    code: int          # optional numeric code (e.g., exit code)
    """
    status: Status
    message: str = ""
    data: Any = None
    hint: Optional[str] = None
    code: int = 0

    @classmethod
    def ok(cls, message: str = "", data: Any = None) -> "CommandResult":
        return cls(Status.OK, message, data, None, 0)

    @classmethod
    def warn(cls, message: str, data: Any = None, code: int = 1) -> "CommandResult":
        return cls(Status.WARN, message, data, None, code)

    @classmethod
    def error(cls, message: str, data: Any = None, code: int = 1, hint: Optional[str] = None) -> "CommandResult":
        return cls(Status.ERROR, message, data, hint, code)

    def __bool__(self) -> bool:  # allow if result: ... semantics
        return self.status == Status.OK
