"""model_domain: the domain model's, the vocabulary's and a line's problems as `model check` facts (v_m1, v_m8,
v_t18-v_t21), over a copy of the domain-model fixture."""
import pathlib
import shutil

import model_check
import model_facts

FIXTURE = pathlib.Path(__file__).parent / "fixtures" / "domain-model"
ARCHIVE = """---
area: archive
kind: supporting
---

```model
service archive
  operation shelve(note)  outcomes: done
```
"""


def _codes(root):
    found, _ = model_check.solve(model_facts.Model(root).read())
    return sorted((name, args[0]) for name, args in found if name[:3] in ("v_m", "v_t"))


def _copy(tmp_path):
    shutil.copytree(FIXTURE, tmp_path, dirs_exist_ok=True)
    return tmp_path


def test_the_fixture_has_none(tmp_path):
    assert _codes(_copy(tmp_path)) == []


def test_v_m8_and_the_vocabularys_problems_are_violations(tmp_path):
    root = _copy(tmp_path)
    model = root / "spec" / "model" / "notes.md"
    model.write_text(model.read_text().replace("event a note is added: raised by notes.add",
                                               "event a note is added: raised by notes.remove"))
    vocab = root / "spec" / "vocabulary" / "notes.md"
    vocab.write_text(vocab.read_text() + "- **shelf** (noun): a place.\n- **box** (noun) → object box.\n"
                     "- **memo** (noun) → object note.\n")
    assert _codes(root) == [("v_m8", "a note is added"), ("v_t18", "shelf"), ("v_t19", "box"), ("v_t20", "memo")]


def test_v_m1_a_line_using_a_word_of_an_area_its_capability_does_not_read(tmp_path):
    root = _copy(tmp_path)
    (root / "spec" / "model" / "archive.md").write_text(ARCHIVE)
    (root / "spec" / "vocabulary" / "archive.md").write_text(
        "---\narea: archive\n---\n\n- **shelve** (verb, action) → operation archive.shelve. Forms: shelves, shelved. "
        "Frame: <actor> shelves <note>.\n")
    cap = root / "spec" / "capabilities" / "notebook.md"
    cap.write_text(cap.read_text() + "\n### [g7] A note shelved is filed\n"
                   "- [r7] When the person shelves a note, the notes service shall file the note.\n")
    assert ("v_m1", "capability/example.org/fixture/domain-model/notebook#r7") in _codes(root)
    model = root / "spec" / "model" / "notes.md"
    model.write_text(model.read_text().replace("imports: []", "imports: [archive]"))
    assert [c for c in _codes(root) if c[0] == "v_m1"] == []
