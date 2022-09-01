#!/usr/bin/env python3

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from braincum.traceback import ErrorTraceback
from braincum.utils import tabulate

__all__ = []


ERROR_SYNOPSIS: str = "\x1b[1m%s:\x1b[22m \x1b[31m%s\x1b[39m"


@dataclass
class BCError:
    errname: str
    args: tuple[type, ...]
    message: str
    code: int = 1

    def _check_args(self: BCError, args: tuple[object, ...]) -> None:
        """
        Checks the provided args and raises an error if they are incorrect.

        Args:
            args (tuple[object, ...]): the provided args

        Raises:
            TypeError: if the number of provided args doesn't match with the expected one 
            TypeError: if the type of the args doesn't match with expected one
        """

        if len(args) != len(self.args):
            raise TypeError("unmatching number of args")

        for arg, arg_type in zip(args, self.args):
            if not isinstance(arg, arg_type):
                raise TypeError(f"unmatching argument types")

    def format(self: BCError, *args: object, note: str | None = None) -> str:
        """
        Returns:
            str: printable formatted string that represents the error
        """

        self._check_args(args)

        output = ERROR_SYNOPSIS % (self.errname, self.message % args)

        if note is not None:
            output += "\n" + tabulate(note, n=1)

        return output

    def throw(self: BCError, *args: object, traceback: ErrorTraceback, note: str | None = None) -> None:
        print(traceback.format() + self.format(*args, note=note))


BCError("FileNotFound", (Path, ), "file '%s' could not be found").throw(
    Path("test"), note="Optional bottom note.", traceback=ErrorTraceback.new("<stdin>", "python src test", 1, (11, 15)))
