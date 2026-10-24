# w123 research notes: work status and work note

Accepted: work-queue r16-r21 (features/work-queue.feature, six scenarios, 12 test ids with the Outline's 7 examples).
Method: `tools tests-of` has no map here (`tools map` not made); `tools refs` ran. Otherwise search by text.
Probes: `.shop/scratch/w123-1-research/probe_work.py`, `probe_model.py` (scratch stores only).

## 1. Why each scenario is red today

Command for all: `python3 -m pytest -q --tb=short -p no:warnings tests/scenarios/test_work_queue.py -k "status_of or status_with or note_"`: 12 failed, each at its first undefined step (run).

- r16 status of an initiative: first failure Given "an initiative i1 under .shop/work/ that is neither done nor abandoned, whose capability-proposal p1 is approved" (feature 242), StepDefinitionNotFound (run). Undefined after it (read): feature 243-248 Givens (question-bearing work-item, uncommitted/untracked files, ledger of twelve lines); Thens 250-256 "work prints i1's status", "it prints p1 with approved...", "it prints i1-delivery and that the remote does not have...", "it prints spec/index.md and notes.txt, and nothing about scratch.log", "it exits successfully". Code: no `status` subcommand in `scripts/work` (its subparsers, lines 53-69, have none); no status reader in `scripts/workqueue.py`.
- r17 status with no initiative: first failure Given at feature 261 "...whose work-item w1 is drafted" (run). Also undefined (read): Givens 262-264; Then "work prints what `work status i1` prints and what `work status i2` prints" (the existing `prints_statuses` in test_work_queue.py:221 needs " with "). Code: as r16, plus no enumeration of initiatives for `status`.
- r18 status --json: first failure Given at feature 272 (run). Then "it gives i1's status and w1 with drafted" (feature 275) does not fit the existing `gives` step (work_queue_withdraw_steps.py:58-64): it splits on " in ", and this text has none, so it would raise ValueError (read). "work prints one JSON object and nothing else" is defined (withdraw_steps:39). Code: no `--json` on status.
- r19 note appends: first failure Given at feature 280 "an initiative i1 ... whose ledger .shop/work/i1/ledger.md has one line" (run). Undefined (read): Then ".shop/work/i1/ledger.md has two lines, the first as it was" (feature 282; `two_lines` in test_work_queue.py:241 is for log.jsonl only) and "its last line has the text ..., with the date the command was run" (283). The When "the session runs `work note ...`" matches the existing `run_work` (test_work_queue.py:173). Code: no `note` subcommand (`scripts/work` subparsers, lines 53-69; dispatch 70-73).
- r20 note commits: first failure Given at feature 288, the ledger Given (run). Then "main has a new last commit, which holds .shop/work/i1/ledger.md as work left it" (289-291) and "nothing under .shop/work/ differs from main's last commit" (292): defined in work_queue_git_steps.py:47-59, but test_work_queue.py imports only `init` from that module; the withdraw module's regex needs " and " so it does not match. Likely undefined in this module (read; confirm once the Given is defined). "the repository is a git repository on the branch main, everything in it committed" (289) is defined (git_steps:39).
- r21 note with line break (Outline, 7 examples): first failure Given at feature 297 (run, all 7 ids). Then "the session runs `work note i1` with a line of two lines broken by <line break>" (299) does not match `run_work_newline` (test_work_queue.py:179, needs "with a newline and ... in the {option} value") (read). Then "work exits with an error, saying that a note is one line" (300), ".shop/work/i1/ledger.md is as it was" (301; `both_as_they_were` needs " and ... are as they were"), "main's last commit is the one it was" (302): all undefined (read).

## 2. What the system answers today

Probes, `run` (probe_work.py, probe_model.py; `python3 -m pytest -q -s -n 0 -p no:warnings <file>`):
- `work status i1` on a store with i1 and w1: exit 2, "argument cmd: invalid choice: 'status' (choose from 'add', 'show', 'withdraw', 'run', 'retry', 'answer')". run.
- `work note i1 "next: plan w2"`: exit 2, "invalid choice: 'note'". run.
- `work show` on the same store: exit 0, "i1/w1 awaiting-answer". run.
- Nearest case, ledger present: `.shop/work/i1/ledger.md` with 12 lines beside w1: `work show` and `work show --json` print only w1 (exit 0). run. Ledger is skipped by `show` because it has no `kind: work-item`.
- The existing one-line refusal (the template for r21): `work answer w1 "a<X>b"` on an awaiting-answer w1, for X in LF, VT, FF, CR, NEL, U+2028, U+2029: each exit 1, "the answer has a line break in it; an answer is one line"; commit count unchanged (1 -> 1); w1 still awaiting-answer. run, all 7. `LINE_BREAKS` in workqueue_answer.py:12 holds exactly those 7 code points (0xa, 0xb, 0xc, 0xd, 0x85, 0x2028, 0x2029): run (printed).
- Nearest case, commit cannot land: `work add i1 title ...` in a store whose git add is refused: exit 1, "git add failed: paths are ignored", and w2.md is not left behind (run). Caveat: the probe store sits under the worktree's ignored `.shop/scratch/`, so the refusal comes from the location; the restore-on-failure effect is what the probe shows.
- `model check` on a store with a valid initiative and w1, with and without `ledger.md`: without, 1 file problem; with, 2 file problems, the new one "file: .shop/work/i1/ledger.md: needs an id and a kind among capability-proposal, ..., work-item" (run, probe_model.py). See section 3, row 1.
- Empty store (no initiatives), `status` with no argument: not probed; the command does not exist (see above).

## 3. Old assumptions

The requirements add; none replaces an existing form. The one place a new file breaks an assumption is the initiative directory: it held only parts, `initiative.md` and `log.jsonl`. `ledger.md` (r19) is a new `*.md` there.

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/model_work.py:123 `read_work` loop over `idir.glob("*.md")` -> `read_part` (line 127) | reads every `*.md` but initiative.md as a part; no id+kind -> problem | ledger.md becomes a "file problem": `model check` reports it (run, probe_model.py); r19 makes this happen on every note | by search: features/design-model-check.feature scenarios on initiative dirs (none holds a ledger) | search (glob) and probe |
| scripts/workqueue.py:102 `items` and :65 `highest` (`glob("*/*.md")`, kind == work-item) | skips files without kind work-item | ledger.md skipped; no change needed | by search: test_work_queue.py show and add steps; no tests/scripts test calls `items` | search; `show` with ledger run in probe |
| scripts/work_items.py:50 `accepted`, :60 `acceptors` (globs, kind check / name match) | reads work-items for --work-item | ledger.md skipped (kind check; name glob) | by search: tests/scripts/test_work_items.py; no test calls `accepted` or `acceptors` by name | search |
| scripts/migrate_upgrade_ids.py:41 (`glob("*.md")` with `front_kind == "work-item"`) | lists work-items of an initiative for migration | ledger.md skipped | none: by search, no test names migrate_upgrade_ids or front_kind | search |
| scripts/supervise.py:77 `check` (git status under .shop/work; refuses when uncommitted) | `work run` refuses to start with any uncommitted .shop/work change | a note not committed (r20 fails) makes `work run` refuse | by search: features/supervision.feature (uncommitted .shop/work changes) | read |
| scripts/supervise_faults.py:91 `checkout_changes` (puts back uncommitted .shop/work paths during a worker's end) | reverts any uncommitted .shop/work change not run's own | a note written but not yet committed during a run is reverted; committing at once avoids it | by search: features/supervision.feature:590 (uncommitted initiative.md in checkout) | read |

## 4. Tests the requirements make impossible to keep

Searched by text (no map). Ran tests/scripts/test_work_add_title.py, test_work_item_ids.py, test_work_items.py, test_work_withdraw.py: 17 passed (run). Searched tests for `choose from|invalid choice` (none), `needs an id|kind among` (none), and `ledger` in test files (only the accepted scenarios and migration's decisions ledger, unrelated). Result: none of the existing tests can no longer pass as they are. read: the `model check` scenarios that exist do not put a ledger in an initiative directory, so they keep passing.

## 5. A step the work-item skips

Existing way: `work add`, `retry`, `withdraw`, `answer` change files through `workqueue.committed()` (workqueue.py:236): refuse when git cannot commit, write, `git add` and commit the paths only, restore the files when the commit fails.
- `note` must commit (r20) through the same step. Its refusal and effect, shown by probe on `add` (run): exit 1, git's first line, the written file removed (w2.md absent). Only that step produces the restore; a note that skipped it would leave a ledger line uncommitted, and `supervise.check` (supervise.py:77) then refuses `work run`.
- The initiative-exists check (`add`, workqueue.py:85) and the name check (`entry`, :56): read. `note` must refuse an unknown initiative the same way (no initiative directory, no ledger to create). Effect of skipping: a ledger created under a non-existent directory.
- Writing the ledger line: the existing way writes through `append()` (workqueue.py:153), whole or truncated back on error (the r7 case in test_work_queue.py `log_cannot_be_written`, a scenario; read). A note written with plain write/append would not have that.
- `status` is read-only; it skips `agrees()` (r6, workqueue.py:169). `items()` (used by `show`) also skips it, so `status` would print the file's status even when log.jsonl disagrees. read.

## 6. Defects

None shown by today's probes. Checked: the answer line-break refusal (7 of 7 refuse, nothing changes), `show` with a ledger present, `add`'s restore on a failed commit. The `model check` extra file problem (section 2) is what r19 would create, not a present defect.

## 7. The file set

Must change for the accepted scenarios and to keep the rest passing:
- scripts/work (80 lines; room 220): `status` and `note` subcommands in `main` and the dispatch dict (lines 53-73).
- scripts/workqueue.py (262; room 38): no room for status; `note` may go here only if it stays under 300. Plan: new modules.
- scripts/workqueue_status.py (new): r16-r18 readers: initiatives, capability-proposals, work-items with open questions (the `## Questions`/`## Answers` split as supervise.py:177-180 does), branch and remote check (as supervise_faults.py:20-62), `git status` as supervise.py:77, ledger tail. New concern: needs a CLAUDE.md module-map row.
- scripts/workqueue_note.py (new, ~40 lines): r19-r21: line-break check reusing workqueue_answer.LINE_BREAKS (workqueue_answer.py:12); initiative check; append via workqueue.append; commit via workqueue.committed. New concern: needs a CLAUDE.md row.
- CLAUDE.md (module map): one row each for the two new modules.
- tests/scenarios/test_work_queue.py (284; room 16): import the two new step modules (one line each).
- tests/scenarios/work_queue_status_steps.py (new): the r16-r18 Givens and Thens listed in section 1.
- tests/scenarios/work_queue_note_steps.py (new): the r19-r21 Givens, Whens and Thens; includes the step text that matches the Outline's <line break>.

Not required by an accepted scenario (plan decides, see questions below): scripts/model_work.py (213; room 87) line 123 to skip ledger.md; scripts/supervise.py (218; room 82) and scripts/supervise_faults.py (160; room 140) if status reuses `held`/`questions` (supervise.py:164-180) or `remote`/`push` logic (supervise_faults.py:20-62) rather than copying.

On the change's path (edited or not), with lines and room under 300:
- scripts/workqueue.py 262 (room 38); scripts/workqueue_answer.py 48 (252); scripts/model 137 (163, loaded by workqueue._load_model); scripts/work_items.py 109 (191); scripts/model_work.py 213 (87); scripts/supervise.py 218 (82); scripts/supervise_faults.py 160 (140).
- tests/scenarios/test_work_queue.py 284 (16); work_queue_git_steps.py 59 (241); work_queue_withdraw_steps.py 64 (236); work_queue_add_steps.py 60 (240); work_queue_answer_steps.py 32 (268); conftest.py 176 (124).
Line counts from `wc -l`. The size check (`tools size --limit 300`) not run.

## Questions for the plan (both readings given)

1. The initiative branch for status. spec/index.md:105 defines it as the branch `work run` commits on; supervise.py:74 takes the checkout's HEAD. Feature 244 names `i1-delivery` without checking it out. Reading A: status uses the checkout's HEAD. Reading B: the name is recorded somewhere (for example initiative.md) and status reads it.
2. The ledger line format: r19 says "with the date", and r16 says the note is the text after the date. Format undecided (date form, separator).
3. The `--json` shape. Feature 275 "it gives i1's status and w1 with drafted" fits no existing step; the existing `gives` expects "name in initiative with status". Reading A: a new step matching the feature. Reading B: change the feature wording (a spec change).
4. `model check` and ledger.md (section 3). Reading A: model_work.read_part skips ledger.md. Reading B: the ledger lives under a name that is not `*.md`.
5. The r20 Then steps (section 1): read as likely undefined in test_work_queue.py. Confirm once the Givens are defined.
