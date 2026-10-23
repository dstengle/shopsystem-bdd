"""design-model-check r110 and work-queue r12, 7: a work-item's held id is checked, `work add` counts ids and refuses a plain note."""
import json
import pathlib
import subprocess
import sys

import pytest

SCRIPTS = pathlib.Path(__file__).resolve().parents[2] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import workqueue

INDEX = "---\nid: bounded-context/o/p/c\nkind: bounded-context\n---\n"
INITIATIVE = "---\nid: initiative/o/p/c/%s\nkind: initiative\nstatus: started\n---\n"


def item(ident):
    return ("---\nid: work-item/o/p/c/%s\nkind: work-item\npart_of: initiative/o/p/c/i1\nstatus: drafted\n---\n\n# T\n"
            % ident)


def git(repo, *args):
    return subprocess.run(["git", "-c", "user.name=T", "-c", "user.email=t@example.com", *args], cwd=repo,
                          capture_output=True, text=True, check=True).stdout


def build(tmp_path, files):
    (tmp_path / "spec").mkdir()
    (tmp_path / "spec/index.md").write_text(INDEX)
    for initiative in ("i1", "i2"):
        (tmp_path / ".shop/work" / initiative).mkdir(parents=True)
        (tmp_path / ".shop/work" / initiative / "initiative.md").write_text(INITIATIVE % initiative)
    for rel, text in files.items():
        (tmp_path / ".shop/work" / rel).write_text(text)
    git(tmp_path, "init", "-q")
    git(tmp_path, "config", "user.name", "T")
    git(tmp_path, "config", "user.email", "t@example.com")
    git(tmp_path, "add", "-A")
    git(tmp_path, "commit", "-q", "-m", "start")
    return tmp_path


def problems(repo):
    out = subprocess.run([sys.executable, str(SCRIPTS / "model"), "--root", str(repo), "check", "--json"],
                         capture_output=True, text=True).stdout
    return json.loads(out)["problems"]


def r110(repo):
    return [p for p in problems(repo) if "a work-item's file is named" in p or "is already held by" in p
            or "work-item id" in p]


def test_two_work_items_holding_one_id_under_different_stems_are_a_file_problem(tmp_path):
    repo = build(tmp_path, {"i1/w3.md": item("w3"), "i2/w5.md": item("w3")})
    assert any("w5.md" in p for p in r110(repo)), problems(repo)


def test_a_work_item_whose_id_is_not_its_file_stem_is_a_file_problem(tmp_path):
    repo = build(tmp_path, {"i1/w3.md": item("w9")})
    assert any("w3.md" in p for p in r110(repo)), problems(repo)


def test_add_counts_the_id_of_a_work_item_not_named_by_it(tmp_path):
    repo = build(tmp_path, {"i1/w1.md": item("w1"), "i1/fix-login.md": item("w7")})
    assert workqueue.add(repo, "i1", "New", "p", "c", ["c#r1"]) == "w8"


def test_add_beside_a_plain_note_refuses_naming_it_as_no_work_item_and_writes_nothing(tmp_path):
    repo = build(tmp_path, {"i1/w1.md": item("w1"), "i1/w2.md": "just a note\n"})
    before = git(repo, "rev-parse", "HEAD")
    with pytest.raises(workqueue.Refused) as error:
        workqueue.add(repo, "i1", "New", "p", "c", ["c#r1"])
    assert ".shop/work/i1/w2.md" in str(error.value) and "not a work-item" in str(error.value)
    assert "already exists" not in str(error.value)
    assert git(repo, "rev-parse", "HEAD") == before
    assert (repo / ".shop/work/i1/w2.md").read_text() == "just a note\n"
