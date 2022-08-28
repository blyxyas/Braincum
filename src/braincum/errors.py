#!/usr/bin/env python3

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path

__all__ = ["Error", "panic"]


_tag = "\x1b[1;41m ERR \x1b[30;47m Braincum \x1b[22;39;49m"


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

    def format(self: BCError, *args: object) -> str:
        """
        Returns:
            str: printable formatted string that represents the error
        """

        self._check_args(args)

        return f"{_tag} \x1b[1m{self.errname}:\x1b[22m \x1b[31m{self.message % args}\x1b[39m"

    def throw(self: BCError, *args: object) -> None:
        print(self.format(*args))


def _incorrect_token(incorrectness: str, token_name: str, *, known: bool) -> str:
    """
    Error message generator for incorrect token errors.

    Args:
        incorrectness (str): name of the incorrectness (e.g. "unexpected", "missing" ...)
        token_name (str): the name of the incorrect token

    Returns:
        str: the error message
    """

    return incorrectness + " " + token_name + (" '%s' " if known else " ") + "at position %d (line %d)"


def _unexpected_token(token_name: str, /) -> str:
    """
    Error message generator for unexpected token errors.

    Args:
        token_name (str): the name of the unexpected token

    Returns:
        str: the error message
    """

    return _incorrect_token("unexpected", token_name, known=True)


def _missing_token(token_name: str, /) -> str:
    """
    Error message generator for missing token errors.

    Args:
        token_name (str): the name of the missing token

    Returns:
        str: the error message
    """

    return _incorrect_token("missing", token_name, known=False)


class Error(Enum):
    Unknown = BCError("Unknown", (), "an unknown error occured")

    # *- I/O Errors -* #
    FileNotFound = BCError("FileNotFound", (Path,),
                           "file '%s' could not be found", code=2)
    NotReadableFile = BCError(
        "NotReadableFile", (Path,), "file '%s' is not readable", code=2)

    # *- Syntax Errors -* #
    UnexpectedSpecifier = BCError(
        "UnexpectedSpecifier", (str, int, int), _unexpected_token("specifier"))
    UnexpectedOperator = BCError(
        "UnexpectedOperator", (str, int, int), _unexpected_token("operator"))
    MissingSpecifier = BCError(
        "MissingSpecifier", (int, int), _missing_token("specifier"))
    MissingOperator = BCError(
        "MissingOperator", (str, int, int), _missing_token("operator"))
    EmptyLoop = BCError("EmptyLoop", (int, int),
                        "empty loop at position %d (line %d)")
    NoOperationInArray = BCError(
        "NoOperationInArray", (int, int), "no operation in array at position %d (line %d)")


def panic(error: Error, *args: object):
    """
    Raises a Braincum error.

    Args:
        error (BCError): error to raise

    Raises:
        SystemExit: _description_
    """

    if not isinstance(error, Error):
        raise TypeError("error must be an Error")

    bc_error: BCError = error.value
    bc_error.throw(*args)

    raise SystemExit(bc_error.code)
