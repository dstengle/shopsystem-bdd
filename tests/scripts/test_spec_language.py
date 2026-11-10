"""spec_language and spec_context under a codified-2 index over codified-1 files (b151, CNL 4's I20): a universal
condition is parsed in its own file's grammar, and `model logic` reads no codified-1 file."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

import spec_context
import spec_language

MIXED = Path(__file__).resolve().parent / "fixtures" / "mixed-index"


def test_a_universal_condition_is_read_in_its_own_files_grammar():
    assert spec_language.four(MIXED, universal=True) is False
    assert spec_language.four(MIXED) is True


def test_the_logic_reads_no_codified_1_file():
    """b240 phase 24c: a codified-1 file is no capability of the context `model logic` reads, nor a codified-1
    `spec/universal.md` its universal conditions; `model check` refuses such a file, naming `migrate upgrade` (v_p0)."""
    ctx = spec_context.load(MIXED)
    assert ctx.caps == {} and ctx.statements == [] and ctx.facts == {} and ctx.refused == {}


def test_model_parse_reads_spec_universal_md_in_its_own_files_grammar():
    import subprocess
    model = Path(__file__).resolve().parents[2] / "scripts" / "model"
    done = subprocess.run([sys.executable, str(model), "--root", str(MIXED), "parse", "--file",
                           str(MIXED / "spec" / "universal.md")], capture_output=True, text=True)
    assert done.returncode == 0, done.stdout + done.stderr
    assert done.stdout.startswith("17: Ubiq ")
