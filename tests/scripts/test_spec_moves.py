"""spec_moves: a session's table of moved lines written as new capability files, the old ones retired with a `## Moved`
table, `spec/moves.json`, and an old id resolved through it (the domain contract design, §9.2)."""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

import spec_moves  # noqa: E402
import spec_read  # noqa: E402
from shop_refused import Refused  # noqa: E402

OLD = """---
id: capability/ex/{name}
title: {name}
narrator: the person
group: service
language: codified-2
retired: [g1, r1]
---

# {name}

## Purpose
Old.

## Terms

- **thing** (noun): a thing.

## Behaviour

### [g2] Two lines
Restates: r7@0.29.
- [r2] When the person runs `x a`, `x` shall exit successfully.
- [r3] When the person runs `x b`, `x` shall exit successfully.

### [g4] A given
Restates: r8@0.29.
- [r4] When the person runs `x c`, `x` shall exit successfully.
```given
the file `a` holds "1"
```

## Dropped

- r1@0.29: gone before.
"""

CAPS = "notes\tnotes\tservice notes\tthe person\tservice\tNotes\tThe notes a person keeps.\n"


def context(tmp_path, names=("alpha", "beta")):
    caps = tmp_path / "spec" / "capabilities"
    caps.mkdir(parents=True)
    for name in names:
        (caps / ("%s.md" % name)).write_text(OLD.format(name=name))
    (tmp_path / "caps.tsv").write_text(CAPS)
    return tmp_path


def table(tmp_path, rows):
    path = tmp_path / "rewording.tsv"
    path.write_text("".join("\t".join(r) + "\n" for r in rows))
    return path


ROWS = [("alpha#r2", "notes", "Adding a note", "When the person adds a note, the notes service shall keep the note."),
        ("alpha#r3", "notes", "Adding a note", "When the person adds a note, the notes service shall return it."),
        ("alpha#r4", "notes", "Listing", "When the person lists the notes, the notes service shall complete it."),
        ("beta#r2", "-", "Gone", "the CLI adapter's"),
        ("beta#r3", "-", "Gone", "the CLI adapter's"),
        ("beta#r4", "notes", "Listing again", "When the person lists the notes, the notes service shall return.")]


def test_apply_writes_the_new_capability_with_new_ids_restates_and_given(tmp_path):
    root = context(tmp_path)
    spec_moves.apply(root, table(tmp_path, ROWS), tmp_path / "caps.tsv")
    cap = spec_read.capability(root / "spec" / "capabilities" / "notes.md")
    assert not cap.problems
    assert [(g.id, [r.id for r in g.requirements]) for g in cap.groups] == [
        ("g1", ["r1", "r2"]), ("g2", ["r3"]), ("g3", ["r4"])]
    assert cap.groups[0].restates == [("alpha", 7)]
    assert cap.groups[1].given is not None
    text = (root / "spec" / "capabilities" / "notes.md").read_text()
    assert "area: notes" in text and "specifies: service notes" in text and "unbuilt: []" in text


def test_apply_retires_the_old_ids_with_a_moved_table_and_drops_the_restated_ids(tmp_path):
    root = context(tmp_path)
    spec_moves.apply(root, table(tmp_path, ROWS), tmp_path / "caps.tsv")
    beta = spec_read.capability(root / "spec" / "capabilities" / "beta.md")
    assert beta.groups == [] and set(beta.retired) >= {"g2", "r2", "r3", "g4", "r4", "g1", "r1"}
    assert ("beta", 7, "the CLI adapter's") in beta.dropped
    text = (root / "spec" / "capabilities" / "beta.md").read_text()
    assert "| r4 | notes#r4 |" in text and "| r2 | dropped |" in text
    assert "## Behaviour" in text and "- **thing**" not in text
    moves = json.loads((root / "spec" / "moves.json").read_text())
    assert moves["alpha#r3"] == "notes#r2" and moves["beta#r2"] is None and moves["alpha#g4"] == "notes#g2"


def test_resolve_gives_the_new_id_none_for_a_dropped_one_and_the_id_itself_else(tmp_path):
    root = context(tmp_path)
    spec_moves.apply(root, table(tmp_path, ROWS), tmp_path / "caps.tsv")
    assert spec_moves.resolve(root, "alpha#r4") == "notes#r3"
    assert spec_moves.resolve(root, "beta#r3") is None
    assert spec_moves.resolve(root, "gamma#r1") == "gamma#r1"
    assert spec_moves.problems(root) == []


def test_a_table_missing_a_live_id_or_naming_one_twice_is_refused(tmp_path):
    root = context(tmp_path)
    with pytest.raises(Refused, match="misses alpha#r4"):
        spec_moves.apply(root, table(tmp_path, ROWS[:2] + ROWS[3:]), tmp_path / "caps.tsv")
    with pytest.raises(Refused, match="twice"):
        spec_moves.apply(root, table(tmp_path, ROWS + ROWS[:1]), tmp_path / "caps.tsv")


def test_a_reused_name_renamed_to_0_37_keeps_its_old_ids_apart(tmp_path):
    root = context(tmp_path, names=("alpha", "notes-0-37"))
    rows = [r for r in ROWS if not r[0].startswith("beta")] + [
        ("notes#r2", "notes", "Again", "When the person adds a note, the notes service shall keep the note."),
        ("notes#r3", "-", "Gone", "the CLI adapter's"), ("notes#r4", "-", "Gone", "the CLI adapter's")]
    spec_moves.apply(root, table(tmp_path, rows), tmp_path / "caps.tsv")
    assert spec_moves.resolve(root, "notes#r2") == "notes#r8"
    cap = spec_read.capability(root / "spec" / "capabilities" / "notes.md")
    assert [r.id for g in cap.groups for r in g.requirements][0] == "r5"
    assert (root / "spec" / "capabilities" / "notes-0-37.md").read_text().count("| r2 | notes#r8 |") == 1
