#!/usr/bin/env python3

from __future__ import annotations


from dataclasses import dataclass
import sys

from braincum.utils import EndPos, File, StartPos, tabulate


ERROR_TRACEBACK_SYNOPSIS: tuple[str, ...] = (
    "Panicked at \x1b[36m\"%s\"\x1b[39m, line %d:\n",
    tabulate("%s\n", n=2),
    tabulate("%s\x1b[1;31m%s\x1b[22;39m\n", n=2),
)

# 100 is an arbitrary value, it's a safe margin to be certain not to raise recursion errors
STACK_SIZE_LIMIT = sys.getrecursionlimit() - 100


class StackLimitError(MemoryError):
    @classmethod
    def new(cls: type[StackLimitError], size: int) -> StackLimitError:
        return cls(f"stack size ({size}) cannot go above {STACK_SIZE_LIMIT}")


class TracebackStack:
    def __init__(self: TracebackStack, *tracebacks: Traceback) -> None:
        self.top: Traceback | None = None
        self.next: TracebackStack | None = None

        if not tracebacks:
            return

        top, *next = tracebacks
        self.top = top

        if next:
            self.next = TracebackStack(*next)

    def push(self: TracebackStack, traceback: Traceback) -> None:
        if self.next is None:
            self.next = TracebackStack()

        if self.size >= STACK_SIZE_LIMIT:
            raise StackLimitError.new(self.size)

        if self.top is not None:
            self.next.push(self.top)
        self.top = traceback

    @property
    def size(self: TracebackStack) -> int:
        if self.top is None:
            return 0
        if self.next is None:
            return 1
        return 1 + self.next.size

    def __len__(self: TracebackStack) -> int:
        return self.size


@dataclass
class Traceback:
    file: File
    line_no: int

    @classmethod
    def new(cls: type[Traceback], file_name: str, contents: str | bytes, line_no: int) -> Traceback:
        return cls(File.new(file_name, contents), line_no)

    @classmethod
    def from_line_update(cls: type[Traceback], old_traceback: Traceback, line_no: int) -> Traceback:
        return cls(old_traceback.file, line_no)

    def get_highlighted_line(self: Traceback) -> str:
        return self.file.get_line(self.line_no)


@dataclass
class ErrorTraceback(Traceback):
    spos: StartPos  # Inclusive
    epos: EndPos  # Exclusive

    @classmethod
    def new(
        cls: type[ErrorTraceback],
        file_name: str,
        contents: str | bytes,
        line_no: int,
        range_pos: tuple[StartPos, EndPos] = (0, 0),
    ) -> ErrorTraceback:
        return cls(File.new(file_name, contents), line_no-1, *range_pos)

    def get_highlighted_line(self: ErrorTraceback) -> str:
        line: str = super(ErrorTraceback, self).get_highlighted_line()
        return line[:self.spos] + "\x1b[1m" + line[self.spos:self.epos] + "\x1b[22m" + line[self.epos:]

    def format(self: ErrorTraceback) -> str:
        header, line, arrows = ERROR_TRACEBACK_SYNOPSIS

        header %= (self.file.name, self.line_no + 1)
        line %= self.get_highlighted_line()
        arrows %= (" " * self.spos, "^" * (self.epos - self.spos))

        return header + line + arrows
