# Notes: migration-tools-1 (accepts r15, r18-r20, r22-r28)

Method: no coverage map (`tools tests-of` says "no map"; `tools map` is a full-suite run, not run), so every test list is `by search`. `tools refs` ran for `uncommitted` and `top_level`: 0 references, because `scripts/migrate` has no `.py` name; the callers are read by search (scripts/migrate:17, :32). `tools size --limit 300`: no file over the limit. Probes: `.shop/scratch/migration-tools-1-1-research/` (probe_status.py, probe_work.py, repos/). The checkout's git status was clean at start and end.

## 1. Why each accepted scenario is red today

Command: `python3 -m pytest -q --tb=short -p no:warnings -n 0 <19 node ids of tests/scenarios/test_migration_tools.py>` (run). Result: 16 failed, 3 passed. Then `... -k <names> --tb=line` (run) for the first undefined step of each. Pytest-bdd stops at the first undefined step, so later steps are also undefined: none of the new Whens or Thens exists (grep of tests/ for `plugin|upgrade|status|SessionStart|hook` finds no step text for them).

- r15 `migrate run` on the old system, tracked README changed / untracked notes/n2.md / README deleted (3 rows, not deprecated): red at Then "it exits with an error" (test_migration_tools.py:335). Only "it exits non-zero" (:215) exists. The code already refuses (scripts/migrate cmd_run, lines 32-35).
- r15 deprecated `migrate run` (3 rows): PASS. Same refusal.
- r15 `migrate upgrade` (3 rows): red at Given "a repository on the final layout whose plugin version is 0.23.1, with a work-item .shop/work/i1/a.md". Code: scripts/migrate has only `run` (argparse `choices` is `run`, scripts/migrate:55-59); no upgrade code.
- r18 `migrate status`: red at Given "a repository on the final layout whose .shop/plugin-version is 0.23.1". Code: no `status` subcommand; nothing in scripts/ reads `.shop/plugin-version` (grep: none).
- r19 no plugin-version: red at Given "a repository with .shop/ and no .shop/plugin-version". Code: none.
- r20 `migrate upgrade` applies step: red at Given "... .shop/plugin-version is 0.23.1, with a work-item .shop/work/i1/a.md". Code: none.
- r22 session offer: red at Given "a repository with .shop/ whose .shop/plugin-version is 0.23.1". Code: no hooks/ directory, no hooks.json (Glob: none); `.claude-plugin/plugin.json` declares no hooks; `.claude/settings.json` enables only superpowers.
- r23 session above: red at Given "... is 99.0.0". Code: as r22.
- r24 session on plugin version: red at Given "... is the plugin's version". Code: as r22.
- r25 numbering: red at Given "... .shop/plugin-version is 0.23.1" (work-items step). Code: none.
- r26 rename: red at the same Given. Code: none.
- r27 no pending step: red at Given "... is the plugin's version". Code: none.
- r28 no .shop/: red at Given "a repository without .shop/". Code: as r22.

Step modules that would hold them: none exists. `tests/scenarios/test_migration_tools.py` has Whens only for `migrate run` (line 38).

## 2. What the system answers today (probes)

- `python3 -m pytest -q -s -p no:warnings -n 0 .shop/scratch/migration-tools-1-1-research/probe_status.py` (run), `test_status_on_0231`: `migrate status` in a repo with `.shop/plugin-version` 0.23.1 → exit 2, `migrate: error: argument cmd: invalid choice: 'status' (choose from 'run')`. Git status clean after.
- `test_upgrade_on_0231` (run): `migrate upgrade` → exit 2, same error, one commit (`init`) only.
- `test_status_without_plugin_version` (run): `migrate status` on a repo with `.shop/` and no plugin-version → exit 2, same error (the r19 case, nothing answered).
- `test_run_on_final_layout_clean` (run): `migrate run --context example.org/acme/shop` on a clean final-layout repo (`.shop/work/i1/a.md`, plugin-version 0.23.1) → exit 0, nothing relocated, git status `A  spec/decisions/index.md`. Nearest case: `run` is not refused on a final-layout repo and writes the decisions index. The upgrade must not rely on `run` for this.
- `test_session_hook_inputs` (run): no `hooks/` dir, no `hooks/hooks.json`; plugin.json version 0.23.1.
- `probe_work.py`, `test_add_writes_what_name` (run): `work add i1 foo --part-of initiative/i1 --under capability/x --accepts x#r1` → exit 0, writes `.shop/work/i1/foo.md` with `id: work-item/example.org/acme/shop/foo`, commit `work add: i1/foo drafted`. No `w<n>` (see defect D1). A first try without a git identity (run, same probe before the fix) → exit 1 `work: git commit failed: Author identity unknown`, and `foo.md` was not left behind (the write was undone).
- `test_show_and_withdraw_on_w_names` (run): `work show` → `i1/w1 drafted`; `work withdraw w1` → `w1 withdrawn` and a commit; `work withdraw nosuch` → exit 1 `there is no work-item nosuch under .shop/work`. So names are looked up by file stem, and `w1` works today.
- Not probed (read): a rename collision in r26 (old `w2.md` becoming `w1.md` while `w1.md` becomes `w2.md`) needs two-phase renames; no probe was run.

