# Plan of w96: upgrade hardening from the reviews of i21

Planned from .shop/work/i22-rulings-round-trips-query-output/runs/w96/1-research/notes.md ("notes §n"). This plan
takes over from the stage-2 plan, whose one open question (F7, the hook) the person has answered: Reading A,
2026-10-23. That answer is in the work-item's `## Answers`. Every decision is now taken.

## 1. What goes green

None of the accepted scenarios is red today. All 10 (16 test items) pass (notes §1, run). The work changes code
they cover, so they must stay green:

- migration-tools#r7: the "finds <found>", "would land on <there>" and "would <what>" outlines; "cannot make two of
  its changes"; "would relocate onto an untracked file"; "outside a git repository".
- migration-tools#r18: `migrate status` prints the versions and the pending step.
- migration-tools#r25: numbering by initiative number, then file name.
- migration-tools#r26: rename and rewrite (the name in its own initiative, in another initiative, in `for:`).

The work-item's fixes have no scenario. Each gets a test under tests/scripts/ that is red today for the reason
given (notes §2, §6):

- N4: the ambiguity refusal says "reference" for every field and repeats a line. The resolver gets one label, and
  upgrade's `refused` list is never deduplicated.
- N5: `for: migration-tools#r26` becomes `for: w2#r26`, and a comment `# item` becomes `# w2`. The token pattern
  rewrites any token equal to a work-item's name.
- N6: the move check (move_failures) has no test. It already refuses (probe), so its tests pass at once. They are
  written to guard it.
- N8: the module docstring of migrate_upgrade_ids.py says blocked_by and depends_on follow only within the
  initiative. It is text, so it has no test.
- F7: when `.shop/plugin-version` holds `next` or nothing, `migrate status`, `migrate status --hook` and
  `migrate upgrade` stop with a ValueError traceback from `number`, exit 1.
- F8: when spec/index.md has no bounded-context id, or does not exist, `migrate upgrade` stops with an
  AttributeError or a FileNotFoundError from context_path.
- F9: initiatives that share a number are numbered in iterdir order, because the sort key is the number alone.
- F12: test_migrate_upgrade_ids.py and test_migrate_write.py make temporary repositories and never remove them.

Deprecated scenarios retired: none (the work-item has no Retires section).

## 2. Where the change lands

- `scripts/migrate_upgrade.py`:
  - F7: a plugin version that is not dotted numbers is caught before `number` is reached. In status and upgrade
    it is refused (decisions 2 and 3). In the hook path it becomes one line of session text (decision 1).
  - N4: the `refused` list is deduplicated, keeping its order.
- `scripts/migrate_upgrade_ids.py`:
  - N4: the resolver gets the field's name (blocked_by, depends_on, for) in place of "reference".
  - N5: the rewrite is narrowed to name values (decision 4).
  - N8: the docstring is corrected.
  - F8: context_path's failure goes into the plan's failures rather than crashing (decision 6).
  - F9: initiatives are sorted by number, then by name (decision 7).
- `tests/scripts/test_migrate_upgrade_ids.py`:
  - F12: each temporary repository is removed, with the cleanup registered where the repository is made, as
    test_model.py does.
  - New tests: N4 (the field is named, no line repeats); N5 (a qualified token and a comment are left alone); F8
    (a missing id and a missing index are refused, nothing changes); F9 (the two directory orders give the same
    numbering).
- `tests/scripts/test_migrate_write.py`: F12, its temporary directory is removed. The researcher found this by
  search. It is not in the findings, but it is the same fault.
- `tests/scripts/test_migrate_upgrade.py` (new):
  - N6: the move check with a tracked runs/w1 and with an ignored one.
  - F7: for both `next` and an empty file, `migrate status` and `migrate upgrade` refuse, and `migrate status
    --hook` exits 0 with its one line.
  - A new module keeps test_migrate_upgrade_ids.py to the ids step. The tests/scripts row of CLAUDE.md already
    covers it, so no row is added.
- Read only, not edited: `scripts/migrate` (dispatch, and the `--hook` help that promises exit 0, which stays
  true), `scripts/migrate_write.py` (check_moves, uncommitted, git), `scripts/migrate_layout.py` (tracked).

The file set is the researcher's, with nothing added or removed (the new test module is already in it). Every
file has room under 300 lines (notes §7).

## 3. Decisions

