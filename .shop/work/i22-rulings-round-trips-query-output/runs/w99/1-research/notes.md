# w99 research notes

Work-item: w99 (`.shop/work/i22-rulings-round-trips-query-output/w99.md`), under migration-tools, accepts r30, r31.
Tools: `tools` at /home/vscode/shopsystem-bdd/scripts. No map exists: `tests-of` and `untested` refused ("no map"); running `tools map` runs the whole suite, which the brief forbids. Lists below marked `by search` where `tests-of` would have answered. `refs` used for names.
Probe file: `.shop/scratch/w99-1-research/probe_version.py` (ignored by git; not in `git status`).

## Accepted scenarios

- `features/migration-tools.feature` @r30 Scenario Outline: `migrate <command>` on a .shop/plugin-version that holds no version exits with an error, naming what it holds (Examples: status, upgrade)
- `features/migration-tools.feature` @r31 Scenario: a session starting in a repository whose .shop/plugin-version holds no version is told to tell the person

## 1. Why each scenario is red today

Command: `python3 -m pytest -q "tests/scenarios/test_migration_tools.py::test_migrate_command_on_a_shoppluginversion_that_holds_no_version_exits_with_an_error_naming_what_it_holds[status]"` (and `[upgrade]`) — run.
Result: `StepDefinitionNotFoundError: Step definition is not found: Given "a repository on the final layout whose .shop/plugin-version holds "next""` (Line 538). Same for `[upgrade]` by the same Given (read: identical Given).

Command: `python3 -m pytest -q "tests/scenarios/test_migration_tools.py::test_a_session_starting_in_a_repository_whose_shoppluginversion_holds_no_version_is_told_to_tell_the_person"` — run.
Result: same undefined Given, line 552.

Undefined steps, by read (grep of `tests/scenarios/`; pytest-bdd stops at the first undefined step, so these are not seen in a run):
- r30 Given `a repository on the final layout whose .shop/plugin-version holds "next"`: the step at `migration_upgrade_steps.py:63` matches only `[\d.]+|the plugin's version`; nothing matches `holds "<text>"`.
- r30 Then `migrate exits with an error`: `migration_upgrade_steps.py:136` is `it exits with an error`; text differs.
- r30 Then `it says that .shop/plugin-version holds "next", which is no version`: no step.
- r30 Then `no file of the repository has changed`: no step (`git status shows nothing uncommitted` at `migration_upgrade_steps.py:219` is a different text).
- r30 When `the session runs \`migrate <command>\`` with the Examples filled: matches `migration_upgrade_steps.py:115` (read).
- r31 When `a session starts in the repository`: existing `the person starts a session in it` (`migration_upgrade_steps.py:127`) differs; no step.
- r31 Then `the session is told to tell the person that .shop/plugin-version holds "next", which is no version`: no step.

Code behind the steps (read): the code side already refuses. `scripts/migrate_upgrade.py`: `no_version` (l.36-42) returns `repr(held)`, so the text is `'next'` in single quotes; `refusal` (l.45-46); `status` (l.59-68) and `upgrade` (l.117-156) refuse on it; `session_text` (l.71-87) returns `".shop/plugin-version holds 'next', which is no version: tell the person.\n"`. The scenario's literal text has double quotes (`"next"`). The missing parts are the step definitions, and the quoting if the scenario's text is asserted literally (see 6).

## 2. What the system answers today

Probes (`probe_version.py`, run with `python3 -m pytest -q -s -n 0 .shop/scratch/w99-1-research/probe_version.py`, 8 passed; each repo built in the scratch dir, `scripts/migrate` of the worktree run by absolute path):

