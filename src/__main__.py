#!/usr/bin/env python3

# pyright: reportUnusedCallResult=false

from argparse import ArgumentParser, Namespace
from pathlib import Path

from braincum import Error, Interpreter, panic


def init() -> Namespace:
    """
    Initialize command line argument parser

    Returns:
        Namespace: parsed args
    """

    parser = ArgumentParser()
    parser.add_argument("file")

    return parser.parse_args()


def main() -> int:
    """
    Main program

    Raises:
        FileNotFoundError: if the provided file was not found

    Returns:
        int: exit code
    """

    args = init()

    file_path = Path(args.file).resolve()

    if not file_path.exists():
        panic(Error.FileNotFound, file_path)

    content = file_path.read_text()
    i = Interpreter(content)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
