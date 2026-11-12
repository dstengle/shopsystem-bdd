"""A batch repository's state built once per xdist worker and copied into each test that asks for it (b265): the
batch tests' published and merged batches took seconds of `work batch` runs per test. `templated(repo, key, build)`
runs `build(repo, outside)` once for each `key` and committed tree of `repo`, on a copy of `repo` and of its outside
directory (its bare `origin`, the stand-in gh's files) under the session's temporary directory, and then copies that
state over the test's own `repo` and outside: the origin's URL set back to the test's bare repository, each
worktree's links repaired and the batch brief's paths written as the copy's, so every path a test reads is its own.
The template is never a test's: a test changes only its copy. Standard library only, but `FACTORY`, which
tests/scripts/conftest.py sets to the session's `tmp_path_factory`."""
import os
import shutil
import subprocess
from pathlib import Path

FACTORY = None      # the session's tmp_path_factory (tests/scripts/conftest.py's batch_templates fixture)
GH = ("SHOPSYSTEM_WORK_GH", "STUB_GH_CALLS", "STUB_GH_STATE")
_built = {}


def _git(repo, *args):
    return subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True, check=True).stdout


def outside():
    """The test's outside directory: where `$SHOPSYSTEM_WORK_GH` (batch_testing.gh_env) is."""
    return Path(os.environ["SHOPSYSTEM_WORK_GH"]).parent


def _replace(source, target, keep=()):
    """`target`'s entries (but `keep`) replaced by `source`'s, symlinks kept as links."""
    for entry in list(target.iterdir()):
        if entry.name in keep:
            continue
        if entry.is_dir() and not entry.is_symlink():
            shutil.rmtree(entry)
        else:
            entry.unlink()
    for entry in source.iterdir():
        if entry.name in keep:
            continue
        if entry.is_dir() and not entry.is_symlink():
            shutil.copytree(entry, target / entry.name, symlinks=True)
        else:
            shutil.copy2(entry, target / entry.name, follow_symlinks=False)


def _relink(repo, where):
    """`repo`'s origin set to `where`'s bare repository and its worktrees' links repaired after a copy."""
    _git(repo, "remote", "set-url", "origin", str(where / "origin.git"))
    trees = [str(p.parent) for p in Path(repo).rglob(".git") if p.is_file()]
    if trees:
        _git(repo, "worktree", "repair", *trees)


def _repath(repo, built, built_out, where):
    """The template's paths in the files a batch command wrote beside its worktrees (the batch brief of
    `batch-<n>-driver/`, never committed) written as the copy's."""
    trees = Path(repo) / ".shop" / "worktrees"
    for folder in trees.iterdir() if trees.is_dir() else ():
        if (folder / ".git").exists():
            continue
        for path in folder.rglob("*.md"):
            text = path.read_text()
            if str(built_out) in text or str(built) in text:
                path.write_text(text.replace(str(built_out), str(where)).replace(str(built), str(repo)))


def _copy(repo, where, into):
    """A copy of `repo` and its outside `where` under `into`, its origin the copy's bare repository."""
    shutil.copytree(repo, into / "repo", symlinks=True)
    shutil.copytree(where, into / "outside", symlinks=True)
    _relink(into / "repo", into / "outside")
    return into / "repo", into / "outside"


def templated(repo, key, build):
    """`build(repo, outside)`'s result, its state built once a worker for `key` and `repo`'s committed tree (its
    working tree clean) and copied over `repo` and its outside directory."""
    repo, where = Path(repo), outside()
    assert _git(repo, "status", "--porcelain") == "", "a template is taken of a committed state only"
    ident = (key, _git(repo, "rev-parse", "HEAD^{tree}").strip())
    if ident not in _built:
        built, built_out = _copy(repo, where, FACTORY.mktemp("template"))
        saved = {name: os.environ[name] for name in GH}
        os.environ.update({name: str(built_out / Path(saved[name]).name) for name in GH})
        try:
            result = build(built, built_out)
        finally:
            os.environ.update(saved)
        _built[ident] = (built, built_out, result)
    built, built_out, result = _built[ident]
    _replace(built, repo)
    _replace(built_out, where, keep=("gh",))
    _relink(repo, where)
    _repath(repo, built, built_out, where)
    return result
