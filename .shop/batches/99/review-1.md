---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-99/review-1
kind: review
batch: batch-99
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/122
head: 52ac2fe7788094b38f111ecf921309aa132400ff
range: 3ea4ba603ccecbb9db529f13be0d87e49afb199e..52ac2fe7788094b38f111ecf921309aa132400ff
result: clean
---

# batch-99 review 1

## Verdict

The batch builds all seven requirement lines of b607 and b601. Each one has a generated scenario and a handler that checks it. The four checks in `## Runs` exit 0, as they do at the base. The scenarios were written by `features generate`, and r94 is properly retired in favour of r103. Nothing needs fixing before the merge. There are five observations: the size, the unlay module with no test, three refusals no line asks for, an `imports: []` line left behind by the unlay, and the wording of r69.

## Findings

### f1 Minor observation: the change is over the review limit
- item: b607
- where: -
`## Size` gives 25 files, +971 -52, which is 1023 changed lines against a limit of 1000. Most of it is b607: three new modules under `scripts/` (`backlog_area_move.py`, `backlog_area_move_lay.py`, `backlog_area_move_unlay.py`), two new scenario handler files, and the cli.toml, model, vocabulary and corpus lines. b601 is a single retired line with its scenario, about 60 lines.

### f2 Minor observation: the unlay of moves is run by no test
- item: b607
- where: scripts/backlog_area_move_unlay.py:116
The risk is that a parked item, or a relay by `work batch amend`, does not put the source's element, its entries and the imports back as they were. `backlog_lines.unlay` reaches this unlay through `backlog_model.unlay`, and `batch_start.py:104` calls `backlog_lines.unlay`. I searched `tests/` for `area_move`, `move-model` and `move_model`. Only `drafting_handlers_move.py` matches (`test_backlog_model_edit.py` only has `--remove-model`). That file covers drafting r66-r69. `batches_handlers_move.py` reads the lay through the batch branch's files. So neither `unlay`, `_element_back`, `_put_bullets` nor `_imports` has a single test. Fix: add a script test that lays a model-line move and a term move on a committed tree, unlays them with the base given, and asserts the source and target files come back byte for byte.

### f3 Minor observation: three refusals that no line or declared reason asks for
- item: b607
- where: scripts/backlog_area_move.py:421
These guards are reasonable, but no line states them:
- `move_model` refuses an element already in the target area (line 421).
- `move_term` refuses a term whose entry means no element the model declares (line 435).
- `move_term` refuses a term already in the target's layer (line 437).
- `_entry` refuses two entries of one word (line 392).

None of them carries a `reason=`. The model declares only `model line not in the domain model` and `term not in the vocabulary` (`spec/model/tracking.md`, `operation move` and `operation move term`). The lay also refuses with no reason when the source area no longer holds the moved element or term (`backlog_area_move_lay.py:598`, `:611`). That can happen when another item changes the area between drafting and `work batch start`. To reproduce the first one, run `work line b1 --into notebook --move-model "object tag"` in the domain-model fixture, where tag is in notes already: it is refused with no reason. Consider either adding lines and reasons for these refusals, or noting them as guards in the module map row.

### f4 Minor observation: the unlay writes `imports: []` into a model file that had no imports line
- item: b607
- where: scripts/backlog_area_move_unlay.py:686
If a model file had no `imports:` line, `_with_imports` inserts one at lay time (`backlog_area_move_lay.py:586`). The unlay then rewrites it as `imports: []` instead of removing it, because `_with_imports(text, kept)` with an empty `kept` still writes the line. So the file does not come back as the base held it. Fix: when the version at the base has no `imports:` line and `kept` is empty, take the line out.

### f5 Minor observation: r69's "no area holds the term" against a term held only in shared.md
- item: b607
- where: spec/capabilities/drafting.md:1034
`_entry` (`scripts/backlog_area_move.py:382`) accepts any layer, `shared.md` among them. r118's scenario moves `the person` from shared. But `shared.md` is a layer, not an area (spec_vocabulary's `layers_of`). Read literally, a term held only in shared is held by no area, and r69 says such a request is refused. The code does what the item's notes intend ("shared.md among them"). Consider rewording the line in a later item to say "no vocabulary layer" or "no vocabulary", which is the reason the model declares (`term not in the vocabulary`).
