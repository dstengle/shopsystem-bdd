"""The given blocks of a codified capability file (design-r2 §9.1), read for spec_read.

A group's fenced `given` block is a list of `(line, Block or None)`: each line not indented is a given line, and the
lines indented under one that ends in ':' are its data, a docstring or a table. `example(line, block)` is the shape
test of example data, with no grammar (check point 14): `the <words> <name> holds:` with a docstring or table after
it, or `the <words> <name> holds` followed by exactly one code span or quoted string. Every other given line restates
a condition the statement already has, and is v15m.
"""
import re
from collections import namedtuple


class Block(namedtuple("Block", "kind lines")):
    """The data indented under a given line ending in ':': a docstring's lines, or a table's `|` rows."""

    @property
    def rows(self):
        return [[c.strip() for c in line.strip().strip("|").split("|")] for line in self.lines]


_NAMED = r"the (?:[\w-]+ )+(?:`[^`]+`|[\w.-]+) holds"
HOLDS_BLOCK = re.compile(r"^%s:$" % _NAMED)
HOLDS_TEXT = re.compile(r"""^%s (?:`[^`]*`|"[^"]*")$""" % _NAMED)


def example(line, block=None):
    """True when a given line is example data by its shape alone."""
    line = line.strip()
    if HOLDS_BLOCK.match(line):
        return block is not None
    return block is None and bool(HOLDS_TEXT.match(line))


class GivenLines:
    """The part of spec_read's Reader that reads the lines inside a ```given fence into the open group's `given`."""

    def given_line(self, n, line):
        given = self.group.given if self.group is not None else []
        if line.strip() == "```":
            self.fence = self.data_under = None
        elif line.startswith("## "):
            self.problem(self.fence, "a given block is not closed")
            self.fence = self.data_under = None
        elif not line.strip():
            return
        elif line.startswith("  "):
            self.data_line(n, line, given)
        else:
            given.append((line.strip(), None))
            self.data_under = len(given) - 1 if line.rstrip().endswith(":") else None

    def data_line(self, n, line, given):
        if self.data_under is None:
            self.problem(n, "an indented line is under no given line ending in ':'")
            return
        text, kind = line[2:], "table" if line.strip().startswith("|") else "docstring"
        step, block = given[self.data_under]
        if block is None:
            given[self.data_under] = (step, Block(kind, [text.strip() if kind == "table" else text]))
        elif block.kind != kind:
            self.problem(n, "a given block mixes table rows and text")
        else:
            block.lines.append(text.strip() if kind == "table" else text)
