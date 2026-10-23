# Research notes: w96 (upgrade hardening, migration-tools r7, r18, r25, r26)

Tools: `tools refs` ran. `tools tests-of` and `untested` found no map (`tools: no map`), so every test
list below is `by search` (grep over tests/). `tools size --limit 300` ran: nothing over.
Probes: `python3 -m pytest -q -s -n 0 -p no:warnings .shop/scratch/w96-1-research/probe_*.py`
(`-n 0`: the suite's addopts run xdist; each probe builds its repos under scratch/repos/).
Scratch is ignored by git: `git status --porcelain` is empty.

## 1. Why each scenario is red today

None is red. All 10 accepted scenarios (16 test items) pass today.
Command: `python3 -m pytest -q --tb=short "<16 node ids>"` in tests/scenarios/test_migration_tools.py -> `16 passed`.
- r7 "finds <found>" outline, 2 items; "would land on <there>" outline, 4 items; "would <what>" outline, 3 items;
  "cannot make two of its changes"; "would relocate onto an untracked file"; "outside a git repository": all pass (run).
- r18 `migrate status` prints versions and pending step: passes (run).
- r25 numbering by initiative number then file name: passes (run).
- r26 rename and rewrite (own initiative's name, other initiative, `for:`): both pass (run).

The work-item therefore changes code the scenarios already cover, and must keep them passing. Its fixes
(N4, N5, N6, N8, F7, F8, F9, F12) have no scenario; their red state is in section 2.

## 2. What the system answers today

Probe file: `.shop/scratch/w96-1-research/probe_upgrade.py`, `probe_upgrade2.py`, `probe_upgrade3.py`.
All lines below are `run`. Each repo: spec/index.md with `id: bounded-context/example.org/acme/shop` unless stated.

**N4 ambiguity (test `test_n4_ambiguous_reference_message`)**: i1-x/a.md, i2-y/a.md, i3-z/c.md
(`blocked_by: [a]`, `for: a`), i3-z/d.md (`depends_on: [a]`); `migrate upgrade` ->
exit 1; stderr:
```
could not rename the reference a of .shop/work/i3-z/c.md: initiatives i1-x and i2-y all hold it
could not rename the reference a of .shop/work/i3-z/c.md: initiatives i1-x and i2-y all hold it
could not rename the reference a of .shop/work/i3-z/d.md: initiatives i1-x and i2-y all hold it
```
`git status` empty. Refusal is correct; wording says "reference" for all three fields; line repeats.

**N5 qualified token**: i1-x/migration-tools.md and i1-x/b.md with `for: migration-tools#r26`;
`migrate upgrade` exit 0; b's w1.md reads `for: w2#r26` (rewritten).
**N5 comment**: i1-x/item.md and b.md with block item `  - work-item/item # item`; w1.md reads
`  - work-item/w2 # w2` (comment rewritten).

**F7 non-version plugin version**: `.shop/plugin-version` = `next`:
- `migrate status --hook` -> exit 1, traceback `ValueError: invalid literal for int() with base 10: 'next'`
  at migrate_upgrade.py:20 (number), called from session_text:55.
- `migrate status` -> exit 1, stdout prints `the repository's plugin version: next` then the same traceback
  (pending():34).
- empty file: `migrate status --hook` -> exit 1, `ValueError ... ''`.

**F8 no bounded-context id**: spec/index.md = `# shop` (no id); `migrate upgrade` with one work-item ->
exit 1, `AttributeError: 'NoneType' object has no attribute 'group'` at migrate_upgrade_ids.py:22 (context_path),
called from plan():95. `git status` empty (nothing written). With spec/index.md absent entirely:
exit 1, `FileNotFoundError` on spec/index.md, same place.

**F9 same initiative number**: (a) i1-b/a.md + i1-a/b.md -> i1-a/w1.md, i1-b/w2.md.
(b) i1-a/a.md + i1-b/b.md -> i1-b/w1.md, i1-a/w2.md. Same shape, different numbering: order is directory
order, not name (migrate_upgrade_ids.py:36 sorts by number alone).

**N6 move check (no unit test today)**: runs/a tracked, tracked runs/w1/y beside it: `migrate upgrade` exit 1,
`could not move .shop/work/i1-x/runs/a onto .shop/work/i1-x/runs/w1`, git status empty.
Ignored runs/w1/y (gitignored, untracked): same refusal, same text. The move check works today; only its test is missing.

**Nearest cases, already passing (run)**: no git identity -> `migrate upgrade` exits 1 with
`migrate put the repository back as it was`, git status empty (commit fails, rollback works).
Uncommitted untracked file under runs/w1 -> refused by the uncommitted check first (exit 1, names the file).

**Symbolic link for the plugin version (not in the work-item; see section 6)**: `.shop/plugin-version`
a tracked link to a file outside the repository holding `0.23.1`: `migrate upgrade` exit 0, the outside file
now holds `0.24.0`, the link is still a link.

**Not probed (read only)**: `migrate status --hook` outside a git repository (exit 0 by contract). Every directory
under scratch sits inside the worktree's repository, so no outside-repo case could be built without writing outside scratch.

## 3. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| migrate_upgrade.py:number (19), used at pending 34-35 and session_text 55 | takes a version as dotted ints; `int()` raises on `next` or empty | F7: refuse, saying why, in status and in hook | by search: scenarios r18-r24 (numeric versions only); the non-numeric branch: none | refs (3 callers) |
| migrate_upgrade.py:repository_version (27) | reads `.shop/plugin-version`, strips it, returns it | F7: a value that is no version is refused, not passed to number | by search: r18, r19 scenarios; the non-version value: none | refs (4 callers) |
| migrate_upgrade.py:status (42) and session_text (50) via run hook branch (134-136) | hook prints session text, exit 0 by contract (only the no-repo path returns 0 for hook) | F7: a crash here gives exit 1 in the SessionStart hook; the fix must decide how a refusal reaches the session | by search: r22-r24, r28 hook scenarios; crash branch: none | read + probe |
| migrate_upgrade_ids.py:context_path (20), called plan 95 | reads spec/index.md with one regex, `.group(1)` on a match | F8: refuse, saying why; also absent spec/index.md crashes | by search: r25, r26 scenarios (index written with id, migration_upgrade_steps.py:31); no-id branch: none | refs (2 callers, workqueue.py has its own) |
| migrate_upgrade_ids.py:initiatives (31-36) sort key `pair[0]` | sorts initiatives by number only; ties keep iterdir order | F9: sort by number, then name | by search: r25 scenario (distinct numbers 2 and 10); tie branch: none | refs (1 caller) |
| migrate_upgrade_ids.py:rewrite_item pattern (line 50) and listing branch (56-65) | rewrites every token of a field line or list line that equals a name, comments and `#r<n>` included | N5: rewrite only the name value | by search: r26 scenarios, test_migrate_upgrade_ids.py:44 (block list); comment and qualifier: none | read |
| migrate_upgrade_ids.py:resolver (81-91) and its call (plan 109) | one label "reference" for every field | N4: name the field (blocked_by, depends_on, for) | by search: test_migrate_upgrade_ids.py:62 (checks only the two initiatives in stderr) | read + probe |
| migrate_upgrade.py:upgrade refused list (104-108) | joins changes.failures with move_failures, no dedupe on the first | N4: repeated lines | by search: test_migrate_upgrade_ids.py:62 (no line count) | probe |
| migrate_upgrade.py:move_failures (81-90) | builds a SimpleNamespace and calls check_moves; dedupes its own list | N6: needs a unit test; no change required | none | read + probe (refusal works) |
| migrate_upgrade.py:apply's `.shop/plugin-version` write (112-113) | writes through a symbolic link, adds with `git add -f`; not in any checked change | not in the work-item; a plan may want check_moves on it | none (by search: no test links the version file) | probe (defect 6.3) |
| migrate_upgrade_ids.py:1-4 module docstring | says blocked_by and depends_on follow within the initiative | N8: now every field, across initiatives | none (docstring) | read |

## 4. Tests the requirements make impossible to keep

No map: the lists are `by search`. Searched: every test that names migrate, or any function above, under tests/
(grep: `could not rename`, `reference a of`, `ValueError`, `AttributeError`, `status --hook`, `plugin-version`,
`bounded-context id`, `could not move`).

- tests/scripts/test_migrate_upgrade_ids.py:62 `test_a_name_held_by_two_other_initiatives_is_refused_and_nothing_changes`:
  keeps passing after N4 (asserts only "i1-x", "i2-y" in stderr). Keep as is.
- tests/scripts/test_migrate_upgrade_ids.py:44 `test_a_blocked_by_written_as_a_block_list_follows_the_rename`:
  asserts `  - work-item/w1\n`; N5's narrowing keeps this. Keep.
- tests/scripts/test_migrate_upgrade_ids.py:53 and :72: `for:` and `blocked_by` and "for: nothing" left alone; keep.
- tests/scripts/test_migrate_upgrade_ids.py:37: repo with a valid id; F8's refusal must not change it. Keep.
- tests/scenarios/test_migration_tools.py r18-r26 and migration_upgrade_steps.py: all write a valid index id and numeric
  versions; each passes under the fixes. None asserts a crash or the old "reference" wording.
- test_migrate_write.py, test_migrate_layout.py: do not run `migrate upgrade`; unaffected.
- Nothing can no longer pass. "None" is by search, not by coverage.

## 5. A step the work-item skips

- **F8 refusal (context id)**. The existing way is `migrate run --context`: the argument names the context, and
  plan_index (r4) writes the id into spec/index.md. The upgrade reads the id and never writes it. Effects only
  the upgrade's read produces: the id stem `work-item/<ctx>/w<n>` in every renamed file (migrate_upgrade_ids.py:46).
  A refusal must come from plan() into the `refused` list, before any apply; plan runs before any apply today (read).
  `status` needs no id, so the refusal must not reach `status` (read).
- **F7 hook path**. Existing contract: `--hook` exits 0 whatever happens (scripts/migrate:62 help text; run() returns 0
  for hook when outside git). A refusal in hook mode that exits 1 breaks that contract. Two readings for the plan:
  (a) exit 0 and print a line saying why, the session tells the person; (b) exit 1, as `status` does. Read; probe (run) shows
  today's crash is exit 1 with a traceback.
- **Version-file write**. `migrate run` checks every text against symbolic links and ignored files (migrate_write.py:70-75,
  check_moves). The upgrade's `.shop/plugin-version` write is outside that check: apply() writes it after the checks
  (migrate_upgrade.py:112). Effect only this path produces: a write through a link (probe, run, section 6.3). Read.
- **N6 move check**. The move check has no test (section 4). Its effect exists only in the upgrade (move_failures). Probe (run) shows refusal.

## 6. Defects

Each reproduced by the probe named; output in section 2.

### 6.1 `migrate status --hook` crashes on a non-version `.shop/plugin-version` (F7)
- Repro: `.shop/plugin-version` = `next`; `python3 scripts/migrate status --hook` in the repo -> exit 1, ValueError traceback. Also `status` and an empty file.

### 6.2 `migrate upgrade` crashes when spec/index.md has no bounded-context id (F8)
- Repro: spec/index.md = `# shop`, one work-item in .shop/work/i1-x/ -> exit 1, AttributeError. Absent file -> FileNotFoundError.

### 6.3 `migrate upgrade` writes `.shop/plugin-version` through a tracked symbolic link
- Repro (probe_upgrade3.py): `.shop/plugin-version` -> `../../outside.txt`, which holds `0.23.1`; `migrate upgrade` exit 0; outside file holds `0.24.0`.
- Expected by the module's contract: scripts/migrate:10 says a symbolic link is never read or written through.

### 6.4 Refusal text for ambiguous names says "reference" and repeats lines (N4)
- Repro in section 2 (N4). Wording only; the refusal itself is right.

### 6.5 Qualified and commented tokens are rewritten (N5)
- Repro in section 2: `for: migration-tools#r26` -> `for: w2#r26`; `# item` comment -> `# w2`.

### 6.6 Initiatives with one number are numbered by directory order (F9)
- Repro in section 2 (F9 a, b): the same tree shape gives different numbering by which directory the OS lists first.

## 7. The file set

Edited (work-item's fixes):
- `scripts/migrate_upgrade.py` (137 lines, room 163): F7 - number/repository_version/status/session_text refuse a value
  that is no version; N4 dedupe of `refused` (line 105). Found: refs (number 4 callers) and probe 6.1.
- `scripts/migrate_upgrade_ids.py` (119 lines, room 181): N4 field name in resolver call (line 110); N5 narrow the
  token pattern (line 50); N8 docstring (1-4); F8 refuse in context_path (20-22); F9 sort key (36). Found: section 2 probes; read.
- `tests/scripts/test_migrate_upgrade_ids.py` (79 lines, room 221): F12 remove temp repos (`addCleanup(shutil.rmtree, root)` as
  in test_model.py:74); tests for N4 wording, N5 qualified and comment, F8, F9. Found: section 4 (search).
- `tests/scripts/test_migrate_write.py` (80 lines, room 220): F12 - line 17 `mkdtemp()` never removed (no cleanup
  in the file; found by search, not in the findings). Found: grep `mkdtemp|rmtree|addCleanup` under tests/scripts.
- NEW `tests/scripts/test_migrate_upgrade.py` (new, room 300): N6 move-check test (tracked and ignored run/w1 cases,
  probe_upgrade.py); F7 refusal tests for status and --hook. A new module keeps test_migrate_upgrade_ids.py to the ids step.
  Found: tests/scripts listing; CLAUDE.md: tests/scripts row covers it, no module-map row needed.

Read, on the change's path, unedited:
- `scripts/migrate` (71 lines, room 229): dispatch to run_upgrade; no change.
- `scripts/migrate_write.py` (126 lines, room 174): check_moves, uncommitted, git, top_level used by upgrade; no change.
- `scripts/migrate_layout.py` (131 lines, room 169): `tracked` used by check_moves; no change.

Not in the file set: `features/` (no scenario changes), `scripts/workqueue.py` (N7 is not in the work-item).
Room is per CLAUDE.md (300 lines) - the size tool printed nothing.
