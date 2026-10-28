# Report w219

## Budget

scripts/supervise_change.py, scripts/supervise_rounds.py, scripts/supervise_brief.py, scripts/supervise_glossary.py (new), CLAUDE.md, agents/initiative-round.md, tests/scenarios/spec_integration_steps.py, tests/scenarios/spec_integration_apply_steps.py (and agents/capability-writer.md if it needs the wording)

Suite record at start: 1034 passed, 2 failed (the two spec_integration scenarios r54, r55) plus the expected failures listed in the brief.

## What changed
- supervise_change.py: `entries` reads one glossary entry (`{"glossary": true, ...}`, capability None); `unknown` and `write_proposals` skip it.
- supervise_brief.py: CHANGE_LIST names the glossary entry, terms only there; the apply brief carries the withheld-terms line.
- supervise_glossary.py (new, row in CLAUDE.md): terms of glossary-proposals whose status is not approved.
- agents/initiative-round.md: wording for both. capability-writer.md not changed (its change list is a note-level table, no per-capability entry form).
- tests: r54 steps in spec_integration_steps.py, r55 steps in spec_integration_apply_steps.py (answered_proposal split into a helper).

## Red and green
Red r54: `python3 -m pytest -q --work-item w219 -k "glossary and integrate"` failed: work run refused "an entry of its `changes` names no `capability`" (expected: no glossary entry in code). Green after the change.
Red r55: failed on the brief lacking "Apply none of them to spec/index.md" (expected). Green after wiring.
Final: `python3 -m pytest -q --work-item w219` -> 182 passed, 1 skipped. test_supervision.py + tests/scripts: 179 passed, 1 skipped. test_spec_integration + test_supervise_change: 5 passed.
Suite at start: 1034 passed, 2 failed (r54, r55) plus expected failures.

## Tests changed under an allowance
none

## Open questions
Plan §5 cases: two glossary entries; a glossary entry with non-term ids; an apply round applying a withheld term anyway (no check); apply for a glossary-proposal itself; model check not knowing kind glossary-proposal.

## Other
The plan contained no code. Size check: nothing over 300. Nothing outside the file set.
Commits: 085527d8 (r54), 55bed875 (r55). tools size --limit 300 printed nothing.
