---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-35/review-1
kind: review
batch: batch-35
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/55
head: de44813fe9f31240f4f4c33c87aeb56ca178dbf6
range: aef61f29e4cec07daa50e05ce686924fd1616ef7..de44813fe9f31240f4f4c33c87aeb56ca178dbf6
result: clean
---

# batch-35 review 1

## Verdict

The batch builds all eleven requirement lines of b275. Each line has a world row in design_model_check_worlds_order.py or a feature-file-tools check, and the clash and no-clash cases are pinned by parametrized script tests. No test was removed or weakened. The features match what `features generate --check` writes, and every check that failed at `Head:` (`model decisions --check`) failed at the base too. Nothing is to fix now. The five observations below are a dead helper, two unguarded edges of the new order atom, a rewording the item's notes promised with no live item to carry it, and the size.

## Findings

### f1 Minor observation: the change is over the size limit
- item: b275
- where: -
The range changes 39 files, +1294 -49, against a limit of 1000 changed lines. All of it is b275, the only item. Most of it is the new modules spec_lf_compare.py (115 lines) and spec_lf_ordered.py (175 lines), the check.lp rules for `ccmp2` and orders, the new language.md and constructs.md sections, the corpus readings, and the tests.

### f2 Minor observation: world_order.check is never called and no handler checks an order Then
- item: b275
- where: tests/scenarios/world_order.py:28
The item's notes ask for "a shared handler in tests/scenarios" that checks an order's Then against the actual output, and the module map row lists `ordered, check`. Only `ordered` is called, by feature_file_tools_uses.counter and test_spec_compare_order. A search of tests/ finds no caller of `world_order.check` and no ThenPrints handler that reads a step's `order`. No line of the batch asks for it, so the merge is not held. Either register it as a handler when a feature first has an order Then, or drop `check` and its mention in the module map.

### f3 Minor observation: an order in a negated response is written as a positive Then
- item: b275
- where: scripts/spec_lf_ordered.py:398
`said` builds the Then with `r.does(event, True)` whatever the polarity. spec_steps4.acts reaches `spec_lf_ordered.then` from a `not` box through `self.acts(item.body, not pos)` as well, so a line such as the one below would get a Then saying `work` prints the worktree:
```
`work` shall not print a worktree that holds a file, ordered by version, in descending order
```
The check side ignores such a fact, since `ordx` needs `resp(R,I,pos,...)`. No line says this today. Fix: refuse an order under a negated act in `np` or `then`, or pass the polarity through.

### f4 Minor observation: an order in a precondition parses but has no reading
- item: b275
- where: scripts/spec_rgl_np.py:1544
`r<n>_in_By_<T>` is typed `K2_NP0 -> Dir -> K2_NP0`, so "ordered by T" is accepted after a collection anywhere, a While clause included. There the form keeps an `ordered` atom in the pre-state. The risk was `model logic`: in spec_lf_facts_atoms.Terms.literal the atom falls to `else: raise ValueError("no translation of an event in a condition")`, so the line is unread with a misleading reason rather than refused by `model parse`. spec_steps4's Givens would hit `self.cond` on the same atom. No line says this. Fix: note a refusal in spec_lf_ordered.np when the NP is not in a response.

### f5 Minor observation: the rewording of migration-tools r77-r79 that the notes promised has no live item
- item: b275
- where: grammar/language.md:723
The notes of b275 say migration-tools r77, r78 and r79 are "retired, in the batch once the constructs parse", reworded with `value-compare` and `value-same` over the new term release. The batch adds the term but retires nothing. language.md now says the lines "keep their plain wording until a reword item retires them". The other backlog items that mention r77 are b131, b152, b153, b157, b166 and the withdrawn b266; I did not open them to confirm none is a live reword item. If none is, CLAUDE.md's rule that a stated intention goes into the backlog in the same turn asks for `work idea` for that reword.
