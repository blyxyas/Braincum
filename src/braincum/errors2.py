#!/usr/bin/env python3

from __future__ import annotations

from dataclasses import dataclass
# from pathlib import Path

from braincum.custom_types import StartPos, EndPos


# _tag = "\x1b[1;41m ERR \x1b[30;47m Braincum \x1b[22;39;49m "
_synopsis_base = "Panicked at \x1b[36m\"%s\"\x1b[39m, line %d:\n    %s\n    "


@dataclass
class File:
    name: str
    contents: str

    def get_lines(self: File) -> list[str]:
        return self.contents.splitlines()

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

    def _synopsis_fill(self: Traceback) -> tuple[str, int, str]:
        return (self.file.name, self.line_no+1, self.file.get_lines()[self.line_no])

    def format(self: Traceback) -> str:
        # header = _tag + "\n"
        header = _synopsis_base % self._synopsis_fill()
        return header + " " * self.spos + "\x1b[31m" + "^" * (self.epos - self.spos) + "\x1b[0m\n"


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

    def format(self: BCError, *args: object, traceback: Traceback) -> str:
        """
        Returns:
            str: printable formatted string that represents the error
        """

        self._check_args(args)

        return traceback.format() + f"\x1b[1m{self.errname}:\x1b[22m \x1b[31m{self.message % args}\x1b[39m"

    def throw(self: BCError, *args: object, traceback: Traceback) -> None:
        print(self.format(*args, traceback=traceback))


# BCError("FileNotFound", (Path, ), "file '%s' could not be found").throw(Path("test"), traceback=Traceback.new("<stdin>", "python src test", 1, (11, 15)))
