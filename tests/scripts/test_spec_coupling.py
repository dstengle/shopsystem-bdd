"""spec_coupling's words (checking r144): a word two areas' layers define couples them, whichever two of the areas
that define it."""
import spec_coupling
import spec_vocabulary


def _entry(term, layer):
    return spec_vocabulary.Entry(term, "noun", "", "", "spec/vocabulary/%s.md" % layer, layer)


def test_a_word_three_areas_define_couples_every_two_of_them(monkeypatch):
    layers = ["a", "b", "c", spec_vocabulary.SHARED]
    monkeypatch.setattr(spec_vocabulary, "entries", lambda root: [_entry("note", x) for x in layers])
    found = {}
    spec_coupling._words("root", found)
    assert {k: v["words"] for k, v in found.items()} == {
        ("b", "a"): {"note"}, ("c", "a"): {"note"}, ("c", "b"): {"note"}}


def test_a_word_one_area_defines_twice_couples_nothing(monkeypatch):
    monkeypatch.setattr(spec_vocabulary, "entries", lambda root: [_entry("note", "a"), _entry("note", "a")])
    found = {}
    spec_coupling._words("root", found)
    assert found == {}


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
