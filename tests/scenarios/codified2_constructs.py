"""The codified-2 constructs `features generate` writes the scenario of, and `model logic` reads (b197): a capability
`shelf` in codified2_world's context whose groups say the construct of a capability condition (feature-file-tools'
distributing ... necessitating; design-model-check's quantifying, thresholded, excepting). A condition's lines, the
glossary entries and `## Relations` rows it adds to the fixture's, and for `features generate` what the feature it
writes must hold (kept for `ThenDoes write` under `holds`); a permitting or necessitating capability's feature holds
no scenario."""
import importlib.util
import re
import sys
from pathlib import Path


def _world():
    if "shop_codified2_world" not in sys.modules:
        spec = importlib.util.spec_from_file_location("shop_codified2_world", Path(__file__).with_name("codified2_world.py"))
        sys.modules["shop_codified2_world"] = loaded = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(loaded)
    return sys.modules["shop_codified2_world"]


NAME = "shelf"
ERROR = "%s the person runs `work start`, `work` shall exit with an error naming `work start`."
# condition -> its lines, each a group of its own
LINES = {"permitting": ["A session may write a file."],
         "necessitating": ["A session always follows a stage."],
         # design-model-check: a line of every, of a count and of a negated restriction, each with a line of its
         # trigger whose response conflicts with it where its condition holds (L1)
         "quantifying": [("While every stage is `done`, when the person runs `work start`, `work` shall exit "
                          "successfully."), ERROR % "While a stage is `done`, when"],
         "thresholded": [("While at least two stages are `done`, when the person runs `work start`, `work` shall exit "
                          "successfully."), ERROR % "While a stage is `done`, when"],
         "excepting": ["When the person runs `work start`, `work` shall print a stage whose status is not `done`.",
                       "When the person runs `work start`, `work` shall not print a stage whose status is not `done`."]}
RUN = "When the person runs `work start`, "
# feature-file-tools: a line of each construct `features generate` writes the scenario of
LINES.update({"distributing": [RUN + "`work` shall print every stage."],
              "generalising": ["While every stage is `done`, w" + RUN[1:] + "`work` shall exit successfully."],
              "confining": ["When a session ends a stage, the session shall write only files in its worktree."],
              "bounding": [RUN + "`work` shall print at least two stages.", RUN + "`work` shall print at most one stage."],
              "tallying": ["While at least two stages are `done`, w" + RUN[1:] + "`work` shall exit successfully."],
              "branching": [("While a stage is `done` or a session follows a stage, w" + RUN[1:] + "`work` shall exit "
                             "successfully.")],
              "linking": ["When a session ends a stage on a worktree, `work` shall print the stage."],
              "valued": ["When a session ends a stage, `work` shall print the status of the stage."],
              "excluding": ["While no stage is `done`, w" + RUN[1:] + "`work` shall exit successfully."],
              "exempting": [RUN + "`work` shall print a stage whose status is not `done`."]})
# condition -> glossary entries and `## Relations` rows it adds
TERMS, ROWS = {}, {"linking": ["| stage | on | worktree |  |"]}
# condition -> the steps the feature `features/shelf.feature` must hold: two Ks of every in a response (R6); one K
# that meets every's scope; a K that meets only's restrictor and the Then on it (R5); the bound's number of Ks, and
# one past "at most one" with the Then on it negated; two Ks of "at least two" in a condition; a scenario a case of
# or; the row's Given; "the T of x" with no value; "no K" said, no K brought in; a K that does not meet a restriction
HOLDS = {"distributing": r"^    Given a stage s1\n    And a stage s2\n.*\n    Then `work` prints the stage s1\n"
                         r"    And `work` prints the stage s2$",
         "generalising": r"^    Given a stage s1\n    And the stage s1 is `done`\n    When the person runs `work start`$",
         "confining": (r"^    And the worktree w1 holds the file f1\n    When the session s1 ends the stage s2\n"
                       r"    Then the session s1 writes the file f1$"),
         "bounding": (r"^    Then `work` prints the stage s1\n    And `work` prints the stage s2\n(?s:.*)"
                      r"^    Given a stage s1\n    And a stage s2\n.*\n    Then `work` does not print the stage s2$"),
         "tallying": r"^    Given a stage s1\n    And the stage s1 is `done`\n    And a stage s2\n    And the stage s2 is `done`$",
         "branching": (r"^  Scenario: line 1 \(case 1\)\n    Given a stage s1\n    And the stage s1 is `done`\n(?s:.*)"
                       r"^  Scenario: line 1 \(case 2\)\n.*\n.*\n    And the session s2 follows the stage s1$"),
         "linking": r"^    And the stage s2 is on the worktree w1\n    When the session s1 ends the stage s2$",
         "valued": r"^    When the session s1 ends the stage s2\n    Then `work` prints the status of the stage s2$",
         "excluding": r"^    Given no stage is `done`\n    When the person runs `work start`$",
         "exempting": (r"^    Given a stage s1\n    And the stage s1 is not `done`\n    When the person runs `work start`\n"
                       r"    Then `work` prints the stage s1$")}


def capability(step, path, word):
    """The context written into the scenario's repository, its capability `shelf` with the lines of `word`; the
    scenario's capability named by it (`ids`)."""
    repo = step.repo
    _world().context(repo, path, LINES[word], NAME)
    index = repo / "spec" / "index.md"
    text = index.read_text()
    for row in ROWS.get(word, ()):
        text = text.replace("|\n\n## Glossary", "|\n%s\n\n## Glossary" % row, 1)
    index.write_text(text + "".join(entry + "\n" for entry in TERMS.get(word, ())))
    step.context.setdefault("ids", {})[step.names[0]] = NAME
    if word in HOLDS:
        step.context.setdefault("holds", {})["features/%s.feature" % NAME] = re.compile(HOLDS[word], re.MULTILINE)
