"""The smallest codified-2 world (the CNL 4 design, I7a; section 13 point 4): a `spec/index.md` with `language:
codified-2` and `imports: [cli]` (the glossary of tests/scripts/fixtures/codified-2/), and one capability `thing`,
also codified-2, whose requirement r1 is the line a requirement condition gives. `model parse` reads it in grammar 4.

A later grammar item adds its condition to LINES: the line r1 says, and what a refusal of it names the scenario's term
t1 by (None when it names no term). I19 extends the world to a mixed spec."""
import re
from pathlib import Path

FIXTURE = Path(__file__).resolve().parents[1] / "scripts" / "fixtures" / "codified-2" / "spec" / "index.md"
# the same world with the time pack imported and a stage's deadline, a moment (I16): the conditions of TIMED read in it
TIME_FIXTURE = FIXTURE.parents[2] / "codified-2-time" / "spec" / "index.md"

# condition -> (the line r1 says, what the refusal names t1 by, or None)
LINES = {"plural": ("When sessions write a file, `work` shall print the file.", None),
         "disagreeing": ("When sessions writes a file, `work` shall print the file.",
                         "the verb write does not agree in number with its subject"),
         "optioned": ("When the person runs `work backlog` with the `--json` option, `work` shall exit successfully.",
                      None),
         # the reading rules' refusals (I11b): a "the" with no antecedent (R2), a negated indefinite in a While
         # clause (R4), a line that obliges with no trigger (R12)
         "antecedentless": ("When the person runs `work start`, `work` shall print the stage.",
                            '"the stage" has no antecedent'),
         "unquantified": (("While a session does not follow a stage, when the person runs `work start`, `work` shall "
                           "exit successfully."), 'says "does not follow a stage"'),
         "triggerless": ("`work` shall write a file.", None),
         "misaspected": ("When a session follows a stage, `work` shall print the stage.",
                         "the verb follow is a state, and a trigger takes an action"),
         "genitive": (("When a session ends a stage, `work` shall print the status of the stage and the worktree of "
                       "the session."), None),
         "denying": (("While a session has no worktree, when the person runs `work start`, `work` shall exit with an "
                      "error naming the session."), None),
         "compound": ("When a session ends a stage, `work` shall print the stage status.", None),
         "restrictive": ("A session shall change only files in its worktree.", None),
         "relative": (("When a session ends a stage that sessions follow, `work` shall print every session that does "
                       "not follow the stage."), None),
         "possessive": (("When a session ends a stage whose status is not `done`, `work` shall print every session "
                         "whose worktree holds a file."), None),
         # the list "a stage and the stage" belongs to follow or to print: two meanings, refused naming the requirement
         "ambiguous": (("When the person runs `work start`, `work` shall print every session that follows a stage and "
                        "the stage."), None),
         # "this" before command, whose entry in the CLI pack has This: (call 6); "the output" would be refused (R2)
         "indexical": ("When the person runs this command, `work` shall print this command.", None),
         # a verb short of a noun its frame takes, or with one of the wrong kind (I10): the refusal names the verb
         "objectless": ("When the person runs `work start`, `work` shall write.", "the verb write takes an object"),
         "mistyped": ("When the person runs `work start`, `work` shall write a stage.",
                      "the verb write takes as its object file or a kind of it"),
         "recipientless": ("When the person runs `work start`, `work` shall give a file.",
                           "the verb give takes a recipient"),
         # a passive, which grammar 4 has not: the verb's frame has a subject it leaves out
         "agentless": ("While a file is not written, when the person runs `work start`, `work` shall write a file.",
                       "the verb write takes a subject"),
         # the line stops after "the", where write's frame needs its object: the hint names the term that may follow
         "unfinished": ("When a session ends a stage, `work` shall write the", "may follow: file"),
         # a count before a number and a noun (I15, call 4)
         "counted": ("When the person runs `work start`, `work` shall print at least two stages.", None),
         # the time pack and the time constructs (I16), in TIME_FIXTURE's world: a moment compared, the clock as a
         # trigger, the perfect of an action verb as history, and a duration with no unit, refused naming the number
         "timed": (("While a deadline of a stage is within the last 7 days, when the person runs `work start`, `work` "
                    "shall print the stage."), None),
         "clocked": ("When the clock reaches a deadline of a stage, `work` shall print the stage.", None),
         "historical": (("While a session has ended a stage, when the person runs `work start`, `work` shall print the "
                         "stage."), None),
         "unitless": (("While a deadline of a stage is within the last 7, when the person runs `work start`, `work` "
                       "shall print the stage."), "the number 7 is a duration"),
         # modality (I17): a permission, and a necessity with no trigger
         "permissive": ("A session may write a file.", None),
         "invariant": ("A session always follows a stage.", None),
         # a "the" inside a modifier of a noun phrase of its own kind (R2, b217), with the state verb precede of TERMS:
         # bound to the trigger's stage, and refused when only the stage it modifies would give it
         "embedding": ("When a session ends a stage, `work` shall print a stage that precedes the stage.", None),
         "self-embedding": ("When the person runs `work start`, `work` shall print a stage that precedes the stage.",
                            '"the stage" has no antecedent')}
