"""A state's parse misses parsed side by side (b430): the lines of a context's codified-2 capabilities and universal
conditions (`texts`) that spec_parse_cache does not hold for its grammar 4 (`misses`, keyed exactly as spec_grammar4's
parse keys them) parsed by a pool of processes and kept in the cache (`prefetch`), so that the readers after it (the
model facts, `spec logic`, `features generate`) only read the cache. The pool is at most min(8, cpus // 4) processes
(`workers`), each a fresh interpreter (the parent has loaded clingo and pgf; nothing of the caller's runs again in it)
that loads the compiled grammar once; a pool that fails leaves the misses to be parsed one by one, as before."""
import json
import os
import subprocess
import sys
from pathlib import Path

import spec_gf
import spec_grammar4
import spec_parse_cache
import spec_read
import spec_rgl


def workers(cpus=None):
    """The pool's size for `cpus` processors (os.cpu_count's when None): a quarter of them, at most 8, at least 1."""
    cpus = (os.cpu_count() or 1) if cpus is None else cpus
    return max(1, min(8, cpus // 4))


def texts(root):
    """The requirement lines of the codified-2 capabilities of `root` and its universal conditions when
    `spec/universal.md` says codified-2, each once, in file order."""
    out = []
    for path in sorted((Path(root) / "spec" / "capabilities").glob("*.md")):
        if spec_read.codified(path, (spec_read.MARKER4,)):
            out += [r.text for g in spec_read.capability(path, (spec_read.MARKER4,)).groups for r in g.requirements]
    universal = Path(root) / "spec" / "universal.md"
    if universal.is_file() and spec_read.codified(universal, (spec_read.MARKER4,)):
        out += [c.text for c in spec_read.read_universal(root).conditions]
    return list(dict.fromkeys(out))


def _keyed(root, lines):
    """(sha, words, [(line, gf text, cache key)]) of `lines` in the grammar 4 of `root`."""
    vocab, _, name = spec_grammar4._named(root)
    words = {w.replace(" ", spec_rgl.TOKEN) for w in vocab.words}
    out = []
    for line in lines:
        text = spec_gf.gf_text(spec_gf.tokenise(line))
        out.append((line, text, spec_parse_cache.key(name, spec_grammar4.GRAMMAR, text, words, spec_grammar4.LIMIT)))
    return name, words, out


def misses(root, lines):
    """The lines of `lines` whose parse the cache does not hold, in order."""
    name, _, keyed = _keyed(root, lines)
    return [line for line, _, digest in keyed if spec_parse_cache.get(name, spec_grammar4.GRAMMAR, digest) is None]


def _work(order):
    """A worker's lines (`order`: the PGF's path, the sha, the words and [(line, key)]) parsed and kept in the cache."""
    import pgf
    gram, words = pgf.readPGF(order["pgf"]), set(order["words"])
    for line, digest in order["jobs"]:
        found = spec_grammar4._gf_trees(gram, words, spec_gf.tokenise(line))
        spec_parse_cache.put(order["sha"], spec_grammar4.GRAMMAR, digest, *found)


def prefetch(root, lines, processes=None):
    """The misses of `lines` parsed and kept in the cache: by a pool of `processes` (`workers()`'s when None) when there
    are more of them than one, else (or when the pool fails) one by one in this process."""
    try:
        name, words, keyed = _keyed(root, lines)
    except (ImportError, spec_gf.GrammarError):        # no grammar: the readers after it say so
        return
    jobs = [(name, line, digest) for line, _, digest in keyed
            if spec_parse_cache.get(name, spec_grammar4.GRAMMAR, digest) is None]
    processes = min(workers() if processes is None else processes, len(jobs))
    if processes > 1:
        try:
            _pool(jobs, processes, str(spec_gf.cache() / name / ("%s.pgf" % spec_grammar4.GRAMMAR)), words)
            return
        except (OSError, RuntimeError, ImportError, EOFError):     # the serial parse below, as before
            pass
    for job in jobs:
        if spec_parse_cache.get(name, spec_grammar4.GRAMMAR, job[2]) is None:
            spec_grammar4._trees(spec_grammar4._named(root)[1], words, spec_gf.tokenise(job[1]), name)


def _pool(jobs, processes, pgf_path, words):
    """The jobs dealt round to `processes` workers, each this file run by a fresh interpreter (nothing of the caller's
    loaded, its `__main__` never run again), its order on stdin; a worker that fails a RuntimeError."""
    name = jobs[0][0]
    workers = [subprocess.Popen([sys.executable, __file__], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL, text=True) for _ in range(processes)]
    for k, worker in enumerate(workers):
        order = {"pgf": pgf_path, "sha": name, "words": sorted(words),
                 "jobs": [(line, digest) for _, line, digest in jobs[k::processes]]}
        worker.stdin.write(json.dumps(order))
        worker.stdin.close()
    failed = [code for code in (w.wait() for w in workers) if code != 0]
    if failed:
        raise RuntimeError("a parse worker exited %d" % failed[0])


if __name__ == "__main__":
    _work(json.load(sys.stdin))
