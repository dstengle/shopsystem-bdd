---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-138/review-1
kind: review
batch: batch-138
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/161
head: 20948a9c0fcf1122f9d4d63d94da6b4762b44b70
range: dd2f835bb82a64c9b335b21e8159c0c00ca4ded4..20948a9c0fcf1122f9d4d63d94da6b4762b44b70
result: clean
---

# batch-138 review 1

## Verdict

The batch builds all four items: b754's r143, b748's chore, b750's r177 and r178, and b751's r46. Every run exits 0, the change is within the size limit (+735 -86, limit 1000) and no test was removed or weakened. Nothing needs fixing before the merge. There are four observations: a fallback in `model_explain.word` that can now drop a preposition, two gaps in the module map, and a docstring that no longer says what its handler does.

## Findings

### f1 Minor observation: spec explain now drops the preposition when no frame of a verb with several frames fits
- item: b751
- where: scripts/model_explain.py:107
`word` uses the frame whose slot kinds match the pair's parts. If none matches and the verb has more than one frame, it returns `""`. That happens when `kind` returns None, for example when a part is not a role of L or of the premise that makes it.
```python
return fit[0] if fit else frames[0][0] if len(frames) == 1 else ""
```
Before b751 the first frame's word was always used. Now, in that case, the recipient comes out with no preposition at all ("lodge a design-decision a shelf"). This happens even when every frame of the verb has the same preposition. No line names this case, and the r46 world (a design-decision and a shelf, both roles) never reaches it.

Hardening: when nothing fits, fall back to the preposition all the frames share if there is one, else the first frame's word, rather than the empty string.

### f2 Minor observation: the new module tests/scenarios/scenario_unread.py has no row in the module map
- item: b748
- where: CLAUDE.md:316
CLAUDE.md says "A new concern gets a new module and a row here." `tests/scenarios/scenario_unread.py` is new: it holds the one failure that a Given no test world reads now ends in. No row names it, and no existing pattern row (`world_*.py`, `<capability>_handlers*.py`) covers it.

The world_fallbacks part of the row at CLAUDE.md:316 also still describes the fallbacks as recording nothing. It says nothing of `INTRODUCED`, `NEGATIVE`, `DEFAULTS`, or the failure for any other Given.

b748's chore names only `tests/scenarios` and `tests/scripts/test_world_fallbacks.py`, so its task could not have edited CLAUDE.md. Fix: add the row and update the world_fallbacks row in a later item.

### f3 Minor observation: the CLAUDE.md row for model_explain does not say how a frame is chosen
- item: b751
- where: CLAUDE.md:208
The `scripts/model_explain.py` row still says only that a response's request is "said with its object and its recipient after the verb's word before it (grammar 4's frame ..., b742)". It does not mention b751's change: the verb's frame is now chosen by the kinds of the object and the recipient (`kind`, `word`).

The module map is binding and b751's commit does not touch it. Fix: add b751 and `word` to the row.

### f4 Minor observation: the module docstring of world_fallbacks still says a Given records nothing
- item: b748
- where: tests/scenarios/world_fallbacks.py:3
The module docstring still reads "The Given records nothing, as supervision's recorded nothing another feature read". Since b748, `given_recorded` records nothing only for the kinds, verbs and default values it allows. Any other Given fails, naming the scenario. The function's own docstring was updated; the module's was not. Fix: reword that sentence.
