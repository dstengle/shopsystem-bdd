"""spec_coupling's words (checking r148, r149): a word one area's layer defines for another area's element couples
them as a word, and a word two areas each define for their own elements is a homonym of every two of them."""
import domain_model
import spec_coupling
import spec_vocabulary


def _entry(term, layer, area):
    element = domain_model.Element("object", term, area)
    return spec_vocabulary.Entry(term, "noun", "object " + term, "", "spec/vocabulary/%s.md" % layer, layer, element)


def _found(monkeypatch, entries):
    monkeypatch.setattr(spec_vocabulary, "entries", lambda root: entries)
    found = {}
    spec_coupling._words("root", found)
    return found


def test_a_word_three_areas_define_for_their_own_is_a_homonym_of_every_two(monkeypatch):
    found = _found(monkeypatch, [_entry("note", x, x) for x in ("a", "b", "c")]
                   + [_entry("note", spec_vocabulary.SHARED, "a")])
    assert {k: (v["words"], v["homonyms"]) for k, v in found.items()} == {
        ("b", "a"): (set(), {"note"}), ("c", "a"): (set(), {"note"}), ("c", "b"): (set(), {"note"})}


def test_a_word_one_area_defines_twice_couples_nothing(monkeypatch):
    assert _found(monkeypatch, [_entry("note", "a", "a"), _entry("note", "a", "a")]) == {}


def test_a_word_meaning_another_areas_element_is_borrowed_not_a_homonym(monkeypatch):
    """b's `note` means a's element: a word of a's coupling by b, and no homonym of a's own `note`."""
    found = _found(monkeypatch, [_entry("note", "a", "a"), _entry("note", "b", "a")])
    assert {k: (v["words"], v["homonyms"]) for k, v in found.items()} == {("a", "b"): ({"note"}, set())}


def test_homonyms_rank_no_coupling(monkeypatch):
    """A coupling of homonyms only is listed with no word, after one of a word."""
    entries = [_entry("x", "a", "a"), _entry("x", "b", "b"), _entry("y", "c", "a")]
    monkeypatch.setattr(spec_vocabulary, "entries", lambda root: entries)
    for part in ("_elements", "_requirements", "_imports"):
        monkeypatch.setattr(spec_coupling, part, lambda root, found: None)
    monkeypatch.setattr(domain_model, "exists", lambda root: True)
    out = spec_coupling.couplings("root")
    assert [(c["area"], c["by"], c["words"], c["homonyms"]) for c in out] == [
        ("a", "c", ["y"], []), ("b", "a", [], ["x"])]
    assert "  homonym: x" in spec_coupling.text(out)


def _repo(tmp_path, files, modules):
    import subprocess
    for name, text in files.items():
        (tmp_path / name).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / name).write_text(text)
    (tmp_path / ".shop").mkdir()
    (tmp_path / ".shop" / "modules.toml").write_text(modules)
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True)
    return tmp_path


def test_imports_between_areas_resolve_bare_dotted_and_from_names(tmp_path):
    """r147: a bare name of the importer's folder, a dotted name under the root and a from-import's module each
    name another area's file (`import store` names no file of b's folder nor of the root); an import within an area
    or of a module the repository does not hold couples nothing."""
    import spec_coupling_imports
    root = _repo(tmp_path, {
        "a/store.py": "", "a/pkg/__init__.py": "", "a/pkg/deep.py": "", "b/a_kept.py": "",
        "b/shelf.py": "import store\nimport a_kept\nimport os\nfrom a.pkg import deep\nimport b.other\n",
        "b/other.py": "", "b/x.py": "from . import other\n",
    }, '[a]\nmodules = ["a/**", "b/a_*.py"]\n\n[b]\nmodules = ["b/*.py"]\n')
    found = sorted(spec_coupling_imports.imports(root))
    assert found == [("a", "b", "b/shelf.py -> a/pkg/__init__.py"), ("a", "b", "b/shelf.py -> a/pkg/deep.py"),
                     ("a", "b", "b/shelf.py -> b/a_kept.py")]


def test_a_file_two_tables_match_is_the_first_tables(tmp_path):
    import spec_coupling_imports
    declared = spec_coupling_imports.groups(_repo(
        tmp_path, {}, '[one]\nmodules = ["src/**/*.py"]\n\n[two]\nmodules = ["src/x_*.py"]\n'))
    assert spec_coupling_imports.area_of(declared, "src/x_y.py") == "one"
    assert spec_coupling_imports.area_of(declared, "src/deep/x_y.py") == "one"
    assert spec_coupling_imports.area_of(declared, "other/x_y.py") is None
