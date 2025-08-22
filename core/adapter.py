from __future__ import annotations
import inspect
from typing import Any, Callable
from .result import CommandResult
from .context import ExecutionContext

def _print_lines_factory(ctx: ExecutionContext):
    def _pl(lines: Any):
        if isinstance(lines, (list, tuple)):
            for line in lines:
                ctx.out(str(line))
        else:
            ctx.out(str(lines))
    return _pl

def call_handler(handler: Callable, args: list[str], ctx: ExecutionContext) -> CommandResult:
    """Call a handler with flexible legacy signatures.

    Supported legacy forms (all normalized here):
      - fn(args, ctx)
      - fn(args)
      - fn(ctx)
      - fn(args, ctx, print_lines=...)
      - fn(args, **kwargs)  (where kwargs may include print_lines/options)
    """
    sig = inspect.signature(handler)
    params = sig.parameters

    # Assemble kwargs by name if present
    kwargs = {}
    if "ctx" in params:
        kwargs["ctx"] = ctx
    if "args" in params:
        kwargs["args"] = args
    if "print_lines" in params:
        kwargs["print_lines"] = _print_lines_factory(ctx)
    if "options" in params:
        kwargs["options"] = ctx.options

    try:
        if kwargs:
            return handler(**kwargs)  # type: ignore[call-arg]
        # Fallback positional guesses
        if len(params) == 2:
            return handler(args, ctx)  # type: ignore[misc]
        elif len(params) == 1:
            name = next(iter(params))
            return handler(args if name == "args" else ctx)  # type: ignore[misc]
        else:
            return handler()  # type: ignore[misc]
    except TypeError:
        # Final attempt: rebuild kwargs minimally
        bound = {}
        if "args" in params:
            bound["args"] = args
        if "ctx" in params:
            bound["ctx"] = ctx
        if "print_lines" in params:
            bound["print_lines"] = _print_lines_factory(ctx)
        if "options" in params:
            bound["options"] = ctx.options
        return handler(**bound)  # type: ignore[call-arg]
