class NovaShellError(Exception):
    """Base error with machine-friendly code mapping."""
    code = 1

class NSyntaxError(NovaShellError):
    code = 2

class NNotFound(NovaShellError):
    code = 3

class NIOError(NovaShellError):
    code = 4

class NPermission(NovaShellError):
    code = 5

class NConflict(NovaShellError):
    code = 6

class NUnexpected(NovaShellError):
    code = 10
