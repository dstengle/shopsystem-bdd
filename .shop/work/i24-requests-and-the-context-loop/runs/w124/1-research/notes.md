# w124 research notes

Scope: migration-tools r24, r32, r33, r34 (accepted); r24 deprecated scenario retired. Base f890f2f. Scripts: `python3 /home/vscode/shopsystem-bdd/scripts/tools`. No coverage map exists (`tests-of`: "no map"), so every test list below is `by search`, and `refs` is the tool's answer. `refs` gives 0 for dotted `workqueue_status.status` and `workqueue_note.note` though `scripts/work` calls them (by search: `scripts/work:48,53`).

Probe files: `.shop/scratch/w124-1-research/probe_hook_status.py`, `probe_status_edges.py`, `probe_note_and_upgrade.py`. Run as `python3 -m pytest -q -s -n 0 -p no:cacheprovider <path>` (`-n 0`: xdist hides prints).

## 1. Why each scenario is red today

Run: `python3 -m pytest -q -n 0 "tests/scenarios/test_migration_tools.py::<name>"` (node ids from `--collect-only`). All four fail at a step with no definition (run):

- r24, done/abandoned: `test_a_session_starting_in_a_repository_on_the_plugins_version_whose_every_initiative_is_done_or_abandoned_is_told_nothing`. StepDefinitionNotFoundError for Given "its initiatives are i1, which is `done`, and i2, which is `abandoned`" (feature line 473). Missing: the Given only (reuse `test_work_queue.initiative`). The code already gives the expected answer: probe 1 hook output is empty. This one can go green with the Given alone.
- r32: `..._with_initiatives_neither_done_nor_abandoned_is_given_what_work_status_prints_for_each_of_them`. Undefined Given (line 572). The Then "gives the session what `work status` prints for i1 and for i2" (line 574) and "gives the session nothing of i3 or i4" (575) are undefined too (read: no step text matches in tests/). Code missing: `scripts/migrate_upgrade.py:session_text` (71-87) adds no work status; the hook command in `hooks/hooks.json` runs only `migrate status --hook`.
- r33: `..._appends_compacted_with_the_time_...`. Undefined Given (line 580) and When "a session in it is about to be compacted" (582, read: no step). Code missing: no PreCompact entry in `hooks/hooks.json` (read: only `SessionStart`); no code writes `compacted`.
- r34: `..._is_told_to_write_its_handoff_with_work_note_and_end`. Undefined Given (line 589) and When (590). Code missing: the PreCompact hook entry and its text ("write its hand-off with `work note`", "end instead of being compacted").

## 2. What the system answers today

Probe 1, `probe_hook_status.py` (run, `python3 -m pytest -q -s -n 0 .shop/scratch/w124-1-research/probe_hook_status.py`). Hook = `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/migrate" status --hook`, run as the step does.

| case | result (run) |
|---|---|
| 0.25.0, i1 `proposed`, i2 `done` (r32 shape) | stdout `''`, rc 0. Today's answer is nothing. |
| 0.25.0, i1 `done`, i2 `abandoned` (r24 shape) | stdout `''`, rc 0 (matches r24) |
| 0.23.1, i1 `proposed` | the upgrade offer only: "This repository is on plugin version 0.23.1 and the plugin is on 0.25.0. Offer the person the upgrade ... only on the person's yes." |
| `.shop/plugin-version` empty, i1 `proposed` | "Tell the person that .shop/plugin-version holds no version, and that it is empty." only |
| `work status` (default), i1 `proposed`, i2 `ready`, i3 `done`, i4 `abandoned` | prints i1 and i2 blocks, each with `branch master: the remote cannot be compared with it`, `uncommitted: none`, `untracked: none`, `ledger:`, `last next: none`. Not i3 or i4. rc 0 |
| `work status i3` (done) | prints the i3 block (a named initiative is shown even when ended) |
| `work status` run from `notes/` inside the repository, i1 `proposed` | stdout `''`, rc 0 (see defect D1) |
| no commit at all, i1 `proposed` | `work status` prints i1 and lists the three fixture files as untracked; hook prints `''` (0.25.0 with nothing pending) |
| i9 directory with no `initiative.md` | ignored by `work status`; hook `''` |

Probe 2, `probe_status_edges.py` (run):

| case | result (run) |
|---|---|
| `initiative.md` with no frontmatter | `work status`: "initiative i1 None", counted as open; hook `''` |
| `initiative.md` with frontmatter but no `status:` | same: "initiative i1 None" |
| `initiative.md` not UTF-8 | `work status`: rc 1, "work: .shop/work/i1/initiative.md is not UTF-8 text", no output; the hook (no call to `work status` today) rc 0, `''` |

Probe 3, `probe_note_and_upgrade.py` (run):

