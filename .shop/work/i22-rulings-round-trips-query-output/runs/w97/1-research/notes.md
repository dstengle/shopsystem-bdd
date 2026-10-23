# w97 research notes

Accepted: design-model-check#r110, work-queue#r12. Base dc9ece7. Worktree clean at start and end (`git status --porcelain` empty; `.shop/` ignored).
Tools: `python3 /home/vscode/shopsystem-bdd/scripts/tools` (refs, check size work). `tools tests-of`/`untested`: no map, not made (a map runs the whole suite). Test lists below are `by search`.
Probe files: `.shop/scratch/w97-1-research/probe_r110_add.py`, `probe_r12_env.py`, `probe_dup_id.py`.

## 1. Why each scenario is red today

None is red. Both pass as run:
- `python3 -m pytest -q <node id>` for `tests/scenarios/test_work_queue.py::test_add_numbers_the_new_workitem_one_above_the_highest_workitem_under_shopwork_in_any_initiative_and_any_status`: passed (run).
- `tests/scenarios/test_design_model_check.py::test_a_workitem_not_named_wnmd_or_two_workitems_with_one_id_is_a_file_problem[...]`, all 4 examples: passed (run).

Why they pass: each fixture gives a work-item an id equal to its file stem, and no fixture makes two stems hold one id. The defects below are cases the scenarios do not give.

## 2. What the system answers today

Probes (run, `python3 -m pytest -q -s -n 0 <file>`; `-n 0` is needed, xdist swallows prints):

| probe | command driven | what came back |
|---|---|---|
| r12 note w2 | `work add i1 New ...` with `i1/w1.md` (work-item), `i1/w2.md` (plain note, no frontmatter) | rc 1: `work: the work-item w2 already exists (.shop/work/i1/w2.md); work add leaves it as it was`. Nothing written. |
| r12 note w3 | same, note is `w3.md` | rc 0, prints `w2`; w2.md written |
| r12 fix-login id w7 | `i1/w1.md`, `i1/fix-login.md` (kind work-item, id w7) | rc 0, prints `w2` |
| r12 non-UTF-8 | `i1/w1.md`, `i1/notes.md` bytes `\xff\xfe` | rc 1: `work: .shop/work/i1/notes.md is not UTF-8 text`; nothing written |
| r12 dup id | `i1/w1.md`, `i1/fix-login.md` (id w2), then `work add` | rc 0, prints `w2`; `w2.md` written with id w2. `model check` then lists id w2 three times under violations and prints no "already held" problem. |
| r110 held id, two stems | `i1/w3.md` and `i2/w5.md`, both id w3 | `model check` prints no `is already held by` problem (only the accepts problems). |
| r110 id differs from stem | `i1/w3.md` with id w9 | no r110 problem. |
| r110 same initiative | `i1/w3.md` and `i1/w5.md`, both id w3 | no `is already held by` problem. |

All are `run`. Probe commands: `model check --root <fixture> check`, `work add i1 "New" --part-of capability-proposal/p1 --under thing --accepts thing#r1`. Fixtures are git repos under `.shop/scratch/w97-1-research/fx/`.

Nearest cases read, not run: `work add` with no work-item in the queue writes w1 (`workqueue.py:82`, `highest` returns 0). Run as the control: `w1 only` gives `w2` beside `w1.md` (`run`).

## 3. Old assumptions

Found by `tools refs` (highest: 3 refs, production only; check_work_item_name: 1 ref; items: 20 refs, 5 production files). Tests: `by search` (no map), the one scenario test named in part 1.

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/workqueue.py:highest (62-65) | max n of `w<n>` names whose `items()` kind is work-item; the only caller is `add` (:82) | must cover every work-item's id/file under `.shop/work/`, not only `w<n>.md` names: a non-work-item `w<n>.md` must not block (D1); a work-item with a non-`w<n>` name and id w<n> must not be given that id (D4) | test_work_queue.py::test_add_numbers… (by search, passes) | refs |
| scripts/workqueue.py:items (93-98) | each `*/*.md` under `.shop/work/`, read through `read()` which refuses non-UTF-8 | `highest` inherits the refusal of any stray `.md` (D2) | none by search (scenario steps read `items` only via `add`) | refs |
| scripts/model_work.py:check_work_item_name (82-89) | r110: stem must be `w<n>`; `held` keyed by stem, not by frontmatter id | id uniqueness must key on the frontmatter id; the id must match the stem (D3) | design_model_check outline, 4 examples (by search, pass) | refs |
| tests/scenarios/design_model_check_problems.py:163-165 | the named-problem step drops r110 lines (`a work-item's file is named`, `is already held by`) for every fixture | narrowing it (N2) changes what that step counts | scenarios that use "it prints a file problem naming …" (by search) | search |
| scripts/migrate_upgrade_ids.py:98-107 | uses `items()`, numbers `w<n>` by initiative then name | read only: not changed by r12, but shares `items()` | none by search for w97 scenarios | refs |

