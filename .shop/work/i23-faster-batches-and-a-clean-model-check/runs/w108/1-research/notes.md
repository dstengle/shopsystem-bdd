# w108 research notes

Tools: `scripts/tools` of plugin 0.24.0. `tools map` not run (it writes outside my scratch and runs the suite), so there is no map: `tests-of` and `untested` unavailable, and every test list below is `by search`. `tools refs` misses uses in the extensionless `scripts/migrate` and by sibling-module import (`plan_index`: 0 refs; `reid`: 1 of 3 call sites), so call lists are `by search` (grep) too. `tools size --limit 300`: no tracked Python file over 300.

Probe file: `.shop/scratch/w108-1-research/probe_migrate.py`, run as `python3 -m pytest -q -s -n 0 -p no:warnings <path>`. It drives the worktree's `scripts/migrate` in scratch git repositories.

## 1. Why each scenario is red today

Run: `python3 -m pytest -q -n 0 --tb=line` on the 19 node ids of the accepted scenarios in `tests/scenarios/test_migration_tools.py`: 8 failed, 11 passed (`run`).

Red (`run`):
- r4, `spec/index.md gives the id bounded-context/shop` (feature 375): AssertionError `tests/scenarios/migration_spec_steps.py:28`. Its Given (`migration_safety_steps.py:40-42`) writes the file and does not commit it, so `migrate run` refuses on an untracked file (P1). With a commit, the code gives the id (P1, committed). Missing: `old.commit()` in that Given.
- r9, decision file plain (feature 392): FileNotFoundError `spec/decisions/0001-x.md`. Its Given (`migration_safety_steps.py:56-59`) writes `decisions/0001-x.md` without a commit; `migrate run` refuses (P2). With a commit, the code gives `design-decision/example.org/acme/shop/x` (P2). Missing: `old.commit()`.
- r30 outline, 4 nodes (feature 567-580, `status`/`upgrade` x `is empty`/`holds "next"`): StepDefinitionNotFound. `Given ... plugin-version is empty` (line 569) has no step: `migration_version_steps.py:14` matches only `holds "{held}"`. `Then it says that ... holds no version, <statement>` (line 572) has no step: `migration_version_steps.py:35` wants `holds "{held}", which is no version`. Code behind: `scripts/migrate_upgrade.py:refusal` (45-46) and `no_version` (36-42) word the refusal as `holds nothing, which is no version` or `holds "next", which is no version` (P3).
- r31 outline, 2 nodes (feature 591-599): StepDefinitionNotFound for `Given ... is empty` (593) and `Then the session is told ... holds no version, <statement>` (595). Code behind: `scripts/migrate_upgrade.py:session_text` (71-77) appends `: tell the person.` to the same wording (P3).

Green today (`run`), so not targets: the four `(deprecated)` scenarios (feature 365, 382, 552, 583), which are in the work-item's Retires and pass against today's wording; r4 plain with no id (162); r9 type-first ids (262); r9 capability short form (277); r9 README outline, 3 nodes (284).

## 2. What the system answers today

P1, `probe_migrate.py::test_r4_*` (`run`), `migrate run --context example.org/acme/shop`:
- `spec/index.md` untracked, id `bounded-context/shop`: rc 1, `could not start from a tree with an uncommitted change: spec/index.md`; file unchanged.
- committed, id `bounded-context/shop`: rc 0, id `bounded-context/example.org/acme/shop`.
- committed, no frontmatter: rc 0, id added.
- no `spec/index.md`, other file tracked: rc 0, no index created.

P2, `probe_migrate.py::test_r9_*` (`run`):
- `decisions/0001-x.md` untracked: rc 1, refusal naming it; nothing moved.
- committed, id `decision/0001-x`: moved to `spec/decisions/0001-x.md`, id `design-decision/example.org/acme/shop/x`.
- committed, no id, `decisions/0002-y.md`: id `design-decision/example.org/acme/shop/y`.
- committed, unnumbered `decisions/z.md`, id `decision/z`: id `design-decision/example.org/acme/shop/z`.

