---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-96/review-1
kind: review
batch: batch-96
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/119
head: 327164e00fd83890231bd1edd5c987ecb94f21fb
range: acf69fe83b331776e494e37770ad15118ef92519..327164e00fd83890231bd1edd5c987ecb94f21fb
result: clean
---

# batch-96 review 1

## Verdict

The batch builds both items. b597 builds review-guarantees r11 and r12. b549 builds checking r95-r99 through `scripts/model_bound.py` and model.lp's v_pb1-v_pb4. Every run exits 0 at the head and at the base, and the change is within the size limit (+732 -57 against 1000). Nothing needs fixing before the merge; two hardening observations and one piece of polish follow.

## Findings

### f1 Minor observation: an operation outcome of kind `passed` can never be handled or excluded
- item: b549
- where: scripts/model_bound.py:16
`model_facts` writes an `outcome(O, X, "passed")` fact for a driven port's operation that declares `passed`, because `KINDS` includes it. But `VERBS` maps no verb to `passed`, and the request pack (grammar/packs/request.md) has no verb for it either. So no core line can produce `on_outcome(_, "passed", _)` and no port line can produce `denies(_, _, "passed")`. A port operation with a `passed` outcome would therefore always raise v_pb2, whatever lines are written.

The same happens to a `done` outcome of an operation that has no `op_object` (no `done →` object and no parameter naming an object): `handled/1` joins on `op_object` and can never hold. No client declares either today. A test with a port operation `outcomes: passed` would show it.

Possible fix: leave `passed` out of the bound check's outcomes until the pack has a verb for it, or name the gap in the rule catalogue.

### f2 Minor observation: `on_outcome` and `denies` do not check who gives the outcome
- item: b549
- where: scripts/model_bound.py:51
`line_facts` counts any trigger act of complete, return, refuse or fail on a thing of the operation's object as handling that outcome. It does not check that the act's subject is the port's service. In the same way, any negated act of those verbs in a port line's response counts as excluding the outcome, whatever its subject or object. For example, "When the notes service completes a reservation" would count as handling `stock.reserve done`, and "shall not refuse" said of a different service would still exclude the refusal.

No line in this repository or the fixtures says either today. Possible fix: require the trigger's subject (for `on_outcome`) and the negated act's subject (for `denies`) to be the actor of the operation's service.

### f3 Minor drop: dead polarity test and a typo in a docstring
- item: b549
- where: scripts/model_bound.py:50
`x.args[2] == 0` tests the event's sense number (`spec_lf_clause.sense`, which is always 1 or more), not its polarity. The check is always false. Negation already comes only from the `not` box, so it does no harm.

Separately, the docstring of tests/scenarios/checking_handlers_response.py says `v_b2` where it means `v_pb2`.
