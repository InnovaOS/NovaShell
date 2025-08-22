from __future__ import annotations
from typing import Callable, Dict

# command name -> handler
REGISTRY: Dict[str, Callable] = {}

def command(name: str):
    """Decorator to register a handler.

    Expected modern signature: handler(args: list[str], ctx: ExecutionContext) -> CommandResult
    """
    def _wrap(fn):
        REGISTRY[name] = fn
        return fn
    return _wrap