## 3. Old assumptions

Places that assume a work-item's name is its file stem, the name the drafter typed, and that the id is `work-item/<ctx>/<name>`. Found by: `grep` for `.md"`, `.stem`, `log.jsonl`, `runs`, `blocked_by`, `depends_on`, then `tools refs` where a name exists (workqueue.add, workqueue.find).

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/workqueue.py:add (62-74) | writes `<name>.md`, id `work-item/<ctx>/<name>` | ids are `w<n>` (r25, r26 for old files; work-queue r1, r12 for new). Left as is: new items get the old form, see D1 | none (no test asserts the id; tests/scripts/test_work_withdraw.py uses `w1`) | read + probe |
| scripts/workqueue.py:items (81-86) | yields the stem as the name | after r26 the stem is `w<n>`, so `work show` prints `w<n>`: consistent | by search: tests/scenarios/test_work_queue.py, work_queue_git_steps.py (not read) | read |
| scripts/workqueue.py:move, agrees, find, withdraw, retry (108-204) | path `WORK/<initiative>/<name>.md`; find globs `*/<name>.md` | a typed old name stops resolving after the upgrade (`work withdraw size-check` refused); `w<n>` resolves | by search: tests/scripts/test_work_withdraw.py:30 (uses w1), tests/scenarios/work_queue_withdraw_steps.py | probe (w1 works, nosuch refused) |
| scripts/work_items.py:acceptors (60-65) | label of each work-item is `path.stem` (pytest `--work-item`) | label becomes `w<n>`; a `# ` heading keeps the old name (r26) | by search: tests/scripts/test_work_items.py (not read) | read |
| scripts/supervise.py (85-87) | commit paths `<name>.md`, `runs/<name>`, `log.jsonl` | after r26 the old names are gone; a run that was on an old name must not be upgraded mid-run (not checked by any scenario) | by search: tests/scenarios/test_supervision.py, supervision_given.py (not read) | read |
| scripts/supervise_worker.py (137-156) | run directory `.shop/work/<initiative>/runs/<work-item>/<k>-<stage>/`; log `work-item` field | r26 renames the directory and rewrites the log's `work-item` fields; the worker writes with the new name afterwards | by search: tests/scenarios/test_supervision.py (not read) | read |
| scripts/model_work.py (182-189) | `blocked_by` and `depends_on` names resolved by `qualify`, then `want(…, "work-item")` | a `blocked_by: size-check` left unrewritten becomes a dangling reference; r26 rewrites it | by search: tests/scenarios/design_model_check_given.py (uses `work-item/ghost`) | read |
| skills/migrating-to-capabilities/SKILL.md:111 | prints `work add <initiative> <name> ...` | a name argument, not the title the coordinator note asks for | none (documentation) | grep `work add` |

Not in the table: scripts/migrate_layout.py plan_moves (maps the old `work/` tree only; the upgrade starts from the final layout), and scripts/migrate_write.py (reused as is; see part 5).

## 4. Tests the requirements make impossible to keep

No map, so this is `by search`. The accepted requirements add commands, a hook and a step; they change no function the existing tests execute. Checked:
- tests/scenarios/test_migration_tools.py, the three deprecated r15 rows (run): pass today and must still pass; the upgrade adds subcommands only, and `run`'s refusal (scripts/migrate:32-35) stays.
- tests/scripts/test_work_withdraw.py:30 `workqueue.withdraw(tmp_path, "w1")`: uses `w1`, passes with the upgrade.
- The rest of test_migration_tools.py (the other 53 scenarios) and tests/scripts/test_migrate_write.py, test_migrate_layout.py: not run. They test `run`, which the accepted requirements do not change. Verdict: none found that can no longer pass; not verified by running.
- Searched for asserts of `work-item/<ctx>/<name>` ids in tests: none.

