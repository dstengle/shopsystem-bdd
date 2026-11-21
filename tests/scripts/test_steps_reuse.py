"""The step grammar compiled over grammar 4's compiled modules (b439): ContextSteps is compiled in a folder holding
Context's .gf and .gfo as grammar 4's compile left them, so GF reads Context's modules and compiles only the step
grammar's; the PGF is byte for byte the one a compile of every source from scratch gives, and so are its parses."""
import pathlib
import sys
import threading

import pytest
import spec_gf
import spec_grammar4
import spec_rgl_steps

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import toolchain

REPO = pathlib.Path(__file__).resolve().parents[2]
FIXTURE = REPO / "tests" / "scripts" / "fixtures" / "codified-2"
STEPS = ("a stage s1", "the stage s1 is `done`", "the person runs `work start`")
REUSED = ("Base.gfo", "BaseEng.gfo", "Time.gfo", "TimeEng.gfo", "Context.gfo", "ContextEng.gfo")


@pytest.fixture(scope="module", autouse=True)
def tools():
    toolchain.require()


@pytest.fixture
def cache(tmp_path, monkeypatch):
    """A cache of the test's own and no grammar loaded in this process."""
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "cache"))
    for module, name in ((spec_rgl_steps, "_loaded"), (spec_rgl_steps, "_by_context"), (spec_grammar4, "_loaded")):
        monkeypatch.setattr(module, name, {})
    return spec_gf.cache()


def parses(gram, line):
    eng = gram.languages[spec_rgl_steps.GRAMMAR + "Eng"]
    return sorted(str(e) for _, e in eng.parse(spec_gf.gf_text(spec_gf.tokenise(line)), n=20))


def test_steps_compile_reads_context_compiled_modules(cache):
    _, _, context = spec_grammar4._context(FIXTURE)
    spec_grammar4.load(FIXTURE)
    _, _, sha = spec_rgl_steps._load(FIXTURE)
    for name in REUSED:
        mine, theirs = cache / sha / name, cache / context / name
        assert mine.read_bytes() == theirs.read_bytes(), name
        assert mine.stat().st_mtime_ns == theirs.stat().st_mtime_ns, "%s compiled again" % name
    assert (cache / sha / "ContextSteps.pgf").is_file()


def test_steps_compile_compiles_grammar4_first_when_missing(cache):
    _, _, context = spec_grammar4._context(FIXTURE)
    _, gram, _ = spec_rgl_steps._load(FIXTURE)
    assert (cache / context / "Context.pgf").is_file()
    assert parses(gram, STEPS[0])


def test_pgf_and_parses_equal_a_compile_from_scratch(cache):
    import pgf
    vocab, srcs, _ = spec_grammar4._context(FIXTURE)
    _, gram, sha = spec_rgl_steps._load(FIXTURE)
    full = dict(srcs)
    full.update({name: (spec_gf.GRAMMARS / name).read_text() for name in spec_rgl_steps.BASE})
    full.update(spec_rgl_steps.modules(vocab))
    spec_gf.compile(full, "scratch", spec_rgl_steps.GRAMMAR)
    old = cache / "scratch" / "ContextSteps.pgf"
    assert (cache / sha / "ContextSteps.pgf").read_bytes() == old.read_bytes()
    before = pgf.readPGF(str(old))
    for line in STEPS:
        assert parses(gram, line) == parses(before, line) != [], line


def test_concurrent_steps_compiles_give_one_whole_pgf(cache):
    _, _, context = spec_grammar4._context(FIXTURE)
    spec_grammar4.load(FIXTURE)
    vocab, srcs, _ = spec_grammar4._context(FIXTURE)
    steps = dict(srcs)
    steps.update({name: (spec_gf.GRAMMARS / name).read_text() for name in spec_rgl_steps.BASE})
    steps.update(spec_rgl_steps.modules(vocab))
    errors = []

    def run():
        try:
            spec_gf.compiled(steps, "race", spec_rgl_steps.GRAMMAR, reuse=cache / context)
        except Exception as err:   # noqa: BLE001 - a thread's failure is the test's
            errors.append(err)
    threads = [threading.Thread(target=run) for _ in range(3)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert not errors, errors
    assert (cache / "race" / "ContextSteps.pgf").stat().st_size > 0
    assert not [p for p in cache.iterdir() if p.name.startswith(".tmp-")]
