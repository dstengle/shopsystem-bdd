"""design-model-check's worlds and Thens of grammar 4's caches (b239, b240 phase 23): `model parse` run with a cache
directory of the scenario's own (`$XDG_CACHE_HOME`), into which the compiled grammar of the smallest codified-2 world
is copied from the person's cache, so that no scenario compiles one. A parse cache that holds the parse of r1 holds,
under r1's key, the parse of another line, so that what `model parse` prints shows it read the cache."""
import importlib.util
import os
import shutil
import sys
from pathlib import Path


def _sibling(name, module):
    if module not in sys.modules:
        spec = importlib.util.spec_from_file_location(module, Path(__file__).with_name(name))
        sys.modules[module] = loaded = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(loaded)
    return sys.modules[module]


H = _sibling("design_model_check_handlers.py", "shop_design_model_check_handlers")
C2 = _sibling("codified2_world.py", "shop_codified2_world")
LINE = "When a session ends a stage, `work` shall print the stage."
OTHER = "When a session ends a stage, `work` shall print the session."


def env(step):
    """The environment of `model` with the scenario's cache directory, or None when the scenario has none."""
    xdg = step.context.get("xdg")
    return dict(os.environ, XDG_CACHE_HOME=str(xdg)) if xdg else None


def _files(base):
    return sorted(str(p.relative_to(base)) for p in base.rglob("*") if p.is_file()) if base.is_dir() else []


def _parse(step, text):
    C2.context(step.repo, H.PATH, [text])
    return step.run("model", "parse", "--file", "spec/capabilities/thing.md", env=env(step), timeout=300)


def compiled(step):
    """The world of LINE, the scenario's cache directory holding its compiled grammar and no parse."""
    C2.context(step.repo, H.PATH, [LINE])
    done = step.run("model", "parse", "--file", "spec/capabilities/thing.md", timeout=600)     # the person's cache
    assert done.returncode == 0, (done.stdout, done.stderr)
    import spec_gf
    import spec_grammar4
    name = spec_grammar4._context(str(step.repo))[2]
    xdg = step.context["xdg"] = step.fixtures("tmp_path_factory").mktemp("xdg")
    shutil.copytree(spec_gf.cache() / name, xdg / "shopsystem-bdd" / "pgf" / name)
    step.context["pgf"] = _files(xdg / "shopsystem-bdd" / "pgf")


def unheld(step):
    compiled(step)


def held(step):
    """The parse cache holds r1's parse, as the parse of OTHER: each line parsed once, OTHER's entry then written
    under LINE's key."""
    compiled(step)
    parses = step.context["xdg"] / "shopsystem-bdd" / "parse"
    done = _parse(step, LINE)
    assert done.returncode == 0, (done.stdout, done.stderr)
    mine = set(_files(parses))
    other = _parse(step, OTHER)
    assert other.returncode == 0, (other.stdout, other.stderr)
    (theirs,) = set(_files(parses)) - mine
    (key,) = [f for f in mine if f.endswith(".json")]
    shutil.copyfile(parses / theirs, parses / key)
    C2.context(step.repo, H.PATH, [LINE])
    step.context["read"] = other.stdout


def then(step, done):
    """`model` reads the parse cache p1 (it printed what the cache held), writes the parse cache p2 (an entry under
    the scenario's cache directory), uses the compiled grammar c1 and does not write a compiled grammar (the compiled
    grammars are those copied in); False for any other step."""
    xdg = step.context.get("xdg")
    if xdg is None:
        return False
    assert done.returncode == 0, (done.stdout, done.stderr)
    said = step.nps[0] if step.nps else ""
    if step.event == "read" and said.startswith("the parse cache"):
        assert done.stdout == step.context["read"], (done.stdout, step.context["read"])
    elif step.event == "write" and step.template == "ThenDoes" and said.startswith("the parse cache"):
        assert any(f.endswith(".json") for f in _files(xdg / "shopsystem-bdd" / "parse")), step.text
    elif step.event == "use" and said.startswith("the compiled grammar") or \
            step.event == "write" and step.template == "ThenDoesNot":
        assert _files(xdg / "shopsystem-bdd" / "pgf") == step.context["pgf"], step.text
    else:
        return False
    return None
