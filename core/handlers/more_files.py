# core/handlers/more_files.py
from __future__ import annotations
from pathlib import Path
from typing import List
from ..registry import command
from ..result import CommandResult
from ..context import ExecutionContext

def _abs(ctx: ExecutionContext, rel: str) -> Path:
    return (ctx.cwd / rel).resolve()

@command("mkdir")
def _mkdir(args: List[str], ctx: ExecutionContext) -> CommandResult:
    """Create a directory (and parents). Usage: mkdir <dir>"""
    if not args:
        return CommandResult.error("Usage: mkdir <dir>")
    p = _abs(ctx, args[0])
    try:
        p.mkdir(parents=True, exist_ok=False)
        return CommandResult.ok(f"Created dir {p.name}")
    except FileExistsError:
        return CommandResult.warn(f"Already exists: {p.name}")
    except Exception as e:
        return CommandResult.error(f"Failed to create dir: {e}")

@command("rmdir")
def _rmdir(args: List[str], ctx: ExecutionContext) -> CommandResult:
    """Remove an empty directory. Usage: rmdir <dir>"""
    if not args:
        return CommandResult.error("Usage: rmdir <dir>")
    p = _abs(ctx, args[0])
    if not p.exists():
        return CommandResult.error(f"No such dir: {args[0]}")
    if not p.is_dir():
        return CommandResult.error(f"Not a directory: {args[0]}")
    try:
        p.rmdir()
        return CommandResult.ok(f"Removed dir {p.name}")
    except Exception as e:
        return CommandResult.error(f"Failed to remove dir: {e}")

@command("rm")
def _rm(args: List[str], ctx: ExecutionContext) -> CommandResult:
    """Remove a file. Usage: rm <file>"""
    if not args:
        return CommandResult.error("Usage: rm <file>")
    p = _abs(ctx, args[0])
    if not p.exists():
        return CommandResult.error(f"No such file: {args[0]}")
    if p.is_dir():
        return CommandResult.error("Refuses to remove directories. Use rmdir.")
    try:
        p.unlink()
        return CommandResult.ok(f"Removed {p.name}")
    except Exception as e:
        return CommandResult.error(f"Failed to remove: {e}")

@command("cat")
def _cat(args: List[str], ctx: ExecutionContext) -> CommandResult:
    """Print file contents. Usage: cat <file>"""
    if not args:
        return CommandResult.error("Usage: cat <file>")
    p = _abs(ctx, args[0])
    if not p.exists() or not p.is_file():
        return CommandResult.error(f"No such file: {args[0]}")
    try:
        return CommandResult.ok(data=p.read_text(encoding="utf-8"))
    except Exception as e:
        return CommandResult.error(f"Failed to read: {e}")

@command("echo")
def _echo(args: List[str], ctx: ExecutionContext) -> CommandResult:
    """Echo text (optionally append to file). Usage: echo <text> [>> <file>]"""
    if not args:
        return CommandResult.ok(data="")
    # support: echo hello >> file.txt
    if len(args) >= 3 and args[-2] == ">>":
        file = _abs(ctx, args[-1])
        text = " ".join(args[:-2])
        try:
            file.parent.mkdir(parents=True, exist_ok=True)
            with file.open("a", encoding="utf-8") as f:
                f.write(text + "\n")
            return CommandResult.ok(f"Appended to {file.name}")
        except Exception as e:
            return CommandResult.error(f"Failed to append: {e}")
    return CommandResult.ok(data=" ".join(args))

