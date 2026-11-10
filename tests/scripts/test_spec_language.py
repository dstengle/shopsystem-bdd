"""spec_language and spec_context under a codified-2 index over codified-1 files (b151, CNL 4's I20): a universal
condition is parsed in its own file's grammar, and `model logic` reads no codified-1 line under a codified-2 index."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

import spec_context
import spec_language

MIXED = Path(__file__).resolve().parent / "fixtures" / "mixed-index"


def test_a_universal_condition_is_read_in_its_own_files_grammar():
    assert spec_language.four(MIXED, universal=True) is False
    assert spec_language.four(MIXED) is True


def test_a_codified_2_index_refuses_every_codified_1_line_naming_migrate_upgrade():
    """b240 phase 24b: a codified-2 context reads no codified-1 line, its capabilities' nor its universal
    conditions'; `model check` refuses such a file too (v_p0)."""
    ctx = spec_context.load(MIXED)
    assert ctx.statements == [] and ctx.facts == {}
    assert set(ctx.refused) == {"shelf#r1", "shelf#r2", "shelf#r3", "U1"}
    assert set(ctx.refused.values()) == {spec_context.OLD} and "`migrate upgrade`" in spec_context.OLD


def test_model_parse_reads_spec_universal_md_in_its_own_files_grammar():
    import subprocess
    model = Path(__file__).resolve().parents[2] / "scripts" / "model"
    done = subprocess.run([sys.executable, str(model), "--root", str(MIXED), "parse", "--file",
                           str(MIXED / "spec" / "universal.md")], capture_output=True, text=True)
    assert done.returncode == 0, done.stdout + done.stderr
    assert done.stdout.startswith("17: Ubiq ")
