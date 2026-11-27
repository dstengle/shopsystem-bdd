"""GF's parse of a line kept on disk (the parse cost `suite-cost.md` and the r3 layer 2 gate measured): its trees
before the guards, or the index GF stopped at, under `${XDG_CACHE_HOME:-~/.cache}/shopsystem-bdd/parse/`.

`key`, `get` and `put` keep a parse under `<sources sha>/<grammar>/<key>.json`, the key everything the parse reads:
the sha of the grammar's sources (the core files and those generated from the lexicon), the grammar, the lexicon's
words (the literal slot refuses them), the text given to GF and `LIMIT` (the step grammar's parses).

`lookup` and `keep` keep grammar 4's parse of a line by its footprint (spec_footprint, b877) under
`../parse-footprint/<grammar>/<footprint>.json`, a store beside the parse cache (so a parse adds one entry to the
cache), the footprint found once a set of sources under the sha's key (`<sources sha>/<grammar>/<key>.json` holding
`{"footprint": ...}`, and the parse too once it is parsed or read): so a change of the sources that leaves the
line's footprint as it was reads the parse kept, with no compile. A parse that GF stopped in (its index depends on
every function of the grammar) or that `LIMIT` cut (its trees on GF's order of them) is read only under the sha it
was parsed with. An entry is written by a rename, so processes side by side read a whole one or none; a cache that
cannot be written or read is passed over, never an error.
"""
import hashlib
import json
import os
import tempfile
from pathlib import Path

import spec_footprint

VERSION = 2


def _base():
    return Path(os.environ.get("XDG_CACHE_HOME") or Path.home() / ".cache") / "shopsystem-bdd" / "parse"


def key(sha, grammar, text, words, limit=0):
    blob = json.dumps([VERSION, sha, grammar, text, sorted(words), limit], ensure_ascii=False)
    return hashlib.sha256(blob.encode()).hexdigest()


def _path(sha, grammar, digest):
    return _base() / sha / grammar / ("%s.json" % digest)


def _tuples(value):
    return tuple(_tuples(v) for v in value) if isinstance(value, list) else value


def get(sha, grammar, digest):
    """(trees, error index or None) of a cached parse, or None on a miss."""
    try:
        data = json.loads(_path(sha, grammar, digest).read_text())
        return [_tuples(t) for t in data["trees"]], data["at"]
    except (OSError, ValueError, KeyError, TypeError):
        return None


def put(sha, grammar, digest, trees, at):
    _write(_path(sha, grammar, digest), {"trees": trees, "at": at})


def _write(path, data):
    tmp = None
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".tmp-")
        with os.fdopen(fd, "w") as out:
            json.dump(data, out, ensure_ascii=False)
        os.replace(tmp, path)
    except (OSError, TypeError, ValueError):
        if tmp is not None:
            Path(tmp).unlink(missing_ok=True)


def _read(path):
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError):
        return None


def _kept(grammar, footprint):
    base = _base()
    return base.with_name(base.name + "-footprint") / grammar / ("%s.json" % footprint)


def lookup(sha, srcs, grammar, text, words, limit):
    """(the slot of `text` in the sources `srcs` named `sha`: its footprint, the names of its functions and its
    key, (trees, error index or None) of its parse kept, or None); `srcs` None when the caller has not the sources,
    whose footprint is then the sha's. A parse kept under the sha's key is read as it is; one kept by the footprint
    is renamed to these sources' names, its trees shortest first, then by their text (spec_grammar4's order), and
    kept under the sha's key too."""
    digest = key(sha, grammar, text, words, limit)
    found = _read(_path(sha, grammar, digest))
    try:
        slot = (str(found["footprint"]), dict(found["names"]), digest)
        if "trees" in found:
            return slot, ([_tuples(t) for t in found["trees"]], found["at"])
    except (KeyError, TypeError, ValueError):
        slot = spec_footprint.of(spec_footprint.index(srcs, sha), sha, text, words, limit) + (digest,)
        if srcs is not None:
            _write(_path(sha, grammar, digest), {"footprint": slot[0], "names": slot[1]})
    data = _read(_kept(grammar, slot[0]))
    try:
        if data["at"] is None and data["complete"] or data["sha"] == sha:
            trees = sorted((spec_footprint.rename(t, slot[1]) for t in data["trees"]), key=lambda t: (len(t), t))
            _alias(sha, grammar, slot, trees, data["at"])
            return slot, (trees, data["at"])
    except (KeyError, TypeError):
        pass
    return slot, None


def _alias(sha, grammar, slot, trees, at):
    """The parse kept under the sha's key with the slot, which `get` reads too."""
    _write(_path(sha, grammar, slot[2]), {"footprint": slot[0], "names": slot[1], "trees": trees, "at": at})


def keep(sha, grammar, slot, trees, at, complete):
    """A parse kept by its slot's footprint, its trees with the footprint's names (`complete` when GF gave every
    tree, fewer than LIMIT), and under the sha's key."""
    names = {n: c for c, n in slot[1].items()}
    _write(_kept(grammar, slot[0]), {"trees": [spec_footprint.rename(t, names) for t in trees], "at": at,
                                     "complete": bool(complete), "sha": sha})
    _alias(sha, grammar, slot, trees, at)
