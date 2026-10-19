---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/behaviour-lines-are-ears
summary: "Every Behaviour line is one EARS requirement in one of EARS's patterns, with \"shall\", one system response, one sentence."
date: 2026-10-19
status: proposed
source: "observation/2026-10-19-lines-not-ears; the person, 2026-10-19"
---

# 0051. Behaviour lines are EARS

## Decision

Every Behaviour line is one EARS requirement, written in one of its patterns, in this order of clauses:

- ubiquitous: `The <system> shall <response>.`
- event-driven: `When <trigger>, the <system> shall <response>.`
- state-driven: `While <state>, the <system> shall <response>.`
- unwanted behaviour: `If <condition>, then the <system> shall <response>.`
- optional feature: `Where <feature>, the <system> shall <response>.`
- complex: the clauses combined, `Where`, then `While`, then one `When` or `If … then`, then the system and its response.

The pattern follows what starts the behaviour, not the wording it had: a response to a command, an input or an event is event-driven, with the trigger in its `When` clause; a refusal or a fault is unwanted behaviour, with its condition in `If … then`; behaviour that lasts for a period is state-driven; behaviour that depends on an option or configuration is optional; only what holds with no trigger at all is ubiquitous. The system is named in the line: a script (`model check`, `features`), an agent, or a skill. One trigger or condition, one "shall" and one response per line: a line with two conditions or two responses is two lines. The response is observable by the narrator, as before. This replaces the "no shall, present indicative" adaptation that docs/capability-format.md taught. The strict form goes back to the design model in shopsystem-knowledge after the migration release.
