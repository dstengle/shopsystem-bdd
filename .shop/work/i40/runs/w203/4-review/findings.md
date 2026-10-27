# Review of w203 (spec-integration#r45)

**Verdict: DONE.** No Critical finding, none triaged fix now. One Minor observation about how strong the new Then is.

## Commits reviewed

The branch `work/w203` no longer exists. The commits were taken from HEAD, between `689248a7 work: w203 ready -> claimed` and `4a3c3110 work: w203 claimed -> done`:

- `1c351ddc` spec-integration r45: an integrate round given answers drafts the lines they ask for. It touches 4 files: `scripts/supervise_brief.py` +4, `agents/initiative-round.md` 1 line, `skills/integrating-a-proposal/SKILL.md` 1 line, `tests/scenarios/spec_integration_steps.py` +48.

This is the one commit the implementer's result.json lists. Every file it touches is in the work-item's fileset and the plan's §2. There is no change under `features/`. The work-item has no Retires section.

## Removed and weakened tests

None. The diff of `tests/` is additions only. I looked for deleted `def`, removed `assert` lines, changed parametrize lists, and added skip or xfail markers, and found none. The existing `@when("work run starts a round of the kind integrate on that note")` on `run_integrate` is kept. The new When text is stacked on the same function, so the r44 scenarios bind as before.

## Allowances

The report's `## Tests changed under an allowance` says "none". That matches the diff: no existing test was changed.

## Cannot verify

- The report says the work-item run gave 145 passed and 1 skipped, and gives the suite figures at the start. I did not re-run the suite, as instructed. I ran only the r45 scenario (below).
- The agent and skill text changes (D3) are not run by any test. Whether a real `initiative-round` keeps an answer-quoted line instead of removing it under r2 cannot be checked from the commits. The new wording in both files does say so, consistently.
- The implementer has no red run of their own (report, Red / green). The plan's research notes record the red: StepDefinitionNotFoundError.

## Findings

### 1. Minor, observation: the Then's check (c) does not pin the drafted capability-proposal
`tests/scenarios/spec_integration_steps.py:154-155`. The step does `proposals = git(repo, "ls-files", ".shop/work")` and then `assert "notifications" in proposals`. The plan's D4(c) is that `work run` wrote the drafted `notifications` capability-proposal, which is `.shop/work/i1/notifications.md` (`supervise_change.py:81`). But this substring also matches the kept drafts path `.shop/work/i1/runs/i1/<k>-integrate/drafts/round-1/spec/capabilities/notifications.md`, if that path is tracked. So the check could pass without the proposal file.
- Why it matters: it is a weaker pin on r92 behaviour that is not this work-item's own line. r45 itself is pinned by checks (a) and (b), the brief sentence and the drafts.
- Fix: `assert ".shop/work/i1/notifications.md" in proposals.splitlines()`.
- Reproduction: from reading the code only. I did not run a variant, because a probe would mean editing tests, which this review does not do.
- Work-item: w203.

### Checked, no finding
- Behaviour against r45 and the Purpose: `ANSWER_LINES` is added to the integrate brief only when `answer_lines(name)` is non-empty (`supervise_brief.py:51-52`; D2). Its wording is conditional ("Where an answer below asks..."). It refers to "below", and the answers come later in the brief, at line 85. Nothing contradicts any Behaviour line.
- Code no line asks for: none. The brief sentence and the agent and skill text each serve r45.
- Risk I checked: whether `answer_lines(name)` on the integrate stage reads the initiative's answers. `name == self.initiative` maps to `initiative.md` (line 36), and `held` reads it there. Confirmed by the scenario passing with the answers in `i1/initiative.md`.

## Commands run

- `git log --oneline -25`, `git log --grep="^work: w203 "`, `git log --stat 689248a7..4a3c3110`, `git diff 689248a7 1c351ddc`
- `python3 <Scripts>/tools check --base 689248a7`:
  - ruff: All checks passed!
  - vulture: clean
  - import-linter: the project states no import contracts
- `python3 <Scripts>/tools size --limit 300`: no output, so no file is over the limit. `supervise_brief.py` is 194 lines and `spec_integration_steps.py` is 155.
- `python3 -m pytest -q tests/scenarios/test_spec_integration.py -k "r45 or integrate_given_answers or notifications"`: 1 passed (the r45 scenario).
- I read `scripts/supervise_brief.py` lines 30-160 and grepped `scripts/supervise_change.py` for the proposal path.
