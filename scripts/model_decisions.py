"""The tiers of spec/decisions/ (decision-tiers): a decision's `tier`, its `enforced_by` entries told apart into tests
and requirements. Standard library only."""

TIERS = ("check", "requirement", "judgement")


def split(entries):
    """(tests, requirements): an entry holding `#` is a requirement id, any other a pytest node id."""
    tests, requirements = [], []
    for entry in entries:
        (requirements if "#" in str(entry) else tests).append(str(entry).strip())
    return tests, requirements


def test_file(entry):
    """The file of a pytest node id: the part before the first `::`."""
    return str(entry).split("::", 1)[0]


def wrong(root, tier, tests, requirements):
    """The file problems of a decision's tier and entries (D2): a tier outside the three, an entry of the wrong kind for
    its tier, `enforced_by` on a judgement decision, a test whose file is not under the root."""
    out = []
    if tier is not None and tier not in TIERS:
        out.append(f"tier {tier!r} is not one of {', '.join(TIERS)}")
    if tier == "judgement" and (tests or requirements):
        out.append("a judgement decision gives no enforced_by")
        return out
    for t in tests:
        if tier == "requirement":
            out.append(f"enforced_by {t}: a test, on a requirement decision")
        elif not (root / test_file(t)).is_file():
            out.append(f"enforced_by {t}: not a file of this repository")
    out += [f"enforced_by {q}: a requirement, on a check decision" for q in requirements if tier == "check"]
    return out
