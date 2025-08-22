# core/handlers/run.py
from __future__ import annotations
from typing import List
from ..registry import command
from ..result import CommandResult
from ..context import ExecutionContext
from ..dispatcher import dispatch

@command("run")
def _run(args: List[str], ctx: ExecutionContext) -> CommandResult:
    """Run a .ns script line by line. Usage: run script <file.ns>"""
    if len(args) < 2 or args[0] != "script":
        return CommandResult.error("Usage: run script <file.ns>")
    script = (ctx.cwd / args[1]).resolve()
    if not script.exists():
        return CommandResult.error(f"No such file: {script.name}")
    try:
        for raw in script.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            res = dispatch(line, ctx)
            if res.data:
                ctx.out(str(res.data))
            if res.status != res.status.OK:
                return CommandResult.error(f"Script aborted on: {line}", hint=res.message)
        return CommandResult.ok(f"Finished: {script.name}")
    except Exception as e:
        return CommandResult.error(f"Failed to run script: {e}")
