---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-45/review-1
kind: review
batch: batch-45
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/68
head: 6d4f8002b3c34edd44e104c5c48aa8009c2a40f7
range: 10f6f2788120c56792657d488c9e65b38298093b..6d4f8002b3c34edd44e104c5c48aa8009c2a40f7
result: fix-now
---

# batch-45 review 1

## Verdict

The batch builds all six requirement lines of b301, b323 and b232. No check that passed at the base fails at the head, and no test was removed or weakened: r43's scenario is retired properly into r57, and the changed assertions in test_backlog_reword and test_backlog_retires now check more. The change is under the size limit. Two findings to fix: module-map rows in CLAUDE.md that the change makes wrong. One observation.

## Findings

### f1 Minor fix now: CLAUDE.md's module map still says `--remove` reads the item's history, and leaves out the `retires:` line
- item: b323
- where: CLAUDE.md:150
CLAUDE.md says its module map is binding. The `scripts/backlog_reword.py` row still reads:

```
and the id a `--retires` line retires (read off the item's history) out of its block's `retired:`
```

That is the behaviour b323 removes. `remove` in scripts/backlog_reword.py now reads the block's `retires:` pairs and keeps any id that no pair names. Two other rows have the same gap:
- The `scripts/backlog_section.py` row (CLAUDE.md:144) lists every line a block holds, but not the new `retires: [r<n> r<m>, ...]` line. That line is now read, refused when it is out of place, and written back.
- The `scripts/backlog_retires.py` row does not say that `with_retired` writes the pair.

Fix: change the backlog_reword row to "read off the block's `retires:` pairs; an id no pair names is kept". Add the `retires:` line to the backlog_section row and the pair to the backlog_retires row.

### f2 Minor fix now: CLAUDE.md's `grammar/` row still says a negated restriction is entailed only by the same one
- item: b232
- where: CLAUDE.md:49
The `grammar/` row describes check.lp as reading:

```
a negated restriction of an object (`onattr`, `onrel`) entailed only by the same one on the other side
```

b232 changed this in grammar/check.lp:401-409. `onattrby` and `onattrof` now also count a value of the same attribute other than W, `absent` included. That is the behaviour r328 and r329 test. The row now describes the old rule. Fix: say the new rule in the row, for example "an `onattr` entailed by the same one on the other side or by another value of its attribute (b232)".

### f3 Minor observation: items that already carry `retired:` ids have no `retires:` pairs, so `--remove` now keeps their retired ids
- item: b323
- where: scripts/backlog_reword.py:56
`remove` used to find a removed line's retired id by searching the git log. It now reads only the block's `retires:` pairs. Items written before this change have `retired:` lines but no pairs. For example, .shop/backlog/b333.md (status `ready`) has `retired: [r49]` and no `retires:` line.

The risk: if such an item returns to `idea` or `shaped` and the person runs `--remove` on its retiring line, r49 stays under `retired:`. The live requirement would then be retired with nothing in its place when the item is laid into a batch.

I checked the in-tree backlog: no item in `idea` or `shaped` carries a `retired:` line today. So this hits no item now, and the alpha no-compat decision (0097) allows a clean break. It is recorded for whoever re-opens such an item: add the pair by hand first.
