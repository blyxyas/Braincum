# 🧠💦 Braincum

Braincum is a non-strict superset of the famous Brainfuck esoteric programming language.

- - - -

## Summary

- [🔎 Differences](#differences)
    - [🔤 Grammar](#grammar)
    - [🔢 Meaning of some characters](#meaning-of-some-characters)
- [🤖 How Braincum works](#how-braincum-works)
- [🚀 To go further](#to-go-further)
- [💬 How to censor the language's name?](#how-to-censor-the-languages-name)

- - - -

## Differences

### Grammar

- Brainfuck relies on 8 characters that provide 8 different operations.
- As for Braincum, the alphabet consists in 25 characters ;
however, in contrary to Brainfuck, some of these can be combined, which gives a total of 33 instructions.

### Meaning of some characters

Let's give an example:
- In Brainfuck, to move the pointer to the right, you would use `>`.
- In Braincum, things are slightly different: to do the same operation, you would type `&+`.

> The meaning of `>` is completely different in Braincum: it shifts all the values to the right.

## How Braincum works

➡️ When you do an operation in Braincum, you need to specify if it applies to the current cell's value (`$`) or the pointer (`&`).

Here's an example in Braincum:
```
$++[&+$++&-$-]
```

Here's the equivalent in Brainfuck:
```bf
++[>++<-]
```


🤔 Coming from Brainfuck, it seems verbose and unnecessary at first...

🤩 But this is incredibly powerful as it means that you can also apply operations to the pointer (whose position is referred as "address" hereafter), making programs that would be long and complex in Brainfuck surprisingly short and simple.

## To go further

Convinced? Check [`specs.md`](specs.md#braincum-language-specifications) to get a complete list of the nice features that Braincum has to offer.

## How to censor the language's name?

In some context, it may be inappropriate to spell the language's full name.

Here are some of my personal recommendations for censoring it:

- Brainsperm
- Brainc*m
- Brainc##
- 🧠💦
- Better Brainfuck (😎)

You can use your own, as long as your interlocutor knows what you are referring to 😆
