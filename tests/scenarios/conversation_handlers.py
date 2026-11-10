"""Handlers of features/conversation.feature (plan 8, D13): `work quote` run in the scenario's repository on a
transcript written into a store of the scenario's own (`CLAUDE_CONFIG_DIR`, never the person's), and the quote it
wrote and committed read back.

A step whose registry key another capability claims (`ThenDoes` with `write`, `commit`, `from`, `has`, `holds` and
`list`, `ThenPrints`) is taken through work_queue_world's `local` table, so it reaches these handlers only in
test_conversation.py, which binds with `bind_all`; each returns False for a step of a scenario that is not about the
conversation (every conversation When and Given sets `step.context["conversation"]`), which then goes on to the
registry. The steps are grammar 4's (b240 phase 15)."""
import datetime
import importlib.util
import json
import os
import re
import sys
from pathlib import Path

import batch_plan
import conversation_prompt
import conversation_quote
import measure_batch_read
from vocab import handler


def shared(name, path):
    """A module loaded once by path, the one the other handler modules load under the same name."""
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, path)
        sys.modules[name] = module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    return sys.modules[name]


HERE = Path(__file__).resolve().parent
W = shared("shop_work_queue_world", HERE / "work_queue_world.py")
B = shared("shop_backlog_world", HERE / "backlog_world.py")
T = shared("shop_transcript_testing", HERE.parent / "scripts" / "transcript_testing.py")
local = W.local

CITED = 2   # the person's message m1 of the transcript: the third of CONVERSATION's six


def talk(step):
    """What the scenario keeps of the conversation: sessions, messages and quotes by the scenario's names."""
    return step.context.setdefault("conversation", {"sessions": {}, "messages": {}, "quotes": {}})


def store(step):
    if "outside" not in step.context:
        step.context["outside"] = step.request.getfixturevalue("tmp_path_factory").mktemp("outside")
    return step.context["outside"] / "store"


def env(step):
    return dict(os.environ, CLAUDE_CONFIG_DIR=str(store(step)))


def transcript(step, session):
    """CONVERSATION written as the transcript of the scenario's session `session`, in the repository's project
    directory of the scenario's store; the person's message m1 is the one its words come from."""
    ident = "session-%s" % session
    rows = [dict(row, sessionId=ident) for row in T.CONVERSATION]
    path = T.write(store(step) / "projects" / measure_batch_read.project_dir(step.repo).name, ident, rows)
    talk(step)["sessions"][session] = ident
    talk(step)["messages"].setdefault("m1", T.IDENTS[CITED])
    return path


def words():
    return T.TEXTS[CITED]


@handler("WhenRuns", "`work quote`")
def work_quote(step):
    """`work quote` on the words of the session's message m1; with the `--hook` option, the prompt hook."""
    if any(o.strip("`") == "--hook" for o, _ in getattr(step, "options", None) or ()):
        return prompt_hook(step)
    transcript(step, step.names[0])
    B.run_work(step, "quote", words(), "--session", talk(step)["sessions"][step.names[0]], env=env(step))


def quote_file(step, name):
    return step.repo / talk(step)["quotes"][name]


def written_quote(step, name):
    """The quote the last run wrote, bound to `name` at the first step that names it."""
    if name not in talk(step)["quotes"]:
        done = step.context["result"]
        assert done.returncode == 0, done.stderr
        files = [rel for rel in B.changed(step) if re.fullmatch(r"\.shop/quotes/[1-9]\d*\.md", rel)]
        assert len(files) == 1, (step.text, B.changed(step))
        talk(step)["quotes"][name] = files[0]
    rel = talk(step)["quotes"][name]
    return conversation_quote.parse((step.repo / rel).read_text(), rel)


