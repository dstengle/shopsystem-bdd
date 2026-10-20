---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/plans-list-the-tests-they-break
summary: "A work-item's plan lists every existing test its decisions make impossible to keep and what becomes of each; any other test an implementer would weaken is BLOCKED, with two reported allowances measured from the initiative's base."
date: 2026-10-19
status: proposed
supersedes: design-decision/tests-the-decisions-break
source: [initiative/i10, design-decision/tests-the-decisions-break]
---

# 0044. Plans list the tests they break

## Decision

The planner writes, under "Tests the decisions break", each test the researcher's notes name and each test in the
file set that a decision of the plan changes: the test, the decisions, and whether it is rewritten (to assert what)
or a question for the person. An implementer changes what a test asserts only when it is listed. Two allowances stay:
a test's setup changed with no assertion touched, and a test first committed after the initiative's base (the
commit `work run` logged when it first started) rewritten to a decision of the plan; each is named in the report and
checked by the review. Deferral to a later slice goes: a work-item's scenarios are expected to fail until it is
claimed, and a test is never skipped to wait for one.
