"""Example data in a requirement line (the CNL 4 design, call 7, I18): each code or quoted string a line holds that
names no declared constant is a parameter, bound by its group's given block, and `model check` warns of it
(`w_example`, the requirement exemplified).

A literal is a declared constant when it is an actor (or another proper noun's name), an attribute's value, a command
(a code that opens with a tool's name, or the code a "runs" takes), an option (a code that opens with `-`, or one
before "option"), or a rule code of `model` (a code of model.lp's labels, or `model logic`'s L<n>). The reading is of
the line's text and the lexicon, so it reads a line of either grammar."""
import re
from pathlib import Path

LITERAL = re.compile(r"`([^`]+)`|\"([^\"]+)\"")
LP = Path(__file__).resolve().with_name("model.lp")
FINDING = re.compile(r"L\d+")


def _rule_codes():
    return set(re.findall(r'^label\("([^"]+)"', LP.read_text(), re.MULTILINE)) if LP.is_file() else set()


def constants(lexicon):
    """(the declared constants of a lexicon, spelled bare, and the names a command may open with)."""
    bare = lambda word: word.replace("`", "").strip()       # noqa: E731
    names = {bare(t.term) for t in lexicon.terms if t.category == "actor"}
    values = {bare(v) for v, _, _, _ in lexicon.values()}
    return names | values | _rule_codes(), names


def declared(word, text, start, end, known):
    """Whether the literal `word` (at text[start:end]) names a declared constant of `known` (constants' pair)."""
    words, names = known
    if word in words or FINDING.fullmatch(word) or word.startswith("-"):
        return True
    if text[:start].rstrip().endswith(("runs", "run")) or text[end:].lstrip().startswith("option"):
        return True
    return word.split()[0] in names       # `work start`: a command of the tool `work`


def parameters(text, known):
    """The literals of a requirement's text that name no declared constant, in the order the line says them."""
    out = []
    for m in LITERAL.finditer(text):
        word = m.group(1) or m.group(2)
        if not declared(word, text, m.start(), m.end(), known) and word not in out:
            out.append(word)
    return out
