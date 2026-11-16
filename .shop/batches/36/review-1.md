---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-36/review-1
kind: review
batch: batch-36
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/56
head: b5d68027d91d911a30150fdfa2d1692bfd94a9cd
range: 243d48d266e747f885a726d985075f5830557804..b5d68027d91d911a30150fdfa2d1692bfd94a9cd
result: fix-now
---

# batch-36 review 1

## Verdict

The batch builds the lines of b288 and b285, and most of b287. Two findings to fix. The ruff check now fails on b285's import in `scripts/spec_lf_read.py`. `model logic` and `model parse` also read two `Order: as listed.` senses of one word as one value order even when their lists differ, which r313 and r309 refuse.

## Findings

### f1 Important fix now: ruff fails on the import block b285 changed
- item: b285
- where: scripts/spec_lf_read.py:33
The `tools check` run exits 1 at `Head:` and exited 0 at the base:

```
== ruff ==
scripts/spec_lf_read.py:33:1: I001 [*] Import block is un-sorted or un-formatted
```

b285 put `import spec_lf_ordered` before `import spec_lf_core as core`, but `core` sorts before `ordered`. Fix: put `import spec_lf_ordered` after the `spec_lf_core` import, or run `ruff check --fix` on the file.

### f2 Important fix now: two as-listed senses with different value lists read as one value order
- item: b287
- where: scripts/spec_lf_order.py:167
The glossary entry **value order** in design-model-check says it is "the order its entry's `Order:` gives". An `Order: as listed.` entry orders its own values, so two such entries with different lists have different value orders. r313 and r309 say `model parse` refuses a comparison of them, naming the term.

`spec_value_kinds.value_order` gives the bare string `as listed` whatever the values are. So the check `spec_lf_order.order(t) != spec_lf_order.order(t2)` in `spec_lf_compare.cond` (scripts/spec_lf_compare.py:697) passes two such senses. Then `domain` keys `tcan` on `(t.term, order(t))`, so both entries become one canonical attribute. In `grammar/check.lp`, the `vkey` points of both lists, which are list positions 1, 2, 3, ..., go into the same cells. Unrelated values then compare by their place in their own lists: the first value of one list counts as equal to the first value of the other. That can report an L1 that no real values can produce, or hide one.

Reproduction: a sense `priority (attribute of file)` with `Values (adjective): a, b. Order: as listed.` beside the fixture's `priority (attribute of stage)` (low, high, urgent, as listed), and the line "While the priority of a stage is after the priority of a file, ...". `model parse` reads it and does not refuse it.

The scenarios do not catch this: the world builder in design_model_check_worlds_order.py pits `as listed` against `by number`. Fix: treat two `LISTED` entries as one value order only when their value lists are equal, in both the refusal in `spec_lf_compare.cond` and the `tcan` key in `domain`. Add a `test_spec_compare_senses.py` case of two different lists.

### f3 Minor observation: world_order.then reads the first entry of the attribute word
- item: b285
- where: tests/scenarios/world_order.py:132
b288 fixed the use of "the first entry of its word" in `spec_lf_ordered.member` and in `feature_file_tools_uses.counter`. The new `then` handler of b285 still does it:

```
entry = next(t for t, _ in spec_rgl_vocab.read(step.repo).attributes if t.term == term)
```

It also takes every recorded value of the term, including the collection's own value when the collection's kind has a sense of the word too. In a consumer's generated feature of `order-by` on a word of two senses with different orders, the members' values are keyed by the wrong entry, so the check can pass or fail wrongly. Today's scenarios do not reach this case.

### f4 Minor observation: value-same over two unordered senses never finds a clash
- item: b287
- where: grammar/check.lp:279
For an attribute with no value order, `tcan(T,T)` maps each entry only to itself. A `ccmp2` on the first side's id therefore finds `hast` on the second thing only through that same id. The second thing's value under its own entry is never matched, so the rules `out(A,B) :- c2w(...,same,...), not ordt(T), hast(...), hast(...)` never fire across two unordered senses. This is an edge no line names (r312 asks for one value order); it is recorded here.

### f5 Minor observation: the spec corpus traces r311-r313 to b287 ids it does not hold
- item: b287
- where: grammar/corpus/spec/design-model-check.md:1990
`## r311` says `From: b287 r306.`, `## r312` says `From: b287 r307.` and `## r313` says `From: b287 r308.`. The item `.shop/backlog/b287.md` holds these lines as r311, r312 and r313, and its r306-r308 do not exist; r306-r308 are b285's lines. The trace points at the wrong lines. Fix: `From: b287 r311.` and the like.

### f6 Minor observation: module-map rows not updated for the new behaviour
- item: -
- where: CLAUDE.md:67
The change gives these modules new concerns, but their rows do not name them:
- `scripts/spec_lf_ordered.py`: `misplaced`, the refusal of an order in a precondition, a trigger or a forbidden act, and `member`'s sense up the kind tree.
- `scripts/spec_lf_compare.py`: the `T1_CmpT_T2` and `T1_SameAs_T2` translations and the refusal of senses with different orders.
- `scripts/spec_lf_order.py`: `tcan`.
- `scripts/spec_lf_read.py`: the order refusal.
- `grammar/`: check.lp's `tcan`, `hast` and `dns`.
- `tests/scenarios/design_model_check_worlds_order.py`: the worlds of b285 and b287.
- `tests/scenarios/feature_file_tools_uses.py`: `order-by` and the members' sense.

Only the rows for spec_rgl_np and world_order were updated.
