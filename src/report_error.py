from sys import stderr

class ParserError(RuntimeError):
    """Used to indicate when an error occurs during parsing."""

class LoxRuntimeError(RuntimeError):
    """Used to indicate when an error occurs during runtime."""

def report_error(line: int, where: str, message: str) -> bool:
    print(f"[ line {line}] Error {where}: {message}",file=stderr)
    return True


