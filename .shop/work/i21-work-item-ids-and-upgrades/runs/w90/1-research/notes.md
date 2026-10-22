# Notes: work-queue-5 (work-queue r1, r12)

Method: no `tools map` exists here (`tools tests-of` / `untested` refused: "no map"); I did not make one. Lists below are `by search` unless marked `refs`. `tools refs` ran on names it could see; it does not read `scripts/work` (no .py suffix), so its `0` for `workqueue.add` is wrong: `scripts/work:15` calls it.

## 1. Why each accepted scenario is red today

Run: `python3 -m pytest -q -n 0 -p no:cacheprovider "<node id>"` (run). Node ids: `tests/scenarios/test_work_queue.py::test_add_...`.

- **r1 deprecated** (`add with --part-of, --under and --accepts writes a drafted work-item with the fields given (deprecated)`): passes (run).
- **r1 new** (`add with a title, ... prints the id`): fails at its first Given, `an initiative i1 under .shop/work/`: StepDefinitionNotFoundError (run). No step matches that phrase; `no_item` needs `with no work-item {name}`. Later steps are also missing: `work prints one id w<n>, and nothing else` matches `prints_statuses` (test_work_queue.py:220-227), which splits on " with " and would fail; `.shop/work/{i}/w<n>.md is a drafted work-item whose id is that w<n>` has no step (`drafted` at :196 wants a literal name2); `its \`# \` heading is` has no step; `given_fields` (:202-205) reads `.shop/work/i1/w1.md`, not the printed id.
  - Code behind: `workqueue.add` (scripts/workqueue.py:62-78) writes `<name>.md` with id `work-item/<ctx>/<name>` and heading `<name>`; `scripts/work` `cmd_add` (scripts/work:14-16) prints nothing and returns 0.
