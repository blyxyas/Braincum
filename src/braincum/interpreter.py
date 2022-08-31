#!/usr/bin/env python3

from __future__ import annotations
from enum import IntEnum

from braincum.errors import Error, panic

__all__ = ["Interpreter"]


class Subject(IntEnum):
    none = 0  # No subject
    ref = 1  # &
    val = 2  # $


class Context(IntEnum):
    glob = 0  # Global context
    loop = 1  # [...] (loop scope)
    sas = 2  # {...} (sliced array scope)


class Interpreter:
    @property
    def code(self: Interpreter) -> list[str]:
        return self.__code.splitlines()

    def __init__(self: Interpreter, source_code: str | bytes) -> None:
        if isinstance(source_code, bytes):
            self.__code = source_code.decode("utf-8")
        else:
            self.__code = source_code

        self.subject: Subject = Subject.none
        self.context: Context = Context.glob

        self.global_ptr: int = 0
        self.scope_ptr: int = 0

        self.memory_table: list[int] = init_memory(size=2048)
        self.stdout: str = ""

        self.syntax_check()

    def syntax_check(self: Interpreter) -> None:
        subject_specifiers = {"&", "$"}
        context_openers = {"[", "{"}
        context_closers = {"]", "}"}
        requires_subject = {"+", "-", "^", "@", "'",
                            "\"", ".", ",", "!", "#", "r", "s", "m"}
        previous_char = ""

        subject: bool = False
        contexts: list[Context] = [Context.glob]

        for line_no, line in enumerate(self.code, start=1):
            for char_no, char in enumerate(line):
                if char in requires_subject and not subject:
                    panic(Error.MissingSpecifier, char_no, line_no)
                elif char in context_closers:
                    if contexts[-1]:
                        if (char == "}" and contexts[-1] == Context.loop) or (char == "]" and contexts[-1] == Context.sas):
                            panic(Error.UnexpectedSpecifier,
                                  char, char_no, line_no)
                        elif previous_char in context_openers and get_opposite_brace(previous_char) == char:
                            panic(Error.EmptyLoop if char ==
                                  "]" else Error.NoOperationInArray, char_no, line_no)
                        else:
                            _ = contexts.pop()
                    else:
                        panic(Error.UnexpectedSpecifier,
                              char, char_no, line_no)
                elif char in context_openers:
                    contexts.append(Context.loop if char ==
                                    "[" else Context.sas)
                    subject = False
                elif char in subject_specifiers:
                    subject = True
                else:
                    if char in requires_subject:
                        if not subject:
                            panic(Error.MissingSpecifier, char_no, line_no)
                    else:
                        if previous_char in subject_specifiers:
                            panic(Error.UnexpectedSpecifier,
                                  char_no-1, line_no)


def get_opposite_brace(char: str) -> str:
    braces = ["(", "[", "{", "}", "]", ")"]

    if char not in braces:
        return char
    return braces[-braces.index(char)-1]


def init_memory(*, size: int) -> list[int]:
    return [0 for _ in range(size)]