1. **`migrate status --hook` with a version file that holds no version.** It exits 0 and prints one line to
   stdout. The line says that `.shop/plugin-version` holds no version, names what it holds (an empty file is named
   as empty), and tells the session to tell the person. It prints no upgrade offer and no update notice, because
   neither can be worked out without a version. This is the person's answer of 2026-10-23 (Reading A), in the
   work-item's Answers. It keeps the `--hook` exit-0 contract. A repository without `.shop/` still gets nothing
   (migration-tools#r28), because there is no version file to read.
2. **`migrate status` with a version file that holds no version** prints nothing to stdout. It prints one line on
   stderr that names `.shop/plugin-version` and what it holds and says that this is not a version, then exits 1.
   It stops before the first status line, because r18's output ends in "exit successfully": a partial status
   followed by a failure is neither. Rests on migration-tools#r18 and the work-item's "refuse, saying why" (taken
   in the stage-2 plan; the answer to decision 1 does not change it, since the answer covers only the hook).
3. **`migrate upgrade` with a version file that holds no version** refuses in the same words, exits 1 and changes
   nothing. Rests on migration-tools#r7.
4. **N5: what the rewrite touches.** On a `blocked_by`, `depends_on` or `for` line, and on each item of a block
   list, only a value that names a work-item is rewritten: the bare name, or the name at the end of
   `work-item/<...>/`. A token with a `#r<n>` qualifier names a requirement, not a work-item, and is left as it is.
   So is anything after a YAML comment marker. Rests on migration-tools#r26 ("every work-item's blocked_by,
   depends_on and for that names it … leave free text in records as it is") and the work-item's N5.
5. **N4 wording.** The refusal names the field the name stands in (blocked_by, depends_on or for), not "reference",
   and each refusal line appears once. The implementer writes the exact sentence. Rests on the work-item's N4 and
   migration-tools#r7 ("naming each change it could not make").
6. **F8: when the missing id is refused.**
   - context_path's failure goes into the plan's failures, and from there into upgrade's `refused` list before any
     apply.
   - It is raised only when the step has a work-item to give an id. With no work-item, no change needs the id.
   - `migrate status` never reads the id.
   - A missing spec/index.md is refused the same way as an index with no id: the refusal names spec/index.md and
     says it has no bounded-context id.
   - Rests on migration-tools#r7, migration-tools#r26 (the id is `work-item/<context path>/w<n>`) and the
     work-item's F8.
7. **F9: the tie-break** is the initiative directory's full name, compared as a string, so i1-a comes before i1-b.
   Rests on migration-tools#r25 and the work-item's F9 ("sort by number, then name").
8. **The symbolic link at `.shop/plugin-version`** (notes §6.3) is out of scope. The work-item does not name it.
   It stays a finding for a later work-item, and this plan does not change it.

## 4. Tests the decisions break

None. There is no coverage map (notes §4), so this was checked by search:
- test_migrate_upgrade_ids.py:62, the refusal when two other initiatives hold a name, asserts only "i1-x" and
  "i2-y" in stderr. It holds under decision 5.
- :44, the block list follows the rename, asserts `  - work-item/w1`. It holds under decision 4.
- :53 and :72 (`for:` and blocked_by, and "for: nothing" left alone) hold.
- :37, a valid id, holds under decision 6.
- The r18–r26 scenarios in tests/scenarios/test_migration_tools.py, with migration_upgrade_steps.py, write a valid
  index id and numeric versions. None asserts a crash, the "reference" wording or a tie order.
- The r22–r24 and r28 hook scenarios never give a version file that holds no version, so decision 1 leaves them
  as they are.

The F12 edits change only cleanup in test_migrate_upgrade_ids.py and test_migrate_write.py. No assertion changes.

## 5. Open cases

For the implementer to name, not to choose:
- A version file with extra parts, a leading `v`, a suffix such as `0.24.0-rc1`, or more or fewer than three
  parts. The scenarios say nothing about what counts as "a version".
- A version file that is a directory, or that git does not track.
- The plugin's own version (plugin.json) holding no version, in status, upgrade or the hook.
- A version file holding surrounding whitespace or several lines, and how the hook's line names what it holds.
- An index id written in another form (quoted, or with spaces around the colon).
- A `for:` that names a work-item with a qualifier other than `#r<n>`.
- Two initiatives with the same number whose names differ only in case.
