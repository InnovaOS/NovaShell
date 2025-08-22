from __future__ import annotations
import argparse
from pathlib import Path
from .context import ExecutionContext
from .dispatcher import dispatch
from .result import Status
import core.handlers.builtin
import core.handlers.files
import core.handlers.run
import core.handlers.more_files
import core.handlers.search

def main() -> int:
    parser = argparse.ArgumentParser(prog="novashell")
    parser.add_argument("--cmd", help="Run a single command and exit")
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    ctx = ExecutionContext(cwd=Path.cwd(), interactive=not bool(args.cmd), debug=args.debug)

    if args.cmd:
        res = dispatch(args.cmd, ctx)
        if res.data:
            print(res.data)
        return res.code if res.status != Status.OK else 0

    # REPL-lite
    try:
        while True:
            line = input("NovaShell > ")
            res = dispatch(line, ctx)
            if res.data:
                print(res.data)
    except (EOFError, KeyboardInterrupt):
        return 0

if __name__ == "__main__":
    raise SystemExit(main())
