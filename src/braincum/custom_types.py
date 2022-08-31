#!/usr/bin/env python3

# pyright: reportUnnecessaryTypeIgnoreComment=false
# Note: mypy does not allow dynamic parent classes

from __future__ import annotations

from typing import Any, Protocol, TypeGuard, overload, runtime_checkable


class _UIntMeta(type(Protocol)):  # type: ignore
    def __instancecheck__(self, __instance: Any) -> TypeGuard[int]:
        if type(__instance) is not int:
            return False

        return __instance >= 0


class _CellValueMeta(_UIntMeta):
    def __instancecheck__(self, __instance: Any) -> TypeGuard[int]:
        return super().__instancecheck__(__instance) and __instance <= 0xFF


@runtime_checkable
class UInt(Protocol, metaclass=_UIntMeta):
    def __int__(self) -> int: ...
    def __index__(self) -> int: ...

    @overload
    def __add__(self, __x: UInt, /) -> UInt: ...
    @overload
    def __add__(self, __x: int, /) -> int: ...
    @overload
    def __add__(self, __x: float, /) -> float: ...
    @overload
    def __sub__(self, __x: UInt, /) -> int: ...
    @overload
    def __sub__(self, __x: int, /) -> int: ...
    @overload
    def __sub__(self, __x: float, /) -> float: ...

    @overload
    def __rmul__(self, __x: UInt, /) -> UInt: ...
    @overload
    def __rmul__(self, __x: int, /) -> int: ...
    @overload
    def __rmul__(self, __x: str, /) -> str: ...


@runtime_checkable
class CellValue(UInt, Protocol, metaclass=_CellValueMeta):
    def __int__(self) -> int: ...
    def __index__(self) -> int: ...

    @overload
    def __add__(self, __x: CellValue, /) -> CellValue: ...
    @overload
    def __add__(self, __x: int, /) -> int: ...
    @overload
    def __add__(self, __x: float, /) -> float: ...
    @overload
    def __sub__(self, __x: CellValue, /) -> int: ...
    @overload
    def __sub__(self, __x: int, /) -> int: ...
    @overload
    def __sub__(self, __x: float, /) -> float: ...

    @overload
    def __rmul__(self, __x: CellValue, /) -> CellValue: ...
    @overload
    def __rmul__(self, __x: int, /) -> int: ...
    @overload
    def __rmul__(self, __x: str, /) -> str: ...


# *- Technically unnecessary, it's for "code readability" -* #
StartPos = UInt
EndPos = UInt
