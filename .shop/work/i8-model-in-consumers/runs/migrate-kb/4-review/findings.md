# Review of migrate-kb (migration-tools#r1-r17)

**Verdict: DONE.** No finding is Critical, and none needs fixing now. One Minor finding (the label on an allowance); it is dropped.

## Commits reviewed

The branch `work/migrate-kb` no longer exists, so the range is taken from the checkout:
- `work: migrate-kb ready -> claimed` is f483cfe.
- `work: migrate-kb claimed -> done` is de179a2.

The only commit between them that is not one of work run's `work:` commits is **8d06d6d**, "migrate: an unnumbered ledger entry is also named without its number in references (r5, r13)". The implementer's result lists exactly this commit (`commits: ["8d06d6d ..."]`), so there is no difference.

The earlier commits 78af164, 8019602 and 63109eb come from the first claim (5dca7d8), whose done state was reverted. They lie before f483cfe, so they are outside this range and were not reviewed here. The feature change 8e03410 (the formulator's new r5 row) is also before the claim.

Diff: 3 files, +25/-8.
- `scripts/migrate_ledger.py:102-106`: `plan_ledger` also maps `decision/<slug>` to `design-decision/<ctx>/<slug>` for an entry whose heading had no number.
- `tests/scenarios/migration_ledger_steps.py:153-164`: a new Then "0007-a.md's supersedes is ..." and a new Given "the entry 0007-a has supersedes: decision/X".
- `tests/scenarios/migration_spec_steps.py:78-99`: the rests_on Given and Then now take the reference as a parameter.

No change under `features/`.

## Removed and weakened tests

None.

Searched the diff for removed `def`s, `assert`s, parametrize cases, `skip` and `xfail`. None were removed or added.

The rests_on Then changed from `assert data["rests_on"] == ["design-decision/%s/a" % CONTEXT]` to `== [ref]`, with `ref` parsed from the step text. Before: the old scenario (feature :165) checked that rests_on is the full id of entry 0007-a. After: the feature's step text supplies the same literal, `design-decision/example.org/acme/shop/a`, where `CONTEXT = "example.org/acme/shop"` (migration_old.py:6). So the old scenario proves exactly what it did before. The Given likewise supplies the same `decision/0007-a` from the feature at :161.

The new parsers could also match other steps, so I checked for that. The new Given and Then regexes end in `\S+$`. The feature's longer steps (:66, :68, :78) contain spaces after the id, so the new steps cannot capture them. The focused run below confirms this.

## Allowances

The report has one row: "migration_spec_steps.py rests_on Given and Then: setup and wording made parametric (interim)."
- **As `setup`** it does not strictly hold, because the Then's `assert` line changed.
- **As `interim`**: the step was first committed in 20d93ac, which comes after the initiative's base 31e9ed3 (checked with `git merge-base --is-ancestor`). What it asserts for the existing scenario is unchanged, as shown above.

The change is not a weakening, so it needs no allowance. The label is imprecise; see M1.

## Cannot verify

- The report's suite numbers (591/1 failing at f483cfe; 592/0 at 8d06d6d, 1 skipped). Not rerun, as the brief says; work run ran the suite.
- The work-item's title, "migrate run on kb as it is": the kb trial is in another repository, which I am not to read.
- The work-item's goals that were implemented in commits before f483cfe (r2 superseded status, r6 `formulated_as` removed and the index written, r7/r15 dirty tree, r8, r9, r14, r17). They are outside this range. Only their scenarios passing at 8d06d6d is evidence, and that is the report's claim.

## Findings

### M1 — Minor — drop
- **Where:** `report.md` "Tests changed under an allowance", for `tests/scenarios/migration_spec_steps.py:96-99`.
- **What is wrong:** the row is called "setup … (interim)", but the Then's assert line changed, so the `setup` label does not strictly hold.
- **Why it hardly matters:** what the test proves is unchanged, because the feature supplies the same expected id.
- **Fix:** none needed; a later report could say "parametrized, same expected value".
- **Work-item:** migrate-kb.

### Risk checked: the new rename alias could rewrite unrelated text (no finding)
The rewrite pattern is `(?<![\w./-])(ids)(?![\w-])` (migrate_spec.py:110-112). So `decision/b` cannot match inside `decision/bar` or `decision/0003-b`.

`supersedes_of` resolves through `plan.renamed` (migrate_ledger.py:76). So a `supersedes: decision/b` now resolves to the new id, and its target gets status superseded (:110-112). That is consistent with r2.

The alias is added only when the stripped heading is exactly `## decision/<slug>`, which is what ENTRY accepts for an unnumbered entry.

### Not this commit
Behaviour when an unnumbered `## decision/a` sits beside a numbered `## decision/0007-a` (both would get the id `design-decision/<ctx>/a`) comes from the earlier ledger code, not from 8d06d6d. The plan's §5 and the report leave it open. This review does not triage it.

## Checks run

- `git log --grep "^work: migrate-kb ready -> claimed$"` and `git log --oneline -15`: range f483cfe..de179a2, one commit, 8d06d6d.
- `git show 8d06d6d`: the diff above.
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base f483cfe`:
  - **ruff:** 31 findings. 30 are UP031 (% formatting, the style of the whole module, including lines this commit did not touch) and 1 is I001 on migration_ledger_steps.py:3, an import block this commit did not touch. Nothing new in kind.
  - **vulture:** clean.
  - **import-linter:** no contracts stated.
- `wc -l`: migrate_ledger.py 113, migration_ledger_steps.py 190, migration_spec_steps.py 209. All under 300.
- `python3 -m pytest -q tests/scenarios/test_migration_tools.py -k "rests_on or supersedes or numbered or frontmatter_id"`: 7 passed.
- `git status --short` afterwards: clean.
