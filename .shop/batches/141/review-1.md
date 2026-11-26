---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-141/review-1
kind: review
batch: batch-141
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/164
head: 3e583f1c0bf08e1cbaa45b6e3074753e6e54d819
range: c1f252ac28fb69101f19d6e5b4ee4afd47ab6597..3e583f1c0bf08e1cbaa45b6e3074753e6e54d819
result: clean
---

# batch-141 review 1

## Verdict

All three items are built: b755 (laying#r5), b756 (consistency#r47) and b757's chore. Every run exits 0, the size is 358 changed lines against a limit of 1000, and no test was removed or weakened. There is nothing to fix now. There are two observations: one about how far b755's put-back reaches, and one about how b756's scenario world picks its frames.

## Findings

### f1 Minor observation: a group put back keeps the `Relied on by:` line of a retired line it leaves out
- item: b755
- where: scripts/backlog_retires.py:174
`unlay` takes another item's still-retired line out of the group it puts back with `_line(other)`. That pattern takes the line and its indented continuation lines. A port line's `Relied on by:` line is not indented, so it stays behind. It then follows the line before it, as `spec/capabilities/laying.md` shows. Reproduction: two items in one batch each retire one of two lines of a port capability's group, and each line has a `Relied on by:` line. Lay both, then lift the first. The group comes back with the first item's line followed by both `Relied on by:` lines, so `spec_read`'s `supports` reads the other line's core ids as relied on by the first. `lay` has the same limit (scripts/backlog_retires.py:91 uses `_line(rid)` too), so this is not new with b755. The cheap fix is to take a line's following `Relied on by:` line together with the line, in both `lay` and `unlay`.

### f2 Minor observation: the r46/r47 world picks its frames by counting the scenario's prepositions
- item: b756
- where: tests/scenarios/design_model_check_worlds_response.py:353
`framed` uses the frames that share a preposition (`SHARED`) when the scenario brings in exactly one `preposition`, and `FRAMED` otherwise. This works for g46 and g47 as generated today. A later group that brings in a single preposition for another reason would quietly get the shared-preposition world. Keying the choice on the group, as `requested.py`'s `ADDED` does, would make it explicit.
