# Re-review of migrate-run: DONE_WITH_CONCERNS

Verdict: the run-2 fixes close the earlier review's F1, F2, F3, F5, F7 (in part), M1, M4 and, with the person's r12, F4. Two things still go to the person:
- **Critical (rule):** the fix commits 115e50c and 5eaf500 change `features/migration-tools.feature`. They add eleven scenarios and outline rows and reword r8's two Thens. The same session wrote the code. Nothing records formulation or a person's approval for anything but r12.
- **Important, fix now:** a moved plan or design note that is not Markdown is still read and given frontmatter. An image under `docs/superpowers/specs/` crashes the run with a traceback. A `.json` plan is corrupted by a YAML header.

## Commits reviewed
The branch `work/migrate-run` is gone. The claim commit is `2a56b96 work: migrate-run ready -> claimed`.

**The implementer's commits.** These are the ten between the claim and `565e14e work: migrate-run claimed -> done`: c8eb7d6, 7323d70, 3b56abe, 4118969, 1a794a5, b4ea412, 20d93ac, 3ca23ed, 588cfc2, bf3a278. They are exactly the commits `3-implement/result.json` lists. They touch only the fileset: `scripts/migrate`, `tests/scenarios/test_migration_tools.py` and `tests/scripts/test_bound.py`.

**The fixes on HEAD after done.** This re-review is of the item as it now stands, so it also takes the run-2 fix commits on the item's files:
- 115e50c: F1, F2, F3, F5, M2.
- ce4584c: the split into modules, and the executable mode.
- 5eaf500: the ledger, binary records, r12.

It leaves these commits out:
- 71b0683: the person's r12 on the capability and work-item;
- 39d46f5: supervision, which is not this item's;
- cb786fa: the test log;
- c9f5569 and 060a0bd: work run's moves and their revert.

## Removed and weakened tests
I searched `git diff 2a56b96 bf3a278` and `git show 115e50c 5eaf500 ce4584c -- tests/` for removed `-` lines with `def`, `assert`, parametrize/Examples rows, `skip` and `xfail`.

- **The implementer's commits: none.** `tests/scripts/test_bound.py` only gains `features/migration-tools.feature` in its list, and loses a comment.
- **The fix commits** change these tests. Each change follows a change to the feature file, which is finding C1:
  - **r8's content Then** (`tests/scenarios/test_migration_tools.py:67-79`).
    - Before: the moved plan and design note were byte for byte what they had been, on a fixture whose files already carried ids.
    - Now: the content is the same "apart from the id r9 and the about r12 give it", on plain files. The test asserts something other than it did, because the scenario's Then was reworded.
    - The plan does not list it. The plan cannot: these are fix commits, not the planned ones.
  - **"nothing under the repository has changed"** now compares `git status` with the status remembered at the Given, where it used to compare with `""`. For every committed-only Given, the remembered status is `""`, so this is the same check. It is not weakened.
  - **"migrate says it could not move work/i1/w1.md onto …"** became a parsed `could not {change}` that keeps the same `in said(context)` assertion. It is not weakened.
  - **The r6 fixture** dropped the `about:` lines from its records. The test now checks a harder case. It is not weakened.
  - **ce4584c moved steps between modules** and removed the unused `ran` fixture. I spot-checked the step texts: the same texts are there, under `migration_*_steps.py`.

## Allowances
The report's `## Tests changed under an allowance` says "none". That holds: every migration test was new in the item's own commits.

## Cannot verify
- The suite records "547 at 2a56b96" and "557 at bf3a278", and 5eaf500's "568 -> 574 tests". I did not run the whole suite.
- The red runs the report claims for each requirement. Its commits show only the green states.
- Whether the scenarios added in 115e50c and 5eaf500 were formulated blind (design-decision 0004, spec-writers-blind-to-code) or shown to the person. The commits say "Five scenarios (ten tests) added", and the code beside them came from the same session.

## Findings

### C1. Critical, fix now (for the person): `features/migration-tools.feature` changed outside formulation
`features/migration-tools.feature`, as changed by 115e50c and 5eaf500. The new lines are at 16-21, 33-105, 155-162 and 194-201. The reworded r8 Thens are at 169-170.
- **What happened:** the run-2 fix commits added these scenarios and outlines:
  - r1: binary record;
  - r2: no blank line before the fields, quoting outline, every paragraph kept;
  - r2 and r5: supersedes and revisit_when;
  - r2 and r11: the ledger's title;
  - two r7 ledger outlines and the r7 untracked destination;
  - r12.

  They also reworded r8's Thens. The commits are by the session that wrote the matching code (Claude-Session in each commit).