# a condition's glossary entries, added to the fixture's
TERMS = {"embedding": ["- **precede** (verb, state): a stage comes before a stage. Frame: stage precedes stage."]}
TERMS["self-embedding"] = TERMS["embedding"]
# a condition whose line `features generate` writes: its capability is `shelf`, and the step its feature must hold
# (the new stage precedes the trigger's, not itself)
SHELVED = {"embedding": r"^    Then the stage s3 precedes the stage s2$"}

TIMED = {"timed", "clocked", "historical", "unitless"}


def capability(name, lines, path):
    """A codified-2 capability file: each line in a group [g<k>] of its own, under the id r<k>."""
    body = "\n".join("### [g%d] line %d\n- [r%d] %s" % (k, k, k, line) for k, line in enumerate(lines, 1))
    return ("---\nid: capability/%s/%s\ntitle: %s\nnarrator: a client\ngroup: service\nlanguage: codified-2\n"
            "rests_on: []\nretired: []\n---\n\n# %s\n\n## Purpose\nSomething.\n\n## Behaviour\n\n%s\n\n"
            "## Not yet\n- None.\n" % (path, name, name, name, body))


# The capabilities of `model logic` (I12a): each condition's lines, which the check reads through their logical form.
# Restricting: a session may change only files in its worktree, and a session changes a file, which may be one.
# Exhaustive: `work` prints every stage, and must not print a done stage, which is one of every stage.
CAPABILITIES = {"restricting": ["A session shall change only files in its worktree.",
                                "When a session ends a stage, the session shall change a file."],
                "exhaustive": ["When the person runs `work start`, `work` shall print every stage.",
                               ("When the person runs `work start`, `work` shall not print a stage whose status is "
                                "`done`.")],
                # Overriding (I12b, call 12): an If line and a When line of one trigger whose responses differ; where a
                # session follows a stage, the If line's response replaces the When line's, so the pair is no clash.
                "overriding": [("While a session follows a stage, if the person runs `work start`, then `work` shall "
                                "exit with an error naming the stage."),
                               "When the person runs `work start`, `work` shall exit successfully."],
                # Contravening (I12b, b117): `work` exits successfully on a command it refuses, which U1 forbids.
                "contravening": ["When `work` refuses a command, `work` shall exit successfully."],
                # Overcounted (I15, call 4): on one trigger `work` prints at least two stages and at most one stage;
                # no number of stages meets both counts.
                "overcounted": ["When the person runs `work start`, `work` shall print at least two stages.",
                                "When the person runs `work start`, `work` shall print at most one stage."],
                # Forbidding (I17): a session may write a file, and no session shall write a file while it follows a
                # stage, which some session may: the "shall not" forbids what the "may" permits (L7)
                "forbidding": ["A session may write a file.",
                               "While a session follows a stage, the session shall not write a file."],
                # Declining (I14a): `work` refuses `work start` (an error exit on a run, by the CLI pack's definition of
                # refuse), so U1 entails its "change nothing" from its other Then.
                "declining": [("If the person runs `work start`, then `work` shall exit with an error naming "
                               "`work start` and change nothing.")]}

# The universal conditions a capability condition needs beside its lines, as spec/universal.md's U1, U2 ...: U1 is an
# If line, which takes no precedence over a line of a capability (it holds in every trace).
UNIVERSAL = {"contravening": [("If a tool refuses a command, then the tool shall exit with an error naming the "
                               "command and change nothing.")]}
UNIVERSAL["declining"] = UNIVERSAL["contravening"]

# What `features generate` writes of a capability condition's lines (I14a): (a step its feature must hold, a step it
# must not, as U1 entails it). Declining: the error exit is the line's own Then; its "change nothing" is entailed.
GENERATED = {"declining": (r"^    Then `work` exits with an error naming `work start`$",
                           r"^\s*(Then|And) `work` changes nothing$")}


