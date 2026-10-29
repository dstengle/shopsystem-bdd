---
id: glossary-proposal/missingmass.io/shopsystem/shopsystem-bdd/i59-glossary
kind: glossary-proposal
part_of: initiative/missingmass.io/shopsystem/shopsystem-bdd/i59
status: awaiting-answer
adds: []
changes: [term/check]
removes: []
date: 2026-10-29
---

# glossary

The drafts of this proposal are in .shop/work/i59/runs/i59/1-integrate/drafts/round-2/.

## Questions
- Glossary change `term/check`: shall the glossary entry change? Now: `- **check**: a command a work-item names in place of scenarios, whose exit code 0 shows its work complete. Not: criterion.` Drafted: `- **check**: a command a work-item names in place of scenarios, whose JSON output holding `ok` true shows its work complete. Not: criterion.` (source: answer A2, commands answer in JSON with `ok`, not by exit code). Readings: (1) approve the new wording, so the glossary matches design-decision/commands-and-agents-answer-in-json [recommended]; (2) keep the old wording, which then contradicts the lines that give `ok` and exit 0 on any non-crash; (3) another wording, which the person gives.
