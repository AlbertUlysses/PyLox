import argparse
from sys import argv, exit, stderr

from scanner import Scanner
from report_error import report_error

def run(source: str) ->bool:
    """..."""
    # can report error here
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()
    for token in tokens:
        print(f"{token}")
    return scanner.has_error

def run_prompt() -> None:
    """..."""
    # when error is here it needs to report and keep running
    while value := input("> "):
        run(value)

def run_file(path: str) ->None:
    """ """
    # when error is here it need to crash and exit(65)
    with open(path, "r") as file_:
        while (data := file_.readline()) != '':
            has_error = run(data)
            if has_error:
                exit(63)

def main():
    parser = argparse.ArgumentParser(
        usage='pylox [script]',
        description='pylox EntryPoint'
    )
    parser.add_argument("script", nargs="?",help="path to script", default=None)
    args = parser.parse_args()
    if len(argv) > 2:
        print(f'Usage: {parser.usage}]')
        exit(64) # follows linux /Unix norm as explained in crafting interpeters
    elif args.script:
        run_file(args.script)
    else:
        print("run prompt - default")
        run_prompt()

if __name__ == "__main__":
    main()