# The requirement conditions of `model logic` (I13a): the lines of the capability `thing`, r1 the one the scenario
# names, and the universal conditions beside them. Restating: r1's exit with an error is r2's, and its change nothing
# is U1's, on the command `work` refuses by exiting with an error on it (the CLI pack's definition of refuse).
REQUIREMENTS = {"restating": ([("If the person runs `work start`, then `work` shall exit with an error naming "
                                "`work start` and change nothing."),
                               "If the person runs `work start`, then `work` shall exit with an error naming `work start`."],
                              UNIVERSAL["contravening"]),
                # `model explain` (I13b). Refusing: r1 refuses its command, which U1 and the CLI pack's definition of
                # refuse say more of. Overridden: r1, a When line, and r2, an If line of its trigger that refuses it.
                "refusing": (["If the person runs `work start`, then `work` shall refuse the command."],
                             UNIVERSAL["contravening"]),
                "overridden": (["When the person runs `work start`, `work` shall exit successfully.",
                                ("While a session follows a stage, if the person runs `work start`, then `work` shall "
                                 "refuse the command.")], UNIVERSAL["contravening"])}
# What `model explain` names a requirement condition's other instances by: U1 as the premise of a consequence, the
# term refuse by its definition in the CLI pack, r2 by its id.
SAYS = {"refusing": {"u1": "(by U1)", "t1": "(by the definition of refuse in the pack cli)"},
        "overridden": {"r2": "thing#r2"}}


def context(repo, path, lines, name="thing", universal=(), fixture=FIXTURE):
    """The world written into `repo`: the fixture's index under the bounded context `path`, the capability `name`
    with `lines` (and `thing` with none, when `name` is another), and spec/universal.md with `universal`, if any."""
    index = fixture.read_text().replace("bounded-context/example.org/fixture/codified-2-time", "bounded-context/" + path)
    index = index.replace("bounded-context/example.org/fixture/codified-2", "bounded-context/" + path)
    files = [("spec/index.md", index), ("spec/capabilities/%s.md" % name, capability(name, lines, path))]
    if name != "thing":
        files.append(("spec/capabilities/thing.md", capability("thing", [], path)))
    if universal:
        body = "\n".join("- [U%d] %s" % (k, line) for k, line in enumerate(universal, 1))
        files.append(("spec/universal.md", "---\nid: capability/%s/universal\ntitle: Universal conditions\nnarrator: "
                      "every trace\ngroup: guarantees\nlanguage: codified-2\nretired: []\n---\n\n# Universal "
                      "conditions\n\n## Behaviour\n\n%s\n" % (path, body)))
    for rel, text in files:
        target = repo / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)


def requirement(step, word, path):
    """The requirement condition `word`: the world with r1 the line LINES gives it, and t1 said as its refusal names it."""
    line, says = LINES[word]
    name = "shelf" if word in SHELVED else "thing"
    context(step.repo, path, [line], name, fixture=TIME_FIXTURE if word in TIMED else FIXTURE)
    index = step.repo / "spec" / "index.md"
    for entry in TERMS.get(word, ()):
        index.write_text(index.read_text() + entry + "\n")
    if word in SHELVED:
        step.context.setdefault("holds", {})["features/shelf.feature"] = re.compile(SHELVED[word], re.MULTILINE)
    if says:
        step.context.setdefault("says", {})["t1"] = says


# A state verb whose frame takes no object (b219): the glossary entry the fixture has not, and r1 of the capability
# `shelf`, whose feature feature-file-tools' scenario names; `model logic` names r1 by `shelf#r1`.
INTRANSITIVE = ("- **stall** (verb, state): a stage makes no progress. Frame: stage stalls.\n",
                "While a stage stalls, when the person runs `work start`, `work` shall print the stage.")


def intransitive(step, path):
    entry, line = INTRANSITIVE
    context(step.repo, path, [line], "shelf")
    index = step.repo / "spec" / "index.md"
    index.write_text(index.read_text() + entry)
    step.context.setdefault("ids", {})[step.names[0]] = "shelf#r1"


# condition -> (the line r1 of the capability `shelf` says, the verb's entry the glossary gains for it, the step its
# feature must hold): the requirements `features generate` writes the feature of (feature-file-tools)
SHELVED = {"oblique": ("When a session ends a stage, `work` shall record the stage in a file.",
                       ("- **record** (verb, action): an agent keeps a stage in a file. Frame: agent records stage "
                        "in file.\n"), r"(?m)^\s*Then `work` records the stage \w+ in the file \w+$")}


def shelved(step, word, path):
    """The requirement condition `word` of SHELVED: the world with `shelf`'s r1 its line, its verb in the glossary."""
    line, entry, holds = SHELVED[word]
    context(step.repo, path, [line], name="shelf")
    step.context.setdefault("holds", {})["features/shelf.feature"] = re.compile(holds)
    index = step.repo / "spec" / "index.md"
    index.write_text(index.read_text().replace("- **write** (verb, action)", entry + "- **write** (verb, action)", 1))