| case | result (run) |
|---|---|
| `work note i1 "hand-off line"` with another untracked file present | rc 0; new commit "work note: i1" touching only `.shop/work/i1/ledger.md` (created it, 1 line); `unrelated.txt` still untracked |
| `work note i7` (no such initiative) | rc 1, "work: the initiative i7 does not exist (no .shop/work/i7)"; no file made |
| bare append of `- 2026-10-24 22:35: compacted` to ledger.md, then `migrate upgrade` on a 0.23.1 repo | rc 1, "migrate changed nothing; it could not start from a tree with an uncommitted change: .shop/work/i1/ledger.md" |
| `work status i1` after a bare `compacted` line with a time | prints the line in the ledger section; `last next: none`; no crash |

Nearest cases not in the scenarios, read (not run):
- `.shop/` present, no `.shop/work/`: `work.glob` yields nothing, hook prints nothing (read: `session_text` never touches work/ today; `workqueue_status.read` only for listed initiatives).
- ledger.md absent for an open initiative: `ledger()` returns `[]` (read `workqueue_status.py:75-79`).
- `compacted` written twice: no de-duplication anywhere (read: `workqueue_note.note` and a bare append both append).
- an open initiative with work-items in `awaiting-answer`: `work status` lists their questions (read: `parts`, `workqueue_status.py:43-46`).

## 3. Old assumptions

Requirements in play: r24 (on-version, nothing ended-only), r32 (SessionStart gives `work status` for open initiatives), r33/r34 (new PreCompact hook, ledger line with time, hand-off text). Table from `tools refs` (session_text, status, run, ledger), callers read, and search.

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/migrate_upgrade.py:session_text (83-84) | returns `""` when no step is pending and the version is not above the plugin's: "told nothing" is the on-version case | r24 and r32: must also return `work status` text when an initiative is neither done nor abandoned; `""` only when neither applies | test_migration_tools: r24 done/abandoned, r24 retired, r28 (hook, `tells the session nothing`), once Givens exist | tools refs session_text (1 caller, scripts/migrate_upgrade.py:168); read |
| scripts/migrate_upgrade.py:run (167-169) | the hook entry: `if hook: write session_text(root); return 0`, the one SessionStart command | r32 adds work status; r33/r34 need a second hook entry, not this one | every SessionStart scenario (r22, r23, r28, r31, r24, r32) | tools refs run; read |
| scripts/migrate_upgrade.py:status (59-68) | prints versions and pending steps for `migrate status`, not the hook | none: r18 unchanged, but the hook must not reuse its exit status (refusal rc 1) | test_migration_tools r18/r19/r30 `migrate status` | tools refs status; read |
| scripts/migrate:61-62 and docstring line 5 | `status --hook`: "print what a session is told at its start, and exit 0" | the contract text is now false: the hook also prints work status and must exit 0 when `work status` refuses (probe 2 UTF-8 case) | none (argparse help) | read |
| hooks/hooks.json (whole file) | one SessionStart command only; no PreCompact key | r33/r34 need a PreCompact entry; r32 may add the work status call here or in migrate | every hook scenario reads it | read; grep PreCompact: none in the repository |
| tests/scenarios/migration_upgrade_steps.py:127-133 (the hook When) and tests/scenarios/migration_version_steps.py:29-35 (`a session starts in the repository`) | both run `hooks["SessionStart"][0]["hooks"][0]` only | a second SessionStart command, or a PreCompact entry, is not run by these helpers; the tests stay green but cover nothing new | every SessionStart scenario | by search (grep `hooks[0]`) |
| scripts/workqueue_status.py:status (110-129) and ENDED (13) | `work status` is read-only, default root `.`; the only "neither done nor abandoned" filter | r32 reuses it: the default-root `.` makes a session from a subdirectory see nothing (D1); a refusal (D3) becomes the hook's text | work_queue_status_steps.py (status scenarios); by search | tools refs status (31 refs, 7 production); read |
| scripts/work:52-53 (`cmd_status`) and `--root` default "." (line 62) | `--root` defaults to cwd | the hook runs in the session's cwd; it must pass the top level, as migrate's `top_level` does | none for the hook | read; probe `work status` from notes/ |
| scripts/workqueue_status.py:DATED (14) and ledger (75-79) | ledger lines are `- YYYY-MM-DD: text`; the last ten lines shown; `next:` detected by DATED | a `compacted` line "with the time" does not match DATED (no crash, probe); each compaction takes one of the ten shown lines | work_queue_status_steps.py ledger scenarios (`ledger_of_twelve`, line 72) | read; probe `work status i1` after compacted line |
| scripts/workqueue_note.py:note (10-21) | the only writer of ledger.md: date-only line, `committed()` commit, LINE_BREAKS and entry checks | r33 says "with the time": the same format cannot carry it; a commit is not required by r33 but is what `work note` does | work_queue_note_steps.py (note scenarios) | tools refs ledger; read |
| scripts/workqueue.py:append (153-166) and committed (236-251) | append is O_APPEND atomic; committed commits only named files and restores on failure | a PreCompact append may call append alone (no commit) or committed (commit): the plan's choice; probe shows a bare append blocks `migrate upgrade` | work_queue_note_steps.py; work status/retry tests (`tools refs workqueue.append`: 3 production, 0 test) | tools refs workqueue.append; probe 3 |
| scripts/migrate_write.py:uncommitted (26-29) via migrate_upgrade.py:122 and migrate:35 | refuses migrate run/upgrade when the tree has any change | a bare `compacted` append leaves the tree dirty; the next `migrate upgrade` refuses (probe 3) | migration_safety_steps.py (r15 scenarios); by search | grep `uncommitted` in scripts/ (migrate_write, migrate_upgrade, migrate); probe 3 |
| tests/scenarios/migration_upgrade_steps.py:224-226 (`tells the session nothing`) | asserts `returncode == 0` and stdout `""` | still correct for the two r24 cases and r28 once the work status text is added only for open initiatives | r24 done/abandoned, r24 retired, r28 | by search |