- **r12** (`add numbers the new work-item one above the highest ...`): fails in its Given (run). `with_items` (test_work_queue.py:64-70) splits `w2 is green and whose work-item w4 is withdrawn` on " and ", so it writes `.shop/work/i2/whose work-item w4.md` (seen in the failure's context). Then `When` writes `Show the queue.md` (no number); Then `work prints w5` raises ValueError in `prints_statuses` (run: `ValueError: not enough values to unpack`). `whose id is w5` and `no other work-item's file has changed` have no step (by search: grep of tests/ finds neither).
  - Code behind: `workqueue.add` has no numbering; `items()` (workqueue.py:81-86) reads every `*/*.md` but nothing numbers.

## 2. What the system answers today (probes)

Probe files: `.shop/scratch/work-queue-5-1-research/probe_add.py`, `probe_numbering.py`; stores under the same scratch dir. Each run: `python3 -m pytest -q -s -n 0 -p no:cacheprovider <path>` (run). `work` = `scripts/work` of this worktree, `--root` a scratch store.

- **P1 title form, empty store** (`test_title_form_empty_store`): `work add i1 "Show the queue" --part-of capability-proposal/p1 --under thing --accepts thing#r1` → rc 0, stdout empty. Writes `.shop/work/i1/Show the queue.md`, id `work-item/ex.com/prod/ctx/Show the queue`, heading `# Show the queue`, commits it (`work add: i1/Show the queue drafted`). run.
- **P2 deprecated form** (`test_deprecated_form_w1`): `work add i1 w1 ...` → rc 0, no output, `w1.md`, id `.../w1`. Second `work add i1 w1 ...` → rc 1, stderr `work: the work-item w1 already exists (.shop/work/i1/w1.md); work add leaves it as it was`, nothing changed. run.
- **P3 numbering case** (`test_numbering_across_initiatives_and_statuses`): store i1 `w1` drafted; i2 `w2` green, `w4` withdrawn. `work add i1 "Show the queue" ...` → rc 0, file `Show the queue.md`, no number (r12 wants `w5`). `work show` → `i1/Show the queue drafted`, `i1/w1 drafted`, `i2/w2 green`, `i2/w4 withdrawn`. `work show --json` → `{"work-items": [{"work-item": "Show the queue", "initiative": "i1", "status": "drafted"}, ...]}`. run.
- **P4 nearest numbering cases** (`test_numbering_nearest_cases`): i1 holds `w9`, `w10` (work-items), `w50` (kind capability-proposal), `w70` (no frontmatter). Add with title → `Show the queue.md`, no number. Today nothing numbers, so the nearest cases for r12 are open (see questions). run.
- **P5 newline** (`test_newline_in_part_of_refused`): `--part-of "x<newline>status: ready"` → rc 1, `work: the value of --part-of has a newline in it; a work-item's field is one line`, nothing written. run.
- **P6 missing initiative** (`test_missing_initiative_refused`): `work add i9 ...` → rc 1, `work: the initiative i9 does not exist (no .shop/work/i9)`. run.
- **P7 show with non-UTF-8 file** (`test_show_with_non_utf8_file`): `w2.md` non-UTF-8 beside `w1` → stdout `i1/w1 drafted` (partial listing), stderr `work: .shop/work/i1/w2.md is not UTF-8 text`, rc 1, no traceback. run.
- **P8 add onto an existing w1 under the title form** (`probe_numbering.py::test_add_title_w1_when_w1_exists`): `w1` ready exists; `work add i1 w1 ...` → rc 1 refused, as P2. Under r12 the same call would write `w2.md`. run (today's answer only).
- **P9 add beside a non-UTF-8 file** (`test_add_with_non_utf8_file_elsewhere`): `w2.md` non-UTF-8 in i1; `work add i1 "Show the queue" ...` → rc 0, written. Today add reads no other file. run.
- **P10 add beside a w-named non-work-item** (`test_add_with_a_file_named_w_and_no_work_item`): `w7.md` with kind capability-proposal → add writes `Show the queue.md`, rc 0. run.

## 3. Old assumptions

Places that assume the name typed is the file stem, the heading and the id segment, or that `add` prints nothing. Tests column by search (`tools tests-of` has no map).

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/workqueue.py:add (62-78) | writes `<name>.md`, id `work-item/<ctx>/<name>`, heading `<name>`; returns the path | r1: file and id `w<n>`, heading = title; r12: `<n>` from the queue | test_work_queue.py: r1 deprecated (passes, run); r2/r7 deprecated (by search, not run) | read, probes P1-P2; refs `0` is wrong (see top) |
| scripts/work:cmd_add (14-16) | calls add, prints nothing | must print the id `w<n>` and nothing else (r1) | none (no test asserts add's output today) | read; scripts/work:15 |
| scripts/workqueue.py:items (81-86) | yields `path.stem` as the name; `show` prints `<initiative>/<stem>` | stems become `w<n>` for new items; old typed stems stay until the upgrade | test_work_queue.py r3/r11 scenarios (by search) | read, P3 |
| scripts/workqueue.py:find (187-192), refs `2` (workqueue.py:168, 197) | globs `*/<name>.md`; a title does not resolve | `w<n>` resolves, the title does not | tests/scripts/test_work_withdraw.py (uses `w1`, by search); tests/scenarios/work_queue_withdraw_steps.py (by search) | refs |
| scripts/workqueue.py:agrees, move, withdraw, retry (108-205) | path `WORK/<initiative>/<name>.md` | consistent with `w<n>` names; no change | tests/scripts/test_work_items.py:93 (`w1`, by search) | read |
| scripts/work_items.py:accepted (47-53), acceptors (57-66) | file stem is the work-item name for `--work-item` | `--work-item w5` works; a title name would not | tests/scripts/test_work_items.py (by search) | read |
| scripts/supervise.py (57, 87, 90, 108, 122, 144, 166, 195, 236), supervise_brief.py:21-22 | `name + ".md"`, `runs/<name>` from `items()` stems | consistent with `w<n>`; no change | test_supervision.py (by search, not run) | read |
| scripts/model_facts.py:check_id (73-77) and model_work.py:75 | checks the id's prefix only, not the stem | none: `w<n>` ids pass | none found by search | read |
| scripts/migrate_upgrade_ids.py:plan (67-88) (migrate step 0.24.0) | numbers existing items `w1..` by initiative order, renames stems | the same scheme as r12 once applied; before it, add's first `w1` can collide with a typed item the upgrade later renames to `w1` | tests/scenarios/migration_upgrade_steps.py (by search) | read |

## 4. Tests the requirements make impossible to keep

`tools tests-of` has no map; list by search: `tests/scenarios/test_work_queue.py` is the only file that runs `work add`. Other `work add` mentions are a docstring (work_queue_git_steps.py:1) and a comment (test_work_queue.py:42).

- **test_work_queue.py: r2 deprecated** `add when the work-item's file already exists leaves the file as it was (deprecated)`: today passes (by search; deselected in this run, see note). Under r12 `work add i1 w1` on an existing w1 writes `w2.md`; `as it was` also compares the whole snapshot (test_work_queue.py:208-212), so it fails. Requirement: r1 and r12. Mechanism: `add` numbers instead of refusing.
- **test_work_queue.py: r7 deprecated** `add when the work-item's file already exists is refused, saying so` (by search): under r12 the call writes `w2.md` and exits 0, so "already exists" is not said. Same mechanism. Probe P8 shows today's refusal.
- **Conflict, both readings:** (a) they are `Deprecated for: removal`, so the plan retires them; (b) they stay and the title form refuses a name that exists. The plan decides; I only give both.
- **test_work_queue.py: r1 deprecated**: stays green under the new code only if `add i1 w1` in an empty store writes `w1.md` with id `w1`. Its Then checks file and fields, not the heading. Verified by reasoning from P2, not run after a change.
- **test_work_queue.py: `given_fields` (202-205) and `prints_statuses` (220-227)**: not impossible to keep, but the deprecated r1 relies on `given_fields`'s `w1.md`. Changing them must keep that.
- `tests/scripts/test_work_withdraw.py`, `test_work_items.py`, `work_queue_withdraw_steps.py`: write `w1` files directly; not run here; by search they do not call `add` and keep passing.
- Checked and sound: P2 and P1 already show the add path's file and fields; `committed` (r9) unaffected by numbering.

Note on the run: a `pytest -q tests/scenarios/test_work_queue.py` collects 3 of 28 (`25 deselected`). `pytest.ini` addopts (`-m "not fixture"`) and the repository's conftest do not deselect. I read this as the work-run environment selecting the accepted scenarios (read; not verified). So the deprecated r2/r7 scenarios were not run; their status is from P2/P8.

## 5. A step the work-item skips

The new `add` path must number from every work-item under `.shop/work/`. Today's `add` reads no other file; its only reads are the initiative directory, `spec/index.md` (`context_path`), and the target path.

- **Refusals that numbering adds** (read; P9 shows none today): reading a non-UTF-8 file beside the new write refuses with `is not UTF-8 text` (`read()`, workqueue.py:48-53), or skipping it must be decided. `items()` already shows P7's partial output before that refusal. A file whose frontmatter cannot be parsed would reach `frontmatter` (read).
- **Effects only the numbering step produces:** none today except the commit. The `path.exists()` check (workqueue.py:72) guards only the title's path; two concurrent `add`s with the same number race between the check and `write_text` (read; no lock).
- **The skipped refusal:** today's "already exists" refusal (workqueue.py:72-73) cannot happen for the title form, because the name is a new title each time. P8 shows it for the deprecated form only.

## 6. Defects

Only what I ran.

- **D1: `work show` prints a partial listing before it refuses a non-UTF-8 file.** Reproduce: scratch store with `i1/w1.md` drafted and `i1/w2.md` = `\xff\xfe---\nkind: work-item\n---\n`; `work show`. Came back: stdout `i1/w1 drafted`, stderr `work: .shop/work/i1/w2.md is not UTF-8 text`, rc 1 (P7). Not a traceback. Not judged.

Not a defect today, but the requirement changes it: P1 writes a title with spaces into the id `work-item/ex.com/prod/ctx/Show the queue`.

## 7. The file set

Production:
- `scripts/work` (71 lines; room 229): `cmd_add` prints the id that `add` returns (r1). Search: scripts/work:14-16.
- `scripts/workqueue.py` (243; room 57): `add` numbers `w<n>` from the queue (r12), writes the title as heading and id `w<n>`, returns the id (r1). Read and P1-P4. Its `entry` check on `name` is then for the initiative only.

Tests:
- `tests/scenarios/test_work_queue.py` (283; room 17): `with_items` (64-70) to take `whose work-item w4 is withdrawn`; `given_fields` (202-205) to read the printed id's file; `prints_statuses` (220-227) for the `one id w<n>` form, or move it to a new step. Room is 17, so new steps must not add much here.
- `tests/scenarios/work_queue_add_steps.py` (new; the `<capability>_*_steps.py` pattern of CLAUDE.md's tests/scenarios row): steps for the r1 and r12 phrases the file does not have.

On the change's path, not edited (with line counts and room):
- `scripts/model` (137; room 163): the frontmatter reader workqueue loads.
- `scripts/work_items.py` (109; room 191): `--work-item` by stem.
- `scripts/supervise.py` (263; room 37), `scripts/supervise_brief.py` (97; room 203), `scripts/supervise_merge.py` (132; room 168): name + `.md` and `runs/<name>`.
- `scripts/model_facts.py` (265; room 35), `scripts/model_work.py` (200; room 100): ids, not stems.
- `tests/scenarios/conftest.py` (176; room 124): `full`, `INDEX`, the `run` fixture.
- `tests/scenarios/work_queue_git_steps.py` (59; room 241), `tests/scenarios/work_queue_withdraw_steps.py` (64; room 236), `tests/scripts/test_work_withdraw.py` (32), `tests/scripts/test_work_items.py` (98; room 202).

`tools size --limit 300` printed no file over 300 (run; the output was empty).

## Questions for the plan (both readings given)

1. Deprecated r2 and r7 (`add` on an existing `w1`: leave as it was / refused) conflict with r12's numbering. (a) retire them (`Deprecated for: removal`); (b) keep them, and the title form refuses an existing name.
2. r12's "any work-item": does a `w<n>.md` without `kind: work-item` (P4's `w50`, `w70`) count? (a) only `kind: work-item` files, as `items()` reads; (b) any `w<n>.md`.
3. A non-UTF-8 file under `.shop/work/` when `add` numbers: (a) `add` refuses, naming it; (b) skips it.
4. An unupgraded store: `add` numbers from 1 beside typed names, and the 0.24.0 upgrade later numbers from 1 as well (migrate_upgrade_ids.py:67-88). Not probed. (a) the upgrade must run first; (b) add must read typed names too.
