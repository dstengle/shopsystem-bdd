# Review of w223: the delegation leaves glossary questions for the person

**Verdict: DONE.** Nothing is Critical and nothing is fix now. The commit does what supervision r162 and r163 say, read word for word. Its tests were only added; none was removed or weakened. One Important observation: in this repository the literal reading leaves almost every question for the person (finding 1). The fix belongs in the wording of r162/r163, not in this code.

## Commits reviewed

- `7581837253f417aea16542d0a7a9952d3c367008` "A delegation leaves questions naming a glossary term or glossary-proposal for the person (r162, r163)". This is the commit `work run` merged, as the brief gives it.
- The implementer's result lists `143ecc98`. Its parent is `884532f5`, and it is the same change: 5 files, 74 insertions, 4 deletions, the same files. So `work run` rebased that commit when it merged it. The two hashes differ only because of the rebase; no change was added or lost.
- Files: CLAUDE.md, scripts/supervise_answers.py, scripts/supervise_glossary.py, tests/scenarios/supervision_delegation_steps.py, tests/scripts/test_supervise_answers.py. All of them are in the work-item's `fileset`. Nothing under `features/` changed.

## Removed and weakened tests

None. I read the whole diff and looked for removed `def test_` functions, removed `assert` lines, changed parametrize lists, and added skips or xfails. Every change to a test file is an addition: one unit test and three step definitions. The plan's "Tests the decisions break" says none, and that matches.

## Allowances

The report's `## Tests changed under an allowance` is "none". The commit matches that, since no existing test changed.

## Cannot verify

- The report says it was red before the change: 4 scenarios failed on undefined steps, then r162 failed on the "given to no session" Then. The commit history has only the final commit, so this cannot be checked from it. The suite record shows w223's scenarios green at 75818372. The expected-failure list holds no r162 or r163 scenario.
- The plan's open case: how `work run` treats the r162 scenario's awaiting-answer glossary-proposal `g1` in a gate or apply round (that is w225's work). The suite passes, but I did not trace what round, if any, starts for `g1` in that scenario.

## Findings

### 1. Important, observation: the glossary's ordinary words make the delegation leave nearly every question for the person

- **Where:** scripts/supervise_glossary.py:49-52 (`names_one`), called at scripts/supervise_answers.py:75. Work-item w223.
- **What:** `names_one` flags a question when it contains any term of `spec/index.md`'s Glossary as a whole word, in any case. This repository's Glossary has 51 terms. Many are everyday words: answer, check, run, status, result, report, input, record, round, session, request, scenario, review, work-item, stage, turn, outcome.
- **Reproduction:** a probe test in `.shop/scratch/w223-4-review/test_probe.py`, run with `python3 -m pytest -q -s -n0 -p no:cacheprovider .shop/scratch/w223-4-review/test_probe.py`, against this worktree's real `spec/index.md`. 9 of the 11 sample questions were flagged:
  - "Should the run stop here?", "Is the status kept?", "Does the answer go to the file?", "Should the check be strict?", "Should the report list it?", "Is the input empty allowed?", "Which work-item owns this file?" and "Should the result be JSON?" all came back True.
  - Only "Which module owns the log?" and "Which queue?" came back False.
- **Why it matters:** r162 and r163 read word for word ("names a term of the glossary") do give this result, so it contradicts no line. But in practice it switches off the delegation of r77 and r163 in any repository with a real glossary. Every such question goes to the person, which defeats the purpose of a delegation. It is a choice of reading (plan decision 3), not a wrong answer; the result is only conservative.
- **Fix:** clarify the line first, through integrating-a-proposal. For example, r162 could say "asks about the meaning or wording of a term of the glossary" (retire it under a new id). Then narrow `names_one` to match, for example a question that quotes or bolds the term, or that names the glossary-proposal. Until the line is reworded, the code is right to follow it.

### 2. Minor, drop: a question after a flagged one still gets a session whose answer is thrown away

- **Where:** scripts/supervise_answers.py:74-78.
- **What:** when an earlier question was flagged, a later unflagged question is still given to `ask`. Its answer is then not written, under the existing rule that no answer is written after a gap. That spends a session for nothing.
- **Why it matters:** the plan's decision 4 chose this, to keep r163's "each question … to a session of its own". The report names it as an open case. No scenario covers the mix.
- **Fix:** none needed now. If the line ever allows it, skip `ask` once `left` is set.

### 3. Minor, drop: the files are read again for every question

- **Where:** scripts/supervise_glossary.py:49-52.
- **What:** `names_one` reads `spec/index.md` and globs every `.shop/work/*/*.md` for each open question.
- **Why it matters:** only cost; nothing comes out wrong.
- **Fix:** read the terms and ids once in `Answers.answers` and pass them in.

## Checks

- **ruff:** 26 errors, none in lines this commit added.
  - The errors are in `.shop/work/i46/runs/*/splice.py`, supervise_change.py, design_model_check_*.py, supervision_integrate_steps.py, supervision_proposal_steps.py and test_design_model_check.py.
  - The two in a file this commit touched, `tests/scripts/test_supervise_answers.py:9-10` (RUF100), are on `noqa` lines that were already there at the base, unchanged.
- **vulture:** clean.
- **import-linter:** the project states no import contracts.
- **size (`--limit 300`):** printed nothing. The touched files have 61, 148, 223 and 71 lines.

## Risks verified

- **Does a reviewer's question bypass the check?** No. `asking()` gives work-items and capability-proposals alike, and every open question goes through `names_one`, as plan decision 6 says.
- **Do regex characters in a term break the match?** No. Each name goes through `re.escape`, and the boundaries `(?<![\w-])…(?![\w-])` keep `g10` from matching `g1` and `pledger` from matching `ledger`. The unit test asserts both.
- **What if there is no `spec/index.md` or no `## Glossary`?** `terms_of` returns [], so the r77 and r78 fixtures are unaffected. This matches the suite record.

## Commands run

- `cat .shop/scratch/4-review/brief.md`, then the work-item, plan, report and result
- `git show --stat 7581837…`, `git show 7581837…`, `git show --stat --format=%H%n%P 143ecc98`, `git log --oneline -1 143ecc98`, `git diff 143ecc98 7581837… --stat`
- `git show 134745663…:tests/scripts/test_supervise_answers.py`
- `grep -n "r162\|r163" spec/capabilities/supervision.md`, `grep -n "^- \*\*" spec/index.md`, `sed -n 55,95p scripts/supervise_answers.py`
- `python3 -m pytest -q -s -n0 -p no:cacheprovider .shop/scratch/w223-4-review/test_probe.py`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 134745663…`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`
- `wc -l` of the touched files
