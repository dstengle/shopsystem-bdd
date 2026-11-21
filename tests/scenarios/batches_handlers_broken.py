"""A ready item whose lines laid violate a rule (batches r89, b478): the item meets the readiness bar, whose copy of
`spec/` holds no rule catalogue, but its line cites a rule code (`v_zz`) that the repository's rule catalogue
(`grammar/rules.md`, which the lay writes again from model.lp) has no entry of, so the laid worktree violates `v_c1`,
a rule of severity error; the Then reads `work batch start`'s output for the rule's code."""
import sys

W, B, T, F = (sys.modules[n] for n in ("shop_work_queue_world", "shop_backlog_world", "shop_batches_world",
                                       "shop_world_four"))
four, parts = F.four, F.parts
RULES = "grammar/rules.md"
UNCATALOGUED = "v_zz"           # a rule code model.lp has no rule of
VIOLATED = "v_c1"               # a requirement names a rule the rule catalogue has no entry of
CITING = "When the person runs `work check`, `work` shall print `%s`."     # a trigger no other group of the world has


@four("GivenK_A", "rule", "batches")
def severity(step):
    """The severity of the rule is `error`: the rule the requirement violates is one (`v...`)."""
    if step.attribute != "severity":
        return False
    assert step.values[0].strip("`") == "error", step.text


@four("GivenDoes", "violate", "batches")
def violates(step):
    """The requirement violates the rule: the item's line cites a rule code the rule catalogue has no entry of, and
    the repository keeps a rule catalogue."""
    (k1, n1), (k2, n2) = parts(step)
    if (k1, k2) != ("requirement", "rule"):
        return False
    R = sys.modules["shop_readiness_world"]
    R.codify(step)
    catalogue = step.repo / RULES
    catalogue.parent.mkdir(parents=True, exist_ok=True)
    catalogue.write_text("# The rule catalogue\n")
    R.give_lines(step, step.context["proposed"][n1], CITING % UNCATALOGUED)
    step.context.setdefault("rules", {})[n2] = VIOLATED


@four("ThenDoes", "name", "batches")
def names_rule(step):
    """The batches service names the rule: `work batch start` printed its code beside the item it gave back."""
    k, name = parts(step)[1]
    if k != "rule" or name not in step.context.get("rules", {}):
        return False
    done = step.context["result"]
    assert done.returncode == 0, (step.text, done.stdout, done.stderr)
    assert step.context["rules"][name] in done.stdout, (step.text, done.stdout)
