"""What the tutorial's end-to-end test reads and runs (b868): docs/tutorial.md walked in order, each step of it a
command of a ```console block, a file the page shows whole or the person's merge, and each run in a folder of its own.

A `$ ` line of a ```console block is a command, its argument quoted over several lines when a quote is left open (a
model's lines); the lines under it, to the next `$ `, are what it prints, a `...` standing for any text within a line
and a line of `...` alone for any lines. A block after the comment `<!-- tutorial: file <path> -->` is that file whole,
written at the path (relative to the folder). The comment `<!-- tutorial: merge <batch> -->` is the person's merge of
the batch's pull request on GitHub: the batch's branch merged into main and pushed, and the stand-in gh told the pull
request is merged at that commit. Other comments may stand between a marker and its block, as `<!-- docs: context
... -->` does."""
import json
import re
import shlex
import subprocess
import sys
from pathlib import Path

from docs_testing import FENCE, REPO

FILE = re.compile(r"^<!--\s*tutorial:\s*file\s+(\S+)\s*-->$")
MERGE = re.compile(r"^<!--\s*tutorial:\s*merge\s+(\S+)\s*-->$")
PULL = re.compile(r"https://github\.com/\S+/pull/\d+")
TOOLS = ("shop", "git")


def steps(text):
    """[(kind, page line, what)] of a page in order: ("run", n, (command, shown lines)), ("file", n, (path, text)) and
    ("merge", n, batch)."""
    out, open_, path = [], None, None
    for n, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        m = FENCE.match(s)
        if open_ is None and m:
            open_ = (m.group(1), m.group(2), [], n, path)
            path = None
        elif open_ is not None and s.startswith(open_[0]) and not s.strip(open_[0][0]):
            _, lang, body, at, file = open_
            open_ = None
            if file:
                out.append(("file", at, (file, "\n".join(body) + "\n")))
            elif lang == "console":
                out += [("run", at, run) for run in commands(body)]
        elif open_ is not None:
            open_[2].append(line)
        elif FILE.match(s):
            path = FILE.match(s).group(1)
        elif MERGE.match(s):
            out.append(("merge", n, MERGE.match(s).group(1)))
        elif s and not s.startswith("<!--"):
            path = None
    return out


def commands(body):
    """[(command, shown output lines)] of a console block, a command's quote left open joined with the lines after
    it."""
    out, i = [], 0
    while i < len(body):
        row = body[i].strip()
        i += 1
        if not row.startswith("$ "):
            continue
        command = row[2:]
        while not _closed(command) and i < len(body):
            command += "\n" + body[i]
            i += 1
        shown = []
        while i < len(body) and not body[i].strip().startswith("$ "):
            shown.append(body[i].rstrip())
            i += 1
        out.append((command, [s for s in shown if s.strip()]))
    return out


def _closed(command):
    try:
        shlex.split(command)
    except ValueError:
        return False
    return True


def argv(command):
    """The process a command of the page runs: `shop ...` as this repository's scripts/shop, `git ...` as git."""
    words = shlex.split(command)
    if words[0] not in TOOLS:
        raise AssertionError("the tutorial runs only shop and git, not: %s" % command)
    return [sys.executable, str(REPO / "scripts" / "shop"), *words[1:]] if words[0] == "shop" else words


def _line(shown, got):
    pattern = ".*".join(re.escape(part) for part in shown.strip().split("..."))
    return re.fullmatch(pattern, got.strip()) is not None


def matches(shown, got):
    """Whether the lines a command printed are the ones the page shows, `...` standing for any text in a line and a
    line of `...` alone for any lines."""
    if not shown:
        return not got
    if shown[0].strip() == "...":
        return any(matches(shown[1:], got[k:]) for k in range(len(got) + 1))
    return bool(got) and _line(shown[0], got[0]) and matches(shown[1:], got[1:])


def run(folder, command, env):
    done = subprocess.run(argv(command), cwd=folder, env=env, capture_output=True, text=True, timeout=900)
    return done.returncode, [x for x in (done.stdout + done.stderr).splitlines() if x.strip()]


def merge(folder, batch, pull, env):
    """The person's merge of the batch's pull request: its branch merged into main and pushed, and the stand-in gh's
    state saying the pull request is merged at that commit."""
    for command in (["git", "merge", "-q", "--no-ff", batch, "-m", "Merge pull request: " + batch],
                    ["git", "push", "-q", "origin", "main"]):
        subprocess.run(command, cwd=folder, env=env, check=True, capture_output=True, text=True)
    oid = subprocess.run(["git", "rev-parse", "HEAD"], cwd=folder, env=env, check=True, capture_output=True,
                         text=True).stdout.strip()
    Path(env["STUB_GH_STATE"]).write_text(json.dumps({pull: {"state": "MERGED", "mergeCommit": {"oid": oid}}}))


def walk(page, text, folder, env):
    """Every step of the page done in order in `folder`; stops at the first command that fails or prints other than
    the page shows, naming it."""
    pull = None
    for kind, n, what in steps(text):
        where = "%s:%d" % (page, n)
        if kind == "file":
            target = folder / what[0]
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(what[1], encoding="utf-8")
        elif kind == "merge":
            assert pull, "%s: a merge before any pull request was opened" % where
            merge(folder, what, pull, env)
        else:
            command, shown = what
            code, got = run(folder, command, env)
            assert code == 0 and matches(shown, got), "%s: $ %s\nexited %d, printed:\n%s\n--- the page shows:\n%s" % (
                where, command, code, "\n".join(got), "\n".join(shown))
            pull = next((m.group(0) for x in got for m in [PULL.search(x)] if m), pull)


def files(root, *parts):
    """{path relative to root: text} of the files under root/<part> (a file itself when it is one), the `.gitkeep`
    placeholders `migrate init` writes in an empty folder aside."""
    out = {}
    for part in parts:
        top = root / part
        for p in ([top] if top.is_file() else sorted(top.rglob("*")) if top.is_dir() else []):
            if p.is_file() and p.name != ".gitkeep":
                out[str(p.relative_to(root))] = p.read_text(encoding="utf-8")
    return out
