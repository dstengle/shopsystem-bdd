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
