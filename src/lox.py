import argparse
from sys import argv, exit, stderr

from scanner import Scanner
from report_error import report_error

def run(source: str) ->None:
    """..."""
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()
    for token in tokens:
        print(f"{token}")
    # print(source)

def run_prompt() -> None:
    """..."""
    while value := input("> "):
        run(value)

def run_file(path: str) ->None:
    """ """
    with open(path, "r") as file_:
        data = file_.read()
    if not run(data):
        exit(65)

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


