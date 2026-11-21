"""upgrades' founding of a bounded context (b318, `migrate init`), read by migration_tools_handlers_thens: the context
scaffold `migrate init` kept in the scenario's repository, in one commit on the given one (its ignore file in it only
when it changed one, b470), the repository's other files left as they were, in which `spec check` finds nothing and
`features generate` writes nothing (`scaffolded`); the ignore file it kept, the repository's own lines first, each
ignored name once as git matches lines (`ignored`, b454, b470); the context purpose it was founded with under the
index file's `## Purpose`, in its one commit (`purposed`, b464); and what each refusal names (`NAMED`)."""
import json
import subprocess
import sys

from scenarios import migration_tools_handlers as M
from scenarios.migration_old import CONTEXT

FILES = ("spec/index.md", "spec/universal.md", "spec/model/.gitkeep", "spec/vocabulary/.gitkeep",
         "spec/capabilities/.gitkeep", ".shop/backlog/.gitkeep", ".shop/records/README.md", ".shop/plugin-version",
         ".shop/delivery.toml", "features/.gitkeep", "tests/scenarios/conftest.py")
# what the ignore file names: the interpreter and the caches (b454)
IGNORED = (".venv/", "__pycache__/", ".pytest_cache/", ".ruff_cache/")
# what a refusal of `migrate init` names: the option of the context id it lacks, the id it was given, the index file,
# the shop directory
NAMED = {"bounded context": "--id", "context id": "not-a-context-id", "index file": "spec/index.md",
         "shop directory": ".shop"}


def tool(step, *args):
    return subprocess.run([sys.executable, str(M.PLUGIN / "scripts" / args[0]), *args[1:]], cwd=step.repo,
                          capture_output=True, text=True)


def scaffolded(step):
    done = step.context["done"]
    assert done.returncode == 0, M.said(step)
    old = step.context["old"]
    assert len(old.git("log", "--oneline").stdout.splitlines()) == step.context["commits"] + 1
    kept = set(old.git("show", "--name-only", "--format=", "HEAD").stdout.split()) - {".gitignore"}
    assert sorted(kept) == sorted(FILES), kept
    assert old.git("status", "--porcelain").stdout == "", old.git("status", "--porcelain").stdout
    index = M.read(step, "spec/index.md")
    for line in ("id: bounded-context/%s\n" % CONTEXT, "title: shop\n", "language: codified-2\n", "imports: [request]\n"):
        assert line in index, (line, index)
    assert "language: codified-2\n" in M.read(step, "spec/universal.md")
    assert M.read(step, ".shop/plugin-version").strip() == M.ours(step)[1]
    for rel, text in M.held(step).items():      # the repository's own files left as they were
        assert rel == ".gitignore" or M.read(step, rel) == text, rel
    checked = tool(step, "spec", "check", "--json")
    report = json.loads(checked.stdout)["content"]
    assert (report["violations"], report["unresolved"], report["problems"]) == ([], [], []), checked.stdout
    generated = tool(step, "features", "generate")
    assert generated.returncode == 0 and old.git("status", "--porcelain").stdout == "", generated.stdout


def ignored(step):
    """The ignore file `migrate init` kept in its one commit, naming the interpreter and the caches."""
    assert step.context["done"].returncode == 0, M.said(step)
    old = step.context["old"]
    assert ".gitignore" in old.git("show", "--name-only", "--format=", "HEAD").stdout.split()
    text = M.read(step, ".gitignore")
    assert text.startswith(M.held(step).get(".gitignore", "")), text
    names = [line.strip().rstrip("/") for line in text.splitlines()]
    assert all(names.count(name.rstrip("/")) == 1 for name in IGNORED), names


def purposed(step):
    """The index file `migrate init` kept in its one commit holds the context purpose under its `## Purpose`."""
    assert step.context["done"].returncode == 0, M.said(step)
    assert "spec/index.md" in step.context["old"].git("show", "--name-only", "--format=", "HEAD").stdout.split()
    index = M.read(step, "spec/index.md")
    assert "\n## Purpose\n\n%s\n\n## Composition\n" % M.PURPOSE in index, index
