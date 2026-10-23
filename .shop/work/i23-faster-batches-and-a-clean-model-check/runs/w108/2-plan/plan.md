# w108 plan: migration-tools, one requirement a scenario, and an empty plugin-version

Planned from `runs/w108/1-research/notes.md`, the feature at 364-400 and 551-600, and `tests/scenarios/migration_version_steps.py`.

## 1. What goes green

- **migration-tools#r4**: "`migrate run` gives spec/index.md whose id is bounded-context/shop the id bounded-context/<path>" (feature 375). Red: its Given (`migration_safety_steps.py` 40-42) writes `spec/index.md` but does not commit it, so `migrate run` refuses on the uncommitted file (notes P1). Once the file is committed, the code already gives the id.
- **migration-tools#r9**: "`migrate run` gives a decision file whose id is decision/<nnnn>-<name> the type-first id" (feature 392). Red: its Given (`migration_safety_steps.py` 56-59) does not commit `decisions/0001-x.md`, so `migrate run` refuses (P2). Once the file is committed, the code already gives `design-decision/example.org/acme/shop/x`. The other r9 scenarios already pass.
- **migration-tools#r30**: outline "`migrate <command>` on a .shop/plugin-version that holds no version exits with an error, naming that it is empty or what it holds" (4 nodes: status/upgrade × is empty/holds "next"). Red: no step matches `whose .shop/plugin-version is empty` or `it says that .shop/plugin-version holds no version, <statement>`. The code also uses the old wording, `holds nothing, which is no version` / `holds "next", which is no version` (P3).
- **migration-tools#r31**: outline "a session starting in a repository whose .shop/plugin-version holds no version is told to tell the person that it is empty or what it holds" (2 nodes). Red: the `is empty` Given and the `holds no version, <statement>` Then have no step definitions, and the hook text is the old wording followed by `: tell the person.` (P3).
- **Retired** (the work-item's Retires, under delivery#r17): the deprecated scenarios at feature 364-372 (@r4), 381-389 (@r9), 551-564 (@r30 outline) and 582-588 (@r31). All four pass today and are removed from the feature.

## 2. Where the change lands

The file set is the researcher's, unchanged:

- `scripts/migrate_upgrade.py`: `no_version` and `refusal` give the new wording. An empty file is named as empty, and a file holding other text is named by quoting that text. `session_text` gives the r31 sentence. `status` and `upgrade` keep their order: they refuse first, exit 1 and change nothing.
- `tests/scenarios/migration_version_steps.py`: add the Given `a repository on the final layout whose .shop/plugin-version is empty`, the r30 Then `it says that .shop/plugin-version holds no version, {statement}` and the r31 Then `the session is told to tell the person that .shop/plugin-version holds no version, {statement}`. Remove the two old-wording Thens (35-38, 48-53), which only the retired scenarios use.
- `tests/scenarios/migration_safety_steps.py`: commit the repository in the two Givens at 40-42 and 56-59, as every other Given in the file does. Remove the step at `migration_spec_steps.py` 96-99 (`rests_on names`) only if a search shows that no other scenario uses it. If it is removed, `tests/scenarios/migration_spec_steps.py` joins the file set. Check that the `about names` step used by the retired r4 scenario is still used too, and treat it the same way.
- `features/migration-tools.feature`: remove the four retired scenarios.

## 3. Decisions

- **D-a. The refusal's wording** (r30, rests on migration-tools#r30). The message names the file, says that it holds no version, then says either that it is empty or what it holds: `.shop/plugin-version holds no version: it is empty` and `.shop/plugin-version holds no version: it holds "next"`. The step checks that this sentence appears in what `migrate` printed, after building it from `<statement>`: "and that it is empty" becomes "it is empty", "and that it holds "next"" becomes `it holds "next"`. The exact punctuation is the plan's choice. The narrator sees what r30 asks for: that the file holds no version, and that it is empty or what it holds. `status` writes it to stderr with exit 1. `upgrade` keeps its existing `migrate changed nothing; ...` prefix.
- **D-b. The hook's wording** (rests on migration-tools#r31). The session text is `Tell the person that ` followed by the D-a sentence and a full stop. It replaces today's trailing `: tell the person.`. `status --hook` still exits 0 (notes §5).
- **D-c. The empty file** (rests on migration-tools#r30/#r31; the Implementation section says the file is one line). The r30/r31 Givens for `is empty` leave `.shop/plugin-version` with nothing in it, committed. The "no file has changed" Then compares the file's stripped content with `""`. `migrate_upgrade_steps.py` is at 274 lines, so the new Given goes in `migration_version_steps.py`. If `final_layout` cannot write an empty file, the Given overwrites the file with nothing before the commit; `migration_upgrade_steps.py` is not grown for this.
- **D-d. r4 and r9 are fixed in their Givens, not in `migrate`** (rests on migration-tools#r15: `migrate run` refuses on uncommitted changes). The Givens commit, and the code is not touched (P1, P2).
- **D-e. The retirement** is the work-item's Retires, under delivery#r17. Already decided.

## 4. Tests the decisions break

- The four retired scenarios in `tests/scenarios/test_migration_tools.py`, which binds every scenario through `scenarios()`. D-a and D-b would turn the deprecated r30 (2 nodes) and r31 (1 node) red. They are removed with their scenarios (Retires), not rewritten. The deprecated r4 and r9 would still pass, but they go because they are retired.
- Their steps: the two old-wording Thens in `migration_version_steps.py` are removed, since nothing uses them after the retirement. The `holds "{held}"` Given stays, because the `holds "next"` example rows use it.
- None among the unit tests. The researcher searched `tests/scripts/` for `holds`, `which is no version` and `tell the person` and found nothing; the 18 unit tests ran green and assert none of this wording.

## 5. Open cases

The implementer names each of these in the report; this plan does not settle them:

- A file holding only whitespace (`" \n"`). Today the file is stripped, so it reads as nothing and would get the "is empty" wording. r30 calls a file empty when it is empty, and otherwise names "what it holds". The scenarios do not cover this case.
- A file of several lines (`0.23.1\nfoo\n`). Today it is quoted with its newline, so the hook sentence runs over two lines (notes D2). The scenarios do not cover this case.
- `repository_version` raises on an empty string. Only the fact that `no_version` runs first in all three callers keeps that from happening (notes §5). Name whether that guard still holds after the change.
