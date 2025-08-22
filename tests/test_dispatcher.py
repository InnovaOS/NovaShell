from __future__ import annotations
from pathlib import Path
from core.context import ExecutionContext
from core.dispatcher import dispatch
from core.result import Status

def test_pwd(tmp_path: Path):
    ctx = ExecutionContext(cwd=tmp_path, interactive=False)
    res = dispatch("pwd", ctx)
    assert res.status == Status.OK
    assert res.data == str(tmp_path)

def test_help_root(tmp_path: Path):
    ctx = ExecutionContext(cwd=tmp_path, interactive=False)
    res = dispatch("help", ctx)
    assert res.status == Status.OK
    assert "Commands:" in res.data

def test_unknown(tmp_path: Path):
    ctx = ExecutionContext(cwd=tmp_path, interactive=False)
    res = dispatch("nope", ctx)
    assert res.status == Status.ERROR
    assert "Unknown command" in res.message
