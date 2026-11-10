"""GF's parse of a line kept on disk (the parse cost `suite-cost.md` and the r3 layer 2 gate measured): its trees
before the guards, or the index GF stopped at, under
`${XDG_CACHE_HOME:-~/.cache}/shopsystem-bdd/parse/<sources sha>/<grammar>/<key>.json`.

The key is everything the parse reads: the sha of the grammar's sources (the core files and those generated from
the lexicon), the grammar, the lexicon's words (the literal slot refuses them), the text given to GF and `LIMIT`. An
entry is written by a rename, so processes side by side read a whole one or none; a cache that cannot be written
or read is passed over, never an error.
"""
import hashlib
import json
import os
import tempfile
from pathlib import Path

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
    path, tmp = _path(sha, grammar, digest), None
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".tmp-")
        with os.fdopen(fd, "w") as out:
            json.dump({"trees": trees, "at": at}, out, ensure_ascii=False)
        os.replace(tmp, path)
    except (OSError, TypeError, ValueError):
        if tmp is not None:
            Path(tmp).unlink(missing_ok=True)
