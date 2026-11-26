"""A ready item reopened at opening naming every bar check it does not meet (batches r187, b758): the item, `ready`,
does not meet the readiness bar (batches_handlers4's line that does not parse); each bar check it does not meet, in
the order the Givens say them, the first its request line not settled (readiness_world's request `q9`, the item taken
in from it), the next its line that does not parse, kept with what `work batch start` names it by; the Then that the
printed line of the item's reopening names each."""
import sys

W, B, T, F = (sys.modules[n] for n in ("shop_work_queue_world", "shop_backlog_world", "shop_batches_world",
                                       "shop_world_four"))
four, parts = F.four, F.parts


def _checks(step):
    return step.context.setdefault("bar_checks", {})


@four("GivenK", "bar check", "batches")
def given_check(step):
    """`a bar check b2`: a check of the bar a later Given says the item does not meet."""


@four("GivenDoesNot", "meet", "batches")
def given_unmet(step):
    """`the item i1 does not meet the bar check b2`: the first such check its request line not settled, the next its
    line that does not parse, which the item holds already."""
    (k1, item), (k2, check) = parts(step)
    if (k1, k2) != ("item", "bar check"):
        return False
    R = sys.modules["shop_readiness_world"]
    checks = _checks(step)
    if not checks:
        R.write_request(step)
        B.write_item(step, item, request=R.REQUEST)
        checks[check] = "line 1 of request %s" % R.REQUEST
    elif len(checks) == 1:
        checks[check] = "frobnicate"
    else:
        raise AssertionError("batches_handlers_checks makes two bar checks an item does not meet: %s" % step.text)


@four("ThenDoes", "name", "batches")
def then_names(step):
    """`the batches service names the bar check b2`: the line `work batch start` printed of the item's reopening
    names what the check is named by."""
    k, check = parts(step)[-1]
    if k != "bar check" or check not in _checks(step):
        return False
    done = step.context["result"]
    assert done.returncode == 0, (done.stdout, done.stderr)
    said = [line for line in done.stdout.splitlines() if line.startswith("%s " % B.ident("i1")) and "-> shaped" in line]
    assert said and _checks(step)[check] in said[0], (step.text, _checks(step)[check], done.stdout)
