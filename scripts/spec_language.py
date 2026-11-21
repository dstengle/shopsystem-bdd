"""The grammar a line is read in (CNL 4's I19, call 15): grammar 4, the one language. `four` says whether a file says
`language: codified-2`: a capability's line by its capability file's marker, a universal condition by
`spec/universal.md`'s own (b151), whatever the index says, and a line of no capability and not universal (a line
`model parse` is given alone) by `spec/index.md`'s; a file in `codified-1` is not read (v_p0 names it, with `migrate
upgrade`). `parse` gives a refusal of a line that a reading rule refuses (spec_lf_read), as `model logic` refuses it,
and of a line that uses a construct the context's construct catalogue has no entry of (spec_catalogued, b369)."""
from pathlib import Path

import spec_grammar4
import spec_held
import spec_read


def four(root, capability=None, universal=False):
    """True when the file of a line of `capability` (or of none; a universal condition with `universal`) says
    `language: codified-2`."""
    if universal:
        return spec_read.codified(Path(root) / "spec" / "universal.md", (spec_read.MARKER4,))
    path = Path(root) / "spec" / "capabilities" / ("%s.md" % capability) if capability else None
    if path is not None and spec_read.codified(path):
        return spec_read.codified(path, (spec_read.MARKER4,))
    return spec_grammar4.marked(root)


def parse(root, text):
    """The line parsed in grammar 4: an object with `tree`, `trees` and `refusal`, as spec_grammar4's parse has; once a
    state of the root's inputs while it is held (spec_held, b430)."""
    return spec_held.memo(root, ("language", text), lambda: _parse(root, text))


def _parse(root, text):
    import spec_catalogued
    import spec_lf_read
    parsed = spec_grammar4.parse(root, text)
    vocab = parsed.tree and spec_grammar4.load(root)[0]
    why = parsed.tree and (spec_lf_read.refusal(vocab, parsed.tree)
                           or spec_catalogued.refusal(root, vocab, parsed.tree))
    return spec_grammar4.Parse(refusal=why, trees=[parsed.tree]) if why else parsed


def hint(root, text):
    """The hint of a refused line: the prefix that parsed, the nearest words and the terms that may follow."""
    return spec_grammar4.hint(root, text)
