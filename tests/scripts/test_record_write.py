"""`work record` (design-model-check r56): the record in the form `model` reads, its row at the end of the README's
table, both committed alone; an existing path refused, changing nothing."""
import subprocess
import sys

from backlog_testing import SCRIPTS, git, state, work
from shop_files import frontmatter

README = ("# Records\n\nIntro.\n\n| path | record | kind |\n|---|---|---|\n| `old.md` | an old one | analysis |\n\n"
          "A footnote.\n")


def body(tmp_path_factory, text="What was found.\n\n## Findings\n\n- One.\n"):
    path = tmp_path_factory.mktemp("body") / "body.md"
    path.write_text(text)
    return str(path)


def record(repo, factory, *more, title="What was found"):
    return work(repo, "record", title, "--kind", "analysis", "--summary", "what was found, one row", "--body",
                body(factory), "--date", "2026-11-05", *more)


def with_readme(repo):
    (repo / ".shop/records").mkdir(parents=True)
    (repo / ".shop/records/README.md").write_text(README)
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "records")


def test_the_record_is_written_whole(backlog_repo, tmp_path_factory):
    done = record(backlog_repo, tmp_path_factory)
    assert done.returncode == 0, done.stderr
    assert done.stdout.strip() == ".shop/records/2026-11-05-what-was-found.md"
    data, text = frontmatter((backlog_repo / done.stdout.strip()).read_text())
    assert data == {"id": "record/ex.com/prod/ctx/2026-11-05-what-was-found", "kind": "analysis",
                    "about": "bounded-context/ex.com/prod/ctx", "date": "2026-11-05"}
    assert text == "# What was found\n\nWhat was found.\n\n## Findings\n\n- One.\n"


def test_a_measurement_is_named_by_its_kind(backlog_repo, tmp_path_factory):
    done = work(backlog_repo, "record", "Runs", "--kind", "measurement", "--summary", "s", "--body",
                body(tmp_path_factory), "--date", "2026-11-05", "--about", "capability/thing")
    data, _ = frontmatter((backlog_repo / done.stdout.strip()).read_text())
    assert data["id"] == "measurement/ex.com/prod/ctx/2026-11-05-runs" and data["about"] == "capability/thing"


def test_the_row_ends_the_table_and_both_are_committed(backlog_repo, tmp_path_factory):
    with_readme(backlog_repo)
    assert record(backlog_repo, tmp_path_factory).returncode == 0
    assert (backlog_repo / ".shop/records/README.md").read_text() == README.replace(
        "| analysis |\n\n", "| analysis |\n| `2026-11-05-what-was-found.md` | what was found, one row | analysis |\n\n")
    files = git(backlog_repo, "show", "--name-only", "--format=", "HEAD").split()
    assert sorted(files) == [".shop/records/2026-11-05-what-was-found.md", ".shop/records/README.md"]
    assert git(backlog_repo, "log", "-1", "--format=%s") == "work record: 2026-11-05-what-was-found\n"
    assert git(backlog_repo, "status", "--porcelain") == ""


def test_a_missing_readme_is_made_with_its_table(backlog_repo, tmp_path_factory):
    assert record(backlog_repo, tmp_path_factory).returncode == 0
    readme = (backlog_repo / ".shop/records/README.md").read_text()
    assert readme.endswith("|---|---|---|\n| `2026-11-05-what-was-found.md` | what was found, one row | analysis |\n")


def test_an_existing_path_is_refused(backlog_repo, tmp_path_factory):
    assert record(backlog_repo, tmp_path_factory).returncode == 0
    before = state(backlog_repo)
    done = record(backlog_repo, tmp_path_factory)
    assert done.returncode == 1
    assert ".shop/records/2026-11-05-what-was-found.md exists" in done.stderr and "--slug" in done.stderr
    assert state(backlog_repo) == before
    assert record(backlog_repo, tmp_path_factory, "--slug", "found-again").returncode == 0


def test_help_says_what_it_writes():
    done = subprocess.run([sys.executable, str(SCRIPTS / "work"), "record", "--help"], capture_output=True,
                          text=True)
    assert done.returncode == 0
    for word in (".shop/records/<date>-<slug>.md", ".shop/records/README.md", "--body", "commit"):
        assert word in done.stdout, word
