---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/a-request-parameter-s-value-is-a-referent-of-the-logical-form
summary: "Every wording of a request parameter's value translates to one referent of the logical form with conditions on it, so that a later wording keeps the meaning of an earlier one."
date: 2026-11-20
status: accepted
tier: judgement
source: [quote-60]
---

# 0110. A request parameter's value is a referent of the logical form

## Context

b418 (quote-60, 'Build around the abstract general case'): a uniqueness rule needs a parameter whose value is another thing's value; a second wording, a condition on the parameter (b427), is to follow without retiring lines of the first.

## Decision

A request's parameter value is a referent of the logical form: param(e, p, v). A code, a listed value, a thing and another thing's value of the attribute p names ('with the title of another checklist': title(x1) = v, distinct(x1, x3)) are each a translation to that referent and conditions on it; no wording gets an atom of its own. spec logic, the entailment check and the generated steps read the referent and its conditions, never the wording.

## Alternatives

A special atom for one phrase (param_from(e, p, x)): quicker, but each later wording would need its own translation and the check would have to learn they are one. Example data documented as the form of a uniqueness rule: the rule stays one example.
