"""The tutorial run as an end-to-end test (b868, quote-115): docs/tutorial.md walked in order in a folder of its own,
from an empty folder to docs/examples/notes-cli. Each `$ ` line of its ```console blocks runs (`shop` through this
repository's scripts/, with tests/scripts/stub_gh.py as $SHOPSYSTEM_WORK_GH and a bare repository standing for the
GitHub remote the page names) and prints what the page shows; each file the page shows whole (an HTML comment naming
its path before the block) is written, the batch's work among them (notes.py, the laid capability, the feature's
steps, cli.toml), since no agent runs in a test; the person's merge is made on the stand-in. Then `spec check` passes,
and the folder's spec/, features/, notes.py and .shop/product/product.toml are docs/examples/notes-cli's: the same
files with the same text, the `.gitkeep` placeholders aside and `spec/universal.md`, which `migrate init` writes and
which holds no condition. The grammar tools come from toolchain.require(), never a skip. docs_tutorial reads and
runs the page."""
import os
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import docs_tutorial
import toolchain
from batch_testing import gh_env
from docs_testing import EXAMPLE, REPO

PAGE = "docs/tutorial.md"
REMOTE = "https://github.com/example/notes-cli.git"
COMPARED = ("spec", "features", "notes.py", ".shop/product/product.toml")


@pytest.fixture
def env(tmp_path):
    """The environment of the walk: a git identity, the page's GitHub remote read as a bare repository under
    tmp_path, the stand-in gh, and no Claude Code session's transcripts."""
    bare = tmp_path / "origin.git"
    docs_tutorial.subprocess.run(["git", "init", "-q", "--bare", str(bare)], check=True)
    config = tmp_path / "gitconfig"
    config.write_text('[user]\n\tname = The Writer\n\temail = writer@example.org\n[url "%s"]\n\tinsteadOf = %s\n'
                      % (bare.as_uri(), REMOTE))
    (tmp_path / "gh").mkdir()
    out = dict(os.environ, GIT_CONFIG_GLOBAL=str(config), GIT_CONFIG_NOSYSTEM="1",
               CLAUDE_CONFIG_DIR=str(tmp_path / "claude"), **gh_env(tmp_path / "gh"))
    out.pop("CLAUDE_PLUGIN_ROOT", None)
    return out


def test_the_tutorial_builds_the_notes_example_from_an_empty_folder(tmp_path, env):
    toolchain.require()
    folder = tmp_path / "notes"
    folder.mkdir()
    docs_tutorial.walk(PAGE, (REPO / PAGE).read_text(encoding="utf-8"), folder, env)
    code, got = docs_tutorial.run(folder, "shop spec check", env)
    assert code == 0, "\n".join(got)
    built = docs_tutorial.files(folder, *COMPARED)
    universal = built.pop("spec/universal.md", "")
    assert "## Behaviour" in universal and "- [U" not in universal
    assert built == docs_tutorial.files(EXAMPLE, *COMPARED), "the folder is not docs/examples/notes-cli"
    assert docs_tutorial.run(folder, "git status --porcelain", env) == (0, [])


SAMPLE = """\
<!-- tutorial: file a/b.txt -->
<!-- docs: context docs/examples/notes-cli -->
```text
one
```

```console
$ shop work line b1 --model "object tag

service notes"
b1 "x": model lines of notes-cli
$ git status
```

<!-- tutorial: merge batch-1 -->
"""


def test_the_steps_of_a_page_are_read_in_order():
    assert docs_tutorial.steps(SAMPLE) == [
        ("file", 3, ("a/b.txt", "one\n")),
        ("run", 7, ('shop work line b1 --model "object tag\n\nservice notes"', ['b1 "x": model lines of notes-cli'])),
        ("run", 7, ("git status", [])),
        ("merge", 15, "batch-1"),
    ]


def test_a_marker_names_only_the_block_after_it():
    assert docs_tutorial.steps("<!-- tutorial: file x -->\nsome words\n```text\none\n```\n") == []


def test_what_a_command_prints_is_matched_with_its_cuts():
    assert docs_tutorial.matches(["batch brief: .../brief.md"], ["batch brief: /tmp/x/brief.md"])
    assert docs_tutorial.matches(["batch-1 merged", "..."], ["batch-1 merged", "- cost: $0.00", "- wall time: 1 s"])
    assert not docs_tutorial.matches(["batch-1 merged"], ["batch-1 merged", "more"])
    assert not docs_tutorial.matches(["declared the job keep-notes"], ["declared the job find-notes"])


def test_a_command_runs_this_repository_s_shop_and_nothing_but_shop_and_git():
    assert docs_tutorial.argv("shop spec check")[1:] == [str(REPO / "scripts" / "shop"), "spec", "check"]
    assert docs_tutorial.argv("git add -A") == ["git", "add", "-A"]
    with pytest.raises(AssertionError):
        docs_tutorial.argv("rm -rf spec")


def test_a_command_that_prints_otherwise_stops_the_walk(tmp_path, env):
    page = "```console\n$ git init -q -b main\n$ git status --short\nnothing at all\n```\n"
    with pytest.raises(AssertionError, match="git status --short"):
        docs_tutorial.walk("x.md", page, tmp_path, env)