@local("ThenDoes")
def quote_does(step):
    """`work` writes (commits) the quote q1; the quote q1 is from the session s1, cites the message m1."""
    if not step.context.get("conversation") or not step.text.startswith(("`work` writes the quote ",
                                                                         "`work` commits the quote ", "the quote ")):
        return False
    if step.term == "write":
        return written_quote(step, step.names[0]) and None
    if step.term == "commit":
        return B.in_commits(step, talk(step)["quotes"][step.names[0]])
    quote, other = step.names
    found = written_quote(step, quote)
    if step.term == "from":
        assert found.session == talk(step)["sessions"][other], (step.text, found.session)
        return None
    assert step.term == "cite", step.text
    wanted = talk(step)["messages"][other]
    assert found.message == wanted, (step.text, found.message)
    heading = next(line for line in quote_file(step, quote).read_text().splitlines()
                   if line.startswith("### ") and ", %s" % wanted in line)
    assert heading.endswith(", cited"), (step.text, heading)
    return None


@handler("ThenDoes", "cite")
def quote_cites(step):
    """`the quote q1 cites the message m1`: the registry's key, which no other capability claims."""
    assert quote_does(step) is not False, "no quote in this scenario: %s" % step.text


def hook(step, event, sub, stdin):
    """Run the command hooks/hooks.json gives for `event` and `sub` (D13) in the scenario's repository, committed
    first, with the hook's stdin JSON."""
    argv = T.hook_command(event, sub)
    script = Path(argv[1])
    assert argv[0] == "python3" and script.parent == HERE.parents[1] / "scripts", argv
    B.index(step)
    if not (step.repo / ".shop").is_dir():
        (step.repo / ".shop").mkdir(parents=True)
        (step.repo / ".shop" / "README.md").write_text("The repository's .shop/.\n")
    step.context["head"] = W.init(step.repo)
    step.context["result"] = step.run(script.name, *argv[2:], input=json.dumps(stdin), env=env(step))
    return step.context["result"]


def prompt_hook(step):
    """The UserPromptSubmit hook on a prompt of the scenario's session s1, whose transcript is written first."""
    path = transcript(step, "s1")
    talk(step)["transcripts"] = {"s1": str(path)}
    hook(step, "UserPromptSubmit", "quote", {"session_id": talk(step)["sessions"]["s1"], "transcript_path": str(path),
                                             "hook_event_name": "UserPromptSubmit", "prompt": "x"})


@local("ThenDoes")
def hook_file(step):
    """After the prompt hook: this git directory holds the file f1 (its pointer, `<git dir>/shopsystem/`), this
    session has the transcript t1, the file f1 lists the transcript t1 (and so the session), `work` writes the file
    f1 and commits nothing."""
    if not step.context.get("conversation") or "transcripts" not in talk(step):
        return False
    done = step.context["result"]
    assert (done.returncode, done.stdout) == (0, ""), (step.text, done.stdout, done.stderr)
    if step.term == "has":
        return None
    if step.term == "holds":
        gitdir = Path(W.git(step.repo, "rev-parse", "--absolute-git-dir").strip())
        assert any((gitdir / "shopsystem").glob("*.json")), step.text
        return None
    wanted = (talk(step)["sessions"]["s1"], talk(step)["transcripts"]["s1"])
    assert conversation_prompt.kept(step.repo) == wanted, (step.text, conversation_prompt.kept(step.repo))
    assert W.git(step.repo, "status", "--porcelain") == "", step.text
    return None


@handler("GivenK", "message")
def given_message(step):
    """A message of the person, kept by the scenario until a quote cites it."""
    name = step.names[0]
    talk(step)["messages"][name] = "message-%s" % name
    talk(step).setdefault("texts", {})[name] = "The words of the person in %s, to be kept." % name


