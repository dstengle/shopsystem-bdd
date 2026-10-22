"""Probe: `work show` and `work show --json` against the worktree's own scripts/work, in scratch-only repositories."""
import pathlib
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
WORKTREE = HERE.parents[2]
WORK = WORKTREE / "scripts" / "work"
INDEX = "---\nid: bounded-context/ex.com/prod/ctx\n---\n# ctx\n"


def item(name, status, kind="work-item"):
    return "---\nid: work-item/ex.com/prod/ctx/%s\nkind: %s\npart_of: initiative/i1\nstatus: %s\n---\n\n# %s\n" % (
        name, kind, status, name)


def repo(name, files):
    root = HERE / name
    shutil.rmtree(root, ignore_errors=True)
    (root / "spec").mkdir(parents=True)
    (root / "spec" / "index.md").write_text(INDEX)
    for rel, text in files.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(text)
    return root


def run(root, *args):
    done = subprocess.run([sys.executable, str(WORK), "--root", str(root), *args], capture_output=True, text=True)
    print("\n$ work --root %s %s  -> exit %d" % (root.name, " ".join(args), done.returncode))
    print("stdout=%r" % done.stdout)
    print("stderr=%r" % done.stderr[-300:])
    return done


def test_scenario_givens():
    root = repo("repo_givens", {
        ".shop/work/i1/w1.md": item("w1", "drafted"),
        ".shop/work/i1/w2.md": item("w2", "ready"),
        ".shop/work/i2/w3.md": item("w3", "claimed"),
        ".shop/work/i2/p1.md": item("p1", "merged", "capability-proposal"),
    })
    run(root, "show")
    run(root, "show", "--json")


def test_nearest_cases():
    root = repo("repo_empty", {})
    run(root, "show")
    run(root, "show", "--json")
    root = repo("repo_no_status", {".shop/work/i1/w1.md": "---\nid: work-item/ex.com/prod/ctx/w1\nkind: work-item\n---\n# w1\n"})
    run(root, "show")
    root = repo("repo_no_frontmatter", {".shop/work/i1/w1.md": "# w1\n\nstatus: drafted\n",
                                       ".shop/work/i1/log.jsonl": "{\"work-item\": \"w1\", \"after\": \"drafted\"}\n"})
    run(root, "show")
    root = repo("repo_quote", {".shop/work/i1/w1.md": item("w1", "drafted").replace("# w1", "# w1 \"quoted\" \\ tab\there")})
    run(root, "show", "--json")
    root = repo("repo_bad_utf8", {".shop/work/i1/w1.md": item("w1", "drafted")})
    (root / ".shop/work/i1/w2.md").write_bytes(b"\xff\xfe---\nkind: work-item\n---\n")
    run(root, "show", "--json")
