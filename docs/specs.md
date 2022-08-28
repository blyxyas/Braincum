# Braincum Language Specifications

[[Go to bottom](#bottom-notes) | [Home](README.md)]

- - - -

## Summary

- [Specifiers](#specifiers)
    - [Subject specifiers](#subject-specifiers)
    - [Context specifiers](#context-specifiers)
- [Operations](#operations)
    - [Memory operations](#memory-operations)
        - [Specifiable](#specifiable)
        - [Non-Specifiable](#non-specifiable)
    - [I/O operations](#io-operations)
        - [Specifiable](#specifiable-1)
        - [Non-Specifiable](#non-specifiable-1)
- [Functions](#functions)
    - [Utilitaries](#utilitaries)
        - [Specifiable](#specifiable-2)
- [Algorithms](#algorithms)
    - [Char algorithm](#char-algorithm)
- [Bottom notes](#bottom-notes)

- - - -

## Specifiers

<sub>[[Summary](#summary)]</sub>

A specifier indicates the execution context of the following operations until another specifier is encountered.

### Subject specifiers

- `&` (ref): the following operations will be applied to the address.
- `$` (value): the following operations will be applied to the value.

### Context specifiers

- `[`...`]` (loop): the enclosed operations will be repeated until the value of the entering cell drops to 0.

- `{`...`}` (sliced array scope): the enclosed operations will only be applied in a subarray whose size is given by the entering cell value.

## Operations

<sub>[[Summary](#summary)]</sub>

### Memory operations

#### **Specifiable**

- `+`: increments value/address by 1.
- `-`: decrements value/address by 1.
- `^`: resets value/address to 0.
- `~`: opposes value/address to bound<sup>[[1](#bottom-note-1)]</sup>.
- `@`:
    - value: sets to address % 255.
    - address: sets to value.
- `'`: applies the [Char algorithm](#char-algorithm).
- `"`: stringifies the value/address and changes to its ordinal<sup>[[2](#bottom-note-2)]</sup>.

#### **Non-Specifiable**

- `>`: shifts all the cells to the right<sup>[[3](#bottom-note-3)]</sup>.
- `<`: shifts all the cells to the left<sup>[[3](#bottom-note-3)]</sup>.

### I/O operations

#### **Specifiable**

- `.`: prints the current value/address as an ASCII character.
- `,`: asks for an integer input between 0 and 255.
- `!`: throws an error. The error code is determined by the value/address.
- `#`: prints value/address as an integer.

#### **Non-Specifiable**

- `:`: prints the `n`-th next cells as a string with `n` as the value of the current cell.
- `;`: prints the last input if not empty, else asksfor another one and prints it.
- `?`: asks for an ASCII string and stores it in following cells starting at current one.

## Functions

<sub>[[Summary](#summary)]</sub>

### Utilitaries

#### **Specifiable**

- `r`: adds a random integer between 0 and 255 to the value/address.
- `s`: sums all the values before the current cell (included) and puts the result as new value/address.
- `m`:
    - value: multiplies by address.
    - address: multiplies by value.

- - - -

## Algorithms

<sub>[[Summary](#summary)]</sub>

### Char algorithm

Ensures that the value is in ASCII letter boundaries.

- If the value is below 64: adds 64.
- If the value is between 64 and 127: does nothing.
- If the value is between 128 and 195: removes 64.
- If the value is above 195: removes 128.

A retranscription in Python of this algorithm would be as following:

```py
if value <= 64:
    value += 64
elif 128 <= value <= 195:
    value -= 64
elif 196 <= value <= 255:
    value -= 128
```

- - - -

## Bottom Notes

<sub>[[Summary](#summary)]</sub>

### Bottom Note 1

Example: 3 would be opposed to 252 (0->3 becomes 255->3).
[[Go back up](#specifiable)]

### Bottom Note 2

Example: 3 would be stringified to "3", which has an ordinal of 51.
[[Go back up](#specifiable)]

### Bottom Note 3

- In the context of the global array scope, it essentially loses the first cell value or adds a 0 to the left according to the shift direction, as the array is infinite.

- In the context of a sliced array scope, the bounds are joined on the shift as it was a loop. For example, applying `>` to `[3, 5, 2, 1]` would give `[1, 3, 5, 2]`.

    [[Go back up](#non-specifiable)]

[[Go to top](#braincum-operations) | [Home](README.md)]
