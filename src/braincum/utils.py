#!/usr/bin/env python3

# pyright: reportUnnecessaryTypeIgnoreComment=false
# Note: mypy does not allow dynamic parent classes

from __future__ import annotations

from dataclasses import dataclass


TABSIZE: int = 2


# *- Technically unnecessary, it's for "code readability" -* #
StartPos = int
EndPos = int


@dataclass
class File:
    name: str
    contents: str

    def get_lines(self: File) -> list[str]:
        return self.contents.splitlines()

    def get_line(self: File, line_no: int) -> str:
        return self.get_lines()[line_no]

    @classmethod
    def new(cls: type[File], name: str, contents: str | bytes) -> File:
        return cls(name, contents.decode("utf-8") if isinstance(contents, bytes) else contents)


def tabulate(string: str, *, n: int) -> str:
    """
    Tabulate a string n times.
    The default tab size is 2.

    Args:
        string (str): the string to tabulate
        n (int): the number of tabs

    Returns:
        str: tabulated string.
    """

    return " " * TABSIZE * n + string
