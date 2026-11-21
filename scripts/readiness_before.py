"""The readiness bar's result of the copy before the item's lines are laid, kept on disk (b430): the lexicon's problems
and the violations of `model.lp`'s rules of the copy's `spec/` (after a batch's `others`), which every run on one
state of `spec/` computes alike. Kept under `${XDG_CACHE_HOME:-~/.cache}/shopsystem-bdd/readiness/<key>.json`, the key
everything it reads (`key`): each file of the copy's `spec/` and `grammar/` (its construct catalogue, b444) by its path
and bytes, the plugin's scripts, grammar and packs, the RGL's release and path, GF's binary, `$SHOPSYSTEM_GF_RGL_SRC`,
and pgf's and clingo's versions. The copy's own path is written as a placeholder, so a result is the same for every
copy of one `spec/`. A result that cannot be written or read is computed again, never an error."""
import hashlib
import json
import os
import tempfile
from importlib import metadata
from pathlib import Path

import tools_grammar

VERSION = 1
PLUGIN = Path(__file__).resolve().parent.parent
HERE = "\0copy\0"


def _base():
    return Path(os.environ.get("XDG_CACHE_HOME") or Path.home() / ".cache") / "shopsystem-bdd" / "readiness"


def _files(top, suffixes=None):
    for d, dirs, names in os.walk(top):
        dirs[:] = sorted(n for n in dirs if n != "__pycache__")
        for name in sorted(names):
            if suffixes is None or name.endswith(suffixes):
                yield os.path.join(d, name)


def _version(name):
    try:
        return metadata.version(name)
    except metadata.PackageNotFoundError:
        return None


def key(copy):
    """The name of the before-lay result of the copy at `copy`: a hash of all it reads."""
    digest = hashlib.sha256()

    def add(*parts):
        for part in parts:
            digest.update(part if isinstance(part, bytes) else str(part).encode())
            digest.update(b"\0")
    gf = tools_grammar.gf_binary()
    stamp = os.stat(gf) if gf and os.path.exists(gf) else None
    add(VERSION, tools_grammar.RGL_RELEASE, tools_grammar.rgl_path(), gf, stamp and (stamp.st_mtime_ns, stamp.st_size),
        os.environ.get("SHOPSYSTEM_GF_RGL_SRC"), _version("pgf"), _version("clingo"))
    for top, suffixes in ((Path(copy) / "spec", None), (Path(copy) / "grammar", None), (PLUGIN / "scripts", None),
                          (PLUGIN / "grammar", (".gf", ".lp", ".md", ".toml"))):
        add(top.relative_to(copy) if top.is_relative_to(copy) else "plugin/%s" % top.name)
        for path in _files(top, suffixes):
            with open(path, "rb") as handle:
                add(os.path.relpath(path, top), handle.read())
    return digest.hexdigest()


def _out(value, copy):
    if isinstance(value, str):
        return value.replace(copy, HERE)
    return [_out(v, copy) for v in value] if isinstance(value, (list, tuple, set, frozenset)) else value


def _in(value, copy):
    if isinstance(value, str):
        return value.replace(HERE, copy)
    return tuple(_in(v, copy) for v in value) if isinstance(value, list) else value


def get(copy, digest):
    """(lexicon problems, violations) kept under `digest`, as sets of tuples, or None."""
    try:
        data = json.loads((_base() / ("%s.json" % digest)).read_text())
        return set(_in(data["lexicon"], str(copy))), set(_in(data["violations"], str(copy)))
    except (OSError, ValueError, KeyError, TypeError):
        return None


def put(copy, digest, lexicon, violations):
    base, tmp = _base(), None
    try:
        base.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=base, prefix=".tmp-")
        with os.fdopen(fd, "w") as out:
            json.dump({"lexicon": _out(sorted(lexicon), str(copy)),
                       "violations": _out(sorted(violations), str(copy))}, out, ensure_ascii=False)
        os.replace(tmp, base / ("%s.json" % digest))
    except (OSError, TypeError, ValueError):
        if tmp is not None:
            Path(tmp).unlink(missing_ok=True)


def before(copy, compute):
    """(lexicon problems, violations) of the copy as it stands: kept, else `compute()` and kept."""
    digest = key(copy)
    found = get(copy, digest)
    if found is None:
        found = compute()
        put(copy, digest, *found)
    return found
