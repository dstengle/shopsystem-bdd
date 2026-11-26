---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-130/review-1
kind: review
batch: batch-130
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/153
head: 06f4fa288a26a6cc07deb9be1b79f59f93166350
range: 94ca7936e8bbdf8245a44db8e9e01b52c4e85aeb..06f4fa288a26a6cc07deb9be1b79f59f93166350
result: fix-now
---

# batch-130 review 1

## Verdict

The batch builds both items. b730's r168 is laid in r166's place and allocates the item. b716's generator says a no box of more than one atom whole, and its new scenario checks that the code is kept. One finding to fix: the regenerated Givens of scenarios#r22 and #r25 no longer reach the test world that their handler builds, so those two scenarios now test the plain catalogue example.

## Findings

### f1 Important fix now: scenarios r22 and r25 lose their "no frame takes `thing`" world after regeneration
- item: b716
- where: tests/scenarios/feature_file_tools_uses.py:102
The regenerated Given of scenarios#r22 and #r25 now reads "no frame of the verb v1 takes `thing`" (features/scenarios.feature:433 and :488). Before, it read "no frame takes `thing`". features_vocab4 sets `call.subject` to the whole noun phrase (scripts/features_vocab4.py:164). feature_file_tools_world's `ref` then records the subject as `("no", "frame of the verb v1")`. But `unthinged` only matches `a == ("no", "frame")`:

```python
return (any(v == "take" and a == ("no", "frame") and o == "`thing`" for v, a, o, _ in w["facts"])
```

So `unthinged` is now False in both scenarios. `prepare` then skips the b298 world, the line said with "return" whose one frame names the collection's kind (feature_file_tools_uses.py:133 and :135). Both scenarios now generate the catalogue's plain `order-by` and `order-by-every` examples instead. Their Thens (a scenario with an order counter-example) still pass, so the suite stays green, but r22 and r25 no longer test what their lines say: a verb whose frames do not take `thing`. That is a test weakened without any assertion being changed.

Fix: make `unthinged` match the new subject. Accept a fact whose subject is `("no", "frame ...")`, or match "frame of the verb" and the verb's name. Then check that r22 and r25 build ORDERED_RETURN and ORDERED_IN again.

### f2 Minor observation: r153's regenerated Givens contradict each other
- item: b716
- where: features/batches.feature:1090
The no box is now said whole, "no task of the batch b1 whose status is `running` exists". But the same scenario then brings in task t5 of batch b1 with status `running` (lines 1097-1099), which is the counter-example of the every box. So the scenario's Givens still contradict each other, as the item's note complained of "the batch b1 has no task". batches_handlers' `given_task_is` returns without doing anything for a "no " Given (tests/scenarios/batches_handlers.py:65), so the world holds a running task while r153's precondition says there is none. r45 only asks for the code to be kept, which it is. The clash comes from the counter-example added beside the box, which no line of this batch covers. It is recorded so that a later item makes the counter-example respect the no box.

### f3 Minor observation: a regenerated Given reads three ways in the step grammar
- item: b716
- where: features/batches.feature:1136
As the implementer notes, "the item i1 holds no capability in `registry`" parses three ways in the step grammar, and features_vocab4 picks one of them. It works today, but the generator now writes a step whose reading depends on the reader's order. Reproduction: parse the step with spec_rgl_steps' `trees` and three trees come back.

### f4 Minor observation: the module map row of feature_file_tools_uses does not name b716's world
- item: -
- where: CLAUDE.md:279
b716 adds `unlinked` and `given_code` to tests/scenarios/feature_file_tools_uses.py: a requirement that uses `no-noun`, `of-relation` and a code, said as a no box of two atoms, plus the Then that a given step uses the code. The module docstring describes both, but the file's module-map row in CLAUDE.md does not. The rule is "a new concern gets ... a row". This is an existing row that is now incomplete, which is cheap to add.
