from sys import stderr
def report_error(line: int, where: str, message: str) -> bool:
    print(f"[ line {line}] Error {where}: {message}",file=stderr)
    return True

