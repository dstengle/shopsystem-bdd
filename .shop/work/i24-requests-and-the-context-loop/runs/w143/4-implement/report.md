# w143 report

## Budget
- skills/integrating-a-proposal/SKILL.md
- agents/initiative-round.md
- scripts/supervise_brief.py

## What changed
- SKILL.md: removed "If the person is talking to you", the Small-Change Path and its pointers; Who Does What says work run starts each round; step 3 is the gate round's result questions; step 5 hands off to the `formulate` round; v_t1 and Terms reworded.
- initiative-round.md: "job" -> "kind"; `gate` gives `questions` in its result (no cards, no coordinator); description and intro no longer say a session dispatches it; ledger counts gate questions.
- supervise_brief.py: `Job:` -> `Kind:`.

## Red/green
No scenario (guarantees work-item); no red run. Ran tests/scripts/test_agents.py and the supervision brief/round tests: 8 passed. Suite record at start: 798 passed, 0 failed (with the listed expected failures).
Plan contained no code.

## Size
`tools size --limit 300` printed nothing.

## Tests changed under an allowance
none

## Open questions
- Form of each gate question: one string per decision (my choice, list of strings per worker()).
- Whether gate.md is read by the gate round: text says it reads each round's gate.md "where it was written"; spec leaves it open.
- Dangling pointers outside file set: skills/checking-spec-consistency/SKILL.md:53,64, skills/migrating-to-capabilities/SKILL.md:106 point at the removed small-change path. Round path drops result questions (supervise_rounds.py:49-55) and nothing starts gate/integrate rounds; supervision r68/r85.

## Outside the file set
none

## Commits
c5f4ecd
