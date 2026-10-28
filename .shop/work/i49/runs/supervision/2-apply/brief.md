# apply of supervision

Capability-proposal: .shop/work/i49/supervision.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: apply
Give the change list of what you applied in your result's `changes`: a list with one entry for each capability, each `{"capability": <name>, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `<capability>#r<n>`. Every term you add, change or remove goes in one entry for the glossary, `{"glossary": true, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `term/<term>`, and in no capability's entry.
Compare each answer below with the drafts you applied, and give each answer they do not hold in your result's `unheld_answers`, a list of the answers' texts, also when you applied some of the drafts; leave out an answer they hold.
Drafts path: .shop/work/i49/runs/i49/1-integrate/drafts/round-1/
Base: b88de23885022b4839fe484ebe70bd8a52d81939
Worktree: /tmp/work-run-i49-k6h3iltt/supervision-2-apply
Branch: round/supervision-2-apply
Answers the person gave, each with the question it answers:
- Question: supervision#r180 (replaces removed r93): drafted line in full: "**When** a `started` initiative that fulfils a request has neither a capability-proposal, a glossary-proposal nor a work-item, `work run` shall start a round of the kind `integrate` for it, given the accepted lines of the request it fulfils." Removed r93 was: "**When** an initiative is `started` and has neither a capability-proposal nor a work-item, `work run` shall start a round of the kind `integrate` given the accepted lines of the request it fulfils." The request's line (q35 line 1) ends at "for it"; the clause "given the accepted lines of the request it fulfils" comes from r93, not the request. Readings: (a, recommended) keep the clause as drafted; (b) end the line at "for it": "**When** a `started` initiative that fulfils a request has neither a capability-proposal, a glossary-proposal nor a work-item, `work run` shall start a round of the kind `integrate` for it."
  Answer: 2026-10-28: r180: reading (a), keep the clause 'given the accepted lines of the request it fulfils' (answered by the person, 2026-10-28)

Read (paths in your worktree):
- .shop/work/i49/supervision.md
- .shop/work/i49/runs/supervision/1-gate
- .shop/work/i49/runs/i49/1-integrate/drafts/round-1/

Run directory: /tmp/work-run-i49-k6h3iltt/supervision-2-apply/.shop/scratch/2-apply
Result file: /tmp/work-run-i49-k6h3iltt/supervision-2-apply/.shop/scratch/2-apply/result.json

You start in your worktree, /tmp/work-run-i49-k6h3iltt/supervision-2-apply: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
