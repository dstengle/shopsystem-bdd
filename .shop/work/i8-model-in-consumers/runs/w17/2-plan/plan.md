# Plan: migration-rebind-4 (migration-tools r14-r17)

## 1. What goes green

- **migration-tools#r14**, "`migrate run` relocates adrs/ to .shop/records/decision-arguments/, with git" (features line 249). Already passing (research notes §1). Nothing to do but keep it green.
- **migration-tools#r15**, Outline "`migrate run` on a repository with <change> refuses, naming it, and changes no file" (line 308; examples: a tracked README.md changed, an untracked notes/n2.md, a tracked README.md deleted). All three examples already pass (notes §1).
- **migration-tools#r16**, "`migrate run` adds every file it wrote or relocated to git and writes spec/decisions/index.md" (line 323). Red because its last Then, "spec/decisions/index.md is what `model decisions` would write" (line 329), has no step definition (StepDefinitionNotFoundError). The staged-status Then at line 328 already passes. Probes show the code already writes and stages the index (notes §2).
- **migration-tools#r17**, Outline "`migrate run` writes a qualified supersedes as the decisions' ids alone, the qualifier going to by, <case>" (line 82; examples "one decision" and "two decisions, the first qualified"). Both examples are red because "And its by has the qualifier "(for artifacts)"" (line 88) has no step definition. The supersedes Then at line 87 already passes. The code already writes the r17 form (notes §2: migrate_ledger.py decision_text and supersedes_of).

Deprecated scenarios retired: none. The work-item has no Retires section.

## 2. Where the change lands

The changes:
- `tests/scenarios/migration_ledger_steps.py`: add one Then step for "its by has the qualifier "<q>"" (r17), next to the existing by steps.
- `tests/scenarios/test_migration_tools.py`: add one Then step for "spec/decisions/index.md is what `model decisions` would write" (r16), next to the `model decisions --check` step.

On the path and expected to stay unchanged (the researcher's set; probes show they already do r14-r17):
- `scripts/migrate`, `scripts/migrate_layout.py`, `scripts/migrate_ledger.py`, `scripts/migrate_spec.py`, `scripts/migrate_write.py`: no production change.
- `scripts/model`, `scripts/model_report.py`, `scripts/model_facts.py`: read by the r16 step's check; unchanged.
- `tests/scenarios/migration_old.py`, `tests/scenarios/migration_spec_steps.py`, `tests/scenarios/migration_safety_steps.py`: unchanged.

No file is added or removed. Both edited files are at about 225 lines, well under the 300-line limit.

## 3. Decisions

- **D-a. What "its by has the qualifier "<q>"" asserts.** The step reads `by` from spec/decisions/0007-a.md's frontmatter and asserts that it contains the given qualifier text. It does not check the exact layout of `by`. Rests on migration-tools#r17 ("the qualifier in `by`"). The `; supersedes <id> <qualifier>` form appears only under "Implementation, may change", so the step must not pin it.
- **D-b. What "spec/decisions/index.md is what `model decisions` would write" asserts.** The step runs `model --root <repo> decisions --check` on the migrated repository and asserts that it exits 0 and reports the index as current. This is the same check as the existing step at test_migration_tools.py:176, so the implementer may share that step's body by stacking the new step text on it. It does not compare against a copy that the test renders itself. Rests on migration-tools#r16 and on the capability's Implementation note: "`spec/decisions/index.md` as `model decisions` writes it". `model decisions --check` is the system's own judgement of that.
- **D-c. No production change.** The research probes show that r14-r17 already hold (notes §2). The implementer confirms each scenario goes red only on the missing step and then green with the new step. If either one stays red for a reason other than the missing step, that is a finding to report, not a reason to edit `scripts/` beyond the file set. Rests on migration-tools#r14-r17 as probed.

## 4. Tests the decisions break

None. Verified from the notes (§4) and by reading migration_ledger_steps.py:205-227 and test_migration_tools.py:155-180:
- The existing by steps (migration_ledger_steps.py:223-227, exact `by is "..."`) only run on entries with no qualified supersedes (features lines 31, 39, 73). D-a adds a step and does not change them.
- The `model decisions --check` step at test_migration_tools.py:176 is unchanged. D-b only adds a step text (or a stacked decorator) beside it.
- tests/scripts/test_migrate_write.py, test_migrate_layout.py and test_model.py:178-182 assert nothing that D-a to D-c change (notes §4).

## 5. Open cases

The accepted scenarios don't cover these. The implementer names them and doesn't settle them:
- D1 (notes §6): a supersedes naming a decision that is not in the ledger is written in the old `decision/<nnnn>-<slug>` form, with rc 0, and is not refused. r17 does not say what happens to it. r7 might bear on it.
- D2 (notes §6): an entry with no `source:` and a qualified supersedes gets a `by` that starts with `; supersedes ...`.
- The step "spec/decisions/0007-a.md's supersedes is {ident} alone" (migration_ledger_steps.py:217-220) is used by no feature line (notes §3). Whether to keep or remove it is outside this work-item.
- r14 nearest case (notes §2): an ADR with a short body shows as A plus D rather than R once migrate adds its id. The scenario uses a long body, so it passes.