P3, `probe_migrate.py::test_version_*` (`run`), `.shop/plugin-version` on the final layout:
- empty file: `status` rc 1, stderr `.shop/plugin-version holds nothing, which is no version`. `upgrade` rc 1, `migrate changed nothing; ...` with the same text. Hook stdout `...holds nothing, which is no version: tell the person.` Git log and status unchanged.
- `next\n`: `status`/`upgrade` rc 1, `holds "next", which is no version`; hook adds `: tell the person.`.
- ` \n` (spaces and newline): `holds nothing`, since the file is stripped.
- `0.23.1\nfoo\n`: `holds "0.23.1\nfoo", which is no version`, rc 1; the hook sentence spans two lines.
- no version file, `.shop/` present: `status` rc 0, repository 0.23.1, plugin 0.24.0, pending `0.24.0 "work-items named by ids"`.
- no `.shop/`: hook stdout empty.

Unit tests (`run`): `tests/scripts/test_migrate_layout.py`, `test_migrate_write.py`, `test_migrate_upgrade.py`, `test_migrate_upgrade_ids.py`: 18 passed.

## 3. Old assumptions

Places that make the old version-file wording or the old id handling. `tests` column: `by search` (grep for the function, the sentence, or the migrate command in `tests/`).

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/migrate_upgrade.py:refusal (45-46) | `holds %s, which is no version` for every held text | r30/r31: `holds no version, and that it is empty` or `..., and that it holds "next"` | r30/r31 nodes in tests/scenarios/test_migration_tools.py (by search) | refs (no_version callers), grep |
| scripts/migrate_upgrade.py:no_version (36-42) | `"<text>"` for held text, `nothing` for empty | the empty case must name the file as empty; other text stays named | r30/r31 nodes (by search); no unit test | refs (3 refs in file), grep |
| scripts/migrate_upgrade.py:status (59-68) | refusal to stderr, rc 1, before any output | r30 keeps it: rc 1, change nothing; wording only | r30 status nodes (by search) | refs, read |
| scripts/migrate_upgrade.py:session_text (71-77) | refusal plus `: tell the person.` | r31: `tell the person that the file holds no version, ...` | r31 nodes (by search) | refs (1 ref, migrate:168), read |
| scripts/migrate_upgrade.py:upgrade (117-126) | refusal before the uncommitted check | r30 keeps order: nothing changes | r30 upgrade nodes (by search) | refs, read |
| scripts/migrate_upgrade.py:repository_version (31-33) | reads `.strip()`; an empty file gives `""`, and `number("")` raises | none; no_version refuses first at 64, 78, 131 | none (no test reaches it with an empty file) | read |
| scripts/migrate_upgrade.py:no_version regex (38-42) | a two-line text is quoted with its newline | r30 `what it holds`: a reading question (see 6) | none (no test) | run (P3) |
| tests/scenarios/migration_version_steps.py:35-38, 48-53 | assert `which is no version` (and `: tell the person.`) | these steps belong to the deprecated scenarios only (by search) | the 4 deprecated nodes | grep |
| scripts/migrate_spec.py:plan_index (79-81) | reid `spec/index.md` to `bounded-context/<context>` | r4 unchanged; it already does it (P1) | scenario nodes through `migrate run` (by search); no unit test (grep) | grep |
| scripts/migrate_layout.py:reid (84-93) | rewrites an old id and records it in `plan.renamed` for references | r5 keeps the rewrite; the retired deprecated scenarios test it, not a requirement change | test_migrate_write.py:41-42 (by search); scenario nodes | grep, refs (1 ref) |
| scripts/migrate_layout.py:plan_ids (109-120) | type-first ids for moved records and decisions | r9 unchanged | test_migrate_layout.py:37-40, test_migrate_write.py:41 (by search) | grep |
| scripts/migrate_layout.py:record_kind (96-106) | kind of a moved record | r9 unchanged | test_migrate_layout.py:26-35 (by search) | refs, grep |
| scripts/model_facts.py:121-133 (not migrate) | reads `spec/index.md` id as `bounded-context/<owner>/<product>/<context>` only | r4 is what makes this hold after migrate | none found: tests/scripts/test_model.py:27 uses the full form (grep) | grep, read of 128-130 |
| README.md:141 | documents the file, `none means 0.23.1` | says nothing of the refusal; none to change unless the plan documents it | none | grep |

## 4. Tests the requirements make impossible to keep

