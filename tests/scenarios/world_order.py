"""The Then that states an order (b275), shared by every feature whose lines order what a tool prints: "`work` prints
every file, ordered by version, in ascending order" and "`work` prints the worktree w1, ordered by version, in
descending order", which features_vocab4 reads as a ThenPrints whose `order` is (attribute, direction, noun phrase).

`ordered` checks the output by a sorted comparison: the members the Givens gave a value of the attribute, each found
where the output first prints it, appear in the direction's order of their values; it is not strict, so members of
one value may appear in either order. `key` gives a value's place in the attribute's value order (spec_lf_order's
key, a value a feature's world recorded); `said` how the output prints a member, its name by default. `then` is the
handler of such a Then (b285, decision 0093), which world_fallbacks registers as a `local` of ThenPrints: the values
codified2_handlers_values recorded under the scenario's `values`, ordered by the attribute's entry, checked against
what the command printed."""


def ordered(output, values, direction, key=None, said=None):
    """Assert that `output` prints the members of `values` ({member: value}) sorted by value in `direction`
    (ascending or descending); a member the output does not print fails it."""
    said = said or (lambda m: m)
    key = key or (lambda v: v)
    where = {}
    for m in values:
        at = output.find(said(m))
        assert at >= 0, "%s is not printed:\n%s" % (said(m), output)
        where[m] = at
    printed = sorted(values, key=lambda m: where[m])
    keys = [key(values[m]) for m in printed]
    want = sorted(keys, reverse=direction == "descending")
    assert keys == want, "printed %s, whose values %s are not in %s order:\n%s" % (
        ", ".join(printed), ", ".join(str(values[m]) for m in printed), direction, output)


def check(step, output, values, key=None, said=None):
    """The order a ThenPrints step states (its `order`), checked against `output` over `values`, the members' values
    of its attribute the scenario's Givens recorded."""
    _, direction, _ = step.order
    ordered(output, values, direction, key, said)


def then(step):
    """A ThenPrints whose `order` is set, checked against the command's output over the members' recorded values of
    its attribute (each printed as what the scenario `says` it is, else its name); False for any other step."""
    if getattr(step, "order", None) is None:
        return False
    import spec_lf_order
    import spec_rgl_vocab
    term = step.order[0]
    values = {m: v for (m, t), v in step.context.get("values", {}).items() if t == term and v is not None}
    assert values, "no member's %s was given: %s" % (term, step.text)
    entry = next(t for t, _ in spec_rgl_vocab.read(step.repo).attributes if t.term == term)
    says = step.context.get("says", {})
    check(step, step.context["result"].stdout, values, lambda v: spec_lf_order.key(entry, v),
          lambda m: says.get(m, m))
    return None
