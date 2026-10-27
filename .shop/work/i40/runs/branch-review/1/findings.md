# Branch review of i40

**Verdict: DONE.** No finding is Critical and none is triaged fix now. Every check was run and verified. There are two Minor observations.

## Range

`96d2b80b..729152c6` (Base `96d2b80b`, the commit that added `.shop/work/i40/initiative.md`; HEAD `729152c6`). The range has 27 commits.

- **w203** (spec-integration#r45, `green`): its one commit is `1c351ddc` "spec-integration r45: an integrate round given answers drafts the lines they ask for". It sits between `689248a7 work: w203 ready -> claimed` and `4a3c3110 work: w203 claimed -> done`. It changes 4 files, all in w203's fileset: `scripts/supervise_brief.py` (+4), `agents/initiative-round.md` (1 line), `skills/integrating-a-proposal/SKILL.md` (1 line) and `tests/scenarios/spec_integration_steps.py` (+48).
- **Commits from the capability-proposals' rounds** (`work run`): `0c09944f` (spec: add r45), `3df7df2e` (features: formulate r45), and the `work:`, `work note:`, `work answer:` and `work add:` commits.
- **One commit belongs to no work-item and no round:** `ce86effc` "records: observation 2026-10-27-silent-exit-on-questions" (see Finding 2).

## Suite

`Suite: 949 passed, 16 failed at 729152c6 in 29.5 s` (pytest's own summary: "16 failed, 949 passed, 1 skipped, 548 warnings, 56 subtests passed in 29.26s").

- **Parallel:** yes. `pytest.ini` has `addopts = -n auto`, and the run used 1597% CPU.
- **In-process:** no. The step definitions run `scripts/work` as a subprocess (for example `spec_integration_steps.py:109`). The suite is under 60 s, so this is not a finding.
- **The 16 failures:** each one is in the expected-failing list of w203's implement brief (16 entries). These are scenarios formulated for other initiatives' lines and not yet implemented: 1 in design-model-check (v17), 14 in requests and 1 in supervision. None is in a file this branch touched. The r45 scenario was the 17th failure at `689248a7` and passes now.

## Checks

- **w203's check:** `python3 -m pytest -q --work-item w203` gives 145 passed, 1 skipped, in 4.33 s.
- **`tools check --base 96d2b80b`:**
  - ruff: All checks passed!
  - vulture: clean
  - import-linter: the project states no import contracts. No contracts are stated, so there was nothing to read by hand.
- **`tools size --limit 300`:** no output, so no file is over the limit. `supervise_brief.py` is 194 lines and `spec_integration_steps.py` is 155.
- **`features deprecated`:** 9 deprecated scenarios. All are in design-model-check, requests and supervision, and none is in this branch's features. None has a replacement whose work-item is in i40.
- **`features bindings`:** "every binding names a scenario".
- **Dry-run against real mode:** the operation this branch changes (the integrate brief) has no dry-run mode, so there was no randomized test to run.

## Removed and weakened tests

None. I searched `git diff 96d2b80b HEAD -- tests features` for:
- deleted `def` lines;
- removed or changed `assert` lines;
- changed parametrize lists;
- added `skip` or `xfail` markers;
- changed step texts.

The `tests/` diff is additions only. The existing `@when("work run starts a round of the kind integrate on that note")` on `run_integrate` is kept, with a second `@when` text stacked on the same function. The r44 scenarios bind as before and pass.

## Allowances

w203's report gives "none" under `## Tests changed under an allowance`. That holds: no existing test was changed.

## Cannot verify

Nothing a work-item names. One note: the D3 text in the agent and skill (a line drafted from an answer quotes the answer and is kept) is prose that no test runs. Its wording is consistent with r45 and r2.

## Findings

### 1. Minor, w203, observation: the Then's check (c) does not pin the drafted capability-proposal
`tests/scenarios/spec_integration_steps.py:154-155`.
- **What is wrong:** `assert "notifications" in git ls-files .shop/work` is a substring check. `work run` commits the kept drafts under `.shop/work/i1/runs/i1/<k>-integrate/drafts/round-1/spec/capabilities/notifications.md`, the same path the lines above glob, so the check holds even without the proposal file `.shop/work/i1/notifications.md` (supervision r92, `supervise_change.py:81`).
- **Why it matters:** r92 is pinned more weakly than the plan's D4(c) intends. r45 itself is still pinned, by the brief check and the drafts check.
- **Fix:** `assert ".shop/work/i1/notifications.md" in proposals.splitlines()`.
- **Reproduction:** from reading the code only. The tracked kept drafts can be seen in this repository too: `git ls-files .shop/work/i40/runs/i40/1-integrate/drafts` lists `.../spec/capabilities/spec-integration.md`. The w203 review gives the same finding.

### 2. Minor, no work-item, observation: a commit belongs to no work-item
`ce86effc`, `.shop/records/observations.md:455-461`.
- **What is wrong:** the coordinator's record of observation 2026-10-27-silent-exit-on-questions was committed on the initiative's branch, outside any work-item or round.
- **Why it matters:** it only adds a record and changes no code or spec, but the branch's history mixes the coordinator's records into the initiative.
- **Fix:** none needed for this branch. Records could be committed outside an initiative's range.
- **Reproduction:** `git show --stat ce86effc`.

### Checked, no finding
- **Behaviour:** `ANSWER_LINES` is added to the integrate brief only when `answer_lines(name)` is non-empty (`supervise_brief.py:51-52`). For the integrate stage, `name` is the initiative, so the brief reads `initiative.md` (line 35). This is what r45 asks: a round given answers is told to draft the lines they ask for under the capabilities they name. Nothing contradicts a Behaviour line or spec-integration's Purpose.
- **Code no line asks for:** none. The brief sentence serves r45. Its "each quoting the answer" serves r2's quoting rule.
- **`features/` changes:** the r45 scenario was added by the formulate round (`3df7df2e`), not by a work-item. w203's commit changes nothing under `features/`.

## Shape

- **CLAUDE.md size limit:** met. 194 and 155 lines.
- **Module map:** the `scripts/supervise*.py` row ("briefs") is met by `supervise_brief.py:18-19,51-52`. The `tests/scenarios/` row (one `<capability>_*_steps.py` module a concern) is met: the r45 steps are in `spec_integration_steps.py:60-95,148-155`.
- **Unreached code and steps:** the two new Givens' helpers and the shared When are each reached by the r45 scenario. vulture reports nothing unreached.

## Coupling

The branch adds no dependency on another project. The brief sentence and the agent text depend on the `initiative-round` and `capability-writer` agents of this same plugin.

## Observations

- Finding 1, check (c): reproduce with `git ls-files .shop/work/i40/runs/i40/1-integrate/drafts`, which shows that kept drafts under `.shop/work` are tracked, so a substring match on a capability name holds without the proposal file.
- Finding 2, stray records commit: `git show --stat ce86effc`, which shows 1 file, `.shop/records/observations.md`, +8.
- Plan §5's open cases are not covered by any line or test: an answer that repeats an accepted line, an answer naming no capability or several, and an `## Answers` bullet with no question. This was found by reading the plan.
- The real case behind q18 is answers on a capability-proposal. Supervision's q18 line, giving an integrate round the capability-proposal's questions and answers, is not applied yet (the ledger's "apply round 2 supervision: nothing applied"). Until then, r45 acts only on an initiative's own answers (plan D1).
