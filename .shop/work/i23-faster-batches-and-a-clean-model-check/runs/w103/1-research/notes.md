# Research of w103: delivery#r17, delivery#r18

Tools: plugin 0.24.0 `scripts/` by path. `tools probe` ok. `tools tests-of` and `untested`: "no map", so no `map` run; test lists are `by search`. `refs` not run.

## Accepted scenarios

None. `features/` has no `delivery.feature` (ls; grep for `delivering-an-initiative` in features: none). Tags `@r17`/`@r18` in features belong to other capabilities (by search): supervision.feature:368,376; migration-tools.feature:81,440; design-model-check.feature:112,120,459; feature-file-tools.feature:161,176,383; analysis-tools.feature:195,286,299. These are not delivery's, so not accepted here.

## 1. Why each scenario is red today

None: no accepted scenario exists (see above).

## 2. What the system answers today

Probes (scratch: `.shop/scratch/w103-1-research/`).

- P1 `probe_deprecated.py`. Command: `python3 -m pytest -q -s -n 0 <probe>`. Run.
  - `features deprecated --json` gives per entry: file, title, deprecated_for, replacement. No tags of the deprecated scenario itself. A deprecated scenario tagged `@r17` is not identifiable from this output.
  - `replacement` came back null: my `Deprecated for:` named a title that differed from the replacement's exact title. Replacement tags come only from an exact title match (read: features_report.py:77-79).
  - Text form: `... | for: the new listing | no scenario has that title`; removal: `deprecated for removal`.
- P2 `probe_model.py`. Command as P1. Run, on a synthetic root (not the checkout).
  - Work-item accepting `delivery#r17` and `#r18`, no scenario naming them: `file: ...w103.md: accepts capability/.../delivery#r17, which no scenario names yet` (same for #r18). Exit 1.
  - Also `v_w4  a work-item has no acceptance and no check (1)`.
  - Artifacts of my synthetic root, not the real checkout: `v9c`, `v_b1` and `unresolved` (the proposal file was absent), and `initiative.md` status `formulated` is not a valid lifecycle value in this root.
  - The real checkout's `model check` was not run (probes never read the checkout's data).
- P3 `probe_zero.py`. Command as P1. Run.
  - `pytest -p work_items --work-item w103 tests`, w103 accepts both requirements, no scenario collected, one plain test: `1 passed`, exit 0. No refusal (see Defects D1).

Nearest cases read (`read`): deprecated scenario with no `@r` tag: model_facts.py:236 skips it as an acceptance-scenario; no requirement to list.

## 3. Old assumptions

The requirements add a `## Retires` list to a work-item and a stop on unnamed scenarios. Places that make a contrary assumption:

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/workqueue.py:add (74-97) | writes front matter and `# title` only; no body section | must write or accept a `## Retires` list (r17) | tests/scripts/test_work_add_title.py (executes `add`, by search; assertion lines 40-41 are substring checks and survive); test_work_item_ids.py (by search, not read) | read + search |
| skills/delivering-an-initiative/SKILL.md, Drafting steps 1-3 (lines 29-37) | drafts with `work add` only, no Retires; no unaccepted-scenario check | must list Retires (r17) and stop with no commit (r18) | none (no test reads SKILL.md; by search) | read + search |
| scripts/features_report.py:deprecated_entry (72-80) | JSON carries replacement tags, not the deprecated scenario's own tags | r17 needs the deprecated scenario's `@r<n>` (or the skill reads the feature file) | tests/scenarios/feature_file_tools_json_steps.py:80,87 (read title only; survives) | P1 + read |
| scripts/model_work.py (184-192) | `accepts X, which no scenario names yet` as file problem | flags w103 itself (P2): accepting requirements with no scenarios is already a problem | none (no test contains the phrase; by search) | P2 + read |
| scripts/model.lp:236 v_w4 | work-item with no acceptance and no check | w103 has acceptance, so v_w4 fires only via facts with no has_sc (P2) | tests/scenarios/design_model_check_one_each.py:44-46 (asserts v_w4 for w1; by search) | P2 + search |
| scripts/work_items.py:pytest_collection_modifyitems (92-107) | refuses only when scenarios were collected and none accepted | with zero scenarios it runs unrelated tests as w103's (D1) | tests/scripts/test_work_items.py (by search, not read) | P3 + read |

## 4. Tests the requirements make impossible to keep

None found that the requirements break. No code path the requirements change is executed by a test that asserts the old behaviour, by search. `tests-of` gave no map, so this is a search, not a coverage list. Verified: test_work_add_title.py (read), feature_file_tools_json_steps.py:80,87 (read; survive an added field). Not read in full: test_work_item_ids.py, test_work_items.py, test_work_queue.py (282 lines).

## 5. A step the work-item skips

- The drafting path (`work add`, SKILL.md:33 then commit at :41) runs no `model check` before committing. r18's stop is a check of that kind. (read)
- The existing `model check` rule for unnamed accepted requirements (model_work.py:184-192) is not run by the skill. (read)
- Refusals and effects only the new step would produce: none to show; the step is not in the existing path.

## 6. Defects

### D1 `--work-item` with no scenario collected runs unrelated tests and passes

Reproduction: P3 `probe_zero.py`, run. Scratch root, `.shop/work/i23/w103.md` with `accepts: [delivery#r17, delivery#r18]`, `tests/test_plain.py` with one plain test.

Command: `PYTHONPATH=<Scripts> python3 -m pytest -q -n 0 -p work_items --work-item w103 tests`

Came back: `1 passed`, exit 0.

Why (read): work_items.py:106-107 raises only when `scenarios` is non-zero and none is kept. A work-item whose requirements name no scenario is run green on any plain test.

## 7. The file set

Edited, by the requirements:
- `skills/delivering-an-initiative/SKILL.md` (70 lines; room 230). Add Retires listing (r17) and stop without commit (r18). Read at lines 29-37, 41.
- `scripts/workqueue.py` (262 lines; room 38), only if `work add` writes Retires. Read at 74-97. Alternative: the skill writes the section itself, and this file does not change.
- `scripts/work` (80 lines; room 220), only if `work add` gains an option. Read at 58.
- `scripts/features_report.py` (116 lines; room 184), only if the listing comes from `features deprecated --json` with the deprecated scenario's tags. Read at 72-80.
- Tests for `work add`, if its output or arguments change: `tests/scripts/test_work_add_title.py` (50 lines), `tests/scripts/test_work_item_ids.py` (77 lines), `tests/scenarios/test_work_queue.py` (282 lines; room 18).

On the change's path, not edited:
- `scripts/model_work.py` (211 lines; room 89).
- `scripts/work_items.py` (109 lines; room 191). Edited only if D1 is fixed.
- `scripts/supervise_brief.py` (110 lines; room 190).
- `scripts/model.lp` (not counted; a Prolog-style rule file).

Not edited: `spec/capabilities/delivery.md` (47 lines; requirements already there).

Size: `tools size --limit 300` printed no file over the limit.

## Questions for the plan (both readings given)

- Delivery has no `features/delivery.feature`, so r17 and r18 have no scenarios. Reading A: delivery is a guarantee of the skill and is not tested by scenarios; then the file set is the skill plus the `work add` change, and D1 matters for any work-item on delivery. Reading B: a feature file is needed; then `features/delivery.feature` is added by a formulate round, and P2's file problems clear.
- Retires: `work add --retires` (edits workqueue.py, work) or the skill writes the section (edits SKILL.md only).
