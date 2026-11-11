"""migrate_upgrade_values (b257): the 0.34.0 upgrade step "value kinds" changes no file and names each attribute that
declares neither adjective nor noun values, and each line that says one of its values in the short form."""
import pathlib
import shutil

import migrate_upgrade_values
import toolchain

FIXTURE = pathlib.Path(__file__).parent / "fixtures" / "codified-2"
CAPABILITY = """---
id: capability/example.org/fixture/codified-2/shelf
title: Shelf
language: codified-2
retired: []
unbuilt: []
---
# Shelf
## Behaviour
### [g1] a review stage
- [r1] While a stage is `review`, when the person runs `work start`, `work` shall end the stage.

### [g2] the full form
- [r2] While the tier of a stage is `check`, when the person runs `work start`, `work` shall end the stage.
"""


def repo(tmp_path, plain=True):
    toolchain.require()
    root = tmp_path / "ctx"
    shutil.copytree(FIXTURE, root)
    index = root / "spec" / "index.md"
    if plain:
        index.write_text(index.read_text().replace("Values (noun): `check`", "Values: `check`"))
    (root / "spec" / "capabilities").mkdir()
    (root / "spec" / "capabilities" / "shelf.md").write_text(CAPABILITY)
    return root


def test_it_names_each_undeclared_attribute_and_each_short_form_of_its_values(tmp_path):
    root = repo(tmp_path)
    before = {p: p.read_text() for p in root.rglob("*.md")}
    changes = migrate_upgrade_values.plan(root)
    assert changes.texts == {} and changes.moves == []
    assert {p: p.read_text() for p in root.rglob("*.md")} == before
    assert any("w_value_kind tier (attribute of stage), spec/index.md: declares neither" in n for n in changes.notes), changes.notes
    assert any("shelf#r1 says `review` of the tier in the short form" in n for n in changes.notes), changes.notes
    assert not any("shelf#r2" in n for n in changes.notes)


def test_a_declared_spec_has_nothing_to_report(tmp_path):
    root = repo(tmp_path, plain=False)
    (root / "spec" / "capabilities" / "shelf.md").write_text(CAPABILITY.replace("While a stage is `review`",
                                                                                "While the tier of a stage is `review`"))
    assert migrate_upgrade_values.plan(root).notes == []