- `migrate status` on `.shop/plugin-version` = `next\n` (scenario Given, final layout with `spec/index.md`): rc=1, stdout empty, stderr `.shop/plugin-version holds 'next', which is no version`. Commits 1, `git status` empty. — run.
- `migrate upgrade`, same repo: rc=1, stderr `migrate changed nothing; .shop/plugin-version holds 'next', which is no version`; commits 1; status empty; file still `next`. — run.
- `migrate status --hook` (the hooks.json command, `status --hook`), same repo: rc=0, stdout `.shop/plugin-version holds 'next', which is no version: tell the person.` — run.
- Nearest cases:
  - `upgrade` with `next` and a dirty tree (`spec/index.md` modified): rc=1, stderr names the version only, not the uncommitted change; the dirty file stays ` M`. — run.
  - empty file (`\n`): status rc=1 `.shop/plugin-version holds nothing, which is no version`; hook rc=0 `... holds nothing, which is no version: tell the person.`; upgrade rc=1 — run.
  - `v0.24.0`: status rc=1 `holds 'v0.24.0'`; hook rc=0 with the same shape — run.
  - `0.24.0 beta`: refused like `next` — run.
  - `next\nfoo`: `holds 'next\\nfoo'` — run.
  - `next` with no trailing newline: same as `next` — run.
  - `0.24` (dotted but short): not refused; status prints `repository's plugin version: 0.24` and a pending step — run. Not in scope; recorded as the boundary of `no_version`'s regex.
  - file absent, `.shop/` present: hook prints an upgrade offer from 0.23.1 (r19 default); status rc=0 — run.
  - no `.shop/` at all: hook prints nothing, rc=0 — run.
- Existing unit tests `tests/scripts/test_migrate_upgrade.py` (5 passed, 6 subtests; run). They cover `next` and empty file for status, upgrade and the hook, checking substrings only.

## 3. Old assumptions

The requirements add no new form; they refuse a form the code already refuses. The old assumption that matters: `.shop/plugin-version` holds dotted numbers, which `number()` relies on. Each place that reads the raw text:

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/migrate_upgrade.py:repository_version (l.31-33) | returns the raw text, `UNRECORDED` if absent | non-dotted text must never reach it: refused first | none (non-dotted text never reaches it; by read) | refs (4 uses) |
| scripts/migrate_upgrade.py:pending (l.49-52) | `number(repository_version(root))`: raises ValueError on `next` | guarded: `status`, `upgrade`, `session_text` call `no_version` first | by search: tests/scripts/test_migrate_upgrade_ids.py and the 0.23.1/0.24.0 scenario steps (dotted only) | refs |
| scripts/migrate_upgrade.py:number (l.23-24) | `int(part)` on each dot part | same; non-numeric parts never reach it | none for non-dotted text (by read) | refs |
| scripts/migrate_upgrade.py:session_text (l.78-79) | `number(here) > number(there)` after the `no_version` check | guarded at l.75-77 | by search: scenario hook steps (dotted only); test_migrate_upgrade.py test_the_hook... (refusal branch only) | refs |
| scripts/migrate_upgrade.py:status (l.64) | prints `repository_version` | after the l.60-63 guard | by search: test_migrate_upgrade.py test_status... (refusal branch only); scenarios for 0.23.1 | refs |
| scripts/migrate_upgrade.py:upgrade (l.131, l.145-147) | `before = repository_version`; writes plugin version to the file | after the l.118-121 guard; a refused file is never overwritten | by search: test_migrate_upgrade.py test_upgrade_refuses... (refusal branch only, asserts file unchanged) | refs |
| scripts/migrate_upgrade.py:refusal (l.45-46) | message `%s holds %s, which is no version` with `held` from `no_version` | scenario text uses double quotes around the held text | by search: test_migrate_upgrade.py (asserts only `.shop/plugin-version` and the held text as substring) | refs |
| scripts/migrate_upgrade.py:no_version (l.36-42) | returns `repr(held)` or `nothing` | quoting differs from the scenario's `"next"` | by search: test_migrate_upgrade.py (substring `next`, so both quotings pass) | refs |

Only `migrate_upgrade.py` reads the file (`grep plugin-version scripts/ tests/`, read). `migrate_upgrade_ids.py` / `migrate_upgrade_answers.py` do not read it (grep, read).

## 4. Tests the requirements make impossible to keep

