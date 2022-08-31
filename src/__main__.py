#!/usr/bin/env python3

from __future__ import annotations

import sys
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import NoReturn

from braincum import Interpreter


class Program:
    @staticmethod
    def _parse_args(args: list[str]) -> Namespace:
        """
        Helper method to parse command line args.

        Args:
            args (list[str]): args to parse

        Returns:
            Namespace: argparse special object that stores parsed args.
        """

        parser = ArgumentParser()
        parser.add_argument("file")  # type: ignore

        return parser.parse_args(args)

    def __init__(self: Program, *, args: list[str] | None = None) -> None:
        """
        Parses command line args and stores the result.

        Note: The argument `args` exists for testing purposes and should not be used otherwise.

        Args:
            args (list[str] | None, optional): args to be parsed. Defaults to None.
        """

        self.args = self._parse_args(args or sys.argv[1:])

    def run(self: Program) -> int:
        """
        Runs the program and returns an exit code.

        Returns:
            int: exit code.
        """

        file_path = Path(self.args.file).resolve()

        if not file_path.exists():
            # panic(Error.FileNotFound, file_path)
            raise SystemExit(1)

        content = file_path.read_text(encoding="utf-8")

        try:
            i = Interpreter(content)
        except:
            return 1
        else:
            return 0

    def execute(self: Program) -> NoReturn:
        """
        Runs the program and exits.

        Raises:
            SystemExit: when the program terminates.
        """

        raise SystemExit(self.run())


if __name__ == "__main__":
    Program().execute()