Mode: `by search`, no map.
- `tests/scenarios/test_migration_tools.py`, deprecated r30 (2 nodes) and deprecated r31 (1 node): pass today; their Then asserts `which is no version` and `: tell the person.`. Once the wording changes (r30/r31) they cannot pass, so they go with their scenarios (Retires). Only retirement keeps none.
- `tests/scenarios/test_migration_tools.py`, deprecated r4 (365) and r9 (382): pass today. r5 still requires the rewrite they check, so they could keep passing; they go only because they are retired.
- `migration_version_steps.py:35-38, 48-53` and `migration_spec_steps.py:96-99` (`rests_on names`, only deprecated r9 by search): become unused once those scenarios are removed.
- Verified sound: the 18 unit tests (run) assert no wording of the version refusal (grep for `holds`, `which is no version`, `tell the person` in `tests/scripts/`: none). The r9 type-first, capability short-form and README nodes pass (run) and keep passing.

## 5. A step the work-item skips

- The Givens of accepted r4 and r9 do not commit, where every other Given of the file does (`old.commit()`). Existing way (P1, P2): `migrate run` refuses on the untracked file with rc 1 and changes nothing. Effect only the commit gives: the file is tracked, so `plan_moves` (`migrate_layout.py:62-66`, `tracked()`) and `plan_index` (`migrate_spec.py:80`) see it. `run`.
- The hook path: `status --hook` prints the session text and exits 0 whatever the file holds (`migrate_upgrade.py:run`, 159-170), and never prints the status refusal or exits 1. Effect only `status` gives: rc 1 and stderr. Verified by reading; the stdout text is `run` (P3). `read`.
- An empty file reaching `repository_version` would raise `ValueError` in `number("")`; only `no_version` (which runs first in all three callers) prevents it. `read`, not probed.

## 6. Defects

D1. An empty `.shop/plugin-version` is named as `holds nothing`. Reproduce: repository on the final layout with an empty file, committed; `python3 scripts/migrate status` gives rc 1, stderr `.shop/plugin-version holds nothing, which is no version` (P3). r30 and r31 say the file is named as empty. Reading A: this is the defect. Reading B: a whitespace-only file also counts as empty, and today's `strip()` gives it the same `nothing`.

D2. A version file of two lines is quoted with its newline: `.shop/plugin-version holds "0.23.1\nfoo", which is no version` (P3), and the hook text spans two lines. r30/r31 say "what it holds". Reading A: acceptable. Reading B: defect, as the hook sentence breaks.

## 7. The file set

Must change:
- `scripts/migrate_upgrade.py` (170 lines; room 130): `refusal`, `no_version`, `session_text` wording for empty and other text; `upgrade` and `status` keep order. Found by refs, grep, P3.
- `tests/scenarios/migration_version_steps.py` (53; room 247): add the `is empty` Given, the `holds no version, <statement>` Then for r30, and the r31 Then; drop the old sentence steps when the deprecated scenarios go. Found by grep, feature 566-599.
- `tests/scenarios/migration_safety_steps.py` (120; room 180): add `old.commit()` to the Givens at 40-42 (spec/index.md) and 56-59 (decisions/0001-x.md). Found by P1, P2.
- `features/migration-tools.feature` (600 lines; not Python, no size limit): remove the four retired scenarios: r4 deprecated (364-372), r9 deprecated (381-389), r30 deprecated outline (551-564), r31 deprecated (582-588). Found by feature grep, the work-item's Retires.

Modules on the change's path, not edited (lines counted with `wc -l`, or the last line read; room under 300):
- `scripts/migrate` (71; room 229), `scripts/migrate_layout.py` (131; 169), `scripts/migrate_spec.py` (132; 168), `scripts/migrate_ledger.py` (123; 177), `scripts/migrate_write.py` (126; 174), `scripts/migrate_upgrade_ids.py` (128; 172), `scripts/migrate_upgrade_answers.py` (43; 257).
- `hooks/hooks.json` (14 lines; no limit: JSON), its SessionStart command runs `migrate status --hook`.
- Test files on the path, not edited: `tests/scenarios/test_migration_tools.py` (228; 72), `tests/scenarios/migration_old.py` (81; 219), `tests/scenarios/migration_upgrade_steps.py` (274; 26: do not add to it).