No `tests-of` answer (no map). By search: the tests that exercise the refusal are in `tests/scripts/test_migrate_upgrade.py`, class `AVersionFileThatHoldsNoVersion` (l.63-95): `test_status_prints_nothing...`, `test_upgrade_refuses...`, `test_the_hook_exits_0...`.
- Ran: 5 passed. Each asserts `.shop/plugin-version` and the held text as substrings and `tell the person` for the hook. Changing the quoting from `'next'` to `"next"` keeps them passing. Found sound.
- No test asserts the single-quoted form or the hook's wording exactly. none that the requirements break.
- The scenario-level steps for r30/r31 do not exist yet: nothing to keep, but the new steps must match the text in the feature.

## 5. A step the work-item skips

The `upgrade` refusal runs before the uncommitted-change check (`migrate_upgrade.py` l.117-126): the existing path checks uncommitted changes first (r15). With `next` and a dirty tree, the r15 refusal is not shown (probe above, run). The version refusal names the version only. This is the existing order, not a new path; the work-item adds nothing that leaves a step out. `status` has no uncommitted check (by read: `status` l.59-68). The hook has no write, so no skipped step.

## 6. Defects

No crash found. One divergence from the scenario's wording:

Reproduction (run): repo on final layout, `.shop/plugin-version` = `next` (line), committed. `python3 <worktree>/scripts/migrate status` → stderr `.shop/plugin-version holds 'next', which is no version`. The scenario's Then reads `.shop/plugin-version holds "next", which is no version` (double quotes). A step asserting that text literally would fail on the quotes. Output is single quotes because `no_version` uses `repr` (migrate_upgrade.py l.42). The hook prints the same single-quoted form (run).

Observation, not a defect: an empty file reads `holds nothing, which is no version` (run); the scenario does not cover it.

## 7. The file set

Production:
- `scripts/migrate_upgrade.py` (170 lines; room 130). Change `no_version`'s `repr` to the double-quoted form the scenario names (or the step decides how to match). Found by: read of l.36-46, scenario text (run probe above).

Tests:
- `tests/scenarios/migration_upgrade_steps.py` (274 lines; room 26). Holds the existing `migrate status|upgrade` and hook steps. Too little room for the new steps; do not add there unless they are a few lines. Found by: read.
- New module `tests/scenarios/migration_version_steps.py` (new; would be well under 300). Holds the new Given `holds "<text>"`, the Thens `migrate exits with an error`, `it says that ... holds "...", which is no version`, `no file of the repository has changed`, the When `a session starts in the repository`, and the hook Then. Must be imported in `tests/scenarios/test_migration_tools.py` (227 lines; room 73), which lists imports at l.10-15. Found by: that file's import lines (read), pytest-bdd undefined steps (run).
- `tests/scenarios/test_migration_tools.py` (227 lines; room 73). Add the import line for the new module. It binds all scenarios by `scenarios()` (read).
- `tests/scripts/test_migrate_upgrade.py` (99 lines; room 201). Keeps passing as it is (run). No change needed.
- `features/migration-tools.feature`: no change; scenarios already present (read).
- `tests/scenarios/migration_old.py` (81 lines): `said`, `CONTEXT`, `Old` reused; no change (read).
- `tests/scenarios/conftest.py` (176 lines): `run` fixture runs `scripts/<name>` (l.27-33); used by the existing When steps; no change (read).

Modules on the change's path, edited or not, with line count and room (300 limit; `tools size --limit 300` printed nothing, so none is over):
- scripts/migrate (71 lines; room 229) — entry point; not edited.
- scripts/migrate_upgrade.py (170; room 130) — edited.
- scripts/migrate_write.py (126; room 174) — imported by migrate_upgrade for `uncommitted`; not edited.
- hooks/hooks.json — not Python; the SessionStart command `status --hook`.
- tests/scenarios/test_migration_tools.py (227; room 73) — edited (import).
- tests/scenarios/migration_upgrade_steps.py (274; room 26) — not edited.
- tests/scenarios/migration_old.py (81; room 219) — not edited.
- tests/scenarios/conftest.py (176; room 124) — not edited.
- tests/scripts/test_migrate_upgrade.py (99; room 201) — not edited.
