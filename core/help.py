from __future__ import annotations
from textwrap import dedent
from .registry import REGISTRY

HELP_HEADER = """NovaShell Help
Use: help [command]
"""

def render_root_help() -> str:
    lines = [HELP_HEADER, "Commands:"]
    width = max((len(name) for name in REGISTRY.keys()), default=4)
    for name, fn in sorted(REGISTRY.items()):
        doc = (fn.__doc__ or "").strip().splitlines()[0] if fn.__doc__ else ""
        lines.append(f"  {name.ljust(width)}  {doc}")
    return "\n".join(lines)

def render_command_help(name: str) -> str:
    fn = REGISTRY.get(name)
    if not fn:
        return f"No such command: {name}"
    doc = dedent(fn.__doc__ or "No help available.").strip()
    return f"{name}\n{'-'*len(name)}\n{doc}\n"