@handler("GivenDoes", "cite")
def given_cites(step):
    """`the quote q1 cites the message m1`: the quote's file, written with conversation_quote.render, its first cited
    message the one it is cited for, after one message of the session, and each other it cites after it; committed."""
    quote, message = step.names
    cites = talk(step).setdefault("cites", {}).setdefault(quote, [])
    cites.append(message)
    name = "quote-1"
    at = datetime.datetime.fromisoformat(T.at(3))
    said = [conversation_quote.C.Message(talk(step)["messages"][m], "person", at + datetime.timedelta(minutes=k),
                                         talk(step)["texts"][m]) for k, m in enumerate(cites)]
    before = conversation_quote.C.Message("a0", "session", at - datetime.timedelta(minutes=1), "Asked before.")
    found = conversation_quote.Quote(name, "quote/ex.com/prod/ctx/%s" % name, "session-s1", said[0].ident,
                                     "2026-11-05", said[0].text, [before, *said])
    rel = conversation_quote.rel_of(name)
    path = step.repo / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(conversation_quote.render(found))
    talk(step)["quotes"][quote] = rel
    B.index(step)
    step.context["head"] = W.init(step.repo)


@local("WhenRuns")
def show_quote(step):
    if not step.context.get("conversation") or step.term != "`work show`" or step.names[0] not in talk(step)["quotes"]:
        return False
    rel = talk(step)["quotes"][step.names[0]]
    B.run_work(step, "show", "quote-%s" % Path(rel).stem)
    return None


@local("GivenDoes")
def item_has_title(step):
    """`the item i3 has the title t1`: the title `work names` gives the item."""
    if not step.context.get("conversation") or step.term != "has" or " has the title " not in step.text:
        return False
    talk(step).setdefault("titles", {})[step.names[1]] = step.names[0]
    return None


@local("GivenK", "title")
def given_title(step):
    talk(step).setdefault("titles", {})


@handler("WhenRuns", "`work names`")
def names_hook(step):
    """The SessionStart hook in a repository of one item for each item the scenario's Thens name (`i1`, titled `Fix
    the parser`, shaped) and one batch for each batch they name, its one task for the first item."""
    talk(step)
    texts = W.scenario_texts(step)
    items = sorted({n for t in texts for n in re.findall(r"\bthe item (i\d+)\b", t)})
    for name in items:
        B.write_item(step, name, title="Fix the parser" if name == "i1" else "Title of %s" % name, status="shaped")
    for name in sorted({n for t in texts for n in re.findall(r"\bthe batch ([a-z]+\d+)\b", t)}):
        number = int(re.sub(r"^\D+", "", name))
        task = batch_plan.Task("t1", B.ident(items[0]), "pending", "batch-%d-%s" % (number, B.ident(items[0])))
        found = batch_plan.Batch("batch-%d" % number, "batch/ex.com/prod/ctx/batch-%d" % number, "building", "main",
                                 "0" * 40, "batch-%d" % number, None, [task])
        path = step.repo / batch_plan.rel_of(found.name)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(batch_plan.render(found))
        talk(step).setdefault("batches", {})[name] = found.name
    hook(step, "SessionStart", "names", {"session_id": "s", "hook_event_name": "SessionStart", "source": "startup"})


@local("ThenPrints")
def names_printed(step):
    """A message of the quote `work show` printed; an item's row of the names table, `| b1 | <title> | <status> |`; a
    title on its item's row; a batch's row."""
    if not step.context.get("conversation"):
        return False
    done, name = step.context["result"], step.names[0]
    assert done.returncode == 0, done.stderr
    rows = [line for line in done.stdout.splitlines() if line.startswith("|")]
    if name in talk(step).get("texts", {}):
        assert talk(step)["texts"][name] in done.stdout and ", cited:" in done.stdout, (step.text, done.stdout)
    elif step.text.startswith("`work` prints the item "):
        assert any(B.cells(line)[:1] == [B.ident(name)] for line in rows), done.stdout
    elif step.text.startswith("`work` prints the title "):
        item = talk(step)["titles"][name]
        assert any(B.cells(line)[:2] == [B.ident(item), "Title of %s" % item] for line in rows), done.stdout
    else:
        batch = talk(step)["batches"][name]
        row = next((line for line in rows if line.startswith("| %s |" % batch)), None)
        assert row is not None, (step.text, done.stdout)
    return None
