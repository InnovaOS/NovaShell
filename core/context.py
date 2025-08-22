from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional, Callable
import sys

Printer = Callable[[str], None]

@dataclass
class ExecutionContext:
    cwd: Path
    profile: str = "default"
    options: Dict[str, Any] = field(default_factory=dict)
    interactive: bool = True
    out: Printer = print
    err: Printer = lambda s: print(s, file=sys.stderr)
    debug: bool = False
