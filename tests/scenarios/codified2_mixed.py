"""The mixed codified spec (the CNL 4 design, I19; section 13 point 4): codified2_world's context, its `spec/index.md`
saying `language: codified-2`, with the capability `shelf` in the new language (`language: codified-2`) beside `thing`
still in the old (`language: codified-1`), each line read in its own file's grammar. A capability that is recodified
is `shelf`: its condition's Given names the scenario's capability by it (`ids`)."""
import importlib.util
import sys
from pathlib import Path


def _world():
    if "shop_codified2_world" not in sys.modules:
        spec = importlib.util.spec_from_file_location("shop_codified2_world", Path(__file__).with_name("codified2_world.py"))
        sys.modules["shop_codified2_world"] = loaded = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(loaded)
    return sys.modules["shop_codified2_world"]


NAME = "shelf"
# grammar 4's lines, each a scenario of its own that `features generate` writes whole; r1 is an If line on the trigger
# of `thing`'s When line, whose response differs: the If line takes precedence (call 12), so the pair is no clash
NEW = [("While a session follows a stage, if the person runs `work start`, then `work` shall exit with an error naming "
        "the stage."),
       "When a session ends a stage, `work` shall print the stage."]
# a line of the old grammar, read by the old pipeline in a file that says codified-1
OLD = ["When the person runs `work start`, `work` shall exit successfully."]


def old(path, lines=OLD):
    """The capability `thing` in the old language: a codified-2 file of codified2_world with its marker put back."""
    return _world().capability("thing", lines, path).replace("language: codified-2", "language: codified-1")


def mixed(repo, path, name=NAME):
    """The mixed spec written into `repo`: the codified-2 index, `name` recodified with NEW, `thing` with OLD."""
    _world().context(repo, path, NEW, name)
    (repo / "spec" / "capabilities" / "thing.md").write_text(old(path))
