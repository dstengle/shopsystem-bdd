## frontmatter
---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/role-boundaries
title: Role boundaries
narrator: the person using the workflow
group: guarantees
rests_on: [design-decision/the-v3-agents, design-decision/spec-writers-blind-to-code, design-decision/the-session-keeps-the-gate, design-decision/commands-and-agents-answer-in-json]
retired: []
---

## Behaviour
- [r1] The plugin's agent definitions shall let only `initiative-round` dispatch.
- [r2] The plugin's agent definitions shall give no reviewer, no researcher and no planner the Edit tool.
- [r3] The plugin's agent definitions shall give the `capability-writer` and the `feature-formulator` no edit and no shell tool.
- [r4] The plugin's agent definitions shall give the implementer the skills listed under its `skills:`, `bdd-red-green` always among them, and the Skill tool, which `work run` allows only for those skills.
- [r5] The plugin's agent definitions shall name each agent's model: Opus for the `capability-writer` and the `feature-formulator`, the planner and the reviewers, Sonnet for the implementer, `initiative-round`, the `spec-checker` and the `trial-runner`, Haiku for the researcher.
- [r6] The plugin's agent definitions shall give the `bdd-planner` no shell tool.
- [r7] The plugin's agent definitions shall give the `bdd-branch-reviewer` no shell tool.
- [r8] The plugin's agent definitions shall have every session started as one of them reply to the session or script that started it with one JSON object giving its outcome, its summary, the files it names and its questions.
