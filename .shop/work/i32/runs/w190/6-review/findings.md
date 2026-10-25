# Review of w190 (supervision#r118, supervision#r119)

**Verdict: DONE.** Nothing is Critical and nothing is fix now. Under a delegation, the commits move a reviewer's work-item to `ready` on a `change` verdict and to `done` on an `accept` verdict, as r118, r119 and decision 0069 ask. Two Minor findings follow, one an observation and one a drop.

## Commits reviewed

The branch `work/w190` is gone. The commits are those between `2c448d35 work: w190 ready -> claimed` and `0a9226a6 work: w190 claimed -> done`, less `work run`'s `work:` commits:

- `6622133a` w190: steps for supervision r118 and r119. Only `tests/scenarios/supervision_delegation_steps.py`, +27 lines.
- `31c86e3c` w190: a delegated answer to a reviewer's question moves the work-item by the session's verdict (r118). `scripts/supervise_answers.py` +18/-4, `scripts/workqueue_answer.py` +6/-1.

How these compare with the implementers' results:
- The first implement result (3-implement) lists `c5561011`. That is the same change as `6622133a`, carried forward after the claim was retaken: `git diff c5561011 6622133a` shows no difference in the test file.
- The second implement result (5-implement) gives `"commits": ["see git log"]` rather than the commit. See finding 2.

None of the commits touches `features/` or `spec/`.

## Removed and weakened tests

None. I searched the diff of `2c448d35..31c86e3c` for:
- deleted `def` lines or deleted `@given`/`@when`/`@then` steps;
- removed `assert` lines;
- `skip` or `xfail`;
- changes to parametrize lists.

The only test change is three new steps added to `supervision_delegation_steps.py`. Nothing changed under `features/`.

## Allowances

Both reports give `## Tests changed under an allowance: none`. The commits agree: no existing test was changed.

## Cannot verify

- The report's "Green: 145 passed, 1 skipped" for `--work-item w190`. As the brief says, I did not run the suite; `work run` ran it before the merge.
- That a real `delegation-answerer` session gives the `verdict` field. The scenarios use a stand-in, and the agent file `agents/delegation-answerer.md` does not mention `verdict`, so the brief's instruction is the only place the agent learns of it. The brief's VERDICT sentence does ask for it.

## Findings

### 1. Minor (observation): a reviewer's work-item with no open question left raises KeyError
- **Where:** `scripts/supervise_answers.py:82`.
- **What is wrong:** `self.verdicts[name]` is filled only by `ask()` within this run. Suppose an awaiting-answer work-item asked by its reviewer reaches `answers()` with every question already answered. Two ways that can happen:
  - an earlier run committed the answer (line 79, "kept now") and stopped before `self.move`;
  - the answer was written into the file by hand.

  Then the question loop never runs, `open_questions(name) == []`, and `self.verdicts[name]` raises `KeyError`. That is a traceback, not a refusal. Before these commits, `asked_from` gave `done` here.
- **Reproduction (code read):** `answers()` sets `self.verdicts = {}` at line 68. The loop at line 72 runs once per open question. With no open question, line 81 is taken and line 82 indexes `self.verdicts[name]` with no entry for `name`.
- **Why it matters:** `work run` would stop with a crash. This is an edge no line names and no client normally produces, so it is hardening.
- **Fix:** when no verdict was given in this run, leave the item awaiting-answer for the person (`self.verdicts.get(name)` is None means no move), or raise `Refused`.
- **Work-item:** w190.

### 2. Minor (drop): the second implement result does not list its commit
- **Where:** `.shop/work/i32/runs/w190/5-implement/result.json`.
- **What is wrong:** `"commits": ["see git log"]` instead of `31c86e3c`. I verified the commits from the history, as listed above.
- **Fix:** the implementer names its commits.
- **Work-item:** w190.

### Checked, no finding
- **Behaviour against r118, r119 and 0069:** a reviewer's question is detected by the log (`asked_by_reviewer`, the same reading `work answer` uses). `change` goes to `ready` and `accept` goes to `done`, through the one helper `workqueue_answer.reviewer_status`. `work answer` uses the same helper.
- **The answer's `by`:** still "work run, under the delegation ..." (r78).
- **No verdict leaves the question for the person:** this is not code no line asks for. It serves r77 ("leaves it for the person otherwise"), and 0069 allows no move without a verdict.
- **The verdict instruction:** added only to a reviewer's question's brief, through the `Reviewer` extra that `answer_brief` reads. `supervise_brief.brief` passes `extra` straight to `answer_brief`, so the extra is not written to the brief as a line of its own.
- **Several questions on one reviewer's item:** the last answered question's verdict decides. This is the plan's open case and no line names it, so it is not a finding.
- **Size:** `tools size --limit 300` prints nothing. The touched files have 142, 77 and 202 lines.

## Tool results
- **ruff:** 1 error, FURB167 `re.M` at `tests/scenarios/supervision_delegation_steps.py:171`. It is already in the base file (line 144 of `2c448d35`), so these commits did not add it.
- **vulture:** clean.
- **import-linter:** the project states no import contracts.
- **size:** none over 300.

## Commands run
- `git log --format='%h %s' -25`
- `git log --stat --format='%h %s' 2c448d35..0a9226a6`
- `git log --format='%h %s' fc76d519..0a9226a6 -- scripts tests features spec`
- `git show --stat c5561011`
- `git diff c5561011 6622133a --stat`
- `git diff 2c448d35 31c86e3c`
- `git show 2c448d35:tests/scenarios/supervision_delegation_steps.py | grep -n "re\.M"`
- `sed -n 1,145p scripts/supervise_answers.py`
- `grep -n extra scripts/supervise_worker.py scripts/supervise.py`
- `grep -n "def brief" -A25 scripts/supervise_brief.py`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 2c448d35`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`
- `wc -l` of the touched files