## 4. Tests the requirements make impossible to keep

Searched by search (no coverage map). I read the step modules the hook and ledger tests use, the feature's Givens and Thens for each hook scenario, and `session_text`'s outputs; I did not read each test body:

- test_migration_tools.py `..._on_the_plugins_version_is_told_nothing_deprecated` (r24, retired): its Given has no initiative, so the new hook still prints `''`. It passes after the change, and the retirement removes it. Verdict: retire as the work-item says; nothing else changes.
- `..._whose_every_initiative_is_done_or_abandoned_is_told_nothing` (r24, accepted): correct under r24; the Given is undefined today (section 1). Keep. Sound: an ended-only repository must print nothing from `work status`.
- r28 `..._without_shop_is_told_nothing`: no `.shop/` means `session_text` returns before any work status is read. Keep, sound.
- r22, r23, r31 (hook Thens: offer, update, tell-the-person): their Givens have no initiatives, so the appended work status text does not change their `in stdout` checks. Keep, sound.
- r30 (`migrate status`/`upgrade` refusal): not on the hook path; unaffected.
- work_queue_status_steps.py and work_queue_note_steps.py: they test `work status` and `work note` directly; unaffected while `status()`, `note()` and the DATED format are unchanged. If the plan changes `ledger()` or DATED, the ledger-of-twelve scenarios (line 72-125) need re-reading.
- No test asserts that an open initiative gets nothing from the hook: none found (search for `tells the session nothing` finds only the three r24/r28 scenarios).

Nothing an accepted requirement makes impossible, beyond the retired scenario. The hook helpers' `hooks[0]["hooks"][0]` (section 3) keep passing but would not run a second command: blind, not broken.

## 5. A step the work-item skips

PreCompact append (r33) against `work note`, the existing way for a ledger line. Effects only `work note` produces, each by probe 3 (run) or read:

- commits the ledger alone ("work note: i1", run); a bare append leaves the file uncommitted, and `migrate upgrade` then refuses (run: rc 1, naming `.shop/work/i1/ledger.md`).
- refuses an initiative that does not exist, with a message and nothing written (run: rc 1 for i7). A bare append to a missing directory fails in the OS (read: `append` opens with O_CREAT, no directory check).
- refuses a line break in the note (read: workqueue_note.py:13-14, LINE_BREAKS); `compacted` has none, so the check is not needed for r33 but is skipped silently.
- checks the name with `workqueue.entry` (read: workqueue.py:56-59; refuses `..`, `/`).
- rolls the files back when git cannot commit (read: workqueue.py:236-251, `committed`). A bare append has no rollback.
- `workqueue.committed` first checks the repository can commit (`rev-parse --is-inside-work-tree`, read).

The hook's own steps that a call to `work status` from the hook skips (read/run):
- the top level: `work status` defaults to cwd `.`; run from `notes/` it prints nothing (D1). `migrate`'s hook uses `top_level`, `work` does not.
- exit status: `migrate status --hook` always exits 0 (migrate_upgrade.py:159-169 docstring). `work status` exits 1 on a non-UTF-8 initiative.md (run, probe 2). Passing that rc through breaks the hook's contract.
- `status --hook` in a repository with no git commit: `migrate` gets top level, but `work status` lists everything as untracked (run, probe 1, no-commit case). The text is noisy, not wrong.

## 6. Defects

D1. `work status` from a subdirectory prints nothing although initiatives are open.
  Commands: create a repository with `.shop/work/i1/initiative.md` (status `proposed`), `mkdir notes`, then run `python3 <worktree>/scripts/work status` in `notes/`, and in the root.
  Came back: in `notes/`, `rc=0 stdout=''`. In the root, the i1 block.
  Reproduced by `probe_hook_status.py::test_work_status_from_subdirectory` (run). The docs say the default is the current directory, so this is documented behaviour; the defect is silence, not a refusal. Shown because the hook will call this command.

