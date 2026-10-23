# Plan of w99: migrate on a version file that holds no version

Work-item `.shop/work/i22-rulings-round-trips-query-output/w99.md`, under migration-tools, accepts r30 and r31. No Retires section, no Rulings. From the research notes `runs/w99/1-research/notes.md`.

## 1. What goes green

- **migration-tools#r30**: the Scenario Outline "`migrate <command>` on a .shop/plugin-version that holds no version exits with an error, naming what it holds" (Examples `status` and `upgrade`). It is red today because the Given "a repository on the final layout whose .shop/plugin-version holds "next"" has no step definition (run: StepDefinitionNotFoundError). By read, the Thens "migrate exits with an error", "it says that .shop/plugin-version holds "next", which is no version" and "no file of the repository has changed" have no steps either. Only the When ("the session runs `migrate <command>`") exists. The code already refuses. Its message, though, quotes the held text as `'next'` (single quotes, from `repr` in `no_version`), where the scenario says `"next"`.
- **migration-tools#r31**: the Scenario "a session starting in a repository whose .shop/plugin-version holds no version is told to tell the person". It is red for the same undefined Given. By read, the When "a session starts in the repository" and the Then "the session is told to tell the person that .shop/plugin-version holds "next", which is no version" are undefined too. The hook (`migrate status --hook`) already prints the refusal followed by "tell the person", with the same single quotes.
- Deprecated scenarios retired: none.

## 2. Where the change lands

- `scripts/migrate_upgrade.py` (170 lines): `no_version` names the held text in double quotes, not through `repr` (decision D1). `refusal`, `status`, `upgrade` and `session_text` stay as they are; they carry the new form unchanged.
- `tests/scenarios/migration_version_steps.py` (new): the steps of section 1 that are missing: the Given, the three r30 Thens, the r31 When and the r31 Then. It reuses `final_layout` and `plugin_version` from `migration_upgrade_steps.py` and `said` from `migration_old.py`.
- `tests/scenarios/test_migration_tools.py` (227 lines): one import line for the new step module, next to the others (l.10-15).

The file set is the researcher's. `tests/scenarios/migration_upgrade_steps.py` (274 lines) is not edited because it has room for only a few more lines (D3). `tests/scripts/test_migrate_upgrade.py` keeps passing unchanged (section 4). `features/migration-tools.feature` is not changed.

## 3. Decisions

- **D1. The refusal names the held text in double quotes**, exactly as the accepted scenarios read: `.shop/plugin-version holds "next", which is no version`. This applies to `status` and `upgrade` (stderr) and to the hook (stdout), which share the message. An empty file still reads "holds nothing". This rests on migration-tools#r30 ("naming what it holds") and #r31, on their accepted scenarios' text, and on the work-item ("change the code only where a scenario shows it differs"). In this feature a Then about what migrate prints treats its quoted text literally: the step behind "it prints the pending upgrade step 0.24.0 "work-items named by ids"" asserts the double quotes in the output. Both quotings satisfy the requirement lines. The scenario text, which is accepted, settles the form, so this is not a question.
- **D2. The steps assert the whole sentence, quotes included.** "it says that …" asserts the sentence in what migrate said (stdout and stderr, as `said` gathers them). The r31 Then asserts the same sentence followed by "tell the person" in the hook's stdout, with exit 0. "migrate exits with an error" asserts a non-zero exit. "no file of the repository has changed" asserts three things: `git status --porcelain` is empty, the commit count equals the one the When recorded (`before_log`), and `.shop/plugin-version` still holds `next`. The Given builds the final layout with `final_layout`, giving the version file the quoted text without the quotes (the feature's convention for a Given's quoted value), and commits it. This rests on #r30 ("change nothing") and #r31.
- **D3. The new steps go in a new step module.** The When "a session starts in the repository" runs the SessionStart command of `hooks/hooks.json`, the way the existing "the person starts a session in it" does. The implementer either reuses that step's body as a shared helper or reproduces the same run; the existing step's text does not change. This rests on CLAUDE.md's 300-line limit and module map ("one `<capability>_*_steps.py` module a concern"). The new module is a concern of an existing row, `tests/scenarios/`, so no new row in the map is needed.

## 4. Tests the decisions break

None. I checked `tests/scripts/test_migrate_upgrade.py`, class `AVersionFileThatHoldsNoVersion` (l.63-95). Its tests `test_status_prints_nothing_and_says_on_stderr_what_the_file_holds`, `test_upgrade_refuses_in_the_same_words_and_changes_nothing` and the hook test assert only these substrings: `.shop/plugin-version`, the held text (`next` or `nothing`) and `tell the person`. They also assert the exit codes, a one-line hook output and no Traceback. None of them asserts the quote character, so D1 keeps them passing. The notes found no other test that executes `no_version` or `refusal` (by search; no coverage map exists). No existing scenario step text changes (D3).

## 5. Open cases

- Held text containing a double quote, a backslash or a newline (the notes probed `next\nfoo`, which `repr` escaped today). How the double-quoted form shows such characters is left for the implementer to name. The hook's output must stay one line (the existing hook test asserts one line).
- A dotted but short value such as `0.24` is not refused (probed). r30 and r31 do not say whether it is a version; it is out of scope here.
- `upgrade` with a non-version file and a dirty tree reports only the version refusal, not the uncommitted change (r15). That is the existing order, and the scenarios do not cover it.
