---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-140/review-1
kind: review
batch: batch-140
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/163
head: f4eecb8c45b4efecce0f3da49127195f16eeb07f
range: 6c6573f1e5a27c3e7b876a7b71f40b542a150be3..f4eecb8c45b4efecce0f3da49127195f16eeb07f
result: fix-now
---

# batch-140 review 1

## Verdict

The batch builds checking#r145 and checking#r146 of b612. It builds checking#r144 only for a word that two areas share. When three or more areas define the same word, `spec coupling` reports no coupling between the second area and the third, although the line asks for one. That is one finding to fix.

## Findings

### f1 Important fix now: a word shared by three areas leaves out the coupling between all but the first area
- item: b612
- where: scripts/spec_coupling.py:245
`_words` keeps only the first layer that defines each word:

```python
held = first.setdefault(e.term, e.layer)
if held != e.layer:
    _coupling(found, e.layer, held)["words"].add(e.term)
```

Take a word that the layers `a`, `b` and `c` all define, in that file order. The report gives `b by a` and `c by a` but no coupling between `b` and `c`. checking#r144 says that whenever an area holds a term with a word and another area holds a term with the same word, the service returns a coupling of the area that holds the word. Its logical form, in grammar/corpus/spec/checking.md under r144, applies to any two distinct areas (`distinct(x4, x1)`), not only to the first area to define the word. So `b` and `c` share the word, and the report says nothing ties them. The disentangling that this report measures would then undercount how tightly those areas are coupled.

This repository's domain model has many areas. The vocabulary layers under spec/vocabulary/ are a real input for this, not a made-up one. The g144 scenario uses only two areas, so it does not catch the gap.

Fix: keep every earlier layer of each word, for example `seen[e.term]`, an ordered list. For each new layer, add the word to `_coupling(found, e.layer, earlier)` for every earlier layer different from it. Add a three-area case to the scenario world or to a script test.

### f2 Minor observation: a requirement that uses a word its own area also defines is not counted
- item: -
- where: scripts/spec_coupling.py:311
`_requirements` counts a coupling only when the requirement's own area does not hold the word (`if area not in areas else ()`). This fits a reading of checking#r146 in which the term a line uses is the entry of its own layer: an area reads its own layer first, as spec_vocabulary's `layers_of` says. The line itself does not say so. A word that both areas define is already reported under r144, so nothing goes unreported. If the person means "another area holds the term" to cover this case as well, the line should say so. Reproduction: give `binder` a layer entry for "note" in tests/scenarios/checking_handlers_coupling.py. `shelving#r1` then drops out of the coupling.
