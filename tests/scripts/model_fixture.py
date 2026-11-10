"""The file builders of the model tests (test_model.py and the modules that import from it): a codified-2 context
(the CLI pack imported) whose index carries the typed glossary of tests/scripts/fixtures/glossary/, capability files
of one group a requirement and their generated feature files."""
import pathlib
import re
import textwrap

ROOT = pathlib.Path(__file__).resolve().parents[2]

PATH = "ex.com/prod/ctx"
CONTEXT = f"bounded-context/{PATH}"
HEAD = f"---\nid: {CONTEXT}\nlanguage: codified-2\nimports: [cli]\n---\n# ctx\n"
GLOSSARY = (ROOT / "tests" / "scripts" / "fixtures" / "glossary" / "spec" / "index.md").read_text()
# the words the CLI pack defines too are marked as redefining it (v_t16)
INDEX = HEAD + "\n" + re.sub(r"^(- \*\*(?:change|command|name|reason|refuse)\*\* .*)$", r"\1 Redefines: cli.",
                              GLOSSARY[GLOSSARY.index("## Glossary"):], flags=re.MULTILINE)
# Every requirement `cap()` writes is this statement, which parses in grammar 4 in the fixture glossary; its id and
# group are the test's subject.
STATEMENT = ("When the person runs `work start` on an initiative whose status is `proposed`, `work` shall set the status "
             "of the initiative to `started`.")


def full(kind, name):
    """A node's id in full: <kind>/<context path>/<name>."""
    return f"{kind}/{PATH}/{name}"


THING = full("capability", "thing")
P1 = full("capability-proposal", "p1")
I1 = full("initiative", "i1")
W1 = full("work-item", "w1")
OBS1 = full("observation", "obs-1")


def codified_lines(reqs):
    """Each `- [r<n>] <text>` as its own group [g<n>] whose statement is STATEMENT; any other line under a group of
    its own, as written."""
    out = []
    for k, line in enumerate(reqs, 1):
        m = re.match(r"- \[r(\d+)\]", line)
        out += [f"### [g{m.group(1)}] r{m.group(1)}", f"- [r{m.group(1)}] {STATEMENT}"] if m else [
            f"### [g{900 + k}] line {k}", line]
    return out


def cap(name, reqs, group="service", retired="[]", rests_on="[]"):
    lines = "\n".join(codified_lines(reqs))
    return textwrap.dedent(f"""\
        ---
        id: capability/{PATH}/{name}
        title: {name}
        narrator: a client
        group: {group}
        language: codified-2
        rests_on: {rests_on}
        retired: {retired}
        ---

        # {name}

        ## Purpose
        Something.

        ## Behaviour
        """) + lines + "\n\n## Not yet\n- None.\n"


def feature(name, *scenarios):
    """Generated scenarios: a tag @r<n> names group g<n> too (`cap()` writes one group a requirement)."""
    out = [f"# generated from spec/capabilities/{name}.md by features generate; do not edit", f"Feature: {name}",
           "  Narrator: a client", ""]
    for tag, title in scenarios:
        tag = re.sub(r"@r(\d+)", r"@g\1 @r\1", tag)
        out += [f"  {tag}", f"  Scenario: {title}", "    Given a thing", "    Then it holds", ""]
    return "\n".join(out)