## 4. Tests the requirements make impossible to keep

`by search`, no map. Tests that assert the current behaviour of the two functions above:
- test_work_queue.py::test_add_numbers… : passes as written; the requirement does not break it (checked: it only asserts `w5` after w1, w2, w4). Sound.
- test_design_model_check.py outline, 4 examples: passes as written; fixtures have id = stem, so the stem-keyed check and an id-keyed check agree. Sound.
- design_model_check_problems.py:163-165 (`it prints a file problem naming`): it filters r110 lines out of the count. It still passes today. If the plan narrows the filter to fixtures not named `w<n>.md` (N2), that step keeps its count for the other scenarios. Not impossible; the plan should check every scenario that uses it. None impossible found.

## 5. A step the work-item skips

`work add` skips the id check that `model check` makes (r110's held-id rule). `add` numbers by file name and writes the id without looking at other work-items' ids. Effect only `add` produces: a new work-item with an id another work-item holds, committed (`workqueue.py:229 committed`). Shown by the dup-id probe (run): `add` returns rc 0 with `w2`, and `model check` then reports the id three times with no held-id problem. The refusal `add` does give ("already exists") is by file name only.

## 6. Defects

Each is a probe above (run). Reproductions are the commands in section 2.

- D1 (work-queue#r12): `work add` refuses, naming `w2.md`, when `w2.md` is a plain note beside a work-item `w1.md`. Repro: r12 note w2. Expected by the requirement's wording: numbering over work-items, so w2 should be free. (Reading: the requirement could mean any `w<n>.md` file. Both readings are given in the plan's file set.)
- D2 (work-queue#r12): `work add` refuses on a non-UTF-8 `.md` note under `.shop/work/i1/`. Repro: r12 non-UTF-8. Judgement left to the plan: a note that is not a work-item should not block numbering.
- D3 (design-model-check#r110): `model check` prints no problem for two work-items holding one id when their stems differ. Repro: r110 held id, two stems; and id differs from stem (w3.md with id w9 prints nothing).
- D4 (work-queue#r12 with design-model-check#r110): `work add` gives a work-item the id a work-item named `fix-login.md` already holds. Repro: r12 fix-login id w7 (w7 is held, add prints w2) and the dup-id probe (add prints w2 while fix-login holds w2).

Reading left open (not a defect by my judgement): "one above the highest work-item" can mean the highest file `w<n>` (current) or the highest id. With fix-login.md holding w7, the current code prints w2; the id reading prints w8.

## 7. The file set

Production:
- scripts/workqueue.py (255 lines; room 45): `highest` counts ids or every work-item, skips non-work-item notes (D1, D4); `items`/`read` non-UTF-8 handling (D2). Found: refs, read.
- scripts/model_work.py (211 lines; room 89): `check_work_item_name` keys `held` by frontmatter id and checks id against stem (D3). Found: refs, read.
- scripts/model (137 lines; room 163): reads the frontmatter reader that model_work and workqueue use. Read only; changed only if the reader changes.
- scripts/model_parse.py (271 lines; room 29): `items` helper of parsing at :140; not on the r110 path (`refs` lists it for `items`). Read only.
- scripts/work (71 lines; room 229): entry, no change needed. Read.

Tests:
- tests/scenarios/design_model_check_problems.py (288 lines; room 12): the named-problem step (:163-165) that drops r110 lines (N2). Found: search. Narrowing it is the one test edit the work-item's N2 finding asks for.
- tests/scenarios/work_queue_add_steps.py (60 lines; room 240): no change for the accepted scenarios; new cases for D1/D2/D4 would add lines here. Read.
- tests/scenarios/test_design_model_check.py (53 lines; room 247): outline binding; no change needed. Read.
- tests/scenarios/design_model_check_then.py (221 lines; room 79): `it does not print a file problem` step; no change needed. Read.
- tests/scenarios/test_work_queue.py (277 lines; room 23): scenario binding; no change needed. Read.

Features (for new cases, not for the accepted scenarios): features/design-model-check.feature, features/work-queue.feature. Not edited by research.

Not in the accepted scenarios: N7 (an unreachable branch of `entry` in scripts/workqueue.py, :56-59). Not probed; it is in the same file, so the plan should know.

Sizes: `tools size` is not run here; the counts above are `wc -l`. All files are under 300.
