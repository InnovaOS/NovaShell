from __future__ import annotations
from pathlib import Path
from core.context import ExecutionContext
from core.dispatcher import dispatch
from core.result import Status
import core.handlers.builtin  # register
import core.handlers.files
import core.handlers.run
import core.handlers.more_files
import core.handlers.search

def run(cmd: str, tmp: Path):
    ctx = ExecutionContext(cwd=tmp, interactive=False)
    return dispatch(cmd, ctx)

def test_touch_ls_rm(tmp_path: Path):
    assert run("touch x.txt", tmp_path).status == Status.OK
    out = run("ls", tmp_path).data
    assert "x.txt" in out
    assert run("rm x.txt", tmp_path).status == Status.OK

def test_mkdir_rmdir(tmp_path: Path):
    assert run("mkdir foo", tmp_path).status == Status.OK
    out = run("ls", tmp_path).data
    assert "foo/" in out
    assert run("rmdir foo", tmp_path).status == Status.OK

def test_find_grep(tmp_path: Path):
    (tmp_path / "a.txt").write_text("Hello\nWorld\n", encoding="utf-8")
    out = run("find a.txt", tmp_path).data
    assert "a.txt" in out
    out = run("grep hello a.txt", tmp_path).data
    assert "a.txt:1: Hello" in out
