# NovaShell (v1 bootstrap)

This is a minimal, clean skeleton for NovaShell with:
- Standardized handler interface via an adapter
- CommandResult and simple Status enum
- Error taxonomy
- `help`, `pwd`, `clear`, `tree` handlers
- Basic CLI and pytest tests

## Quickstart

```bash
# 1) enter this folder, then install in editable mode
pipx install -e .    # or: pip install -e .

# 2) try a command
novashell --cmd "pwd"

# 3) run tests
pytest -q
```
