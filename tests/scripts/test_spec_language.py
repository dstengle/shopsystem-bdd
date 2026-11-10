"""spec_language and spec_context under a codified-2 index over codified-1 files (b151, CNL 4's I20): a universal
condition is read in its own file's grammar, and a codified-1 line's facts do not depend on the index's marker."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

import spec_context
import spec_language

MIXED = Path(__file__).resolve().parent / "fixtures" / "mixed-index"


def test_a_universal_condition_is_read_in_its_own_files_grammar():
    assert spec_language.four(MIXED, universal=True) is False
    assert spec_language.four(MIXED) is True


def test_a_codified_2_index_loads_a_codified_1_universal_condition():
    assert spec_context.load(MIXED).refused == {}


def test_model_parse_reads_spec_universal_md_in_its_own_files_grammar():
    import subprocess
    model = Path(__file__).resolve().parents[2] / "scripts" / "model"
    done = subprocess.run([sys.executable, str(model), "--root", str(MIXED), "parse", "--file",
                           str(MIXED / "spec" / "universal.md")], capture_output=True, text=True)
    assert done.returncode == 0, done.stdout + done.stderr
    assert done.stdout.startswith("17: Ubiq ")


def _codified_1(tmp_path):
    """A copy of the fixture whose index says codified-1 (its imports left out)."""
    import shutil
    copy = tmp_path / "mixed-1"
    shutil.copytree(MIXED, copy)
    index = copy / "spec" / "index.md"
    index.write_text(index.read_text().replace("language: codified-2", "language: codified-1")
                     .replace("imports: [cli]\n", ""))
    return copy


def test_a_codified_1_lines_facts_are_in_the_layered_ids_under_a_codified_2_index(tmp_path):
    """b151: shelf#r2's `open` is the old lexicon's `c_open_2` (the glossary's file is `c_open`, its stage `c_open_3`),
    the layered lexicon's `c_open`; its facts carry the layered id, which the context's vocabulary reads as the
    shelf's `open`, and are otherwise the facts of the line under a codified-1 index."""
    old = spec_context.load(_codified_1(tmp_path)).facts["shelf#r2"]
    ctx = spec_context.load(MIXED)
    new = ctx.facts["shelf#r2"]
    assert any(",c_open_2," in f for f in old) and not any("c_open_2" in f for f in new)
    assert [f.replace(",c_open_2,", ",c_open,") for f in old] == new
    assert (ctx.vocab.cond_terms["c_open"], ctx.vocab.kinds[ctx.vocab.conds["c_open"]]) == ("open", "shelf")


def test_a_codified_1_line_using_an_entry_the_layered_lexicon_left_out_is_refused_naming_it(tmp_path):
    import shutil
    copy = tmp_path / "mixed"
    shutil.copytree(MIXED, copy)
    shelf = copy / "spec" / "capabilities" / "shelf.md"
    shelf.write_text(shelf.read_text() + "\n### [g3] A stage that is open is counted\n"
                     "- [r3] While a stage is open, when a clerk stocks a shelf, the clerk shall count the shelf.\n")
    ctx = spec_context.load(copy)
    assert ctx.refused == {"shelf#r3": "refused: the condition open of stage has no entry in the layered lexicon"}
    assert "shelf#r3" not in ctx.facts and "shelf#r2" in ctx.facts
