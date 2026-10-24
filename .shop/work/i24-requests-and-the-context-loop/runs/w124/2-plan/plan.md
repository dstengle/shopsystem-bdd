# Plan of w124: the SessionStart hook gives work status; the PreCompact hook notes `compacted` and asks for a hand-off

From the research notes `.shop/work/i24-requests-and-the-context-loop/runs/w124/1-research/notes.md`.

## 1. What goes green

- **migration-tools#r24**, "a session starting in a repository on the plugin's version whose every initiative is done or abandoned is told nothing". Red because the Given "its initiatives are i1, which is `done`, and i2, which is `abandoned`" has no step definition. The code already prints nothing here (probe 1), so the Given is all it needs. It must stay green once r32's text is added.
- **migration-tools#r32**, "a session starting in a repository with initiatives neither done nor abandoned is given what `work status` prints for each of them". Red because its Given and both Thens have no step definitions. On the code side, `session_text` in `scripts/migrate_upgrade.py` gives no work status, and `hooks/hooks.json` runs only `migrate status --hook`. Today the hook prints `''` (probe 1).
- **migration-tools#r33**, "a session about to be compacted appends `compacted`, with the time, to the ledger of each initiative neither done nor abandoned". Red because its Givens and the When "a session in it is about to be compacted" have no step definitions. `hooks/hooks.json` has no PreCompact entry, and no code writes `compacted`.
- **migration-tools#r34**, "a session about to be compacted in a repository with an initiative neither done nor abandoned is told to write its hand-off with `work note` and end". Red because its Given and When have no step definitions, and there is no PreCompact hook or text.
- **Retired:** "a session starting in a repository on the plugin's version is told nothing (deprecated)" (`@r24 @deprecated`, features/migration-tools.feature lines 461-468). Its scenario is removed, along with its binding in `tests/scenarios/test_migration_tools.py` if the binding names it by title.

## 2. Where the change lands

