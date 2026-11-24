---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-79/review-1
kind: review
batch: batch-79
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/103
head: e8b5022339d9804fe3951810cada7c2c9bd62726
range: 44ca12e838ff24b8fef10a74121cfe821186790c..e8b5022339d9804fe3951810cada7c2c9bd62726
result: clean
---

# batch-79 review 1

## Verdict

The batch builds b548's two lines, checking#r69 and checking#r70. Nothing needs fixing before merge. There are two observations: one on how `Relied on by:` treats an old id, one on what the scenario tests read.

## Findings

### f1 Minor observation: a `Relied on by:` id that was moved passes, and its `supports` fact names the old id
- item: b548
- where: scripts/model_spec.py:192
checking#r70 says `spec check` fails when a requirement supports an id that no requirement has. The new loop passes each id to `self.want(found, "requirement", where)`. Then `check_refs` in `scripts/model_facts.py:274` skips any id that `spec/moves.json` maps (`self.moved`) before it tests the id against the requirement nodes. This repository's `spec/moves.json` maps `design-model-check#r54` to `checking#r1`. So a port line with this line under it:

```
Relied on by: design-model-check#r54.
```

passes `spec check` with no finding, even though no live requirement has that id. The `supports` fact it writes also keeps the moved id (`capability/.../design-model-check#r54`), not `checking#r1`. The bound check that comes next (C-4) would read a `supports` edge that points at no requirement node. No port line in this repository names an old id today, so this is hardening.

Fix: resolve each id through `spec_moves.resolve` before writing the fact, or refuse a moved id outright.

What I checked: `check_refs` and `moved` (`scripts/model_facts.py:258-284`), and lines 2, 34 and 38 of `spec/moves.json`.

### f2 Minor observation: the r70 scenario checks only that the short id appears in stdout
- item: b548
- where: tests/scenarios/checking_handlers_port.py:460
`then_names` passes when any stdout line contains `notebook#r99`. The dangling message names the qualified id `capability/<path>/notebook#r99`, so the check holds. But stdout from a different rule that happened to name the same id would also pass it. The test does not confirm that the failure is the unresolved reference. A tighter assertion would match `is not a requirement in this repository` next to the id.
