"""Two more probes of answers under a delegation: a question with no log line of its move (the answer is written, then
work run refuses), and the next run after the two-question fault. Uses probe_delegation's setup, run and report."""
from probe_delegation import DELEGATION, report, run, setup
from tests.scenarios.supervision_delegation_steps import fulfils_with_delegation
from tests.scenarios.supervision_rounds_steps import DIR
from tests.scenarios.supervision_world import commit_all, git, item_text, write


def test_no_log_line_for_the_question():
    repo, plan = setup("no_log")
    git(repo, "rm", "-q", "--", DIR + "/log.jsonl")
    commit_all(repo, "no log of the move")
    fulfils_with_delegation(repo, {}, DELEGATION)
    write(repo, DIR + "/w1.md", item_text("w1", "awaiting-answer") + "\n## Questions\n- Does scripts/log.py own the log?\n")
    commit_all(repo, "w1 awaiting")
    report("no log line of the move to awaiting-answer", repo, run(repo, plan))
    print("STATUS-AFTER-FIRST", repr(git(repo, "status", "--porcelain").strip()))
    report("second run after that", repo, run(repo, plan))


def test_two_questions_second_run():
    repo, plan = setup("two_second")
    fulfils_with_delegation(repo, {}, DELEGATION)
    write(repo, DIR + "/w1.md", item_text("w1", "awaiting-answer") + "\n## Questions\n- Does scripts/log.py own the log?\n"
          "- Does scripts/queue.py own the queue?\n")
    commit_all(repo, "w1 awaiting, two questions")
    run(repo, plan)
    report("two questions, second run", repo, run(repo, plan))
