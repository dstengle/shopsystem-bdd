"""Grammar 4's inputs and their state (b430): the files the vocabulary and the packs read (`inputs`: `spec/index.md`,
`spec/packs/`, of a context with a domain model `spec/model/` and `spec/vocabulary/`, else the capability files, the
plugin's packs and the base grammar's files), their (path, mtime_ns, size) and whether `spec/model/` is a folder
(`state`). Outside a held scope every call stats them again; while a root is held (`held`, as the readiness bar holds
its copy) they are statted once, until a writer of the root says it changed (`invalidate`, as a lay and an unlay do),
and what is kept for that state (`memo`: a line's parse) lives exactly as long."""
import contextlib
import functools
import os
from pathlib import Path

GRAMMARS = Path(__file__).resolve().parent.parent / "grammar"
PACKS = GRAMMARS / "packs"
BASE = ("Base.gf", "BaseEng.gf", "Time.gf", "TimeEng.gf")
_held = {}      # resolved root: [its state or None, {memo key: value}, depth]


def _md(top):
    """The .md files right under `top`, sorted; none when it is no folder."""
    try:
        return sorted(os.path.join(top, n) for n in os.listdir(top) if n.endswith(".md"))
    except OSError:
        return []


def inputs(root):
    """The paths of the files grammar 4's vocabulary is read from, in a fixed order."""
    spec = os.path.join(str(root), "spec")
    modelled = os.path.isdir(os.path.join(spec, "model"))
    own = (_md(os.path.join(spec, "model")) + _md(os.path.join(spec, "vocabulary")) if modelled
           else _md(os.path.join(spec, "capabilities")))
    return ([os.path.join(spec, "index.md")] + _md(os.path.join(spec, "packs")) + own + _md(str(PACKS))
            + [str(GRAMMARS / name) for name in BASE])


def _stat(root):
    out = [os.path.isdir(os.path.join(str(root), "spec", "model"))]
    for path in inputs(root):
        try:
            st = os.stat(path)
            out.append((path, st.st_mtime_ns, st.st_size))
        except OSError:
            out.append((path, None, None))
    return tuple(out)


def _key(root):
    return os.path.realpath(str(root))


def state(root):
    """The state of the inputs of `root`: statted once while it is held, on every call otherwise."""
    entry = _held.get(_key(root))
    if entry is None:
        return _stat(root)
    if entry[0] is None:
        entry[0] = _stat(root)
    return entry[0]


@contextlib.contextmanager
def held(root):
    """`root`'s inputs statted once and its memo kept within the block (nested blocks share one); cleared on exit."""
    key = _key(root)
    entry = _held.setdefault(key, [None, {}, 0])
    entry[2] += 1
    try:
        yield
    finally:
        entry[2] -= 1
        if entry[2] == 0:
            _held.pop(key, None)


def invalidate(root):
    """`root` was written: a held state and its memo are dropped, statted again on the next call."""
    entry = _held.get(_key(root))
    if entry is not None:
        entry[0], entry[1] = None, {}


def resolved(root):
    """`Path(root).resolve()`, once a held scope."""
    return memo(root, ("resolved",), lambda: Path(root).resolve())


def memo(root, key, make):
    """`make()`, kept under `key` for the held state of `root`; computed every time outside a held scope."""
    entry = _held.get(_key(root))
    if entry is None:
        return make()
    if key not in entry[1]:
        entry[1][key] = make()
    return entry[1][key]


def writes(function):
    """A writer of the spec under its first argument, `root`: its held state invalidated after it, whatever happens."""
    @functools.wraps(function)
    def written(root, *args, **kwargs):
        try:
            return function(root, *args, **kwargs)
        finally:
            invalidate(root)
    return written
