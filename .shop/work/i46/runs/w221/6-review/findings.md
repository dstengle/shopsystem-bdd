# Review of w221 (design-model-check r122, r123, r124)

**Verdict: DONE.** No Critical finding, none triaged fix now. Two Minor findings: two unused imports this commit introduced (observation), and the commit ids differing from those the implementer's results list (drop).

## Commits reviewed

- df968241 "design-model-check: glossary-proposal is a part kind; r122 terms, r123 approved closes, r124 shapes" (the brief's `Commits:`). Its parent chain: b7f62e4e `work: w222 ready -> claimed`, 5ae2e173 `work: w221 ready -> claimed`.
- The implementer's results list 6a7131c0 (stages 3 and 4) and 22e14b24 (stage 5). The id differs from df968241, but `git diff X^ X -- scripts tests features | md5sum` is the same for all three (9e0713019bb8dfc2e9481c40c2439a37). They are the same change, rebased by `work run`. See Finding 2.
- Suite taken from the brief's record: 1053 passed, 0 failed at df968241; the expected failures listed are other work-items' (requests, supervision).

## Removed and weakened tests

None outside what the work-item retires. I searched the diff for deleted `def test_`, dropped parametrize cases, removed or loosened `assert`, added skip/xfail, and removed step definitions:

- `features/design-model-check.feature`: 60 lines removed, nothing added. Every removed line belongs to one of the five `@deprecated` scenarios the work-item lists under Retires. I checked each removed line that is not a `deprecated` line.
- `tests/scenarios/design_model_check_problems.py`:
  - The step `malformed_work` moved to the new `design_model_check_work.py`. Every old branch is kept except "a status not in its kind's lifecycle" (`status="loved"`). Only the retired Outline used that row, and the new @r124 Outline has no such row. Its "not in lifecycle" cases are now `capability-proposal built` and `glossary-proposal formulated`.
  - The Givens `a work-item in .shop/work/i1/w1.md that accepts thing#r2` and `... with status {status} that accepts thing#r2` were removed. A grep of `features/` and `tests/` shows that only the retired scenarios used them.
- `tests/scripts/`: untouched. The plan's "Tests the decisions break" says "None", and that holds.

## Allowances

The report's `## Tests changed under an allowance` says "none" in all three stages, so there are no rows to verify.

## Cannot verify

- Stage 4's report says the earlier stage "left no report". Stage 3's directory does hold a report.md, so stage 4's statement is inaccurate. This does not affect the change.
- The plan's open cases are still open, as the report says, and no line names them:
  - a glossary-proposal entry that is not `term/…` is silently ignored;
  - a glossary-proposal with `argues`;
  - whether an approved glossary-proposal's `removes` excuses a capability-proposal's term reference (r66);
  - whether an initiative may have a glossary-proposal as its only part (v_k3 now allows it).

## Risks checked

- **v_k3 narrowed** (`scripts/model.lp:199`). This is not in the plan, and the report gives the reason. It is not code that no line asks for: r124 makes glossary-proposal a part kind, and the glossary (`spec/index.md`) defines it as "the part of an initiative, beside its capability-proposals". Without the change, r123's scenario names its own initiative.
- **`glossary_refs` / `glossary_removed` set only in `read_work`.** I grepped the callers: `read_part` and `read_initiatives` are reached only through `read_work` (`model_facts.py:117`), so no AttributeError path exists.
- **Glossary terms read before they are judged.** `read_index` runs before `read_work` (`model_facts.py:110-121`), so `self.nodes` holds the terms when `judge_glossary_refs` runs.
- **`unread()` and the new lists.** `unread()` reports only folded or literal blocks, not unknown keys, so a glossary-proposal's `adds`/`changes`/`removes` are not flagged.
- **`closed()`.** `approved` closes only `node(P, "glossary-proposal")`, which matches r123 and r36. A capability-proposal is unaffected.
- **Real `.shop/work/`.** It holds no glossary-proposal (grep for `kind: glossary-proposal`), so the repository's own `model check` is not affected today.

## Findings

### 1. Minor (observation): two unused imports introduced by the move of `malformed_work`
- `tests/scenarios/design_model_check_problems.py:6` imports `I1`, which is now unused: its only use moved to `design_model_check_work.py`. At base, line 89 used it.
- `tests/scenarios/design_model_check_work.py:6` imports `THING`, which is unused.
- Why it matters: `tools check` reports ruff F401 on both, which adds to the lint noise.
- Fix: drop `I1` from the first import and `THING` from the second.
- Reproduction: `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 5ae2e173`, under `== ruff ==`, prints `design_model_check_problems.py:6:32: F401 .conftest.I1 imported but unused` and `design_model_check_work.py:6:27: F401 .conftest.THING imported but unused`.
- Already present at base and not w221's: the `CONTEXT` F401 in the same import line, and I001 in `test_design_model_check.py`.

### 2. Minor (drop): implementer's results list commit ids other than the one merged
- `.shop/work/i46/runs/w221/{3,4}-implement/result.json` list 6a7131c0, `5-implement/result.json` lists 22e14b24, and the merged commit is df968241.
- I verified that the three diffs are identical (md5 of the diff restricted to scripts, tests and features). They are rebases, and no work is missing or extra.

## Checks

- `tools check --base 5ae2e173`:
  - ruff: 10 errors. w221's are the two F401 of Finding 1. The rest are pre-existing or from other work-items (supervise_change.py B023, supervision_* RUF059/RUF100, the problems.py `CONTEXT` F401, the test_design_model_check.py I001).
  - vulture: clean.
  - import-linter: the project states no import contracts.
- `tools size --limit 300`: printed nothing. The touched files are 240, 183, 264, 248, 48 and 223 lines, plus the one-line import change in `test_design_model_check.py`.

## Commands run

- `cat` of the brief; reads of the work-item, plan, stage 3–5 reports and results.
- `git show --stat df968241`; `git show df968241 -- scripts tests features`; `git log --oneline -3 df968241`.
- `git diff X^ X -- scripts tests features | md5sum` for 6a7131c0, 22e14b24, df968241.
- `grep` of the capability for r122/r123/r124/r36/v_k lines; `grep` of `spec/index.md` for glossary-proposal.
- `grep -rn` of `features/` and `tests/` for the removed Givens and the dropped case.
- `grep -rn` of `scripts/` for read_work/read_initiatives/read_part/glossary_refs; `sed` of `model_facts.py` read order and `model_work.py` read_part.
- `grep -rl "^kind: glossary-proposal" .shop/work`.
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 5ae2e173`; `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`; `wc -l` of touched files.
- `git show 5ae2e173:<file>` for the base imports of problems.py and test_design_model_check.py.
