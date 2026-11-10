"""spec_language and spec_context under a codified-2 index over codified-1 files (b151, CNL 4's I20): a universal
condition's file is read by its own marker, and `model logic` reads no codified-1 file."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

import spec_context
import spec_language

MIXED = Path(__file__).resolve().parent / "fixtures" / "mixed-index"


def test_a_universal_condition_s_file_is_read_by_its_own_marker():
    assert spec_language.four(MIXED, universal=True) is False
    assert spec_language.four(MIXED) is True


def test_the_logic_reads_no_codified_1_file():
    """b240 phase 24c: a codified-1 file is no capability of the context `model logic` reads, nor a codified-1
    `spec/universal.md` its universal conditions; `model check` refuses such a file, naming `migrate upgrade` (v_p0)."""
    ctx = spec_context.load(MIXED)
    assert ctx.caps == {} and ctx.statements == [] and ctx.facts == {} and ctx.refused == {}
