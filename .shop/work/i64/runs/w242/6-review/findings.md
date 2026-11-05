# Review of w242 (supervision#r221@0.29)

**Verdict: DONE.** No Critical finding and nothing to fix now. There are two Minor findings, both observations.

## Commits reviewed

- `4fa77b43` "supervision r221: a sent-back glossary-proposal gets a new integrate round". This is the brief's `Commits:`, the only commit after `4a3f3b0d work: w242 ready -> claimed`.
- The implementer's results list `79b36ae5` (stages 3 and 4) and `5960964a` (stage 5). Both have the same subject, author, date and `--stat` as `4fa77b43`: 4 files, +12 −9. They are the same change rebased by `work run` onto later queue commits, so the content does not differ.

The change:
- `scripts/supervise_rounds.py:59-60`: in `due`'s glossary loop, a glossary-proposal at `awaiting-answer` or `approved` that `sent_back` (its last apply gave `nothing_applied` or `unheld_answers`) is routed to `integrate` with `drafted` as the status after. This check comes before `supervise_glossary.route`. It mirrors r150's handling in `route` for capability-proposals.
- `scripts/supervise_brief.py:135-137` (outside the plan's file set; the 3-implement report names it): `integrate_lines` leaves out the `Request:` and accepted-lines lines when the initiative fulfils no request. Before the change it refused with "there is no request under .shop/work/requests".
- Steps: the answers regex of the g1 Given now accepts commas. The "apply round … applies nothing" Given and the "integrate was started … after the apply round had ended" Then now take `[pg]1`.

## Removed and weakened tests

None. I looked for deleted test or step functions, dropped parametrize cases, removed or loosened asserts, added skip/xfail, and rewritten assertions.
- `integrate_after_apply` (supervision_reintegrate_steps.py:69-73) is now parameterized by name. Before, it called `position(repo, stage=…)` (default `node="p1"`, supervision_rounds_steps.py:231) and `rounds(repo, "integrate", "p1")`. Now it passes `name`, so for `p1` it asserts exactly what it did before, and it also covers `g1`.
- `apply_applies_nothing` gains a `name` parameter. Its plan entry `round:apply` is unchanged.
- The answers regex in `glossary_proposal_answered` was widened (`[^,]+?` → `.+?`). This matches more step lines and asserts nothing less. The `(?: only)?$` suffix is still stripped because the match is lazy.

The plan's "Tests the decisions break" lists none, which agrees with this.

## Allowances

The report's `## Tests changed under an allowance` says "none" in stages 3 and 5. There are no rows to verify.

## Cannot verify

- The red run the 3-implement report gives (the hang from a repeated apply, then "no request" refused). The commits do not record it.
- The 4-implement result says no 3-implement report existed when it ran. One exists now. I cannot tell from the commits how the stages ran in order.
- The suite record shows r221's scenario is not among the expected failures and the suite passed at `4fa77b43` (1090 passed, 0 failed). I take this from the record and did not run the suite.

## Findings

### 1. Minor (observation): `integrate_lines` changes for every proposal re-integrated in an initiative that fulfils no request
`scripts/supervise_brief.py:135-137`. An integrate round for a capability-proposal (r149/r150 re-integration) in an initiative with no `fulfils` used to be refused, which faulted the round. Its brief is now built with no Request lines.
- This is brief mechanism that r221 needs (the scenario's i1 fulfils nothing). It contradicts no Behaviour line: r79 (`due` line 47) still keeps the initiative's own integrate round behind `fulfils`. So it is not code that no line asks for.
- The docstring ("The request the initiative fulfils and the lines of it …") does not say that the lines can be absent.
- It is outside the plan's file set but named in the report.
- Fix: add one sentence to the docstring about the case with no request.

Reproduction: the scenario of r221 (features/supervision.feature:2072) drives it. The suite record shows it passing.

### 2. Minor (observation): ruff findings in files the commit touched, on lines it did not change
`python3 <Scripts>/tools check --base 4a3f3b0d` reports:
- RUF100 at supervision_proposal_steps.py:102 and :146
- F401 at supervision_reintegrate_steps.py:13
- FURB167 at supervision_reintegrate_steps.py:174

None of these lines is in the diff (the hunks are :142-143, :30-32 and :69-72), so they were there before. Fix: `ruff --fix` in the work that next touches these files.

## Checks

- **ruff:** 4 findings, all on lines the commit did not change (finding 2).
- **vulture:** clean.
- **import-linter:** the project states no import contracts.
- **size (`--limit 300`):** no output. The touched files are supervise_brief.py (217 lines), supervise_rounds.py (277), supervision_proposal_steps.py (213) and supervision_reintegrate_steps.py (175).
- **features/:** the commit does not change it.

## Commands run

- `git show 4fa77b43…`
- `git log --oneline -3 4fa77b43`
- `git show --stat 5960964a` and `git show --stat 79b36ae5`
- `git log --oneline 86582d02..4fa77b43`
- `git show 86582d02:tests/scenarios/supervision_reintegrate_steps.py | grep position`
- `grep` of `due`, `sent_back`, `integrate_lines`, `position` and `rounds` in scripts/ and tests/scenarios/
- `sed` of supervise_rounds.py:40-75 and supervise_brief.py:55-75 and :120-145
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 4a3f3b0d`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`
- `wc -l` of the touched files