- `hooks/hooks.json`: gains a PreCompact entry that runs the new `migrate` hook subcommand (decision 3). SessionStart stays one command, `migrate status --hook` (decision 1).
- `scripts/migrate`: a new subcommand for the PreCompact hook. The `status --hook` help and the docstring change to say the start-of-session text now includes work status for open initiatives, and that the command still always exits 0.
- `scripts/migrate_upgrade.py`: `session_text` (or `run`'s hook branch) adds the work status text of open initiatives after the version text (decision 2). There is room for this: 170 lines.
- `scripts/migrate_session.py` (new): the session-hook concern. It builds the work status text for open initiatives at the repository's top level, and it does the PreCompact work: the `compacted` line in each open initiative's ledger, its commit, and the hand-off text. It is new because CLAUDE.md gives each new concern its own module, and because `migrate_upgrade.py` and `workqueue.py` have little room left. The researcher suggested this module.
- `scripts/workqueue_status.py`: shows a function the hook can call with a root that returns `work status`'s text for the open initiatives (the ENDED filter), with no printing and no exit. `work status` itself prints exactly what it prints today.
- `CLAUDE.md`: a new row in the module map for `scripts/migrate_session.py` (the SessionStart work status and the PreCompact hook).
- `features/migration-tools.feature`: remove the retired scenario.
- `tests/scenarios/migration_session_steps.py` (new): the initiative Givens (reusing the existing `initiative` helper of the work-queue tests), "each of i1, i2 and i3 has a ledger", the PreCompact When (it runs `hooks["PreCompact"][0]["hooks"][0]` the way the SessionStart helpers run theirs), and the Thens: the `work status` text, nothing of i3/i4, the `compacted` line with the time, the unchanged ledger, and the hand-off and "end" text. It is new because `migration_upgrade_steps.py` has only 26 lines of room.
- `tests/scenarios/test_migration_tools.py`: import the new step module, and drop the retired scenario's binding if it has one.

Removed from the researcher's set, as no decision here edits them (they are only read or called): `scripts/work`, `scripts/workqueue.py`, `scripts/workqueue_note.py`, `scripts/migrate_write.py`, `tests/scenarios/migration_upgrade_steps.py`, `tests/scenarios/migration_version_steps.py`, `tests/scenarios/work_queue_status_steps.py`, `tests/scenarios/migration_old.py`. The hook calls `workqueue.append`/`committed` and `migrate_write.top_level` as they stand. If the implementer finds that `committed` cannot take several files without an edit, `workqueue.py` comes back into the set, and it has only 38 lines of room.

## 3. Decisions

1. **The work status goes into the one SessionStart command, `migrate status --hook`, not into a second hook command.** This rests on the capability's Implementation note ("The plugin's SessionStart hook runs `migrate status` to learn what it tells the session") and on r24/r28: one command decides between "nothing" and text. The existing hook step helpers run only the first SessionStart command, so they keep covering the whole of it.
2. **The text is `work status`'s own, at the repository's top level, after the version text.** The hook asks the new workqueue_status function for the open initiatives' text, with the root from `migrate_write.top_level`. Running `work status` from the session's cwd would print nothing from a subdirectory (D1). r32 is "what `work status` prints for each such initiative", so the text is not rewritten. When there is version text too (r22, r23, r31), it comes first and the work status follows. When no initiative is open, nothing is added, which keeps r24 and r28 at `''`. When there is no `.shop/`, nothing is read at all (r28).
3. **The PreCompact hook is a new `migrate` subcommand with its code in `scripts/migrate_session.py`.** This rests on `under: migration-tools`: the capability's hooks live in `migrate`. Like `status --hook`, it always exits 0, because a hook's failure must not stop the session (the `--hook` contract of `migrate_upgrade.run`). With no `.shop/` or no open initiative, it writes nothing and says nothing: r33 and r34 apply only "in a repository with an initiative that is neither `done` nor `abandoned`".
4. **The `compacted` line is a ledger line with the date and the local time to the minute, in the form `- YYYY-MM-DD HH:MM: compacted`.** This rests on design-decision/the-ledger-is-tracked ("one line an event") and r33 ("with the time"). The line extends the date-only form that `work note` writes. It does not match `workqueue_status.DATED`, which is harmless: it is not a `next:` line, and probe 3 shows `work status` shows it as a plain line. DATED and `ledger()` are not changed.
5. **The PreCompact hook commits the ledgers it appended to, in one commit, with `workqueue.committed`, naming only those ledger files.** This rests on design-decision/the-ledger-is-tracked (the ledger is tracked, and written as `work note` writes it) and on migration-tools#r15. A bare append leaves the tree dirty, and then the next `migrate upgrade`, which a session's start offers (r22), refuses it (probe 3). `committed` commits only the files it names, so the session's other uncommitted work is left as it is (probe 3: `unrelated.txt` stayed untracked).
6. **The PreCompact text tells the session to write its hand-off with `work note <initiative> "<hand-off>"` for each open initiative it names, and then to end instead of being compacted.** It is printed on stdout, the channel the SessionStart hook uses, and the scenario steps read it there. This rests on r34.
7. **Step-level checks.** r32's first Then runs `work status` in the repository and checks that the hook's stdout holds its output. That output is i1's and i2's blocks only, as `work status` leaves out ended initiatives. The second Then checks that the stdout has no `initiative i3` or `initiative i4` block. r33's Then checks that the last line of i1's and of i2's ledger is `compacted` with a date and time, and that i3's ledger is byte for byte what it was. These rest on the scenarios' text.

## 4. Tests the decisions break

None, beyond the retired scenario that is removed. What I checked, from the notes (section 4) and the decisions above:
- r24 (done/abandoned), r28, and the retired r24 scenario still get `''`: no open initiative, or no `.shop/`, so decision 2 adds nothing. The retired scenario is removed anyway.
- r22, r23 and r31 have no initiatives in their Givens, so their stdout is unchanged. Their `in stdout` Thens would hold even with the work status appended after the text (decision 2).
- r18, r19 and r30 (`migrate status`/`upgrade` without `--hook`) are off the hook path and unchanged.
- The work-queue status and note scenarios, including the ledger-of-twelve ones, are unchanged: `work status`'s printing, `work note`, DATED and `ledger()` are not changed (decisions 2 and 4). They should be run again once the workqueue_status function is shown.
- No coverage map exists, so this list is the researcher's, found by search.

## 5. Open cases (for the implementer to name, not to choose)

- An open initiative's `initiative.md` is not UTF-8 (D3): `work status` refuses for every initiative. What the SessionStart and PreCompact hooks print then (both exit 0).
- An `initiative.md` with no status (D2) is shown by `work status` as `None` and counted as open. The hook passes this through, and the PreCompact hook would append to its ledger.
- The commit of decision 5 fails (no git identity, not a repository, or a repository with no commit, where probe 1 found everything untracked). `committed` rolls the files back, so the `compacted` line would be lost. Whether the hook still says the hand-off text then.
- `compacted` written by several compactions in a row: no de-duplication, and each one uses up one of the ten ledger lines `work status` shows.
- Whether Claude Code delivers a PreCompact hook's stdout to the model, as it does SessionStart's. The scenarios check stdout only, and the notes do not establish it.
- `.shop/` present with no `.shop/work/`: both hooks are silent about initiatives.
- An open initiative with no `ledger.md`: the PreCompact hook creates the ledger (O_CREAT), as `work note` does.
