"""features/work-queue.feature's steps of `work status` (r16-r18): the repository, branch, remote and ledger it is read
from, and what the output must hold."""
import re
import shlex

from pytest_bdd import given, parsers, then

from .conftest import full
from .work_queue_git_steps import git

NOTES = ["next: plan w1", "planned w1"] + ["filler note %d" % n for n in range(3, 11)] + ["next: answer w2", "w1 ready"]


@given(parsers.parse("an initiative {ident} under .shop/work/ that is {state}, whose capability-proposal "
                     "{proposal} is {pstatus}"))
def open_with_proposal(repo, ident, state, proposal, pstatus):
    from .test_work_queue import initiative, item_text, write
    initiative(repo, ident)
    write(repo, ".shop/work/%s/%s.md" % (ident, proposal), item_text(proposal, pstatus, ident, "capability-proposal"))


@given(parsers.re(r"an initiative (?P<ident>\w+) under \.shop/work/ that is (?P<state>[^,]+), whose work-items? (?P<items>.+)$"))
def with_state(repo, ident, state, items):
    from .test_work_queue import item_text, write
    text = "---\nid: %s\nkind: initiative\nstatus: %s\n---\n" % (full("initiative", ident), state.replace("neither done nor abandoned", "started"))
    from .test_work_queue import initiative
    initiative(repo, ident)
    write(repo, ".shop/work/%s/initiative.md" % ident, text)
    for item, state_of, question in re.findall(r'(\w+) is ([\w-]+)(?: with the question "([^"]*)" not yet answered)?', items):
        write(repo, ".shop/work/%s/%s.md" % (ident, item), item_text(item, state_of, ident)
              + ("\n## Questions\n- %s\n" % question if question else ""))


@given(parsers.parse('i1\'s work-item w1 is ready, and its work-item w2 is awaiting-answer with the question "{question}" '
                     'not yet answered'))
def w1_and_w2(repo, question):
    from .test_work_queue import item_text, write
    write(repo, ".shop/work/i1/w1.md", item_text("w1", "ready"))
    write(repo, ".shop/work/i1/w2.md", item_text("w2", "awaiting-answer") + "\n## Questions\n- %s\n" % question)


@given("the repository is a git repository whose initiative branch i1-delivery has one commit the remote does not have")
def branch_ahead_of_remote(repo):
    from .work_queue_git_steps import init
    init(repo)
    remote = repo.parent / (repo.name + "-remote.git")
    git(repo, "init", "-q", "--bare", str(remote))
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "the repository as the scenario gives it")
    git(repo, "checkout", "-q", "-b", "i1-delivery")
    git(repo, "remote", "add", "origin", str(remote))
    git(repo, "push", "-q", "origin", "i1-delivery")
    (repo / "delivered.txt").write_text("one commit more\n")
    git(repo, "add", "delivered.txt")
    git(repo, "commit", "-q", "-m", "a commit the remote does not have")


@given("the tracked file spec/index.md has uncommitted changes")
def index_changed(repo):
    with (repo / "spec/index.md").open("a") as f:
        f.write("an uncommitted line\n")


@given("notes.txt is untracked and git does not ignore it")
def notes_untracked(repo):
    (repo / "notes.txt").write_text("a note\n")


@given("scratch.log is untracked and git ignores it")
def scratch_ignored(repo):
    (repo / ".git/info/exclude").write_text("scratch.log\n")
    (repo / "scratch.log").write_text("noise\n")


@given(parsers.parse(".shop/work/i1/ledger.md has twelve lines, each written by `work note` with its date, whose notes are "
                     "in turn {notes}"))
def ledger_of_twelve(repo, notes):
    lines = "".join("- 2026-10-%02d: %s\n" % (n + 1, note) for n, note in enumerate(NOTES))
    (repo / ".shop/work/i1/ledger.md").write_text(lines)


def lines_of(context):
    assert context["done"].returncode == 0, context["done"]
    return context["done"].stdout.splitlines()


def has_line(lines, *words):
    return [l for l in lines if all(w in l.split() for w in words)]


@then("work prints i1's status")
def prints_initiative_status(context):
    assert has_line(lines_of(context), "i1", "started"), context["done"].stdout


@then(parsers.parse('it prints p1 with approved, w1 with ready and w2 with awaiting-answer and the question "{question}"'))
def prints_items(context, question):
    lines = lines_of(context)
    for name, status in (("p1", "approved"), ("w1", "ready"), ("w2", "awaiting-answer")):
        assert has_line(lines, name, status), (name, lines)
    assert [l for l in lines if question in l], lines


@then("it prints i1-delivery and that the remote does not have every commit of it")
def prints_branch(context):
    lines = [l for l in lines_of(context) if "i1-delivery" in l]
    assert lines and "the remote does not have every commit" in lines[0], context["done"].stdout


@then("it prints spec/index.md and notes.txt, and nothing about scratch.log")
def prints_files(context):
    out = context["done"].stdout
    assert "spec/index.md" in out and "notes.txt" in out and "scratch.log" not in out, out


def ledger_lines(context):
    return lines_of(context)[lines_of(context).index("ledger:") + 1:][:10]


@then("it prints the ledger's last ten lines, the eight notes, \"next: answer w2\" and \"w1 ready\", and neither of its first two lines")
def prints_ledger(context):
    shown = ledger_lines(context)
    assert [l.strip().split(": ", 1)[1] for l in shown] == NOTES[2:], shown
    assert "next: plan w1" not in context["done"].stdout.replace("last next: ", ""), context["done"].stdout


@then("it prints the ledger's line whose note is \"next: answer w2\" as its last line whose note begins next:")
def prints_last_next(context):
    nexts = [l for l in lines_of(context) if l.startswith("last next:")]
    assert len(nexts) == 1 and nexts[0].endswith("2026-10-11: next: answer w2"), nexts


@then("it exits successfully")
def exits_successfully(context):
    assert context["done"].returncode == 0, context["done"]


@then(parsers.parse("work prints what `work status {first}` prints and what `work status {second}` prints"))
def prints_each_status(repo, run, context, first, second):
    out = lines_of(context)
    for ident in (first, second):
        one = run("work", *shlex.split("status " + ident)).stdout.splitlines()
        assert one and any(out[i:i + len(one)] == one for i in range(len(out))), (ident, one, out)


@then(parsers.parse("it prints nothing about {first} or {second}"))
def nothing_about_either(context, first, second):
    assert not has_line(lines_of(context), first) and not has_line(lines_of(context), second), context["done"].stdout


@then(parsers.parse("it gives {whose}'s status and {name} with {status}"))
def a_status_is_given(context, whose, name, status):
    ident = whose
    for found in context["json"]["initiatives"]:
        if found["initiative"] == ident:
            assert found["status"], found
            assert {"work-item": name, "status": status} in [{k: i[k] for k in ("work-item", "status")}
                                                             for i in found["work-items"]], found
            return
    raise AssertionError(context["json"])