## 5. A step the work-item skips

`migrate run` checks uncommitted changes first (scripts/migrate:32-35) and never commits. `migrate upgrade` must check first (r15) and commit (r20). Existing ways of committing:
- `work add`, probe (run): without a git identity → exit 1 and `foo.md` removed again. The commit's failure undoes the write (workqueue commit path). The upgrade's commit needs the same: a failed commit must leave no renamed file (`read`: the migrate write() rollback is `git reset --hard HEAD` plus removing written files, migrate_write.py:119-125, which runs only for failures of the writing, not of the commit).
- `migrate_write.write` adds each written file with `git add -f` (migrate_write.py:108), so ignored files are added; the upgrade's commit must do the same for files it wrote or renamed (`read`).
- `git reset --hard HEAD` in write()'s rollback would discard the uncommitted changes that r15 forbids: harmless only because r15 refuses first. An upgrade that runs the step after writing must keep that order (`read`).

## 6. Defects

D1. `work add` names files and ids by the name given, not `w<n>` as spec/capabilities/work-queue.md r1 and r12 say.
Reproduction: `python3 -m pytest -q -s -p no:warnings -n 0 .shop/scratch/migration-tools-1-1-research/probe_work.py::test_add_writes_what_name`. Output: `work add -> (0, '', '')`, `files -> ['foo.md', 'initiative.md', 'w1.md']`, `frontmatter id line -> ['id: work-item/example.org/acme/shop/foo']`. Not an accepted requirement of this work-item; reported only.

## 7. The file set

Production and test files the work-item must change or add:
- scripts/migrate (63 lines, room 237): add `status` and `upgrade` subcommands (argparse choices, scripts/migrate:55-59); the `run` path unchanged. Found: read.
- scripts/migrate_upgrade.py (NEW): the upgrade steps list (0.24.0 "work-items named by ids"), `status` output, the r25/r26 renames, the commit with the step's name, r15 check reused from migrate_write.uncommitted. A new concern: CLAUDE.md module map needs a row.
- scripts/migrate_write.py (126 lines, room 174): read by the upgrade (uncommitted, git add -f); change only if the upgrade needs a commit helper. Found: read.
- scripts/migrate_layout.py (131 lines, room 169): read only, for `git mv` conventions; change not required. Found: read.
- hooks/hooks.json (NEW): SessionStart hook running `migrate status` from `${CLAUDE_PLUGIN_ROOT}/scripts`; (per the coordinator note). Found: Glob (none exists).
- hooks text/logic for r22, r23, r24, r28: produced by `migrate status` or a helper; decision left to the planner. Found: read.
- .claude-plugin/plugin.json (15 lines, room 285): version 0.23.1 → 0.24.0 is a question (Q1). Found: read.
- CLAUDE.md (27 lines): module map row for scripts/migrate_upgrade.py. Found: read.
- tests/scenarios/migration_upgrade_steps.py (NEW): the Givens/Whens/Thens of r18-r28 and r15 upgrade rows; a new module, since test_migration_tools.py is near its room (225 lines, room 75). Found: grep (no step text exists).
- tests/scenarios/test_migration_tools.py (225 lines, room 75): add an import of the new steps module (1-2 lines). Found: read.
- tests/scripts/test_migrate_upgrade.py (NEW, optional): unit tests of the steps' numbering and rename, if the planner wants them. Found: read.

Modules on the change's path, edited or not, with line counts and room under 300:
- scripts/migrate 63 (237); scripts/migrate_write.py 126 (174); scripts/migrate_layout.py 131 (169); scripts/migrate_spec.py 132 (168), not changed; scripts/migrate_ledger.py 123 (177), not changed.
- scripts/workqueue.py 243 (57), not changed; the upgrade's log.jsonl rewrite does not reuse it.
- scripts/work_items.py 109 (191), not changed.
- tests/scenarios/test_migration_tools.py 225 (75); tests/scenarios/migration_old.py 81 (219), not changed.

## Questions

Q1. r18 and r22 need a pending 0.24.0 step on a 0.23.1 repository. `.claude-plugin/plugin.json` says 0.23.1. Reading A: bump the plugin to 0.24.0 in this work-item. Reading B: keep 0.23.1, and no step is pending on any repository the scenarios build, so r18/r22/r25 cannot show the step. The planner chooses; I did not.
Q2. The coordinator note says `delivering-an-initiative` must say `work add <initiative> <title>`. The accepted requirements do not include it, and `work add` today takes `<name>` (D1). Left to the planner.
