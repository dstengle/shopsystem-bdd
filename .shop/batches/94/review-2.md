---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-94/review-2
kind: review
batch: batch-94
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/117
head: 850710c277640308f43c219280d069eaf496d7c9
range: 97ea2329b7246e0cb2d6fb02ddfe05c084ace0bf..850710c277640308f43c219280d069eaf496d7c9
result: clean
---

# batch-94 review 2

## Verdict

The fix reverts 0d40a84eb's change to `judgement`, so `work batch brief` again lists every judgement decision whatever its status, as review-guarantees#r2 says. f1 is fixed. One minor observation, which does not hold the merge.

## Findings

### f4 Minor observation: the repair of the base's failing decision test rides on b591
- item: b591
- where: tests/scripts/test_decision_checks.py:83
On `main`, `test_the_judgement_decisions_reach_the_brief` expects only the accepted judgement decisions (`d.status == "accepted" and d.tier == "judgement"`). Commit 8f8424d2b changes that expected set to every judgement decision.

I checked the risk that this weakens the test. It does not. The base fails the test: 0123 is `status: superseded` and `tier: judgement`, and the base's `judgement` lists it. 0135, which supersedes it, is `tier: requirement`. After the change the test asserts the same exact-set equality against a larger set, and that set matches review-guarantees#r2. The test the batch itself had added (`test_a_superseded_judgement_decision_is_left_out_of_the_brief`) is gone, but it was never on the base, so no base test is lost.

What remains is that a test repair no line of b591 asks for travels on b591's branch. That is the second of the two ways f1 offered, only half taken. The idea b597 ("The brief gives the reviewer only the judgement decisions in force") is already in the backlog. When it is built, it should retire review-guarantees#r2 and change this test back with a line behind it.

## Earlier findings
- f1: fixed
