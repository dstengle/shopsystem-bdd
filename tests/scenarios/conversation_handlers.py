"""Handlers of features/conversation.feature (plan 8, D13): `work quote` run in the scenario's repository on a
transcript written into a store of the scenario's own (`CLAUDE_CONFIG_DIR`, never the person's), and the quote it
wrote and committed read back.

A step whose registry key another capability claims (`ThenDoes` with `write` and `commit`, `ThenR` with `cites`) is
taken through work_queue_world's `local` table by its kind, so it reaches these handlers only in test_conversation.py,
which binds with `bind_all`; each returns False for a step of a scenario that is not about the conversation (every
conversation When and Given sets `step.context["conversation"]`), which then goes on to the registry."""
import datetime
import importlib.util
import json
import os
import re
import sys
from pathlib import Path

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
    transcript(step, step.names[0])
    B.run_work(step, "quote", words(), "--session", talk(step)["sessions"][step.names[0]], env=env(step))


def quote_file(step, name):
    return step.repo / talk(step)["quotes"][name]


def read(step, name):
    rel = talk(step)["quotes"][name]
    return conversation_quote.parse((step.repo / rel).read_text(), rel)


@local("ThenDoes", "quote")
def does_to_quote(step):
    if not step.context.get("conversation") or step.term not in ("write", "commit"):
        return False
    name = step.names[0]
    if step.term == "write":
        done = step.context["result"]
        assert done.returncode == 0, done.stderr
        files = [rel for rel in B.changed(step) if re.fullmatch(r"\.shop/quotes/[1-9]\d*\.md", rel)]
        assert len(files) == 1, (step.text, B.changed(step))
        talk(step)["quotes"][name] = files[0]
    else:
        B.in_commits(step, talk(step)["quotes"][name])


@local("ThenR", "quote")
def quote_of(step):
    if not step.context.get("conversation") or step.term not in ("from", "cites"):
        return False
    quote, other = step.names
    found = read(step, quote)
    if step.term == "from":
        assert found.session == talk(step)["sessions"][other], (step.text, found.session)
        return None
    wanted = talk(step)["messages"][other]
    assert found.message == wanted, (step.text, found.message)
    heading = next(line for line in quote_file(step, quote).read_text().splitlines()
                   if line.startswith("### ") and ", %s" % wanted in line)
    assert heading.endswith(", cited"), (step.text, heading)
    return None


@handler("ThenR", "from")
def quote_from(step):
    """`the quote q1 is from the session s1`: the registry's key, which no other capability claims."""
    assert quote_of(step) is not False, "no quote from a session in this scenario: %s" % step.text


def hook(step, event, sub, stdin):
    """Run the command hooks/hooks.json gives for `event` and `sub` (D13) in the scenario's repository, committed
    first, with the hook's stdin JSON."""
    argv = T.hook_command(event, sub)
    script = Path(argv[1])
    assert argv[0] == "python3" and script.parent == HERE.parents[1] / "scripts", argv
    B.index(step)
    shop = step.repo / ".shop" / "README.md"
    shop.parent.mkdir(parents=True, exist_ok=True)
    shop.write_text("The repository's .shop/.\n")
    step.context["head"] = W.init(step.repo)
    step.context["result"] = step.run(script.name, *argv[2:], input=json.dumps(stdin), env=env(step))
    return step.context["result"]


@handler("WhenRuns", "`work quote --hook`")
def prompt_hook(step):
    """The UserPromptSubmit hook on a prompt of the scenario's session s1, whose transcript is written first."""
    path = transcript(step, "s1")
    talk(step)["transcripts"] = {"s1": str(path)}
    hook(step, "UserPromptSubmit", "quote", {"session_id": talk(step)["sessions"]["s1"], "transcript_path": str(path),
                                             "hook_event_name": "UserPromptSubmit", "prompt": "x"})


@local("ThenDoes", "session")
def keeps_session(step):
    if not step.context.get("conversation") or step.term != "keep":
        return False
    done, name = step.context["result"], step.names[0]
    assert (done.returncode, done.stdout) == (0, ""), (step.text, done.stdout, done.stderr)
    wanted = (talk(step)["sessions"][name], talk(step)["transcripts"][name])
    assert conversation_prompt.kept(step.repo) == wanted, (step.text, conversation_prompt.kept(step.repo))
    assert W.git(step.repo, "status", "--porcelain") == "", step.text
    return None


@handler("GivenK", "message")
def given_message(step):
    """A message of the person, kept by the scenario until a quote cites it."""
    name = step.names[0]
    talk(step)["messages"][name] = "message-%s" % name
    talk(step).setdefault("texts", {})[name] = "The words of the person in %s, to be kept." % name


@handler("GivenK", "quote")
def given_quote(step):
    talk(step)["quotes"].setdefault(step.names[0], None)


@handler("GivenR", "cited by")
def given_cited_by(step):
    """`the message m1 is cited by the quote q1`: the quote's file, written with conversation_quote.render, its cited
    message the message with one message of the session before it, committed."""
    message, quote = step.names
    number = len([q for q in talk(step)["quotes"].values() if q]) + 1
    name = "quote-%d" % number
    at = T.at(3).replace("Z", "+00:00")
    cited = conversation_quote.C.Message(talk(step)["messages"][message], "person",
                                         datetime.datetime.fromisoformat(at), talk(step)["texts"][message])
    before = conversation_quote.C.Message("a0", "session", cited.at - datetime.timedelta(minutes=1), "Asked before.")
    found = conversation_quote.Quote(name, "quote/ex.com/prod/ctx/%s" % name, "session-s1", cited.ident, "2026-11-05",
                                     cited.text, [before, cited])
    rel = conversation_quote.rel_of(name)
    path = step.repo / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(conversation_quote.render(found))
    talk(step)["quotes"][quote] = rel
    B.index(step)
    step.context["head"] = W.init(step.repo)


@local("WhenRuns", "quote")
def show_quote(step):
    if not step.context.get("conversation") or step.term != "`work show`":
        return False
    rel = talk(step)["quotes"][step.names[0]]
    B.run_work(step, "show", "quote-%s" % Path(rel).stem)
    return None


@local("ThenPrints", "message")
def prints_message(step):
    if not step.context.get("conversation"):
        return False
    done = step.context["result"]
    assert done.returncode == 0, done.stderr
    assert talk(step)["texts"][step.names[0]] in done.stdout and ", cited:" in done.stdout, (step.text, done.stdout)
    return None
