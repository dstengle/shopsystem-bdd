"""A line that uses a construct the construct catalogue has no entry of, refused (parsing#r6, b369): the catalogue of
the context the line is read in, `grammar/constructs.md` (one `## <code>` heading an entry, as `spec constructs
--write` writes it), against the constructs of grammar 4 (model_constructs_table); a context that keeps no catalogue
checks nothing. A construct is told in a tree as `spec constructs` tells it (model_constructs' `uses`), and only the
constructs the catalogue lacks are looked for, so a current catalogue costs one read of its headings."""
import re
from functools import cache
from pathlib import Path

CATALOGUE = "grammar/constructs.md"


@cache
def _codes(path, _stamp):
    """The construct codes of the catalogue at path; `_stamp`, its mtime, only keys the cache."""
    return frozenset(re.findall(r"^## ([a-z]+(?:-[a-z]+)*)\s*$", Path(path).read_text(), re.MULTILINE))


def missing(root):
    """The constructs of grammar 4 the context's catalogue has no entry of ([] when it keeps none)."""
    from model_constructs_table import CONSTRUCTS
    path = Path(root) / CATALOGUE
    if not path.is_file():
        return []
    have = _codes(str(path), path.stat().st_mtime_ns)
    return [e for e in CONSTRUCTS if e["code"] not in have]


def refusal(root, vocab, tree):
    """The refusal of a tree that uses a construct the catalogue has no entry of, naming the construct, or None."""
    lacking = missing(root)
    if not lacking:
        return None
    import model_constructs
    frames = model_constructs.roles(vocab)
    found = next((e["code"] for e in lacking if model_constructs.uses(e, tree, frames)), None)
    return found and ("refused: the line uses the construct `%s`, which the construct catalogue %s has no entry of"
                      % (found, CATALOGUE))
