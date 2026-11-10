"""The smallest codified-2 world (the CNL 4 design, I7a; section 13 point 4): a `spec/index.md` with `language:
codified-2` and `imports: [cli]` (the glossary of tests/scripts/fixtures/codified-2/), and one capability `thing`,
also codified-2, whose requirement r1 is the line a requirement condition gives. `model parse` reads it in grammar 4.

A later grammar item adds its condition to LINES: the line r1 says, and what a refusal of it names the scenario's term
t1 by (None when the line parses). I19 extends the world to a mixed spec."""
from pathlib import Path

FIXTURE = Path(__file__).resolve().parents[1] / "scripts" / "fixtures" / "codified-2" / "spec" / "index.md"

# condition -> (the line r1 says, what the refusal names t1 by, or None)
LINES = {"plural": ("When sessions write a file, `work` shall print the file.", None),
         "disagreeing": ("When sessions writes a file, `work` shall print the file.",
                         "the verb write does not agree in number with its subject"),
         "optioned": ("When the person runs `work backlog` with the `--json` option, `work` shall exit successfully.",
                      None),
         "misaspected": ("When a session follows a stage, `work` shall print the stage.",
                         "the verb follow is a state, and a trigger takes an action"),
         "genitive": ("When a session ends a stage, `work` shall print the status of the stage and the worktree of the "
                      "session.", None)}


def capability(name, lines, path):
    """A codified-2 capability file: each line in a group [g<k>] of its own, under the id r<k>."""
    body = "\n".join("### [g%d] line %d\n- [r%d] %s" % (k, k, k, line) for k, line in enumerate(lines, 1))
    return ("---\nid: capability/%s/%s\ntitle: %s\nnarrator: a client\ngroup: service\nlanguage: codified-2\n"
            "rests_on: []\nretired: []\n---\n\n# %s\n\n## Purpose\nSomething.\n\n## Behaviour\n\n%s\n\n"
            "## Not yet\n- None.\n" % (path, name, name, name, body))


def context(repo, path, lines):
    """The world written into `repo`: the fixture's index under the bounded context `path`, and `thing` with `lines`."""
    index = FIXTURE.read_text().replace("bounded-context/example.org/fixture/codified-2", "bounded-context/" + path)
    for rel, text in (("spec/index.md", index), ("spec/capabilities/thing.md", capability("thing", lines, path))):
        target = repo / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)


def requirement(step, word, path):
    """The requirement condition `word`: the world with r1 the line LINES gives it, and t1 said as its refusal names it."""
    line, says = LINES[word]
    context(step.repo, path, [line])
    if says:
        step.context.setdefault("says", {})["t1"] = says
