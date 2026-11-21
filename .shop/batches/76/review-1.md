---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-76/review-1
kind: review
batch: batch-76
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/100
head: fa619cc8c2d62a073511b115d9628ed11a1f2ac9
range: 9aa0383dbb47751f042f54def81d8896f6e97387..fa619cc8c2d62a073511b115d9628ed11a1f2ac9
result: fix-now
---

# batch-76 review 1

## Verdict

The batch builds checking#r63, but b538's change in `scripts/model_spec.py` moved the existing `overlapping` fact under the new attribute branch. As a result, `spec check` no longer reports `v_t15` for a verb whose two senses overlap. One finding to fix.

## Findings

### f1 Important fix now: v_t15's `overlapping` fact now only fires for attributes, so spec check stops reporting overlapping verb senses
- item: b538
- where: scripts/model_spec.py:90
In the base, the `if t.term in overlapping:` block sat inside the verb-senses branch (`t.category == "event"`), which is where `spec_frames.overlapping` looks: it only collects verbs. Commit 485e7607f inserted the attribute branch just above that block without re-indenting it. The block now sits inside the new branch:
```python
            if t.category == "attribute" and attribute_senses(terms, t.term):
                self.fact("senses", ident)     # one attribute word of two kinds (b538)
                if t.term in overlapping:
                    self.fact("overlapping", ident)
```
`overlapping` only ever holds verbs, so an attribute's term is never in it and this branch never writes the fact. The verb branch no longer writes it either. So `v_t15(T) :- overlapping(T).` in `scripts/model.lp` (line 389) can never fire under `spec check`, though its catalogue entry in `grammar/rules.md` still lists it. Only `spec lexicon --check` (through `spec_frames.problems`) still reports v_t15.

What I checked: nothing in the tree's `spec/` or `features/` cites `v_t15` any more. The only thing that exercises it is the world row `term violate \`v_t15\`` in `tests/scenarios/design_model_check_worlds.py:184` (no generated scenario reaches it now), and no script test checks it. That is why the passing runs do not show the break. No line asks for this change; it drops a rule check that worked before.

Fix: put the `overlapping` fact back under the verb branch (after `self.fact("senses", ident)` on line 89), outside the attribute branch. Add a test in `tests/scripts/test_model_spec_terms.py` that two overlapping verb senses (the `overlapping` entries of `design_model_check_handlers_conditions.SENSES`) still give `v_t15` under `spec check`.

### f2 Minor observation: attribute entries whose kinds overlap are still counted as separate senses
- item: b538
- where: scripts/model_spec.py:122
`attribute_senses` compares each entry's whole sorted tuple of kinds. Entries `(attribute of stage, file)` and `(attribute of stage)` give different tuples, so they count as two senses and raise no v_t2, even though both are said of `stage`, which the kinds then cannot tell apart. The line and the item's note only mention attributes of other kinds, and no spec today has such a pair. Reproduction: write those two glossary entries for one word and run `spec check`; it reports no v_t2. Hardening: count them as senses only when their kind sets do not overlap.
