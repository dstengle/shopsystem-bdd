"""supervision r156: a commit belongs to a work-item of the initiative or to none; a capability-proposal's transition
commit names no work-item; so does a proposal's `work answer:`; a `work answer`, `work withdraw`, `work retry` or
`work add` commit belongs to the work-item it names."""
import pathlib
import subprocess
import sys

SCRIPTS = pathlib.Path(__file__).resolve().parents[2] / "scripts"
sys.path.insert(0, str(SCRIPTS))
from supervise_review_read import ReviewRead


def git(repo, *args):
    return subprocess.run(["git", "-c", "user.name=T", "-c", "user.email=t@example.com", *args], cwd=repo,
                          capture_output=True, text=True, check=True).stdout


class Stand(ReviewRead):
    def __init__(self, root):
        self.root, self.dir = root, root / ".shop/work/i1"

    def items(self):
        return [("w1", "claimed")]


def test_a_proposals_transition_commit_belongs_to_no_work_item(tmp_path):
    git(tmp_path, "init", "-q")
    git(tmp_path, "commit", "-q", "--allow-empty", "-m", "base")
    base = git(tmp_path, "rev-parse", "HEAD").strip()
    git(tmp_path, "commit", "-q", "--allow-empty", "-m", "work: supervision approved -> awaiting-answer")
    git(tmp_path, "commit", "-q", "--allow-empty", "-m", "work: w1 ready -> claimed")
    head = git(tmp_path, "rev-parse", "HEAD").strip()
    lines = [line.split() for line in Stand(tmp_path).commits_text(base, head).splitlines() if line.startswith("    ")]
    assert [line[1] for line in lines] == ["none", "w1"], lines


def owners(tmp_path, subject):
    git(tmp_path, "init", "-q")
    git(tmp_path, "commit", "-q", "--allow-empty", "-m", "base")
    base = git(tmp_path, "rev-parse", "HEAD").strip()
    git(tmp_path, "commit", "-q", "--allow-empty", "-m", subject)
    head = git(tmp_path, "rev-parse", "HEAD").strip()
    return [line.split()[1] for line in Stand(tmp_path).commits_text(base, head).splitlines() if line.startswith("    ")]


def test_a_commit_of_work_answer_withdraw_retry_or_add_belongs_to_the_work_item_it_names(tmp_path):
    subjects = ["work answer: w1 awaiting-answer -> ready", "work withdraw: w1 ready -> withdrawn",
                "work retry: w1 failed -> ready", "work add: i1/w1 drafted"]
    for number, subject in enumerate(subjects):
        (tmp_path / str(number)).mkdir()
        assert owners(tmp_path / str(number), subject) == ["w1"], subject


def test_a_proposals_answer_commit_belongs_to_no_work_item(tmp_path):
    assert owners(tmp_path, "work answer: supervision") == ["none"]
