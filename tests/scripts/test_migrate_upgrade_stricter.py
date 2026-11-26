"""The 0.45.0 upgrade step "the stricter rules" (b851, upgrades r47): its report names each term by its word as its
entry writes it, the lexicon's term whose id is `spec check`'s node, a hyphen kept (b854)."""
import shutil
from pathlib import Path

from upgrades import migrate_upgrade_stricter

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "domain-model"
VOCABULARY = Path("spec") / "vocabulary" / "notes.md"
LABEL = "- **label** (verb, action) → operation notes.label. Forms: labels, labelled. Frame: <actor> labels <note>."
HYPHENED = ("- **follow-up** (verb, action) → operation notes.label. Forms: follows-up, followed-up. "
            "Frame: <actor> follows-up <gadget>.")


def test_a_term_with_a_hyphen_in_its_word_is_reported_with_the_hyphen_kept(tmp_path):
    shutil.copytree(FIXTURE / "spec", tmp_path / "spec")
    path = tmp_path / VOCABULARY
    path.write_text(path.read_text().replace(LABEL, LABEL + "\n" + HYPHENED, 1))
    notes = [n for n in migrate_upgrade_stricter.plan(tmp_path).notes if " v_t13 " in n]
    assert any(n.startswith("the stricter rules: v_t13 follow-up: ") for n in notes), notes
    assert not any(" follow up" in n for n in notes), notes
