"""brainstorming r1, r2 (workflow simplification plan 3, Task 5, D15) and r3 (plan 8, D14), checked by reading the skills as test_agents.py
reads the agents: the brainstorming session writes an item's lines and runs `work ready`, and nothing after it waits
on the person; the intake session's skill names only commands `work` and `model` have."""
import ast
import re
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
import spec_unbuilt

REPO = Path(__file__).resolve().parents[2]
SKILLS = REPO / "skills"
SHAPING = SKILLS / "shaping-items" / "SKILL.md"
NAMES = ("shaping-items", "taking-in-a-request", "building-a-batch")
PINNED = "Do not ask the person to approve the lines: nothing waits on their reading."


def process(path):
    """The numbered steps of the skill's `## Process`, each with the lines that continue it."""
    section = path.read_text().split("\n## Process\n", 1)[1].split("\n## ", 1)[0]
    return [s.strip() for s in re.split(r"(?m)^(?=\d+\. )", section) if re.match(r"\d+\. ", s.strip())]


def commands(text, script):
    """The subcommands of `script` the text names: `` `work ready `` or `` `python3 <scripts>/work ready ``."""
    return set(re.findall(r"(?:`|/)%s ([a-z][a-z-]*)" % script, text))


def choices(script):
    """The subcommands `<script> --help` lists."""
    done = subprocess.run([sys.executable, str(REPO / "scripts" / script), "--help"], capture_output=True, text=True)
    return set(re.search(r"\{([a-z,-]+)\}", done.stdout).group(1).split(","))


def test_r4_the_session_writes_lines_and_readies():
    steps = process(SHAPING)
    first = {cmd: next(n for n, s in enumerate(steps) if commands(s, "work") & {cmd}) for cmd in ("idea", "line", "ready")}
    assert first["idea"] <= first["line"] < first["ready"], first


def test_r2_nothing_waits_on_the_person():
    assert PINNED in SHAPING.read_text()
    steps = process(SHAPING)
    ready = next(n for n, s in enumerate(steps) if "ready" in commands(s, "work"))
    for step in steps[ready:]:
        assert "ask the person" not in step.lower() and not re.search(r"\bwait", step.lower()), step


def test_r5_a_quote_is_written_with_work_quote():
    """The brainstorming session quotes the person's words with `work quote`, before `work shape`, and cites the quote
    in the item's note."""
    steps = process(SHAPING)
    first = next(n for n, s in enumerate(steps) if "quote" in commands(s, "work"))
    shape = next(n for n, s in enumerate(steps) if "shape" in commands(s, "work"))
    assert first <= shape, (first, shape)
    assert steps[first].index("work quote") < steps[first].index("work shape"), steps[first]
    text = SHAPING.read_text()
    assert "quote-<n>" in text and "Until `work` keeps quotes" not in text


def test_r5_the_skill_says_where_an_earlier_sessions_id_is():
    """Plan 8's review, M6: `--session <id>` is advised only with where the id is found."""
    step = next(s for s in process(SHAPING) if "quote" in commands(s, "work"))
    assert "--session <id>" in step and "`<id>.jsonl`" in step and "~/.claude/projects/" in step, step
    assert "--transcript <path>" in step, step


def test_each_built_brainstorming_line_has_its_test():
    """The strict xfail of a guarantees capability: each brainstorming id out of `unbuilt:` has a `test_r<n>_` here,
    and each id in it has none."""
    ids = set(re.findall(r"(?m)^- \[(r\d+)\] ", (REPO / "spec/capabilities/brainstorming.md").read_text()))
    unbuilt = spec_unbuilt.unbuilt(REPO).get("brainstorming", set())
    tested = {m.group(1) for node in ast.parse(Path(__file__).read_text()).body if isinstance(node, ast.FunctionDef)
              for m in [re.match(r"test_(r\d+)_", node.name)] if m}
    assert ids and ids - unbuilt == tested & ids, (ids, unbuilt, tested)


@pytest.mark.parametrize("script", ["work", "model"])
def test_the_skills_name_only_commands_work_has(script):
    have = choices(script)
    for name in NAMES:
        text = (SKILLS / name / "SKILL.md").read_text()
        named = commands(text, script)
        assert named and named <= have if script == "work" else named <= have, (name, named - have)


@pytest.mark.parametrize("name", NAMES)
def test_each_skill_has_a_use_when_description(name):
    text = (SKILLS / name / "SKILL.md").read_text()
    head = text.split("---\n")[1]
    assert re.search(r"(?m)^name: %s$" % name, head), head
    assert re.search(r"(?m)^description: Use when ", head), head


def test_a_bug_in_delivered_work_is_a_defect_first():
    """Plan 7, D14: a fault in what a delivered item built is recorded against it before its fix is shaped."""
    assert "measure defect <item>" in SHAPING.read_text()
