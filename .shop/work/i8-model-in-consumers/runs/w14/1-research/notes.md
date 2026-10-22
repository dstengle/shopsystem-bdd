# migration-rebind-1 research (requirements r1, r2, r4, r5 of migration-tools)

Map: none (`tools tests-of` says "no map"); tests-of lists are `by search`. `tools refs` used for names; it does not read the extensionless `scripts/migrate`, so its callers in `migrate` are `read`.

## 1. Why each scenario is red today

Accepted: 18 scenarios (`features/migration-tools.feature`), 21 test ids in `tests/scenarios/test_migration_tools.py` (the work-item filter, from the environment, keeps those 21 of 58).

Run: `python3 -m pytest -q --tb=short tests/scenarios/test_migration_tools.py` → 20 passed, 1 failed.

Red (run):
- `test_migrate_run_gives_specindexmd_whose_id_is_boundedcontextshop_the_id_boundedcontextpath`
  (`features/migration-tools.feature:340`, r4). Failed at `tests/scenarios/migration_spec_steps.py:28`, `assert data.get("id") == ident`; `--showlocals` gives `data={'id': 'bounded-context/shop'}`, ident `bounded-context/example.org/acme/shop`, the file still `# shop` body.
  Cause: the Given `tests/scenarios/migration_safety_steps.py:40-42` writes `spec/index.md` and does not commit it. Migrate then refuses on the uncommitted tree (`scripts/migrate:32-35`, `migrate_write.uncommitted`), writes nothing, and the Then reads the old id. The product rewrite is right (probe P1). See section 5.

Green today (run, all in the 20): the r1 relocation, r1 non-text, r1 subdirectory, r2 ledger entry (plain, no-blank-line, the three quote outlines, whole text, supersedes+revisit_when, two supersedes, `by`-qualifier outline row 1 and 2 both reported as in the set), r4 `spec/index.md` without id, r5 path/link/frontmatter, r5 ledger-numbered id, r5 `by` outline (2 rows), r5 context id, r5 decision old id, r5 symlink, r5 CRLF.
Counted: 3 r1, 6 r2 (+3 outline rows), 2 r4, 7 r5 (+2 outline rows) = 18 scenarios / 21 ids; 20 green, 1 red.

Note for the planner: the work-item says the scenarios are not green yet; 20 of 21 already pass. Only the Given needs a fix.

Also run: `python3 -m pytest -q --whole-suite tests/scripts/test_migrate_layout.py tests/scripts/test_migrate_write.py` (run, with `-o addopts=""`) → 7 passed.

## 2. What the system answers today

Probes: `.shop/scratch/migration-rebind-1-1-research/probe_index.py` (run, `python3 -m pytest -q -s -p no:cacheprovider -o addopts="" --whole-suite <path>`, the work-item filter needs `--whole-suite` to let scratch tests run) and `probe_uncommitted.py` (run). Each runs `python3 <worktree>/scripts/migrate run --context example.org/acme/shop` in a scratch repo.

- P1 `spec/index.md` `id: bounded-context/shop`, committed → rc 0; index now `id: bounded-context/example.org/acme/shop`; status `A spec/decisions/index.md`, `M spec/index.md` (run).
- P2 same with the id quoted `"bounded-context/shop"` → rc 0, id rewritten unquoted (run).
- P3 index id plus `notes/n1.md` with `about: bounded-context/shop` → both rewritten, rc 0 (run).
- P4 index with no frontmatter (`# shop`) → rc 0, id `bounded-context/example.org/acme/shop` added (run).
- U1 same as the failing Given, not committed → rc 1, `could not start from a tree with an uncommitted change: spec/index.md`; file unchanged; `?? spec/` (run).

Nearest cases not probed: an index whose id is already the new one (read: `reid` returns the text unchanged on equality, `scripts/migrate_layout.py:84-93`).

## 3. Old assumptions

