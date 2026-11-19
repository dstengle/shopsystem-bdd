"""work line and the readiness bar in a context with a domain model (the domain contract design, §10): an item's
model lines and vocabulary entries kept in its `### <area> model` block byte-stable, laid into spec/model/ and
spec/vocabulary/ with its requirement lines, the item passing `work ready`, and the unlay leaving spec/ as it was."""
import pathlib
import shutil

import backlog_items
import backlog_lines
import backlog_section
import pytest
from backlog_testing import git, work, write_item

FIXTURE = pathlib.Path(__file__).parent / "fixtures" / "domain-model"
MODEL = "service notes\n  operation pin(note)  outcomes: done"
TERM = "- **pin** (verb, action) → operation notes.pin. Forms: pins, pinned. Frame: <actor> pins <note>."
LINE = "When the person pins a note, the notes service shall complete the request."


@pytest.fixture
def modelled(backlog_repo):
    import toolchain
    toolchain.require()
    shutil.rmtree(backlog_repo / "spec")
    shutil.copytree(FIXTURE / "spec", backlog_repo / "spec")
    shutil.rmtree(backlog_repo / "spec" / "adapters")
    shutil.copytree(FIXTURE / "features", backlog_repo / "features")
    git(backlog_repo, "add", "-A")
    git(backlog_repo, "commit", "-q", "-m", "the domain-model fixture")
    write_item(backlog_repo, "b1", status="shaped")
    return backlog_repo


def ok(done):
    assert done.returncode == 0, done.stderr
    return done


def test_the_model_block_is_read_and_written_byte_stable():
    section = ("### notebook\n\n#### [g1] Pinned\n- [r10] %s\n\n### notes model\n\n```model\n%s\n\nobject shelf\n"
               "  attributes: name (text)\n```\n\n%s" % (LINE, MODEL, TERM))
    item = backlog_items.Item.__new__(backlog_items.Item)
    item.sections = {"Requirements": section}
    blocks = backlog_section.read(item, "b1")
    assert blocks.models[0].area == "notes" and blocks.models[0].terms == (TERM,)
    assert blocks.models[0].lines[-1] == "  attributes: name (text)"
    assert backlog_section.render(blocks) == section


def test_an_item_with_a_model_line_a_term_and_a_line_is_ready(modelled):
    ok(work(modelled, "line", "b1", "--into", "notebook", "--model", MODEL))
    ok(work(modelled, "line", "b1", "--into", "notebook", "--term", TERM))
    ok(work(modelled, "line", "b1", "--into", "notebook", "--relation", "note: pinned on → tag (one, optional)"))
    ok(work(modelled, "line", "b1", "--into", "notebook", LINE))
    blocks = backlog_section.read(backlog_items.find(modelled, "b1"), "b1")
    assert blocks.models[0].lines == ("service notes", "  operation pin(note)  outcomes: done", "", "object note",
                                      "  relations: pinned on → tag (one, optional)")
    done = work(modelled, "ready", "b1")
    assert done.returncode == 0, done.stderr + done.stdout
    assert backlog_items.find(modelled, "b1").status == "ready"


def test_the_lay_and_the_unlay(modelled, tmp_path):
    ok(work(modelled, "line", "b1", "--into", "notebook", "--model", MODEL))
    ok(work(modelled, "line", "b1", "--into", "notebook", "--relation", "note: pinned on → tag (one, optional)"))
    ok(work(modelled, "line", "b1", "--into", "notebook", "--term", TERM))
    ok(work(modelled, "line", "b1", "--into", "notebook", LINE))
    into = tmp_path / "copy"
    shutil.copytree(FIXTURE, into)
    before = {p: p.read_bytes() for p in (into / "spec").rglob("*") if p.is_file()}
    item, files = backlog_items.find(modelled, "b1"), []
    backlog_lines.lay_onto(into, item, files)
    model = (into / "spec/model/notes.md").read_text()
    assert "  operation list()  outcomes: returned → every note\n  operation pin(note)  outcomes: done" in model
    assert "  relations: carries → tag (many)\n  relations: pinned on → tag (one, optional)" in model
    assert TERM in (into / "spec/vocabulary/notes.md").read_text()
    assert {"spec/model/notes.md", "spec/vocabulary/notes.md"} <= set(files)
    backlog_lines.unlay(into, item)
    after = {p: p.read_bytes() for p in (into / "spec").rglob("*") if p.is_file()}
    assert after == before


def test_a_model_line_that_does_not_read_is_refused(modelled):
    done = work(modelled, "line", "b1", "--into", "notebook", "--model", "service notes\n  operation pin(note")
    assert done.returncode == 1 and "work:" in done.stderr
    done = work(modelled, "line", "b1", "--into", "notebook", "--term", "- **pin** (verb, action): no element.")
    assert done.returncode == 1 and "→ <element>" in done.stderr


REPO = pathlib.Path(__file__).resolve().parents[2]


@pytest.mark.parametrize("name", ["b309", "b318", "b334"])
def test_the_ready_items_reworded_for_the_migrated_spec_meet_the_readiness_bar(name):
    """The items `ready` when the domain contract moved this spec (plan 5, task 8): their lines reworded into the new
    capabilities and words, their model lines and vocabulary entries laid into spec/model/ and spec/vocabulary/."""
    import readiness_bar
    import toolchain
    toolchain.require()
    assert readiness_bar.check(REPO, backlog_items.find(REPO, name)) == ([], [])


def test_a_member_line_joins_an_element_declared_with_its_kind():
    import backlog_model
    body = ["object item kind of file", "  attributes: size (text)", "", "service backlog",
            "  operation show(item)"]
    lines = ["object item", "  relations: has → label (many)", "service backlog", "  operation tag(item)"]
    laid = backlog_model.merged(body, lines)
    assert laid == ["object item kind of file", "  attributes: size (text)", "  relations: has → label (many)", "",
                    "service backlog", "  operation show(item)", "  operation tag(item)"]
    assert backlog_model.unmerged(laid, lines) == body