D2. `work status` lists an initiative whose `initiative.md` has no status as open, printed as `None`.
  Commands: `.shop/work/i1/initiative.md` with `---\nid: ...\n---` (no status), then `python3 <worktree>/scripts/work status`.
  Came back: `initiative i1 None`, rc 0. Reproduced by `probe_status_edges.py::test_initiative_status_missing` (run). Also a file with no frontmatter (`test_initiative_without_frontmatter`).

D3. `work status` refuses all output when one initiative.md is not UTF-8.
  Commands: `.shop/work/i1/initiative.md` holding `b"---\nstatus: proposed\n---\n\xff\xfe\n"`, then `python3 <worktree>/scripts/work status`.
  Came back: rc 1, stderr "work: .shop/work/i1/initiative.md is not UTF-8 text", no stdout (also for any other open initiative). Reproduced by `probe_status_edges.py::test_initiative_file_not_utf8` (run). A session hook would lose every initiative's status to one file.

## 7. The file set

Production files the change must touch (each by `refs`, search or read):
- `hooks/hooks.json` (14 lines): add the PreCompact entry (r33, r34); decide whether `work status` is one more SessionStart command or part of `migrate status --hook`. Read.
- `scripts/migrate_upgrade.py` (170 lines; room 130): `session_text` returns work status text for open initiatives (r24, r32). `tools refs session_text`, read.
- `scripts/migrate` (71 lines; room 229): the `status --hook` help and docstring line 5 (contract text). Read.
- `scripts/workqueue_status.py` (129; room 171): a function the hook can call that returns the text for open initiatives, and the top-level root. Read; refs status.
- `scripts/work` (97; room 203): `--root` default or a hook-side call with the top level (D1). Read.
- New module for the PreCompact text and the append (e.g. `scripts/migrate_session.py`, name the plan's choice): a new concern, so a new row in CLAUDE.md's module map. Read.
- `scripts/workqueue.py` (262; room 38) and `scripts/workqueue_note.py` (21; room 279), only if the PreCompact append reuses `append` or `committed`, or a note-format change is made. Read/refs.
- `features/migration-tools.feature`: remove the retired scenario (lines 461-468, `@r24 @deprecated`). Read.

Test files the change must touch (so that the accepted scenarios pass and what passes today keeps passing):
- `tests/scenarios/migration_upgrade_steps.py` (274; room 26): the hook When reads `hooks[0]["hooks"][0]` (127-133); the Givens and Thens for initiatives and PreCompact belong in a new step module, not here. Read; by search.
- `tests/scenarios/migration_version_steps.py` (61; room 239): the hook helper (29-35) and the `tells the session` steps. Read.
- New step module, e.g. `tests/scenarios/migration_session_steps.py`: the initiative Givens (may reuse `test_work_queue.initiative`, `work_queue_status_steps.py`), the PreCompact When, the Thens for `work status` text, `compacted`, and `work note`. A new concern (a row for tests/scenarios in CLAUDE.md's module map, if the plan adds one). Read.
- `tests/scenarios/test_migration_tools.py` (228; room 72): pytest-bdd binds the feature; add the new step module's import (the file imports step modules, e.g. line 10). Read.
- `tests/scenarios/work_queue_status_steps.py` (157; room 143): only if the hook's `work status` text is compared to it (`initiative` helper). Read.

Modules on the change's path, edited or not (line counts by `wc -l`; room under the 300 limit `tools size` uses; CLAUDE.md gives the same limit):
- scripts/migrate: 71, room 229
- scripts/migrate_upgrade.py: 170, room 130
- scripts/migrate_write.py: 126, room 174 (uncommitted, top_level; on the hook path)
- scripts/workqueue_status.py: 129, room 171
- scripts/workqueue.py: 262, room 38
- scripts/workqueue_note.py: 21, room 279
- scripts/work: 97, room 203
- hooks/hooks.json: 14 (JSON; the line limit is for Python, not applied)
- tests/scenarios/migration_upgrade_steps.py: 274, room 26
- tests/scenarios/migration_version_steps.py: 61, room 239
- tests/scenarios/test_migration_tools.py: 228, room 72
- tests/scenarios/migration_old.py: 81, room 219 (the `old` fixture the Givens use)
- tests/scenarios/work_queue_status_steps.py: 157, room 143 (if reused)

`tools size --limit 300` printed nothing (run): no tracked Python file is over the limit now.

Working tree: `git status --porcelain --ignored .shop` shows only `!! .shop/scratch/` (run); the worktree is clean apart from ignored scratch and the stage directory.