Accepted requirements change: the ledger form (r2), the context id form (r4), and the rewrite of references (r5).

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| `scripts/migrate_spec.py:rewrite_text` (LINK regex, line 84) | rewrites inline links `](target)` only; reference-style `[x]: path` links are not rewritten | r5 says "relative Markdown link"; reference-style links stay stale | the r5 link scenario (by search: test_migration_tools.py, the notes/n1.md link); reference style: none | read |
| `scripts/migrate_spec.py:rewrite_text` (path regex, line 102) | rewrites a moved path only where it is not preceded by `[\w./-]` | a path inside a longer path stays; no test asserts it | none | read |
| `scripts/migrate_layout.py:with_id` (line 69-81) | keeps a frontmatter that has any `id:` line | used by `reid` only for ids in the same form, so r5/r4 renames go through `reid`; a record from `records/` with another id keeps it (r9, not accepted) | the r5 and r9 scenarios by search | read |
| `scripts/model_facts.py:read_layout` (OLD_LAYOUT, line 20, 103) | a path of the old layout under the root is a file problem | after a run they are gone, so no problem; consistent with r1/r2 | none by search in tests/scenarios for read_layout (not searched by names) | read |
| `scripts/model_work.py` line 40 `supersedes` (as_list) | reads supersedes as ids | r2/r17 write ids alone, consistent | none (no map) | read |

## 4. Tests the requirements make impossible to keep

No accepted-requirement change makes an existing test fail. Read of `tests/scripts/test_migrate_layout.py` (4 tests) and `tests/scripts/test_migrate_write.py` (3 tests): names assert kinds, plan_ids on images, rollback on failed git add, the uncommitted-move case; all 7 pass (run). Sound, none can fail under r1/r2/r4/r5. `tests-of` has no map: this is `by search` for `migrate` tests (`tests/scripts/test_migrate_*.py`, `tests/scenarios/migration_*`). Result: none.

## 5. A step the work-item skips

The r4 scenario Given at `tests/scenarios/migration_safety_steps.py:40-42` writes `spec/index.md` and does not call `old.commit()`, unlike the other Givens (`migration_spec_steps.py:19-22`). The existing way is `old.commit()`, which migrate's uncommitted check (r15, `scripts/migrate:32-35`) requires. Refusal effect shown by U1 (run): rc 1, names the file, no change. No other effect of the step is skipped.

## 6. Defects

None found in the product by probes P1-P4 and U1 (run). The red scenario is a test-step defect, section 5.

## 7. The file set

Must change for the red scenario to pass:
- `tests/scenarios/migration_safety_steps.py` (line 40-42): add `old.commit()` after the write, as the other Givens do. Found by the run and U1.

Must not change (green today, keep green): `scripts/migrate`, `scripts/migrate_layout.py`, `scripts/migrate_ledger.py`, `scripts/migrate_spec.py`, `scripts/migrate_write.py`, `tests/scenarios/test_migration_tools.py`, `tests/scenarios/migration_old.py`, `tests/scenarios/migration_ledger_steps.py`, `tests/scenarios/migration_spec_steps.py`. Read and run; none needs an edit.

Line counts (`wc -l`) and room under 300 (CLAUDE.md size limit):
- scripts/migrate 63 (room 237)
- scripts/migrate_layout.py 131 (169)
- scripts/migrate_ledger.py 123 (177)
- scripts/migrate_spec.py 132 (168)
- scripts/migrate_write.py 126 (174)
- scripts/model 132 (168) — read by path from migrate (`load_model`)
- scripts/model_report.py 80 (220) — `render_decisions`, the index written (`migrate_write.write_all`)
- tests/scenarios/migration_safety_steps.py 120 (180) — the edit
- tests/scenarios/test_migration_tools.py 225 (75)
- tests/scenarios/migration_old.py 81 (219)
- tests/scenarios/migration_ledger_steps.py 227 (73)
- tests/scenarios/migration_spec_steps.py 209 (91)

Other repository files over the limit (not on this path): `scripts/measure` 644, `tests/scripts/test_measure.py` 700 (`tools size --limit 300`, read).
