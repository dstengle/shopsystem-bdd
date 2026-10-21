---
id: initiative/missingmass.io/shopsystem/shopsystem-bdd/i16
title: The session keeps the gate and nothing else
summary: The session talking to the person holds only the gate and a ledger; integrating, gate assembly, applying verdicts, code, trials and analysis go to the plugin's own roles, which reply in a few lines and leave the rest in files.
kind: capability-change
owner-level: shopsystem-bdd
status: proposed
priority: 1
source: [observation/2026-10-21-session-keeps-the-gate]
date: 2026-10-21
---

Next release (the person, 2026-10-21: "I like keeping the context small. How can we keep this practice?";
"This looks good for next release").

Covers (lines to be drafted in EARS for a small gate):
- `initiative-round` gains a `gate` job: from drafts and reports it writes the gate page's data; the session
  publishes it and reads only the verdicts; its `apply` job applies them.
- a `trial-runner` agent: runs a plugin tool or `work run` on a real target or a fixture repository, reads only the
  target and the plugin's scripts, writes a measurement record, replies in a few lines.
- code changes, fix rounds and refactors only through `work run`; a fix work-item sends new scenario rows to the
  blind formulator.
- term and consistency analysis through `spec-checker`.
- the skills teach the session's rules: agents reply in a few lines, the rest in files the session reads only to
  decide; one ledger per piece of work (rulings and verdicts), appended by `initiative-round` on the spec side, as
  `log.jsonl` is on the delivery side.
- after a release, the installed plugin is updated so the next session runs the new agents.
