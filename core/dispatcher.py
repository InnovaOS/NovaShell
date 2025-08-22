from __future__ import annotations
from typing import List
from .context import ExecutionContext
from .errors import *
from .result import CommandResult, Status
from .registry import REGISTRY
from .adapter import call_handler

def parse_command(line: str) -> tuple[str, List[str]]:
    parts = line.strip().split()
    if not parts:
        raise NSyntaxError("Empty command")
    return parts[0], parts[1:]

def dispatch(line: str, ctx: ExecutionContext) -> CommandResult:
    try:
        name, args = parse_command(line)
        handler = REGISTRY.get(name)
        if not handler:
            raise NNotFound(f"Unknown command: {name}")

        result = call_handler(handler, args, ctx)
        if isinstance(result, CommandResult):
            return result
        if isinstance(result, bool):
            return CommandResult.ok("ok" if result else "failed", data=result)
        if result is None:
            return CommandResult.ok("")
        return CommandResult.ok(data=result)

    except NovaShellError as ne:
        return CommandResult.error(str(ne), code=getattr(ne, "code", 1))
    except Exception as e:
        return CommandResult.error(
            f"Unexpected error: {e.__class__.__name__}: {e}", code=NUnexpected.code,
            hint="Run with --debug and open an issue if it persists."
        )
