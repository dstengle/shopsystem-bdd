# Plan: migration-rebind-2 (migration-tools r6-r9)

From the research notes (`runs/migration-rebind-2/1-research/notes.md`), checked against `features/migration-tools.feature` and the two Given step definitions the notes name.

## 1. What goes green

- **migration-tools#r6**: "after `migrate run` on a repository with <what>, `model check` prints no unresolved reference or file problem" (4 Examples). **Green today** (notes part 1, run). No change; it must stay green.
- **migration-tools#r7**: red today. Each fails at `And it exits with an error` with StepDefinitionNotFoundError. The only step there is `it exits non-zero` (test_migration_tools.py:215). According to the notes' CLI probes (part 2), migrate already prints every message the Thens expect and exits 1.
  - "`migrate run` that finds <found> in spec/decisions.md names it, exits with an error and changes no file, the ledger included" (2 Examples)
  - "`migrate run` whose ledger entry's decision file would land on <there> names it, exits with an error and changes no file" (4 Examples)
  - "`migrate run` that cannot make two of its changes names both, exits with an error and changes no file"
  - "`migrate run` that would relocate a file onto an untracked file names the relocation, exits with an error and changes no file"
  - "`migrate run` that would <what> names it, exits with an error and changes no file" (3 Examples)
  - "`migrate run` outside a git repository says so, exits with an error and changes no file"
- **migration-tools#r8**: "`migrate run` relocates docs/superpowers/plans/, specs/ and requests/ under .shop/records/archive/, with git". **Green today**.
- **migration-tools#r9**:
  - "... gives a capability, a decision file, a plan, a request, a design note, an ADR and a test log the type-first id of its kind": green today.
  - "... gives a capability whose id is the short form capability/<name> its full id": green today.
  - "... gives a README.md it relocates to <new> no id, kind or about" (3 Examples): green today.
  - "`migrate run` gives a decision file whose id is decision/<nnnn>-<name> the type-first id": **red today**, FileNotFoundError on `spec/decisions/0001-x.md`. Its Given (migration_safety_steps.py:56-59) writes `decisions/0001-x.md` and never commits it. Migrate therefore refuses on its r15 check (uncommitted change) and moves nothing. Probe 10 shows that on a committed file migrate writes the expected id.
- Retired deprecated scenarios: none. The work-item has no Retires section.

## 2. Where the change lands

- `tests/scenarios/test_migration_tools.py`: the step `it exits non-zero` becomes `it exits with an error` and keeps the same non-zero return-code assertion (decision 1).
- `tests/scenarios/migration_safety_steps.py`: the Given "a repository on the old system with decisions/0001-x.md whose id is decision/0001-x" commits what it wrote (decision 2).

Production code (`scripts/migrate`, `scripts/migrate_*.py`) does not change. The notes' probes show that every r7 message and r9 id already comes back.

I removed one change from the researcher's proposal: the extra commit in the Given at test_migration_tools.py:182-185. That scenario's next Given (196-200) calls `old.commit()`. In migration_old.py that runs `git add -A` and then commits, so `.shop/work/i1/w1.md` and `work/i1/w1.md` are already committed before the When. The notes' probe 7 left that file untracked on purpose, so it did not match the scenario.

## 3. Decisions

1. **"it exits with an error" means a non-zero exit code.** It is checked the same way `it exits non-zero` checks it today. The step is renamed rather than added next to the old one, because no feature uses the old text any more (search over `features/`), and keeping it would leave a dead step. The naming of each change and the "changes no file" part are the scenario's other Thens, so this step asserts the exit alone. Rests on migration-tools#r7.
2. **The decision-file Given commits.** A repository "on the old system" is a committed tree. Migrate rightly refuses an uncommitted one, so a Given that leaves its subject untracked tests r15 instead of r9. Rests on migration-tools#r9 and migration-tools#r15. The r5 scenario "rewrites a frontmatter id that names a decision file's old id" uses the same Given and then writes a capability. The implementer should check that its second Given still has a change to commit, or commits without failing on an empty commit.
3. **No production change.** Each red scenario's Then already holds against the CLI (notes part 2, probes 1-13). Rests on migration-tools#r7 and #r9.

## 4. Tests the decisions break

- Decision 1: `it exits non-zero` disappears. No feature line uses that text (searched `features/` and `tests/`), so no scenario breaks.
- Decision 2: the r5 scenario sharing the Given (feature line 362) gets an extra commit before its own. It should stay green; see decision 2 for what to check.
- `tests/scripts/test_migrate_write.py` and `test_migrate_layout.py` are untouched and keep passing (notes part 4: 7 passed). `design_model_check_problems.py:58-60` is untouched.

## 5. Open cases

- Defect D1 (notes part 6) is not covered by any accepted scenario. Run inside a subdirectory of another repository that is not itself a repository, `migrate run` works on the enclosing repository and exits 0. The r7 "outside a git repository" scenario runs in pytest's tmp dir with no enclosing repository, so it passes either way. The implementer should name this, not fix it here.
- Notes part 5: when a tracked file is gone, `scripts/migrate` returns before planning moves, so only the r15 line is printed and not every r7 change. No scenario covers this.
- Notes part 5: after a failed write, `git reset --hard` does not remove ignored files migrate wrote. No scenario covers this.
- Probe 5 (an untracked spec/decisions/0007-a.md) prints both the r15 and the r7 line. The scenario's Then is a substring check, so it passes; whether r7 wants the r7 line alone is unsaid.
- The research probe left the checkout's own repository changed: 150 files staged (notes part 0). This planning worktree may need restoring to HEAD before the implementer's run is trusted.
