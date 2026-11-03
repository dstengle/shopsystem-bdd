"""The scenario of a group read off its minimal trace (design-r2 §7): Givens from the translation (no given block),
`and` between responses as separate Thens, one solve for a contrast, and the same spec giving the same bytes."""
import os
import pathlib
import re
import shutil
import subprocess
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import toolchain

REPO = pathlib.Path(__file__).resolve().parents[2]
FEATURES = REPO / "scripts" / "features"
G13 = ("- [r16] While a result is outputless, when a session ends a `plan` stage for a work-item with the result, "
       "`work run` shall set the status of the work-item to `awaiting-answer` and ask a question on the work-item.\n")


def copy_spec(tmp_path, name):
    root = tmp_path / name
    shutil.copytree(REPO / "spec", root / "spec")
    return root


def edit(path, old, new):
    text = path.read_text()
    assert old in text, old
    path.write_text(text.replace(old, new, 1))


def add_group(path, text):
    """`text` added as the last group of the capability's Behaviour."""
    body = path.read_text()
    at = body.index("\n## ", body.index("## Behaviour"))
    path.write_text(body[:at] + "\n" + text + body[at:])


def steps(root, gid):
    """The step texts of one group of the spec at `root`, as `features generate` writes them."""
    import features_vocab
    import spec_solve
    import spec_trace
    ctx = spec_solve.Context(root, None)
    group = next(g for g in ctx.groups if g.id == gid)
    v = features_vocab.load(root)
    model = spec_trace.trace(ctx, group)
    return [(k, v.text(t)) for k, t in spec_trace.read(model, gid, [s.id for s in group.statements], ctx.vocab, v)]


@pytest.fixture(scope="module")
def edited(tmp_path_factory):
    """The live spec with supervision g2's given block deleted (and r53, whose L1 against r2 layer 4 removes), g13's
    two statements merged with `and`."""
    toolchain.require()
    root = copy_spec(tmp_path_factory.mktemp("trace"), "spec-copy")
    sup = root / "spec" / "capabilities" / "supervision.md"
    text = sup.read_text()
    g2 = text[text.index("### [g2]"):text.index("### [g3]")]
    sup.write_text(text.replace(g2, re.sub(r"```given\n.*?```\n", "", g2, flags=re.DOTALL)))
    edit(sup, "- [r53] While a work-item is `drafted`, when the person runs `work run` on an initiative, `work run` "
         "shall not start a stage for the work-item.\n", "")
    edit(sup, "- [r1] While a remote is not unpushable, when the person runs `work run` on an initiative, `work run` "
         "shall set the status of every open work-item to `green`.\n", "")
    text = sup.read_text()
    g13 = text[text.index("- [r16]"):text.index("```given", text.index("- [r16]"))]
    sup.write_text(text.replace(g13, G13 + "\n"))
    return root


def test_a_while_clause_gives_its_given_with_no_given_block(edited):
    got = steps(edited, "supervision#g2")
    assert ("given", "a work-item w1 that is `drafted`") in got
    assert ("then", "`work run` starts the stage s1") in got


def test_a_merged_statement_gives_one_then_for_each_response(edited):
    thens = [t for k, t in steps(edited, "supervision#g13") if k == "then"]
    assert "the work-item w1 is `awaiting-answer`" in thens
    assert "`work run` asks the question q1" in thens


def test_commit_and_push_gives_two_thens(edited):
    thens = [t for k, t in steps(edited, "supervision#g25") if k == "then"]
    assert "`work run` commits the transition t1" in thens
    assert "`work run` pushes the commit c1" in thens


def generate(root, seed):
    env = dict(os.environ, PYTHONHASHSEED=str(seed))
    done = subprocess.run([sys.executable, str(FEATURES), "generate", "supervision", "work-queue"], cwd=root,
                          capture_output=True, text=True, env=env)
    assert done.returncode == 0, done.stderr[-3000:]
    return {n: (root / "features" / ("%s.feature" % n)).read_text() for n in ("supervision", "work-queue")}


UNRELATED_WHEN = "### [g99] Probing twice\n- [r99] When the person runs `tools probe`, `tools` shall exit successfully.\n"
WIDGET = "- **widget** (kind): a thing only this test names.\n- **broken** (condition of widget): a widget that fails.\n"
UNRELATED_WHILE = "### [g99] A broken widget\n- [r99] While a widget is broken, `tools` shall print the widget.\n"
RELATED_WHILE = "### [g98] A drafted work-item\n- [r98] While a work-item is `drafted`, `tools` shall print the work-item.\n"


def test_byte_stable(tmp_path):
    """Two processes with different hash seeds give the same bytes, and so does the spec with a requirement outside
    the groups' cones: a `When` no response triggers, and a `While` over a kind no cone uses (design-r2 §7.4)."""
    toolchain.require()
    root = copy_spec(tmp_path, "stable")
    first = generate(root, 1)
    assert generate(root, 2) == first
    caps = root / "spec" / "capabilities"
    add_group(caps / "analysis-tools.md", UNRELATED_WHEN)
    edit(caps / "trials.md", "## Terms\n\n", "## Terms\n\n" + WIDGET)
    add_group(caps / "trials.md", UNRELATED_WHILE)
    assert generate(root, 3) == first


def test_related_while_enters(tmp_path):
    """A `While` over a kind the cone uses enters it: it constrains every such trace (design-r2 §7.4 (c))."""
    toolchain.require()
    import spec_solve
    import spec_trace
    root = copy_spec(tmp_path, "related")
    add_group(root / "spec" / "capabilities" / "trials.md", RELATED_WHILE)
    ctx = spec_solve.Context(root, None)
    g2 = next(g for g in ctx.groups if g.id == "supervision#g2")
    assert "trials#r98" in spec_trace.cone(ctx, g2)[0]
    widget = copy_spec(tmp_path, "widget")
    edit(widget / "spec" / "capabilities" / "trials.md", "## Terms\n\n", "## Terms\n\n" + WIDGET)
    add_group(widget / "spec" / "capabilities" / "trials.md", UNRELATED_WHILE)
    ctx = spec_solve.Context(widget, None)
    g2 = next(g for g in ctx.groups if g.id == "supervision#g2")
    assert "trials#r99" not in spec_trace.cone(ctx, g2)[0]
