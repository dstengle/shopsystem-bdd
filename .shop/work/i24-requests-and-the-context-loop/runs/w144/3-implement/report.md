## Budget

- agents/initiative-round.md
- scripts/supervise_worker.py
- skills/integrating-a-proposal/SKILL.md
- skills/formulating-features/SKILL.md

## Changed

- agents/initiative-round.md "The ledger": the line goes to `.shop/work/<initiative>/ledger.md` by `work note <initiative> "<line>"`, after the job's own commit, single line; the initiative comes from the dispatch or the brief's `Capability-proposal:` path. If no initiative is named or `work note` refuses, the round replies with its work and says the line was not written.
- scripts/supervise_worker.py: each ROUNDS kind gets `Bash(python3 <SCRIPTS>/work note *)` only; comment rewritten.
- Both skills: dispatches give the initiative's name; the initiative-round paragraph ends with the ledger line.

## Red/green

Guarantees work-item: no scenario, so no red run. Final run: `python3 -m pytest -q --work-item w144` -> 142 passed, 1 skipped. `tests/scripts/test_agents.py tests/scenarios/test_supervision.py` -> passed.
Suite at start: 798 passed, 0 failed (with a listed expected-failing set, none of which failed in my module run).

## Tests changed under an allowance
none

## Open questions
- A round that ends BLOCKED: whether it still appends a line is unchosen (the agent file is silent).
- Defect D1 (empty `work note` text accepted) is not fixed here.

## Other
Plan contained no code. `tools size --limit 300`: nothing printed. Commit: 6d5851d.
Files: the four above.
