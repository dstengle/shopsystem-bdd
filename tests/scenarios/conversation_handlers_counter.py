"""conversation's counter-examples (b273), beside conversation_handlers.py: a message another quote cites, which
`work show` on the quote does not print, and a title a record has, not the item, which `work names` does not print;
each read off what `work` printed."""
import hashlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
C = sys.modules["shop_handlers_%s" % hashlib.sha256(str(HERE / "conversation_handlers.py").encode()).hexdigest()[:12]]
local, talk, write_quote = C.local, C.talk, C.write_quote


@local("GivenDoesNot")
def given_cites_not(step):
    """`the quote q1 does not cite the message m3` (a counter-example, b273): the message is another quote's, the
    quote-2 file of the repository, which `work show` on the quote q1 does not read."""
    if not step.context.get("conversation") or step.term != "cite":
        return False
    write_quote(step, "quote-2", [step.names[1]])
    return None


@local("GivenDoesNot")
def item_has_title_not(step):
    """`the item i5 does not have the title t3` (a counter-example, b273): the title is a record's heading in the
    repository, `Title of t3`, and the item's is its own."""
    if not step.context.get("conversation") or step.term != "has" or " the title " not in step.text:
        return False
    path = step.repo / ".shop" / "records" / ("2026-11-05-%s.md" % step.names[1])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("---\nid: record/ex.com/prod/ctx/%s\n---\n# Title of %s\n" % (step.names[1], step.names[1]))
    return None


def title(step, name):
    """The words of the title `name`: its item's title, else the record heading a counter-example gave it."""
    item = talk(step).get("titles", {}).get(name)
    return "Title of %s" % (item or name)


@local("ThenPrintsNot")
def names_not_printed(step):
    """A counter-example (b273): the message m3's words, the title t3's words are nowhere in what `work` printed."""
    if not step.context.get("conversation"):
        return False
    done, name = step.context["result"], step.names[0]
    assert done.returncode == 0, done.stderr
    said = talk(step)["texts"][name] if name in talk(step).get("texts", {}) else title(step, name)
    assert said not in done.stdout, (step.text, said, done.stdout)
    return None
