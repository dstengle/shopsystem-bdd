# Report of w202 (implement)

## Budget
- tests/scenarios/test_spec_integration.py (new)
- tests/scenarios/spec_integration_steps.py (new)
- scripts/supervise_brief.py
- agents/initiative-round.md
- skills/integrating-a-proposal/SKILL.md
- docs/capability-format.md

Suite record at start: Suite: 947 passed, 0 failed at d8fd6b33 in 27 s (with the listed expected-red tests).
The plan contained no code, so none was pasted.

## What changed
- scripts/supervise_brief.py: `Briefs.upstreams` reads the `## Upstreams` bullets (`- <id>: <path>`) of spec/index.md. The integrate brief gets an `Upstream:` line for each, the spec path in its Read list, and the `requests` form (REQUEST_LINES). With no upstream named the brief is unchanged.
- agents/initiative-round.md, skills/integrating-a-proposal/SKILL.md, docs/capability-format.md: the round gives `requests`, and the form is documented.
- tests/scenarios/test_spec_integration.py and spec_integration_steps.py (new): bind the r44 scenario.

## Red and green
- Red: `python3 -m pytest -q --work-item w202 -x` failed in "the round's result gives the lines of a request into billing", on the assertion that the brief names BILLING and `requests`. Expected: nothing read upstreams.
- Green: the same command, 145 passed, 1 skipped.
- Also green: tests/scripts/test_agents.py and test_supervise_change.py (9 passed); `--whole-suite tests/scenarios/test_supervision.py -k integrate` (18 passed, 1 xfailed, the r135 scenario, as before).
- `tools size --limit 300` printed no file.

## Tests changed under an allowance
none

## Open questions
Plan section 5's cases are left unchosen, and the code is silent on them: a missing spec path, a malformed bullet, several upstreams, `requests` naming an upstream the index does not name, the pin.

## Outside the file set
none

## Commits
6e3c4f04 spec-integration r44: the integrate round is told its upstreams and gives the lines of a request into them
