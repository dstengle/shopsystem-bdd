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


def test_a_codified_1_lines_facts_are_its_facts_under_a_codified_1_index(tmp_path):
    """b151: the glossary's and the capabilities' entries stand side by side in the layered lexicon, so every line's
    facts, and the domain's facts of its definitions, are those of the context under a codified-1 index."""
    old = spec_context.load(_codified_1(tmp_path))
    ctx = spec_context.load(MIXED)
    assert ctx.refused == {} and ctx.facts == old.facts
    assert any(",c_open_2,neg)" in f for f in ctx.facts["shelf#r3"])
    assert (ctx.vocab.cond_terms["c_open_2"], ctx.vocab.kinds[ctx.vocab.conds["c_open_2"]]) == ("open", "shelf")
    assert {f for f in old.domain if f.startswith(("dalt", "dlit"))} <= set(ctx.domain)


def _shop_pack(tmp_path):
    """A copy of the fixture that imports a pack of its own whose `Open` takes the number `c_open` before the
    context's three `open`s: the shelf's is the old lexicon's `c_open_2`, the layered one's `c_open_3`."""
    import shutil
    copy = tmp_path / "mixed-pack"
    shutil.copytree(MIXED, copy)
    (copy / "spec" / "packs").mkdir()
    (copy / "spec" / "packs" / "shop.md").write_text(
        "# shop\n\n## Glossary\n\n- **Open** (adjective of shelf): the shelf is open for the day.\n")
    index = copy / "spec" / "index.md"
    index.write_text(index.read_text().replace("imports: [cli]", "imports: [cli, shop]"))
    return copy


def test_a_codified_1_lines_ids_are_mapped_to_the_layered_lexicons(tmp_path):
    old = spec_context.load(_codified_1(tmp_path)).facts["shelf#r2"]
    ctx = spec_context.load(_shop_pack(tmp_path))
    assert ctx.refused == {}
    assert [f.replace(",c_open_2,", ",c_open_3,") for f in old] == ctx.facts["shelf#r2"]
    assert (ctx.vocab.cond_terms["c_open_3"], ctx.vocab.kinds[ctx.vocab.conds["c_open_3"]]) == ("open", "shelf")


def test_a_scenario_reads_a_codified_1_definition_in_the_old_lexicon_under_a_codified_2_index(tmp_path):
    """shelf#r3's `full` is defined as not `open`, in the old lexicon's `c_open_2`: its scenario keeps `full` and
    leaves out the definition's literal, the layered `c_open_3`."""
    import spec_steps_facts
    ctx = spec_context.load(_shop_pack(tmp_path))
    facts = ctx.facts["shelf#r3"]
    assert 'ccond("shelf#r3",v1,c_open_3,neg).' in facts
    own = [str(s) for s in spec_steps_facts.own(ctx.vocab, facts)]
    assert 'ccond("shelf#r3",v1,c_full,pos)' in own and not any("c_open" in f for f in own)


def test_an_id_the_layered_lexicon_has_not_is_refused_naming_its_entry():
    import pytest
    import spec_context_ids
    import spec_lexicon
    import spec_logic_vocab
    lex = spec_lexicon.read(MIXED)
    old = spec_logic_vocab.Vocab(lex)
    left = [t for t in lex.terms if not (t.term == "open" and "shelf" in t.where)]
    ids = spec_context_ids.Ids(old, spec_logic_vocab.Vocab(spec_lexicon.Lexicon(left, lex.rows)))
    assert ids.fact('ccond("shelf#r2",v1,c_open,pos).') == 'ccond("shelf#r2",v1,c_open,pos).'
    with pytest.raises(spec_context_ids.Unmapped, match="the condition open of shelf has no entry"):
        ids.fact('ccond("shelf#r2",v1,c_open_2,pos).')
