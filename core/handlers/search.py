# core/handlers/search.py
from __future__ import annotations
from pathlib import Path
from typing import List
from ..registry import command
from ..result import CommandResult
from ..context import ExecutionContext

@command("find")
def _find(args: List[str], ctx: ExecutionContext) -> CommandResult:
    """Find files by name (substring, case-insensitive).
    Usage: find <name-part> [in <dir>]
    """
    if not args:
        return CommandResult.error("Usage: find <name-part> [in <dir>]")
    needle = args[0].lower()
    base = ctx.cwd
    if len(args) >= 3 and args[1] == "in":
        base = (ctx.cwd / args[2]).resolve()
        if not base.exists() or not base.is_dir():
            return CommandResult.error(f"No such dir: {args[2]}")
    out: list[str] = []
    for p in base.rglob("*"):
        if p.is_file() and needle in p.name.lower():
            out.append(str(p.relative_to(ctx.cwd)))
    return CommandResult.ok(data="\n".join(out))

@command("grep")
def _grep(args: List[str], ctx: ExecutionContext) -> CommandResult:
    """Search for text inside files (case-insensitive).
    Usage: grep <text> <file>
    """
    if len(args) < 2:
        return CommandResult.error("Usage: grep <text> <file>")
    text = args[0].lower()
    file = (ctx.cwd / args[1]).resolve()
    if not file.exists() or not file.is_file():
        return CommandResult.error(f"No such file: {args[1]}")
    lines = []
    try:
        for i, line in enumerate(file.read_text(encoding="utf-8").splitlines(), 1):
            if text in line.lower():
                lines.append(f"{file.name}:{i}: {line}")
        return CommandResult.ok(data="\n".join(lines))
    except Exception as e:
        return CommandResult.error(f"Failed to read: {e}")
