---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-143/review-1
kind: review
batch: batch-143
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/166
head: 11ee6185cee3f1f8d129d9d8db47035b6049e422
range: 02cc3e9e6683a1b5b55b50a7fe3d67f34d531235..11ee6185cee3f1f8d129d9d8db47035b6049e422
result: clean
---

# batch-143 review 1

## Verdict

The batch builds b745. The eight batches lines are retired through the item's `retired:` in the lay's commit. Their successors, laying#r7, r8 and r22-r27, are laid with `Relied on by: batches#r179`, and laying_handlers_pieces makes each new scenario pass by calling `laying.lay` directly. No script changes, and every given run exits 0 at the head. Nothing needs fixing; there are two observations.

## Findings

### f1 Minor observation: the change is over the review limit
- item: b745
- where: -
The change is 20 files, +548 -941 (1489 changed lines), against a limit of 1000. b745 is the only item. Most of the change is deletion: the eight retired batches scenarios, their corpus blocks and cli.toml annotations, and the handler modules batches_handlers_area.py, _form.py, _pack.py, _port.py and _serves.py. The new laying_handlers_pieces.py adds 246 lines. The item's own estimate was about 450 lines.

### f2 Minor observation: laying#r26's scenario no longer goes through renumbering
- item: b745
- where: tests/scenarios/laying_handlers_pieces.py:97
The retired batches#r128 ("An item's term of a pack kept when its ids are renumbered") was tested through `work batch start`, whose pick renumbers the item's ids (batches_handlers_collide with batches_handlers_pack). Its successor laying#r26 is tested by `_colliding`. That function gives the item the ids `g1` and `r1`, which work-queue already holds, and passes them straight to `laying.lay`. Nothing renumbers them, and the Then only checks that `spec/packs/household.md` changed. Line r26 does not mention renumbering, so the scenario meets it. But no remaining scenario checks that a pack term survives the pick's renumbering: batches_handlers_collide now covers only r126 and r127, an operation table and a moved term. If that behaviour still matters, it needs a line of its own on the pick (batches).
