"""The Then that states an order (b275), shared by every feature whose lines order what a tool prints: "`work` prints
every file, ordered by version, in ascending order" and "`work` prints the worktree w1, ordered by version, in
descending order", which features_vocab4 reads as a ThenPrints whose `order` is (attribute, direction, noun phrase).

`ordered` checks the output by a sorted comparison: the members the Givens gave a value of the attribute, each found
where the output first prints it, appear in the direction's order of their values; it is not strict, so members of
one value may appear in either order. `key` gives a value's place in the attribute's value order (spec_lf_order's
key, a value a feature's world recorded); `said` how the output prints a member, its name by default."""


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
