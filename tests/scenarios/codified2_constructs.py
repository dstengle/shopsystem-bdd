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
# condition -> glossary entries and `## Relations` rows it adds
TERMS, ROWS = {}, {}
# condition -> a step the feature `features/shelf.feature` must hold
HOLDS = {}


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