- **Why it matters:** design-decision/feature-files-read-only-in-red-green says "only formulation writes features", and design-decision/spec-writers-blind-to-code keeps the formulator away from the code. The work-item still says the feature was "formulated by the blind formulator". Only r12 carries a recorded ruling, from the person in 71b0683.
- **Fix:** the person confirms these scenarios as formulation, for example with a line in the work-item's `## Rulings` or in the proposal. Otherwise they go back through the formulator. Each one reads as a correct pin of r1, r2, r7, r8, r11 or r12. I found none that contradicts its line.

### F1. Important, fix now: a plan or design note that is not Markdown is read as text and given frontmatter
`scripts/migrate_layout.py:114-122` (`record_kind`) and `:128-133` (`plan_ids`).
- **What happens:** `record_kind` gives a kind to every file under `.shop/records/archive/plans/` or `design-notes/`, whatever its extension. `plan_ids` then reads the file and prepends `id`, `kind` and `about`.
  - **Probe p1:** with `docs/superpowers/specs/diagram.png` beside `s1.md`, migrate exits 1 with a `UnicodeDecodeError` traceback from `migrate_layout.py:82` and names no change. No file changes.
  - **Probe p1b:** with `docs/superpowers/plans/p1.json` (`{"a": 1}`), migrate exits 0. The moved file is `'---\nid: initiative-archive/…/p1\nkind: initiative-archive\nabout: bounded-context/…\n---\n{"a": 1}\n'`, which is no longer JSON.
- **Why it matters:**
  - The image case is a crash where r8 says the directory moves with git. It is the earlier F7 again: 5eaf500 fixed it only for `records/img/`.
  - The JSON case loses the file's form.
  - design-decision/references-are-ids asks for id, kind and about only on "every Markdown file under `.shop/records/`".
- **Fix:** have `record_kind` return a kind only for a `.md` file (`final.endswith(".md")`). Then any other file moves as it is.

### F2. Important, observation: a moved decision file with an old-form id keeps it, and `model check` fails
`scripts/migrate_layout.py:99-107` and `:134-136`.
- **What happens:** `with_id` leaves any existing `id:` alone. In probe p7, `decisions/0001-d0.md` with `id: decision/0001-d0` keeps that id. `model check` then reports, with rc 1: `id 'decision/0001-d0' is not design-decision/example.org/acme/shop/<name>`.
- **Why it matters:** this is against r6 on an old repository whose decision files carry the ledger's id form. The report lists the case as unhandled. Whether old `decisions/` files carry such ids today is not shown, so it is hardening.
- **Fix:** rewrite an id of the form `decision/[<nnnn>-]<slug>` to `design-decision/<path>/<slug>`, adding it to `plan.renamed` so its references follow. Or refuse it under r7.

### F3. Important, observation: r6 is green on a fixture whose `work/` already has a final-form `initiative.md`
`tests/scenarios/migration_spec_steps.py:129-131`.
- **What happens:** the r6 fixture writes `work/i1/initiative.md` in final form. Plan D10 says model check needs one in every work directory, and migrate writes none. On an old repository whose `work/` has no initiative, r6 does not hold.
- **Why it matters:** this has the same shape as the earlier F4. The plan grounds it in "migrate plan" being Not yet (design-decision/living-plan-to-work-items), so it is not graded a wrong answer here.
- **Fix, for the person:** narrow r6 to repositories whose `work/` directories are in final form, or keep it until `migrate plan`.

### F4. Minor, observation: a link from a moved file to a file that stays is left broken
`scripts/migrate_spec.py:178-186`. This is the earlier F6, unchanged.
- **What happens:** in probe p4, `.shop/work/i1/w1.md` still says `[index](../../spec/index.md)`. From its new place, that link resolves to `.shop/spec/index.md`.
- **Fix:** resolve every relative link in a moved file against its old directory, and write it relative to its new one.

