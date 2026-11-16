---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-39/review-1
kind: review
batch: batch-39
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/61
head: c9ad390ccd9be1d9f6c32c9568cb5cce62e6d3e4
range: 02701bc42b37478e2a33f5a13b0d88a11535e590..c9ad390ccd9be1d9f6c32c9568cb5cce62e6d3e4
result: clean
---

# batch-39 review 1

## Verdict

The batch builds all four items: b303 (migration-tools#r84), b310 (design-model-check#r316, feature-file-tools#r129), b14 (readiness#r42-r45) and b203 (readiness#r46, batches#r39). No finding needs fixing before the merge. The new module `backlog_reword.py` has its row in the module map. No test is removed or weakened. `features generate --check` exits 0, and the change is under the size limit. Two observations follow.

## Findings

### f1 Minor observation: laying b203's relation row dropped the blank line under `## Relations` in readiness.md
- item: b203
- where: spec/capabilities/readiness.md:37
The lay at batch start added the row `| translation | of | universal condition | one |`, and it also deleted the blank line between `## Relations` and the table:

```
 ## Relations
-
 | from | word | to | cardinality |
```

No line asks for this. It is a byte change to the capability file that the lay made (it comes from `backlog_forms`' relation lay, which this batch did not change), not by-hand editing. It does not change how the table reads, but it means laying a relation row is not byte-stable on a table that already exists. Reproduction: lay an item with `--relation` onto a capability whose `## Relations` heading has a blank line before its table, then diff the file. Recorded as hardening of the lay; it does not hold the merge.

### f2 Minor observation: `--remove` reads the id a line retires off the commit subjects, so a later line reusing the id can clear the wrong one
- item: b14
- where: scripts/backlog_reword.py:529
`_retiring` searches `git log --format=%s` for the newest subject `work line: ... <cap>#r<n> retires <cap>#r<m>`. Suppose a line written with `--retires` is removed, and a later plain `work line` gives a new line the same id. If that new line is then removed, the old subject still matches. `remove` then takes `r<m>` out of `retired:` if `r<m>` is there again, for example because another `--retires` line put it back. I checked `backlog_lines.py:102`, the source of the subject format (`work line: %s %s retires %s`), and `backlog_section.Block`, which has fields `retired` and `language`. The common path works, and `test_remove_takes_the_line_its_group_and_the_id_it_retires` covers it. Only an id reused within one item hits this edge, and no line names that case. A sturdier source would be the item's own text: for example, keep which line retires which id in the block, so history is not needed.
