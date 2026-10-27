"""requests r32 and design-model-check r120 with a context id of several parts, as real repositories have: `work request`
raises as this repository under each spelling the rest of `work` reads as its own (`internal`, the bounded-context id),
and a request raised for a bare q<n> names it by the full id model check reads."""
import pathlib
import re
import subprocess
import sys

import pytest

SCRIPTS = pathlib.Path(__file__).resolve().parents[2] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import workqueue
import workqueue_request

CONTEXT = "ex.com/prod/ctx"
INDEX = "---\nid: bounded-context/%s\nkind: bounded-context\n---\n\n# ctx\n" % CONTEXT
LINE = "**When** `work list` is run, `work` shall print each request with its status.\n"


def git(repo, *args):
    return subprocess.run(["git", "-c", "user.name=T", "-c", "user.email=t@example.com", *args], cwd=repo,
                          capture_output=True, text=True, check=True).stdout


@pytest.fixture
def repo(tmp_path):
    (tmp_path / "spec").mkdir()
    (tmp_path / "spec/index.md").write_text(INDEX)
    (tmp_path / "lines.md").write_text(LINE)
    git(tmp_path, "init", "-q")
    git(tmp_path, "config", "user.name", "T")
    git(tmp_path, "config", "user.email", "t@example.com")
    git(tmp_path, "add", "-A")
    git(tmp_path, "commit", "-q", "-m", "init")
    return tmp_path


@pytest.mark.parametrize("asker", ["internal", "bounded-context/" + CONTEXT, CONTEXT, "ctx"])
def test_this_repository_raises_under_each_spelling_of_its_own_asker(repo, asker):
    workqueue_request.gate(repo, asker, ["observation/o1"], None, None)


def test_another_asker_is_refused_naming_it(repo):
    with pytest.raises(workqueue.Refused, match="bounded-context/ex.com/prod/other"):
        workqueue_request.gate(repo, "bounded-context/ex.com/prod/other", ["observation/o1"], None, None)


def test_a_bare_raised_for_is_written_as_the_full_request_id(repo):
    name = workqueue_request.request(repo, "t", "internal", str(repo / "lines.md"), ["observation/o1"], None,
                                     raised_for="q7")
    text = (repo / ".shop/work/requests" / (name + ".md")).read_text()
    assert re.search(r"(?m)^raised_for: request/%s/q7$" % re.escape(CONTEXT), text), text


def test_a_full_raised_for_is_written_as_given(repo):
    full = "request/ex.com/prod/app/q3"
    name = workqueue_request.request(repo, "t", "internal", str(repo / "lines.md"), ["observation/o1"], None,
                                     raised_for=full)
    assert "\nraised_for: %s\n" % full in (repo / ".shop/work/requests" / (name + ".md")).read_text()
