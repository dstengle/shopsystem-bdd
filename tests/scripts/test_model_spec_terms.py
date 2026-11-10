"""Unit tests of scripts/model_spec's term ids: a condition that shares its word with another entry is
keyed `<term> of <kind>`, so same-named entries are two terms and no v_t2 (a term with two entries)."""

from test_model_spec import INDEX, PATH, CodifiedTest

TWO = ("- **open** (adjective of work-item): A work-item is open when the work-item is not `green`.\n"
       "- **open** (adjective of initiative): An initiative is open when the initiative is not `done`.\n")


class TermIdTest(CodifiedTest):
    def test_same_named_conditions_with_glosses_are_two_terms(self):
        text = INDEX.replace(
            "- **open** (adjective of initiative): its status is not `done` and not `abandoned`.\n", TWO)
        self.write("spec/index.md", text)
        f = self.facts()
        self.assertIn(f'category("term/{PATH}/open-of-work-item", "condition").', f)
        self.assertIn(f'category("term/{PATH}/open-of-initiative", "condition").', f)
        found, _ = self.check()
        self.assertEqual(self.rows(found, "v_t2"), [])

    def test_a_condition_with_a_gloss_and_no_twin_is_keyed_by_its_word(self):
        text = INDEX.replace(
            "- **open** (adjective of initiative): its status is not `done` and not `abandoned`.\n",
            TWO.splitlines(True)[0])
        self.write("spec/index.md", text)
        self.assertIn(f'category("term/{PATH}/open", "condition").', self.facts())


def _model_check(root):
    import pathlib
    import subprocess
    import sys
    model = pathlib.Path(__file__).resolve().parents[2] / "scripts" / "model"
    return subprocess.run([sys.executable, str(model), "check"], cwd=root, capture_output=True, text=True).stdout


def _codified_2(tmp_path):
    import pathlib
    import shutil
    shutil.copytree(pathlib.Path(__file__).resolve().parent / "fixtures" / "codified-2", tmp_path / "c2")
    return tmp_path / "c2"


def test_a_codified_2_index_has_no_v_t13_for_a_frame_naming_agent(tmp_path):
    """b199: a frame naming grammar 4's base kind `agent`, or an imported pack's kind, reads."""
    out = _model_check(_codified_2(tmp_path))
    assert "v_t13" not in out, out
    assert out.strip().splitlines()[-1].startswith("0 violations"), out


def test_a_codified_1_index_still_reads_agent_as_unknown(tmp_path):
    root = _codified_2(tmp_path)
    index = root / "spec" / "index.md"
    text = index.read_text().replace("language: codified-2", "language: codified-1").replace("imports: [cli]\n", "")
    index.write_text(text)
    out = _model_check(root)
    assert "v_t13" in out and "write" in out, out
