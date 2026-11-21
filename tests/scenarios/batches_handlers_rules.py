"""Handlers of batches' batch rules (r98, r99, b75), each in world_four's chain: "the settings file s1 holds the batch
rule b1", an entry of `[batch] rules` in the `.shop/delivery.toml` batches_world writes (its text the rule's name
in a sentence of its own), "no settings file holds a batch rule", a settings file with no `rules`; and the Thens
that the batch brief the run wrote holds the batch rule, or holds no batch rule: none of the rules a Given named,
nor any of the session rules the plugin's code kept before b75 (`SESSION`)."""
import sys

W, T, F = (sys.modules[n] for n in ("shop_work_queue_world", "shop_batches_world", "shop_world_four"))
four, parts = F.four, F.parts
BOTH = ("backlog", "batches")
SESSION = ("Don't chain `cp` and `rm`", "Worktrees of older work")


def _text(name):
    return "Rule %s: say the word %s-%s in the reply." % (name, name, "said")


def _rules(step):
    return step.context.setdefault("batch_rules", {})


@four("GivenK", "batch rule", *BOTH)
def given_rule(step):
    """A batch rule, its text made of its name."""
    _rules(step)[step.names[0]] = _text(step.names[0])


@four("GivenK", "settings file", *BOTH)
def given_settings(step):
    """The settings file: batches_world's `.shop/delivery.toml`."""


@four("GivenDoes", "holds", *BOTH)
def settings_holds_rule(step):
    """The settings file holds the batch rule as an entry of `[batch] rules`; "no settings file holds a batch rule",
    a settings file with no `rules`."""
    if step.text == "no settings file holds a batch rule":
        step.context["delivery"] = T.DELIVERY
        return
    found = parts(step)
    if found[-1][0] != "batch rule" or found[0][0] != "settings file":
        return False
    held = step.context.setdefault("held_rules", [])
    held.append(_rules(step)[found[-1][1]])
    step.context["delivery"] = T.DELIVERY + "rules = [%s]\n" % ", ".join('"%s"' % r for r in held)


def _brief(step, name):
    done = step.context["result"]
    assert done.returncode == 0, (step.text, done.stdout, done.stderr)
    rel = W.node_rel(step.context, name)
    assert rel, (step.text, "no batch brief was written")
    return (step.repo / rel).read_text()


@four("ThenDoes", "holds", *BOTH)
def brief_holds_rule(step):
    """The batch brief holds the batch rule (its text), or holds no batch rule (none a Given named, no session
    rule)."""
    (k1, brief), (k2, rule) = parts(step)
    none = step.nps == ["no batch rule"]
    if k1 != "batch brief" or (k2 != "batch rule" and not none):
        return False
    text = _brief(step, brief)
    if none:
        for said in list(_rules(step).values()) + list(SESSION):
            assert said not in text, (step.text, said, text)
        return
    assert _rules(step)[rule] in text, (step.text, text)
