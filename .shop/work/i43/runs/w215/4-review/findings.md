# Review of w215 (review r32, r33, r34)

**Verdict: DONE.** No Critical finding, none triaged fix now. Three Minor findings, all observations.

## Commits reviewed

- `1b92df68` review r32-r34: the branch reviewer runs nothing; its own stage list without Bash
  (agents/bdd-branch-reviewer.md, scripts/supervise_review.py, scripts/supervise_worker.py; +15 −12).

The implementer's result lists `8af4a7ec`, which has the same subject and an identical diff. `work run` merged it
(rebased) as `1b92df68`. No difference in content. The suite comes from the brief's record: 1020 passed, 0 failed at
1b92df68 in 29 s, with the expected failures it lists, none of them review's.

## Removed and weakened tests

None. The commit touches no file under `tests/` and none under `features/` (`git show --stat`). The plan lists none
under "Tests the decisions break".

## Allowances

The report's `## Tests changed under an allowance` says "none". That matches the commit, which changes no tests.

## Cannot verify

- That a branch review started under `branch-review` actually reads its runs, commits and change from the brief.
  The brief that `supervise_review.py:64-71` writes today gives no runs, commits or change. Supervision r154-r156 add
  them in w216, which is `claimed` and not yet merged. The agent body follows w216's fields as the plan describes them
  (plan decision 4). I cannot check those field names against code that does not exist yet.
- That `claude -p` with `--allowedTools Read,Glob,Grep` under `acceptEdits` refuses every Bash call. This is how
  `answer` and `plan` already work. I did not run a session.

## Findings

1. **Minor · observation · w215 · scripts/supervise_review.py:66.** The branch review's brief still says "You start
   in your worktree: run every command from there and never change directory".
   - **Why it matters:** this contradicts review r32 and the agent body's "you run nothing" (agents/bdd-branch-reviewer.md:29).
     The stage list has no Bash, so nothing is actually run. The text is only inconsistent.
   - **Fix:** drop that sentence when w216 rewrites the brief (w216 owns its contents).
   - **Reproduction:** a search for "run every command" in scripts/supervise_review.py returns line 66.

2. **Minor · observation · w215 · agents/bdd-branch-reviewer.md:59.** The Triage section still defines an
   observation's reproduction as "the commands and what came back".
   - **Why it matters:** it reads as if the reviewer ran those commands. Line 39 says the reproduction is drawn from
     the given runs' output or from what was read (r32, r33).
   - **Fix:** reword line 59 to point at line 39.
   - **Reproduction:** a search for "the commands and what came back" in agents/bdd-branch-reviewer.md returns line 59.

3. **Minor · observation · w215 · ordering with w216.** The plan's result gives `depends_on: [w216]`. The work-item
   file `.shop/work/i43/w215.md` carries no `depends_on`, and w215 merged while w216 is still `claimed`.
   - **Why it matters:** if a branch review ran between the two merges, the reviewer would have no Bash and no runs or
     commits in its brief. Every check would land under `Cannot verify` and the review would end
     `DONE_WITH_CONCERNS`. That is a safe failure, not a wrong answer, and the branch review runs only after every
     work-item of i43 is merged.
   - **Fix:** none needed if w216 merges before the branch review. Otherwise record the dependency on the work-item.
   - **Reproduction:** `.shop/work/i43/w215.md` has no `depends_on`; the plan's `result.json` has it.

Risks I checked outside the diff:

- **Does the reviewer lose the write of `findings.md` and the result now that its list has no Write?**
  `Workers.tools` strips any bare Write anyway, and writes go through `--permission-mode acceptEdits`, inside the
  worktree (supervise_worker.py:21-25, 222-230). The run directory is `<tree>/.shop/scratch/branch-review`, inside
  the worktree. Holds.
- **Does the stage key change anything besides the tool list?** `session()` uses `stage` for the tool list,
  `MAX_TURNS` (no entry for either key) and `rounds` (neither key). `branch-review` was already the log's stage
  (`STAGE`, supervise_review.py:10). Nothing else changes.
- **Is a consumer's `.shop/delivery.toml` `[allowed_tools].review` used for the branch review?** It no longer is. That
  follows r32. This repository has no `.shop/delivery.toml`.
- **Is there code no line asks for?** The new `branch-review` list serves review r32 and supervision r14. No new
  output, file, status or refusal is added.
- **Behaviour against the lines:** the body states r32 (line 29), r33 (line 39), r34 (line 38), r6 (line 37) and r7
  (lines 35 and 66). The agent's `tools:` line keeps Bash, by the 2026-10-28 ruling (q24 in i44, plan decision 1). The
  stage list holds r32 in the meantime.

## Checks

- `tools check --base c0e0ec4d`:
  - ruff: All checks passed!
  - vulture: clean
  - import-linter: the project states no import contracts
- `tools size --limit 300`: no output, so no file is over the limit. supervise_worker.py grows by 3 lines, from 256.

## Commands run

- `git show 1b92df68`, `git log --oneline -1 8af4a7ec`, `git diff 8af4a7ec 1b92df68 --stat -- agents scripts`
- `git log --format='%H %s' -1 --grep="^work: w215 ready -> claimed$"` → c0e0ec4d
- `sed -n` / `cat -n` of scripts/supervise_worker.py, scripts/supervise_review.py, agents/bdd-branch-reviewer.md
- `grep -n "STAGE\|stage" scripts/supervise_review.py`; `grep -rn '"review"' scripts/supervise*.py`
- Grep for "run every command" and "the commands and what came back"
- `ls .shop/delivery.toml` (absent)
- `python3 <Scripts>/tools check --base c0e0ec4d…`; `python3 <Scripts>/tools size --limit 300`
