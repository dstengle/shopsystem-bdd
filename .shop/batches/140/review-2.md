---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-140/review-2
kind: review
batch: batch-140
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/163
head: 382a2702fcb33fad5d9c08502441301e9925ad0b
range: f4eecb8c45b4efecce0f3da49127195f16eeb07f..382a2702fcb33fad5d9c08502441301e9925ad0b
result: clean
---

# batch-140 review 2

## Verdict

The fix builds checking#r144 for a word that three or more areas define: each pair of areas that define it now gets a coupling. A script test covers the three-area case and the case of one area that defines a word twice. All runs pass. One observation: the module map row for spec_coupling still describes the old behaviour.

## Findings

### f3 Minor observation: the module map row of spec_coupling still says "of the area of its second entry"
- item: b612
- where: CLAUDE.md:274
The fix changed the module docstring at scripts/spec_coupling.py:4 from "second entry" to "later entry", and it rewrote `_words` to couple every two areas that define a word. CLAUDE.md's module map row for `scripts/spec_coupling.py` still reads:

```
holding each word both areas' layers define (of the area of its second entry, `_words`)
```

That describes the behaviour f1 removed. A reader of the map would expect a word shared by `a`, `b` and `c` to couple `b` and `c` only to `a`. The row does not hold the merge. Fix: say "of the area of its later entry, for every two areas that define it".

## Earlier findings
- f1: fixed
