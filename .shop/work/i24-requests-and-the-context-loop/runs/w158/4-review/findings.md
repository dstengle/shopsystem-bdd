# Review of w158: DONE (no findings)

**Verdict:** the commits do what the plan and supervision#r79 ask, plus the work-item's ruling of 2026-10-25. No finding is Critical, and none is to be fixed now.

## Commits reviewed

The branch `work/w158` is gone. On the checked-out HEAD, between `e5a100c work: w158 ready -> claimed` and `80c25cd work: w158 claimed -> done`, leaving out `work:` commits and commits of other work-items (w157 `6e6d314`, w159 `460e639`, w160 `d04cc02`):

- `38bc1ca A proposed initiative that fulfils no request gets no integrate round (r79)`. It touches scripts/supervise_rounds.py (+1/-1), tests/scenarios/supervision_rounds_steps.py (+36/-1) and tests/scenarios/test_supervision.py (+5).

The implementer's result lists `00095da`. That commit is still in the repository. It has the same author, date, message and per-file stat as `38bc1ca`, so `38bc1ca` is the same patch after `work run` merged it onto HEAD. The two match.

The files are all inside the work-item's `fileset`. Nothing under `features/` changed.

## Removed and weakened tests

None. I read the diff for deleted `def test_`/step functions, removed `assert` lines, parametrize or Examples rows, and added skip or xfail markers. The commit only adds code. Its one changed line in the tests is an import (`git` added to the `supervision_world` import).

## Allowances

The report says "none", and the commits agree: no existing test changed.

## Cannot verify

- The report's green run (`--work-item w158`: 144 passed, 1 skipped) and its suite at start (822 passed). I did not run the whole suite. I ran the two @r79 scenarios: 2 passed.
- The plan's open cases (section 5) are not covered by any scenario, and I did not reproduce them. They are not findings:
  - A proposed initiative with no `fulfils` now reaches the capability-proposal check in `Rounds.due` (supervise_rounds.py:34). Before this change that path could not be reached for a proposed initiative.
  - `fulfils` names a request that is not kept.
  - The request has no accepted lines.
  - `supervise_all.run_all` over such an initiative.
  - A branch review over an initiative with zero work-items.

## Findings

None.

Risk checked: the change narrows r79 ("When an initiative is `proposed` … shall start a round of the kind `integrate`"). The second @r79 scenario and the work-item's ruling bind that narrowing. r84 holds only when an integrate round starts, so `start_initiative` not being reached here contradicts no line. A `fulfils` that is empty, or an empty list, counts as no request, which is the same reading.

The new Thens assert what their step texts say. "i1 is proposed" checks `\nstatus: proposed\n`. "no branch" checks `git branch --list round/*` is empty. "nothing uncommitted" checks `git status --porcelain -- .shop/work` is empty. "the second run was not refused" checks exit 0 and no `work:` in stderr. None of them is looser than its text.

## Commands run

- `git log --oneline -15`, `git show --stat 38bc1ca`, `git show --stat 00095da`, `git show 38bc1ca`
- `git diff --stat e5a100c HEAD -- features/ tests/`: no change under features/
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base e5a100c`:
  - ruff: 5 errors, all in files w158 did not touch (design_model_check_problems.py, supervision_delegation_steps.py, test_design_model_check.py, stub_claude.py). They come from other work-items' commits in the range.
  - vulture: clean
  - import-linter: the project states no import contracts
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`: no output, so no file is over the limit. The touched files have 97, 236 and 257 lines.
- `python3 -m pytest -q tests/scenarios/test_supervision.py -k proposed_initiative`: 2 passed
