# Review of w188: fix the findings of branch review 1 of i30

**Verdict: DONE.** There are no findings. The one commit changes `agents/code-scout.md:24` from 40 turns (`--max-turns 40`) to 80 turns (`--max-turns 80`). This is branch review 1's finding 1 (the one triaged fix now), which plan §2 and decision 1 ask for. It now matches supervision#r19 and `scripts/supervise_worker.py:54` (`MAX_TURNS = {"research": 80}`). No code, test or `features/` file was touched.

## Commits reviewed

The branch `work/w188` is gone, so the range is taken on the checked-out history. It runs from `44667d3a work: w188 ready -> claimed` to `71732a3c work: w188 claimed -> done`.

- `2e913069 code-scout: tell the researcher its limit is 80 turns (branch review 1, finding 1)`: `agents/code-scout.md`, 1 line changed. This file is in the work-item's `fileset:`.
- `71732a3c` is `work run`'s own `work:` commit (log, stage files, status) and is left out.

The implementer's `result.json` lists exactly `2e913069`, so the result and the history agree.

## Removed and weakened tests

None. The only commit touches `agents/code-scout.md` alone, so no test file, step file or `features/` file changed. I searched for deleted tests, parametrize or assert changes, and added skip or xfail; there is nothing to find in a one-file diff of agent text.

## Allowances

The report gives "none", and that holds: no test was changed.

## Cannot verify

- The report's final run (`--work-item w188`: 146 passed, 1 skipped; `test_agents.py`: 8 passed). I did not run it again: `work run` runs the suite before it merges, and the change is to text that no test reads (plan §4).

## Findings

None.

These were checked and found sound:
- **Risk: the stated limit disagrees with the code or the line.** `scripts/supervise_worker.py:54` gives 80, `:222` passes it as `--max-turns`, and `spec/capabilities/supervision.md:100` (r19) says 80 turns. All three agree with the new text.
- **Risk: other places still state 40.** `git grep -n -E "40 turns|max-turns 40" -- ':!.shop'` finds only `README.md:174`, the 0.24.0 release note. That is history, and branch review 1 judged it fine.
- **Code no line asks for:** none. The change is text only, and it serves r19.
- Findings 2 to 4 of the branch review are triaged observation or drop. The plan rightly leaves them out (decision 2). The open cases D1 and D3 are named in the report as unchosen, as the plan asked.

## Checks

- `tools check --base 44667d3a`: ruff "nothing to check", vulture "nothing to check", import-linter "the project states no import contracts".
- `tools size --limit 300`: printed nothing. No file is over the limit, touched or not.

## Commands run

- `git log --format=%H -1 --grep="^work: w188 ready -> claimed$" work/w188` failed: the branch is gone.
- `git log --format='%H %s' -1 --grep="^work: w188 ready -> claimed$"` and the same for `claimed -> done`
- `git log --format='%h %s' 44667d3a..71732a3c`
- `git show --stat 2e913069`, `git show 2e913069`, `git show --stat 71732a3c`
- `grep -n "MAX_TURNS\|max-turns" scripts/supervise_worker.py`; `grep -n "r19" spec/capabilities/supervision.md`; `git grep -n -E "40 turns|max-turns 40" -- ':!.shop'`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 44667d3a83f6a6e53fe7777c9951d2dc53960932`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`
- `git status --short`: clean.