### F5. Minor, observation: two decision files that share a slug get one id
- **What happens:** in probe p3, `decisions/0001-x.md` and a ledger entry `0002-x` both become `design-decision/example.org/acme/shop/x`. migrate exits 0, and `model check` does not report the duplicate.
- **Fix:** refuse a second file for one id under r7 ("refuses rather than guesses").

### F6. Minor, observation: a `supersedes:` list of old ids is not rewritten
`scripts/migrate_ledger.py:70-71`.
- **What happens:** in probe p2, the entry has `supersedes: [decision/0003-b]`. The list is kept as it is, and `model check` reports `decision/0003-b is not a design-decision in this repository`.
- **Why it is only Minor:** the documented old form is a scalar, `supersedes: decision/<slug>`, and that form is handled.
- **Fix:** map each item of the list.

### F7. Minor, observation: a paragraph that begins with a field word is taken as a field and lost
`scripts/migrate_ledger.py:38-47`.
- **What happens:** in probe p8, the paragraph `source: of truth is the ledger, said bob.` is read as a `source:` field. The later `source: alice` overwrites it, and the paragraph is in no Decision.
- **Fix:** read fields only in the run of `key:` lines at the end of an entry.

### F8. Minor, observation: `spec/decisions/index.md` is not written
- **What happens:** in probe p6, `model check` is clean, but `model decisions --check` says: `spec/decisions/index.md is not what model decisions writes: run it`.
- **Why it matters:** the capability's Implementation note says migrate writes it. No Behaviour line asks for it, and the report names the gap.
- **Fix:** render it with model's renderer, which migrate already loads.

### F9. Minor, observation: `--context` is not checked
- **What happens:** in probe p5, `--context shop` writes `id: bounded-context/shop`.
- **Fix:** refuse a value that is not three `/`-separated names.

### F10. Minor, observation: the fix commits widen the claimed file set without updating it
- **What happens:** 115e50c, ce4584c and 5eaf500 add or change files outside the work-item's `fileset`:
  - `scripts/migrate_layout.py`, `scripts/migrate_ledger.py` and `scripts/migrate_spec.py`;
  - `tests/scenarios/conftest.py`;
  - `tests/scenarios/migration_old.py`, `migration_ledger_steps.py` and `migration_spec_steps.py`.

  The fileset still lists three files.
- **Why it matters:** design-decision/the-file-set-is-the-claim. Another work-item could claim these files.
- **Fix:** add them to `fileset:`.

### M1. Minor, drop: lint in the new modules
- `B023` at `scripts/migrate_layout.py:82`: the lambda is called within its own iteration, so it is harmless.
- `PLW1510` at `scripts/migrate_spec.py:71`: deliberate, since the return code is read.
- `I001` and `RUF100` in the step modules, and `UP031` throughout.

## Checks run
- **Finding the commits:**
  - `git log --grep "^work: migrate-run ready -> claimed$"` gives 2a56b96.
  - `git log --grep "^work: migrate-run claimed -> done$"` gives 565e14e.
  - `git log --stat 2a56b96..HEAD` lists every commit and its files.
- **The diffs read:**
  - `git diff 2a56b96 HEAD -- features/migration-tools.feature` gives the C1 changes. `git diff 2a56b96 bf3a278 -- features/` is empty.
  - `git show 115e50c 5eaf500 -- tests/` gives the test changes listed above.
- **`tools check --base 2a56b96`:**
  - **ruff:** 139 findings across the files changed since the base. 50 are in the migration files, and those are mostly UP031. The others are under M1. The supervision and stub_claude findings belong to 39d46f5, not this item.
  - **vulture:** clean.
  - **import-linter:** the project states no import contracts.
- **Probes:** `.shop/scratch/migrate-run-4-review/test_probe.py`, run with `python3 -m pytest -q -s`. All nine ran, and their outputs are quoted in the findings:
  - p1: binary design note; p1b: JSON plan;
  - p2: supersedes list; p3: one slug twice;
  - p4: link from a moved file; p5: bad context;
  - p6: decisions index; p7: old-form id; p8: field word in prose.
- **Re-checks of the earlier findings, by reading the code:**
  - F1, F2 and F3 are fixed: `migrate_ledger.py:15-35` and `migrate_layout.py:150-166`.
  - F5 is fixed: `quoted()`, checked by model's own reader.
  - F7 is fixed for `records/` only (F1 above).
  - M1 is fixed: `scripts/migrate` is executable.
  - M4 is fixed: every file is under 300 lines.
