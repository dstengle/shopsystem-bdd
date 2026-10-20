# Plan: migrate-run (accepts migration-tools#r1-r11)

## 1. What goes green

All ten scenarios of `features/migration-tools.feature`. Today each one fails at its first Given with StepDefinitionNotFoundError. `scripts/migrate` does not exist, `tests/scenarios/test_migration_tools.py` does not exist, and `tests/scripts/test_bound.py` does not list the feature (notes 1).

- r1: "run moves decisions/ to spec/decisions/, work/ to .shop/work/ and each records/<x> to .shop/records/<x>, with git"
- r2, r11: "run replaces a ledger that has only entries with a decision file for each, named by its heading, with its first paragraph, accepted, with its date and source". r11 has no other scenario.
- r3: "run deprecates a @holding scenario as `features deprecate` does"
- r4: "run gives spec/index.md the id bounded-context/<path>"
- r5: "run rewrites a repository-relative path, a relative Markdown link and a frontmatter id that name what it moved or renamed"
- r6: "after run, model check reports no violation, unresolved reference or file problem"
- r7: "run that cannot make two of its changes names both, exits non-zero and changes no file"
- r8: "run moves docs/superpowers/plans/ and docs/superpowers/specs/ under .shop/records/archive/, with git"
- r9: "run gives a capability, a decision file, a plan, a design note and a test log the type-first id of its kind"
- r10: "run numbers each Behaviour line with no id, in Behaviour order, from one above the highest id its capability has ever used"

The work-item retires no deprecated scenarios. It has no Retires section and no Rulings.

## 2. Where the change lands

The researcher's set, unchanged:

- `scripts/migrate` (new). The `run --context <owner/product/context>` subcommand, written in Python 3 with the standard library only. It works in two phases: first it plans every move and every new file text, then it checks the plan, then it writes. It loads `scripts/model` by file path to read frontmatter and to render `spec/decisions/index.md`, and it runs `scripts/features` for deprecation (decision D3).
- `tests/scenarios/test_migration_tools.py` (new). Binds `scenarios("migration-tools.feature")` once. Holds the step definitions, which build each old-system repository as a committed scratch git repository and use the existing `run` fixture from `tests/scenarios/conftest.py`.
- `tests/scripts/test_bound.py`. Adds `features/migration-tools.feature` to the list of bound features.

No file is added or removed. `scripts/model`, `scripts/features` and `conftest.py` are used but not changed.

## 3. Decisions

- **D1. Every change is computed and checked before the first write.** All moves, new files, rewritten texts and the ledger's removal are planned in memory first. Then migrate checks the whole plan: a destination that already exists, two sources with one destination, an untracked source, and a deprecation that `features deprecate` refuses. If any check fails, migrate lists every failed change, one line each naming its source(s) and destination, exits 1, and touches nothing: no working-tree file and no index entry. Only after that does it run `git mv` and write texts. Rests on migration-tools#r7 and its Implementation note ("computed first, then written"; a move onto an existing file cannot be made). The notes show `git mv` is not atomic (5b), which is why the checks must all come first.
- **D2. Moves go file by file, not directory by directory.** Each tracked file under `decisions/`, `work/`, `records/<x>/`, `docs/superpowers/plans/` and `docs/superpowers/specs/` gets its own `git mv` to its mapped path, creating parent directories as needed. Moving a whole directory onto an existing `spec/decisions/` would nest it (notes 2.9), and the ledger split creates that directory in the same run. Old directories left empty are removed. Rests on migration-tools#r1, #r8 and the r7 Implementation note. Nothing is committed: the renames stay staged, which is what the "git status shows renamed" Thens read.
- **D3. A `@holding` scenario is deprecated by `features deprecate`, then its `@holding` tag is removed.** For each scenario tagged `@holding`, migrate runs `scripts/features deprecate <title> --for-removal --file <feature>` on a temporary copy of the feature files outside the repository. It takes the result as that file's planned text and then drops the `@holding` tag from the scenario's tag line. A refusal from `features deprecate` (a `Rule:` block, an ambiguous title, an already deprecated scenario) is a change migrate cannot make, under D1. It uses `--for-removal` because a held scenario names no replacement, and picking one is the session's judgment, not transcription. Test files are left untouched, which is what `features deprecate` does too. Rests on migration-tools#r3 ("as features deprecate does … with no @holding tag left"), design-decision/migration-in-one-pass ("refuses rather than guesses"; mapping scenarios is the session's job) and the work-item's "reuses … `features deprecate`".
- **D4. In the r3 Then, the copy is compared after its `@holding` tag is dropped.** The copy made by running `features deprecate` keeps `@holding` (notes 2.1, D1 of the notes). The step definition therefore compares the migrated feature file with the copy's file once the `@holding` tag is removed from the copy, checks that no `@holding` is left, and compares the test file byte for byte. Rests on migration-tools#r3. The feature file is not edited (design-decision/feature-files-read-only-in-red-green).
- **D5. How a ledger entry is read.** The ledger is the old form in `.shop/records/archive/design-notes/2026-09-29-capability-spec-design.md`: a `## decision/<nnnn>-<slug>` heading, a first paragraph, then `date:`, optional `revisit_when:`, `supersedes:` and `source:` lines. Each entry becomes `spec/decisions/<nnnn>-<slug>.md` with frontmatter `id`, `summary` (the first paragraph), `date`, `status: accepted` and `by` (the source, in words), and a body holding a `## Decision` section with the first paragraph. The id is `design-decision/<path>/<slug>`, without the number. Once every entry is replaced, `spec/decisions.md` is removed, and `spec/decisions/index.md` is written with model's own renderer, loaded by path. Rests on migration-tools#r2, #r9, #r11, the Implementation note (the index "as `model decisions` writes it") and design-decision/references-are-ids (a source that is not an id goes in `by`).
- **D6. Ids are written only where none is given, and records get `id` plus `kind`.** A capability, a decision file, a moved plan, a moved design note or a moved test log that has no frontmatter `id` gets `<kind>/<path>/<stem>`. A decision file's stem loses its number. Moved records also get `kind`: `initiative-archive`, `decision-argument` or `measurement`. Model check refuses a record that has an id but no kind (notes 2.3), and design-decision/references-are-ids gives those kinds. Any other moved record (for example `records/logs/r1.md`) gets no id and keeps its content byte for byte, as the r1 Then requires; model check skips records without an id. Rests on migration-tools#r9, #r1, #r6 and design-decision/references-are-ids.
- **D7. Reference rewriting works on the planned texts of all tracked text files.** The tracked files are those `git ls-files` lists that decode as UTF-8. Rewriting covers three things:
  - a repository-relative path equal to a moved file's old path, or to a directory prefix of it, matched on path boundaries;
  - a relative Markdown link, resolved from the linking file's old location and rewritten relative to its new location;
  - an old id in frontmatter. `decision/<nnnn>-<slug>` becomes `design-decision/<path>/<slug>`, written in full form as the r5 Then expects.

  This happens within the same plan, so D1's all-or-nothing holds. Rests on migration-tools#r5 and design-decision/capability-ids-are-context-scoped.
