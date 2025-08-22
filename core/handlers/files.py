# core/handlers/files.py
from __future__ import annotations
from pathlib import Path
from typing import List
from ..registry import command
from ..result import CommandResult
from ..context import ExecutionContext

@command("cd")
def _cd(args: List[str], ctx: ExecutionContext) -> CommandResult:
    """Change directory. Usage: cd <path>"""
    target = args[0] if args else str(Path.home())
    p = (ctx.cwd / target).resolve()
    if not p.exists():
        return CommandResult.error(f"No such path: {target}")
    if not p.is_dir():
        return CommandResult.error(f"Not a directory: {target}")
    ctx.cwd = p
    return CommandResult.ok(data=str(ctx.cwd))

@command("ls")
def _ls(args: List[str], ctx: ExecutionContext) -> CommandResult:
    """List files. Usage: ls [path]"""
    path = (ctx.cwd / args[0]).resolve() if args else ctx.cwd
    if not path.exists():
        return CommandResult.error(f"No such path: {path}")
    if path.is_file():
        return CommandResult.ok(data=path.name)
    names = []
    for e in sorted(path.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower())):
        names.append(e.name + ("/" if e.is_dir() else ""))
    return CommandResult.ok(data="\n".join(names))

@command("touch")
def _touch(args: List[str], ctx: ExecutionContext) -> CommandResult:
    """Create an empty file. Usage: touch <file>"""
    if not args:
        return CommandResult.error("Usage: touch <file>")
    p = (ctx.cwd / args[0]).resolve()
    if p.exists():
        return CommandResult.warn(f"File exists: {p.name}")
    try:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.touch()
        return CommandResult.ok(f"Created {p.name}")
    except Exception as e:
        return CommandResult.error(f"Failed to create: {e}")

@command("mv")
def _mv(args: List[str], ctx: ExecutionContext) -> CommandResult:
    """Rename/move. Usage: mv <src> <dst>"""
    if len(args) < 2:
        return CommandResult.error("Usage: mv <src> <dst>")
    src = (ctx.cwd / args[0]).resolve()
    dst = (ctx.cwd / args[1]).resolve()
    if not src.exists():
        return CommandResult.error(f"No such file or dir: {args[0]}")
    try:
        src.rename(dst)
        return CommandResult.ok(f"Moved to {dst.name}")
    except Exception as e:
        return CommandResult.error(f"Failed to move: {e}")
