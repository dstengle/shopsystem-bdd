"""The grammar a line is read in, in a mixed spec (CNL 4's I19, call 15; its design's section 10.1 and section 13
point 3): a capability's line in its capability file's grammar, grammar 4 when the file says `language: codified-2`,
the old grammar when it says `codified-1`; a universal condition in the grammar `spec/universal.md`'s own marker
names (b151), whatever the index says; a line of no capability and not universal (a line `model parse` is given
alone) in the grammar `spec/index.md`'s marker names. `parse` gives a refusal of a grammar 4 line that a reading
rule refuses (spec_lf_read), as `model logic` refuses it."""
from pathlib import Path

import spec_grammar
import spec_grammar4
import spec_read


def four(root, capability=None, universal=False):
    """True when a line of `capability` (or of none; a universal condition with `universal`) is read in grammar 4."""
    if universal:
        return spec_read.codified(Path(root) / "spec" / "universal.md", (spec_read.MARKER4,))
    path = Path(root) / "spec" / "capabilities" / ("%s.md" % capability) if capability else None
    if path is not None and spec_read.codified(path):
        return spec_read.codified(path, (spec_read.MARKER4,))
    return spec_grammar4.marked(root)


def parse(root, text, capability=None, universal=False):
    """The line parsed in its grammar: an object with `tree`, `trees` and `refusal`, as spec_grammar's and
    spec_grammar4's parses have."""
    if not four(root, capability, universal):
        return spec_grammar.parse(root, text)
    import spec_lf_read
    parsed = spec_grammar4.parse(root, text)
    why = parsed.tree and spec_lf_read.refusal(spec_grammar4.load(root)[0], parsed.tree)
    return spec_grammar4.Parse(refusal=why, trees=[parsed.tree]) if why else parsed


def hint(root, text, capability=None, universal=False):
    """The hint of a refused line, in its grammar: the prefix that parsed and the nearest words (and, in grammar 4,
    the terms that may follow)."""
    return (spec_grammar4 if four(root, capability, universal) else spec_grammar).hint(root, text)
