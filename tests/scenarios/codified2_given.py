"""The given lines of example data in grammar 4 (b218): a codified-2 capability `shelf` in codified2_world's context,
whose one group has a given block with a line "the K `n` holds" of a noun of two words, the capability's own term
(`feature file`, under its `## Terms`), with a docstring (illustrated), a table (tabulated) or one value (quoted)
under it. `features generate` writes the group's scenario with that Given and its data first (`WRITTEN`, what the
feature must hold, kept for `ThenDoes write` under `holds`)."""
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
LINE = "When a session ends a stage, `work` shall print the stage."
TERMS = "## Terms\n\n- **feature file** (noun): a file of scenarios.\n\n"
# condition -> the given block's lines under the group's requirement
GIVEN = {"illustrated": ["the feature file `features/a.feature` holds:", "  Feature: A", "    Scenario: One"],
         "tabulated": ["the feature file `features/a.feature` holds:", "  | step | count |", "  | Given | 2 |"],
         "quoted": ['the feature file `features/a.feature` holds "Feature: A"']}

# condition -> what features/shelf.feature holds: the Given and its data, as the scenario's first step
WRITTEN = {"illustrated": ('    Given the feature file `features/a.feature` holds:\n      """\n      Feature: A\n'
                           '        Scenario: One\n      """\n    When '),
           "tabulated": ("    Given the feature file `features/a.feature` holds:\n      | step | count |\n"
                         "      | Given | 2 |\n    When "),
           "quoted": '    Given the feature file `features/a.feature` holds "Feature: A"\n    When '}


def capability(repo, path, word):
    """The context written into `repo`, its capability `shelf` with the given block of `word`; the name the scenario's
    command runs on."""
    world = _world()
    world.context(repo, path, [LINE], NAME)
    target = repo / "spec" / "capabilities" / ("%s.md" % NAME)
    block = "\n```given\n%s\n```\n" % "\n".join(GIVEN[word])
    text = target.read_text().replace("- [r1] %s\n" % LINE, "- [r1] %s\n%s" % (LINE, block))
    target.write_text(text.replace("## Behaviour\n", TERMS + "## Behaviour\n"))
    return NAME
