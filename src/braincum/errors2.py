#!/usr/bin/env python3

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from braincum.custom_types import StartPos, EndPos

__all__ = []


# _tag = "\x1b[1;41m ERR \x1b[30;47m Braincum \x1b[22;39;49m "

TRACEBACK_SYNOPSIS: list[str] = [
    "Panicked at \x1b[36m\"%s\"\x1b[39m, line %d:\n",
    "    %s\n",
    "    %s\x1b[1;31m%s\x1b[22;39m\n",
]

ERROR_SYNOPSIS: str = "\x1b[1m%s:\x1b[22m \x1b[31m%s\x1b[39m"


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


@dataclass
class Traceback:
    spos: StartPos  # Inclusive
    epos: EndPos  # Exclusive
    line_no: int
    file: File

    @classmethod
    def new(
        cls: type[Traceback],
        file_name: str,
        contents: str | bytes,
        line_no: int,
        range_pos: tuple[StartPos, EndPos],
    ) -> Traceback:
        return cls(*range_pos, line_no-1, File.new(file_name, contents))

    def get_highlighted_line(self: Traceback) -> str:
        line = self.file.get_line(self.line_no)
        return line[:self.spos] + "\x1b[1m" + line[self.spos:self.epos] + "\x1b[22m" + line[self.epos:]

    def format(self: Traceback) -> str:
        header, line, arrows = TRACEBACK_SYNOPSIS

        header %= (self.file.name, self.line_no + 1)
        line %= self.get_highlighted_line()
        arrows %= (" " * self.spos, "^" * (self.epos - self.spos))

        return header + line + arrows


@dataclass
class BCError:
    errname: str
    args: tuple[type, ...]
    message: str
    note: str | None = None
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

    def format(self: BCError, *args: object) -> str:
        """
        Returns:
            str: printable formatted string that represents the error
        """

        self._check_args(args)

        output = ERROR_SYNOPSIS % (self.errname, self.message % args)

        if self.note is not None:
            output += "\n  " + self.note

        return output

    def throw(self: BCError, *args: object, traceback: Traceback) -> None:
        print(traceback.format() + self.format(*args))


BCError("FileNotFound", (Path, ), "file '%s' could not be found", "Optional bottom note.").throw(
    Path("test"), traceback=Traceback.new("<stdin>", "python src test", 1, (11, 15)))
