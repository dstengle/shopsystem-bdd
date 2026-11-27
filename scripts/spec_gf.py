"""GF's plumbing for grammar 4 and its step grammar: a line's tokens and their text for GF, a grammar's sources
compiled and cached, a pgf expression read into nested tuples and written back, the token a parse stopped at, and the
String callback of a literal slot.

A compiled PGF is cached under `${XDG_CACHE_HOME:-~/.cache}/shopsystem-bdd/pgf/<sha>/`, the sha being that of every
source, and is written by a rename so two processes compiling at once both get a whole one. A grammar over another
already compiled (the step grammar over grammar 4) is compiled beside that one's .gf and .gfo files, copied with
their times, so GF reads its modules and compiles only the new ones (`compiled`'s `reuse`, b439), under a lock of its
sha so that processes side by side compile it once.
"""
import fcntl
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

import tools_grammar
from plumbing import phases

GRAMMARS = Path(__file__).resolve().parent.parent / "grammar"
PLACEHOLDER = "\ue000"   # a space inside one token (a backticked or quoted span) as GF is given it
TOKEN = re.compile(r'`[^`]*`|"[^"]*"|[^\s`"]+')


class GrammarError(Exception):
    """The grammar could not be built: no gf, no gf-rgl, or gf refused the sources."""


def tokens(text):
    """Words, backticked and quoted spans (kept whole), and trailing punctuation as tokens of their own."""
    out = []
    for found in TOKEN.finditer(text):
        token = found.group()
        if token[0] in '`"':
            out.append(token)
            continue
        trail = []
        while token and token[-1] in ",.;:":
            trail.insert(0, token[-1])
            token = token[:-1]
        out += ([token] if token else []) + trail
    return out


def tokenise(line):
    """A line's tokens, the first word in lower case (the grammar writes it so)."""
    out = tokens(line)
    if out and out[0][:1].isupper() and (out[0][1:].islower() or len(out[0]) == 1):
        out[0] = out[0][0].lower() + out[0][1:]
    return out


def detokenise(words):
    text = " ".join(words).replace(PLACEHOLDER, " ")
    for mark in ",.;:":
        text = text.replace(" " + mark, mark)
    return text[:1].upper() + text[1:]


def normalise(line):
    """The line as the grammar writes it: single spaces, no space before punctuation, a capital first letter."""
    return detokenise(tokenise(line))


def gf_text(words):
    return " ".join(t.replace(" ", PLACEHOLDER) for t in words)


def cache():
    return Path(os.environ.get("XDG_CACHE_HOME") or Path.home() / ".cache") / "shopsystem-bdd" / "pgf"


def _run_gf(gf, directory, concrete):
    """GF's compile of <concrete>, the built RGL (its compiled .gfo) on GF's library path when there is one."""
    rgl, env = tools_grammar.rgl_path(), dict(os.environ)
    if rgl:
        env["GF_LIB_PATH"] = os.pathsep.join(filter(None, (rgl, env.get("GF_LIB_PATH"))))
    return subprocess.run([gf, "-make", "--output-dir=" + str(directory), concrete], cwd=directory,
                          capture_output=True, text=True, env=env)


def compiled(srcs, sha, grammar, reuse=None):
    """`<grammar>.pgf` of the sources under the cache's folder `sha`, compiled unless it is there, under a lock of
    `sha`; the modules compiled in the folder `reuse` read from their .gfo."""
    base = cache()
    base.mkdir(parents=True, exist_ok=True)
    with open(base / (".lock-" + sha), "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        if not (base / sha / ("%s.pgf" % grammar)).is_file():
            compile(srcs, sha, grammar, reuse)


def _reused(tmp, srcs, reuse):
    """The names of `srcs` whose .gf and .gfo the folder `reuse` holds, copied into `tmp` with their times (a .gfo
    newer than its .gf, so GF compiles it not again)."""
    out = set()
    for name in srcs:
        gfo = Path(reuse) / (name[:-3] + ".gfo")
        if name.endswith(".gf") and gfo.is_file() and (Path(reuse) / name).is_file():
            shutil.copy2(Path(reuse) / name, tmp / name)
            shutil.copy2(gfo, tmp / gfo.name)
            out.add(name)
    return out


def compile(srcs, sha, grammar, reuse=None):
    """`<grammar>.pgf` of the sources {file name: text}, written under the cache's folder `sha`; the modules
    compiled in the folder `reuse` read from their .gfo; timed as the phase of grammar 4's compile (b876)."""
    with phases.phase(phases.COMPILE):
        _compile(srcs, sha, grammar, reuse)


def _compile(srcs, sha, grammar, reuse):
    gf = tools_grammar.gf_binary()
    if not gf:
        raise GrammarError("no gf: run `python3 scripts/shop tools install`, or set $SHOPSYSTEM_GF")
    base = cache()
    base.mkdir(parents=True, exist_ok=True)
    tmp = Path(tempfile.mkdtemp(dir=base, prefix=".tmp-"))
    try:
        copied = _reused(tmp, srcs, reuse) if reuse else set()
        for name, text in srcs.items():
            if name not in copied:
                (tmp / name).write_text(text)
        done = _run_gf(gf, tmp, "%sEng.gf" % grammar)
        if not (tmp / ("%s.pgf" % grammar)).is_file():
            raise GrammarError("gf could not compile %s:\n%s%s" % (grammar, done.stdout[-2000:], done.stderr[-2000:]))
        final = base / sha
        try:
            os.rename(tmp, final)
            tmp = None
        except OSError:
            if not (final / ("%s.pgf" % grammar)).is_file():
                os.replace(tmp / ("%s.pgf" % grammar), final / ("%s.pgf" % grammar))
    finally:
        if tmp is not None:
            shutil.rmtree(tmp, ignore_errors=True)


def tree(expr, gram):
    """A pgf expression as nested tuples. An argument the English leaves unsaid is a metavariable: `<k>_It` in a
    kind's noun-phrase slot `k_<k>_NP`, else `("?",)`."""
    unpacked = expr.unpack()
    if not isinstance(unpacked, tuple):
        return unpacked.replace(PLACEHOLDER, " ") if isinstance(unpacked, str) else unpacked
    fun, args = unpacked
    if fun is None:
        return None
    out = [fun]
    for (_, _, typ), arg in zip(gram.functionType(fun).hypos, args):
        sub = tree(arg, gram)
        if sub is None:
            cat = str(typ)
            sub = (cat[:-3] + "_It",) if cat.startswith("k_") and cat.endswith("_NP") else ("?",)
        out.append(sub)
    return tuple(out)


def expr(t):
    """Nested tuples as a pgf expression."""
    import pgf
    if isinstance(t, tuple):
        return pgf.Expr(t[0], [expr(a) for a in t[1:]])
    return pgf.Expr(t.replace(" ", PLACEHOLDER) if isinstance(t, str) else t)


def position(words, offset):
    """The index of the token at a character offset of the text given to GF."""
    start = 0
    for i, t in enumerate(words):
        start += len(t) + 1
        if offset < start:
            return i
    return len(words)


def literal(words, text):
    """GF's String callback: a literal slot reads one token, but not a vocabulary word nor a mark of punctuation,
    which ends a clause; so a line of many backticked words is not read 3^n ways."""
    import pgf

    def read(_, start):  # offsets count characters
        while start < len(text) and text[start] == " ":
            start += 1
        end = text.find(" ", start)
        end = len(text) if end < 0 else end
        token = text[start:end]
        return None if not token or token in words or token in ",.;:" else (pgf.Expr(token), 0.0, end)
    return read
