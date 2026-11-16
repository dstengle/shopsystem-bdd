"""conversation's directives (b20), beside conversation_handlers.py: a directive of each status written into the
scenario's repository as `.shop/directives/<n>.md` with the quote it cites, `work directive`, `work directives --hook`
(the SessionStart hook), `work promote` and `work drop` run, and the directive the command wrote or changed read back.

Each handler takes a step only in a scenario about directives (`mine`); a directive dN is `directive-N` citing
`quote-N`, and what a refusal names it by is kept under the scenario's `says`."""
import hashlib
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
C = sys.modules["shop_handlers_%s" % hashlib.sha256(str(HERE / "conversation_handlers.py").encode()).hexdigest()[:12]]
B, W, local, talk = C.B, C.W, C.local, C.talk
WHY = "Done by the batch's own check instead."


def mine(step):
    return any("directive" in text for text in W.scenario_texts(step))


def held(step):
    """The directives the Givens name: name -> status."""
    return talk(step).setdefault("directives", {})


def number(name):
    return int(re.sub(r"^\D+", "", name))


def rel(name):
    return ".shop/directives/%d.md" % number(name)


@local("GivenK", "directive")
def given_directive(step):
    held(step).setdefault(step.names[0], "live")


@local("GivenK_A", "directive")
def given_status(step):
    """`the status of the directive d1 is v`; `... is not v`, another of its values."""
    value = step.values[0].strip("`")
    if " is not " in step.text:
        value = next(v for v in ("promoted", "dropped", "live") if v != value)
    held(step)[step.names[0]] = value


@local("GivenDoesNot")
def item_absent(step):
    """`the item i1 does not exist`: its file taken out of the repository, so `--to` names an item no file holds."""
    if step.term != "exist" or not mine(step) or not step.text.startswith("the item "):
        return False
    rel_ = B.item_rel(step.context, step.names[0])
    if rel_ and (step.repo / rel_).exists():
        (step.repo / rel_).unlink()
    talk(step).setdefault("absent", set()).add(step.names[0])
    return None


def prepare(step):
    """Each directive the Givens name written with its quote, the quote's message the person's words of it."""
    import directive
    for name, status in held(step).items():
        n = number(name)
        message = "md%d" % n
        talk(step)["messages"][message] = "message-%s" % message
        talk(step).setdefault("texts", {})[message] = "Directive words of %s: merge when the checks pass." % name
        C.write_quote(step, "quote-%d" % n, [message])
        found = directive.Directive("directive-%d" % n, "directive/ex.com/prod/ctx/directive-%d" % n, status,
                                    "2026-11-0%d" % n, "quote-%d" % n, talk(step)["texts"][message],
                                    "b90" if status == "promoted" else None, WHY if status == "dropped" else None)
        (step.repo / rel(name)).parent.mkdir(parents=True, exist_ok=True)
        (step.repo / rel(name)).write_text(directive.render(found))
        step.context.setdefault("says", {})[name] = found.name
    for text in W.scenario_texts(step):
        for d, q in re.findall(r"\bthe directive (d\d+) has the quote (q\d+)\b", text):
            talk(step)["quotes"][q] = ".shop/quotes/%d.md" % number(d)


def run(step, *args):
    B.index(step)
    step.context["head"] = W.init(step.repo)
    step.context["result"] = step.run("work", *args)


@local("WhenRuns")
def when_directive(step):
    """`work directive` on the words of the session's message m1; `work directives --hook`, the SessionStart hook;
    `work promote --to` an item (a written one when the step names none); `work drop --why`."""
    if not mine(step):
        return False
    talk(step)
    if step.term == "`work directive`":
        C.transcript(step, step.names[0])
        B.run_work(step, "directive", C.queued().words(step), "--session", talk(step)["sessions"][step.names[0]],
                   env=C.env(step))
        return None
    prepare(step)
    if step.term == "`work directives`":
        C.hook(step, "SessionStart", "directives", {"session_id": "s", "hook_event_name": "SessionStart",
                                                     "source": "startup"})
        return None
    target = next(n for n in step.names if n.startswith("d"))
    if step.term == "`work drop`":
        return run(step, "drop", "directive-%d" % number(target), "--why", WHY)
    assert step.term == "`work promote`", step.text
    items = [n for n in step.names if n.startswith("i")]
    item = items[0] if items else "i1"
    if item not in talk(step).get("absent", ()) and not B.item_rel(step.context, item):
        B.write_item(step, item)
    step.context.setdefault("says", {})[item] = B.ident(item)
    talk(step)["promoted_to"] = B.ident(item)
    return run(step, "promote", "directive-%d" % number(target), "--to", B.ident(item))


def read(step, name):
    import directive
    return directive.parse((step.repo / rel(name)).read_text(), rel(name))


@local("ThenDoes")
def directive_does(step):
    """`work` writes, sets the status of, commits the directive d1; the directive d1 has the quote q1."""
    if not mine(step) or not any(n.startswith("d") for n in step.names) or step.term not in (
            "write", "set", "commit", "has"):
        return False
    done = step.context["result"]
    assert done.returncode == 0, (step.text, done.stderr)
    name = next(n for n in step.names if n.startswith("d"))
    if step.term == "write":
        assert rel(name) in B.changed(step), (step.text, B.changed(step))
    found = read(step, name)
    if step.term == "commit":
        B.in_commits(step, rel(name))
        if name not in held(step):     # `work directive`: the quote in the directive's one commit
            assert set(W.committed(step.repo)) == {rel(name), talk(step)["quotes"]["q1"]}, W.committed(step.repo)
    elif step.term == "set":
        wanted = step.values[0].strip("`")
        assert found.status == wanted, (step.text, found.status)
        if wanted == "promoted":
            assert found.promoted_to == talk(step)["promoted_to"], (step.text, found.promoted_to)
        else:
            assert found.why == WHY, (step.text, found.why)
    elif step.term == "has":
        quote = step.names[1]
        if quote not in talk(step)["quotes"]:
            C.written_quote(step, quote)
        assert found.quote == "quote-%s" % Path(talk(step)["quotes"][quote]).stem, (step.text, found.quote)
    return None


@local("ThenPrints")
def quote_printed(step):
    """`work prints the quote q1` after the SessionStart hook: the quote's name and its words, which only a live
    directive's line holds."""
    if not mine(step) or not step.text.startswith("`work` prints the quote "):
        return False
    done = step.context["result"]
    assert done.returncode == 0, done.stderr
    n = int(Path(talk(step)["quotes"][step.names[0]]).stem)
    words = talk(step)["texts"]["md%d" % n]
    line = next((x for x in done.stdout.splitlines() if "quote-%d" % n in x), None)
    assert line is not None and words in line, (step.text, done.stdout)
    return None
