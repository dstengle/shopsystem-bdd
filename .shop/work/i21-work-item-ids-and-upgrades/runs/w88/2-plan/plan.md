# Plan of w1: references from another initiative and `for:` follow the rename (migration-tools#r26)

## 1. What goes green

- migration-tools#r26, features/migration-tools.feature:
  - S1 "the upgrade step "work-items named by ids" renames a work-item's file and stage directories and rewrites its name where its initiative names it" (line 483). Not red: it passes today (notes §1). It must stay green.
  - S2 "the upgrade step "work-items named by ids" rewrites a reference from another initiative and a for: to the id of the work-item they name" (line 497). Red today: its Givens at lines 500-502 and its Thens at 504-505 have no step definitions (StepDefinitionNotFoundError at line 500). Behind the steps the code is wrong too (notes §2 P1, §6 D1, D2): `plan` in scripts/migrate_upgrade_ids.py resolves a name only inside the referring work-item's own initiative, and `rewrite_item` rewrites `blocked_by` and `depends_on` lines and never `for:`. So i3 docs keeps `blocked_by: [size-check]` and `for: size-check`.
- Retires: none (the work-item has no Retires section).

## 2. Where the change lands

- scripts/migrate_upgrade_ids.py: name resolution across the whole context (Decision 1), `for:` rewritten as a scalar and as a list, inline or block (Decision 2), and `plan` returning the changes it cannot make alongside the changes it can (Decision 3).
- scripts/migrate_upgrade.py: `upgrade` refuses when the step's plan names changes it cannot make: it prints each, exits with an error and changes no file, before any `git mv` (Decision 3). It also runs the move check before writing (Decision 4).
- scripts/migrate_write.py: changes only if `check_moves` cannot be called as it is from the upgrade path (Decision 4). Kept in the set for that reason; the implementer leaves it alone if no change is needed.
- tests/scenarios/migration_upgrade_steps.py: the Givens of S2 lines 500, 501 and 502 and the Thens of 504 and 505. The Given of line 500 and the existing literal Given for `i10/a.md, i2/b.md, i2/a.md` (line 75) can become one parsed step over a list of paths. The Thens find "the work-item that was <path>" by its old path; the step that renames records which new file each old path became, or the Then reads it from the files' headings. The file is 227 lines and must stay at or under 300.
- tests/scripts/test_migrate_upgrade_ids.py: unit cases for the cases the scenarios do not drive: `for:` as a block list, a name held only by another initiative, a name held by two other initiatives refused (r7), and a name that names no work-item left alone (Decision 5).

Not changed: scripts/migrate, scripts/model_work.py, scripts/workqueue.py, tests/scenarios/test_migration_tools.py (its S2 function already exists, notes §7).

## 3. Decisions

1. **How an old name resolves.** A bare name in a work-item's `blocked_by`, `depends_on` or `for` resolves to the work-item of that name in the referring work-item's own initiative. If its own initiative has none, it resolves to the one work-item of that name in any other initiative. The resolution map is built over every initiative under `.shop/work/`, not per initiative. Rests on migration-tools#r26 ("in every work-item's `blocked_by`, `depends_on` and `for` that names it, a name several initiatives hold being the naming work-item's own initiative's") and design-decision/work-items-named-by-ids (an id is the context's). The qualified form `work-item/<ctx>/<name>` keeps its current handling, which is right today (notes P6), and resolves the same way.
2. **`for:` is rewritten like `blocked_by` and `depends_on`.** This covers the scalar form `for: size-check`, the inline list and the block list. Rests on migration-tools#r26, which names `for`. Only a value that names a work-item changes. A `for` value that names no work-item stays as it is (Decision 5).
3. **A name several initiatives hold, none of them the referring work-item's own initiative, is refused.** The step plans everything first. If any reference is ambiguous, `migrate upgrade` exits with an error naming each one (the referring work-item's path, the field and the name, and which initiatives hold the name). It changes no file and makes no commit. Rests on migration-tools#r7, migration-tools#r20 and design-decision/upgrades-between-plugin-releases ("all or none"), and the work-item text says so ("a change `migrate` cannot make (r7)"). Today the upgrade exits 0 and says nothing (notes D3). The implementer chooses the wording of the message, as long as it names each change.
4. **The upgrade path runs the move check before writing.** It runs the same check `migrate run` uses (`check_moves` in scripts/migrate_write.py). A rename onto an existing file, or two sources to one destination, is then refused with the change named, and no file changes. Today such a collision fails inside `git mv` and the repository is reset, with a message that names nothing (notes §5). Rests on migration-tools#r7 and the Implementation note "A relocation onto a file that exists is a change it cannot make". The scenarios do not drive this, so it is covered by a unit test only.
5. **A name that names no work-item in any initiative is left as it is, and is not refused.** r26 rewrites a name "that names it", meaning a work-item. r7 refuses only a change `migrate` was asked to make. A name that names nothing asks for no change. Rests on migration-tools#r26 and migration-tools#r7. This keeps the upgrade working on a repository that already has a dangling reference, and the reference stays as dangling as it was.

## 4. Tests the decisions break

None. I checked the notes' §4, which searched `tests/` for `blocked_by`, `depends_on`, `for:` and the step's names: no test asserts that a cross-initiative or `for:` reference is left unchanged, or that an ambiguous name passes. Both tests that assert the step's behaviour stay true:
- tests/scripts/test_migrate_upgrade_ids.py, `test_a_blocked_by_written_as_a_block_list_follows_the_rename`: one initiative, so Decision 1 resolves the same way.
- S1's steps in tests/scenarios/migration_upgrade_steps.py: same-initiative `depends_on`.

`test_a_repository_with_shop_and_no_work_directory_records_the_version` is untouched: with no work-items there is nothing to resolve or refuse. If the literal Given at line 75 becomes a parsed step, the scenario that uses it must still match it; that is a rewrite of the step, not of what it asserts.

## 5. Open cases

- A work-item that names itself, or a name repeated within one list: what the rewrite gives for these.
- `for:` holding something other than a work-item name (a requirement or capability reference), which Decision 5 leaves alone. Is there such a form, and does the check that a value names a work-item tell it apart?
- A reference whose qualified form names a different context path: left as it is, or resolved?
- A name two work-items in one initiative hold (two files cannot share a stem, but the frontmatter `id` could differ from the stem): which one the step resolves to.
- Whether the refusal for an ambiguous name and the move check's refusals appear in one message when both occur.
- On this repository, the work-item's target that `model check` reports no unresolved reference after `migrate upgrade` on a clone: the implementer runs it and names any reference still unresolved and why.
