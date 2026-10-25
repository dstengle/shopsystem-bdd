## Budget
- skills/formulating-features/SKILL.md
- agents/initiative-round.md

## Changed
- SKILL.md: "Who Does What" now says work run starts the formulate round; "If the person is talking to you" and the small-change sentence gone; step 3 returns the question in the reply; step 4's last sentences say the round rewords v_t1 scenarios; "The Small-Change Path" became "A Word the Glossary Avoids" (reword rules kept, round dispatches a feature-formulator for other capabilities' rows, no re-following).
- initiative-round.md: formulate reply clause reports the rewording done.

## Runs
Guarantees work-item: no scenario, so no red run. `python3 -m pytest -q --work-item w145`: 142 passed, 1 skipped (exit success). tests/scripts/test_agents.py: 8 passed. Suite record at start: 798 passed, 0 failed at 121fade (expected-failing list in brief). `tools size`: prints nothing.

## Tests changed under an allowance
none

## Open questions
none beyond the plan's §5: reword in a capability this round also wrote (text unchanged: step 4's blocking rule applies); formulator question during a reword goes in the reply like any question.

## Outside the file set
none. Dangling reference for the review: skills/checking-spec-consistency/SKILL.md l.62-64 still mentions the small-change path; integrating-a-proposal's too (w143). The Hand-back Template's closing paragraph ("The session verifies ... writes the drafted scenario") still has a session writing a feature file; not changed.

The plan contained no code. Commit: a8a59c7.