- **D8. Numbering.** A capability's highest used id is the largest of its live `[r<n>]` ids and the entries of its frontmatter `retired:`. Lines with no id get the next numbers in Behaviour order, written as `[r<n>] ` before the line's text. Rests on migration-tools#r10 and design-decision/retired-ids-in-capability-frontmatter.
- **D9. `spec/index.md` gets `id: bounded-context/<path>`** in its frontmatter. If it has no frontmatter, one is added. Rests on migration-tools#r4.
- **D10. The r6 fixture is a complete old-system repository; migrate writes no initiative.** The fixture includes:
  - `spec/index.md` with no id;
  - a capability whose every line has a `@r<n>` scenario and whose `rests_on` names the ledger entry;
  - `work/i1/` with a final-form `initiative.md`;
  - `records/logs/run1-test-log.md`;
  - one file each under `docs/superpowers/plans/` and `docs/superpowers/specs/`;
  - the ledger;
  - `decisions/` holding one final-form decision file;
  - a `@holding` scenario.

  model check needs `initiative.md` in every work directory (notes 2.6), but writing an initiative is not transcription: it belongs to the living-plan step, which the capability lists as "Not yet". Rests on design-decision/migration-in-one-pass and design-decision/living-plan-to-work-items. In the same spirit, the r1 fixture's `decisions/0001-d0.md` already carries a final-form id, so D6 and D7 change nothing in it and its content survives byte for byte (migration-tools#r1).

## 4. Tests the decisions break

None. I checked the notes' list (part 4):
- the deprecate tests in `tests/scenarios/test_feature_file_tools.py`: `features deprecate` is used, not changed (D3);
- the `@holding` and OLD_LAYOUT tests in `tests/scenarios/test_design_model_check.py`: `scripts/model` is loaded, not changed (D5);
- `tests/scripts/test_plan.py` and `test_measure.py`: their code is not touched;
- `tests/scripts/test_bound.py`: it only gains an entry and stays green once the feature is bound exactly once.

No decision above changes any other file in the set.

## 5. Open cases

The scenarios don't settle these. The implementer names each one in the report, without choosing for the requirement:

- a directory under `work/` with no `initiative.md`: migrate leaves model check failing for it, or refuses;
- whether a moved record also gets `about`, and what it names (references-are-ids lists it; r9 asks only for the id);
- a ledger with text outside its entries, and entries carrying `supersedes:` or `revisit_when:`;
- the title line of a new decision file;
- an existing id in an old form (`decision/<slug>` with no number, `<context name>/<name>`, a `decision/` id inside a moved decision file);
- `spec/index.md` that already has a different id, or no `spec/index.md` at all;
- an untracked or binary file under a moved directory;
- a `--context` value that is not three names;
- prose that names an old directory (for example "work/") rather than a file;
- references to `spec/decisions.md` after it is removed;
- a scenario that is tagged `@holding` and already `@deprecated`.
