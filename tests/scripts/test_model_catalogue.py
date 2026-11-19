"""The catalogues' entries in `spec check` (model_catalogue, b370): an entry that mentions no item passes while its
`Since:` names a release that is a section of CHANGELOG.md (checking r58), and fails when the version it names is no
section; v_c3's facts and model.lp's rule solved over them."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "tests"))
import toolchain

CHANGELOG = "# Changelog\n\n## 0.31.0: the workflow simplified\n\nThings.\n\n## 0.30.0\n\nOlder things.\n"


class Reading:
    """The part of Model that model_catalogue's mixin needs: a root, a context path, the facts and the lines."""

    def __init__(self, root):
        import model_catalogue
        self.root, self.path, self.facts, self.req_text = Path(root), "ex.com/prod/ctx", [], {}
        self.mixin = model_catalogue.CatalogueReading

    def fact(self, name, *args):
        self.facts.append((name, args))

    def node(self, ident, kind):
        self.fact("node", ident, kind)

    def asp(self):
        return "\n".join('%s(%s).' % (n, ", ".join('"%s"' % a for a in args)) for n, args in self.facts)


def violations(tmp_path, since):
    toolchain.require()
    from model_check import solve
    (tmp_path / "grammar").mkdir()
    (tmp_path / "grammar" / "rules.md").write_text(
        "# Rule catalogue\n\n## v15a\n\na requirement has no id\n\n- Purpose: every line is cited by its id.\n"
        "- Since: %s\n" % since)
    (tmp_path / "CHANGELOG.md").write_text(CHANGELOG)
    reading = Reading(tmp_path)
    reading.mixin.read_catalogues(reading)
    return {name for name, _ in solve(reading)[0]}


def test_an_entry_whose_since_names_a_release_of_the_changelog_mentions_a_release(tmp_path):
    assert "v_c3" not in violations(tmp_path, "0.31.0")


def test_an_entry_whose_since_names_a_version_no_section_has_mentions_nothing(tmp_path):
    assert "v_c3" in violations(tmp_path, "9.9.9")


def test_an_entry_that_mentions_an_item_passes(tmp_path):
    assert "v_c3" not in violations(tmp_path, "b1")
