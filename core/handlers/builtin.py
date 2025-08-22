from __future__ import annotations
from pathlib import Path
from typing import List
from ..registry import command
from ..result import CommandResult
from ..context import ExecutionContext
from ..help import render_root_help, render_command_help

@command("help")
def _help(args: List[str], ctx: ExecutionContext) -> CommandResult:
    """Show general help or help for a specific command.

    Examples:
      help
      help ls
    """
    if not args:
        return CommandResult.ok(data=render_root_help())
    return CommandResult.ok(data=render_command_help(args[0]))

@command("pwd")
def _pwd(args: List[str], ctx: ExecutionContext) -> CommandResult:
    """Print working directory."""
    return CommandResult.ok(data=str(ctx.cwd))

@command("clear")
def _clear(args: List[str], ctx: ExecutionContext) -> CommandResult:
    """Clear the screen (TTY only)."""
    if not ctx.interactive:
        return CommandResult.ok("noop in non-interactive mode")
    ctx.out("\033[2J\033[H")
    return CommandResult.ok()

@command("tree")
def _tree(args: List[str], ctx: ExecutionContext) -> CommandResult:
    """Show a simple directory tree (depth 2)."""
    root = ctx.cwd
    max_depth = 2
    lines: list[str] = []

    def walk(p: Path, depth: int = 0):
        if depth > max_depth:
            return
        indent = "  " * depth
        lines.append(f"{indent}{p.name}/" if p.is_dir() else f"{indent}{p.name}")
        if p.is_dir():
            for child in sorted(p.iterdir()):
                walk(child, depth + 1)

    walk(root)
    return CommandResult.ok(data="\n".join(lines))
