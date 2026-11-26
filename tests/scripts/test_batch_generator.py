"""The generator a tree holds writes its features (b740, batches r170): a tree with `scripts/features` and
`scripts/features_generate.py` has them written by that program in a process of its own, a refusal of it a
GenerateError; a tree with none by features_generate in this process."""
import batch_generator
import features_generate
import pytest

STAND_IN = '''import sys
args = sys.argv[1:]
if "--preview" in args:
    if "refused" in args[-1]:
        sys.stderr.write("features: the capability is refused\\n")
        sys.exit(1)
    sys.stdout.write("# the tree's own of %s\\n" % args[-1].rsplit("/", 1)[-1])
    sys.exit(0)
out = args[args.index("--dir") + 1]
for name in args[args.index("--root") + 2:]:
    open("%s/%s.feature" % (out, name), "w").write("# the tree's own run of %s\\n" % name)
'''


def _tree(tmp_path):
    scripts = tmp_path / "scripts"
    scripts.mkdir()
    (scripts / "features").write_text(STAND_IN)
    (scripts / "features_generate.py").write_text("")
    return tmp_path


def test_a_tree_with_its_own_generator_writes_with_it(tmp_path):
    tree = _tree(tmp_path)
    assert batch_generator.generate(tree, tree / "spec" / "capabilities" / "a.md") == "# the tree's own of a.md\n"
    found = batch_generator.generate_all(tree, [tree / "spec" / "capabilities" / "a.md"])
    assert list(found.values()) == ["# the tree's own run of a\n"]


def test_a_refusal_of_the_trees_generator_is_a_generate_error(tmp_path):
    tree = _tree(tmp_path)
    with pytest.raises(features_generate.GenerateError, match="the capability is refused"):
        batch_generator.generate(tree, tree / "refused.md")


def test_a_tree_with_no_generator_of_its_own_writes_in_this_process(tmp_path, monkeypatch):
    monkeypatch.setattr(features_generate, "generate", lambda tree, path: "in process %s\n" % path.name)
    assert batch_generator.generate(tmp_path, tmp_path / "b.md") == "in process b.md\n"


def test_a_generator_past_its_time_limit_is_a_generate_error_naming_it(tmp_path, monkeypatch):
    """b749: a run that does not end within `$SHOPSYSTEM_GENERATE_TIMEOUT` seconds is refused, and generate_all
    falls back to each capability alone, finding none."""
    tree = _tree(tmp_path)
    (tree / "scripts" / "features").write_text("import time\ntime.sleep(30)\n")
    monkeypatch.setenv("SHOPSYSTEM_GENERATE_TIMEOUT", "0.5")
    with pytest.raises(features_generate.GenerateError, match="feature generator .* timed out after 0.5 s"):
        batch_generator.generate(tree, tree / "a.md")
    assert batch_generator.generate_all(tree, [tree / "a.md"]) == {tree / "a.md": None}


def test_a_generator_that_cannot_start_is_a_generate_error_naming_it(tmp_path, monkeypatch):
    def fail(*args, **kwargs):
        raise OSError("no interpreter")
    monkeypatch.setattr(batch_generator.subprocess, "run", fail)
    with pytest.raises(features_generate.GenerateError, match="feature generator .* could not start: no interpreter"):
        batch_generator.generate(_tree(tmp_path), tmp_path / "a.md")
