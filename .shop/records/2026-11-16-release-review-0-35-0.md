---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-16-release-review-0-35-0
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-16
---

# Release 0.35.0: an adversarial review of its branch

A fresh agent's adversarial review of the branch `plan-release-0.35.0` (commits 4216b5aaa..0094d92c0), against the plan .shop/records/2026-11-16-release-0.35.0/plan.md. It checked each claim of the CHANGELOG section, docs/upgrading.md and docs/writing-requirements.md against the code with `model parse --form`, `model logic` and `features generate` on a throwaway copy of notes-cli. All six findings were fixed in 7430ff6ef.

## Findings

1. Medium. What a count's scenario gets was overstated in writing-requirements.md, CHANGELOG.md and upgrading.md. A count on what a response prints gets one thing past an upper bound and a Then that states the count, which a handler checks by counting. It does not get a negated Then. A count that restricts a written thing gets no counter-example (backlog b296). every and only do get a failing thing with a negated Then.
2. Medium. The CHANGELOG presented the order Then as checked by a sorted comparison. That comparison is this repository's handler (tests/scenarios/world_order.py), not one the plugin gives a consumer. upgrading.md did not say that a ThenPrints with `step.order` set needs a handler.
3. Low. "a comparison on an attribute with no value order is refused" is not true of `value-same`, which takes any attribute.
4. Low. upgrading.md left out the negated value Givens that counter-examples give ("the T of X is not `v`").
5. Low. upgrading.md's opening sentence implied that lines which parsed before may now be refused. Orders and two-thing comparisons are new, so none is.
6. Low. The Versions rule did not name this release's reason for a y bump: scenarios that consumers' handlers must meet.
7. Low, outside the branch. A refusal says "the status of a item" (spec_lf_ordered.py:45, spec_lf_compare.py:28; backlog b295).

## Found sound

- Items and PRs: #54 holds b268, b272, b273 and b274; #55 holds b275; #56 holds b285, b287 and b288; #57 holds b284.
- Every construct code named exists.
- Every line in writing-requirements.md parses to the form the page gives, and the refused line is refused for the reason the page gives.
- "holds nothing" reads `not [x2: thing]` and "holds no item" reads `not [x2: item]`.
- Opposite orders give the L1, and a requirement `model logic` cannot translate is named as unread.
- The version is 0.35.0 where a reader takes the current release from, and no history was rewritten.
- The docs tests pass (25).
