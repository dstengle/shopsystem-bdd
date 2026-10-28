# integrate of supervision

Initiative: .shop/work/i46/supervision.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: integrate
Request: q30
Accepted lines of the request:
- 1. The bounded context's glossary shall be a target of spec work in its own right, beside its capabilities.
- 2. **When** a round of the kind `integrate` drafts a change to the glossary, the round's change list shall give the terms it adds, changes and removes in an entry of the glossary, and in no entry of a capability.
- 3. **When** a change list that `work run` reads names the glossary, `work run` shall write a `drafted` proposal for the glossary with the terms it adds, changes and removes.
- 4. The gate shall approve the terms of a proposal for the glossary before they are applied to `spec/index.md`.
- 5. **When** an initiative changes only the glossary, `work run` shall deliver the initiative without a capability-proposal.
- 6. `model check` shall check the terms of a proposal for the glossary as it checks the terms a capability-proposal names.
- 7. **When** a question of an initiative names a term of the glossary or a proposal for the glossary, `work run` shall give the question to the person and to no answer under a delegation.
- 8. **While** a proposal for the glossary awaits the person's answer, `work run` shall apply none of its terms to `spec/index.md`.
Ids drafted elsewhere (number added lines above each on the same capability): supervision#r3, supervision#r5, supervision#r16, supervision#r71, supervision#r77, supervision#r80, supervision#r92, work-queue#r3, work-queue#r11, work-queue#r16, work-queue#r17, work-queue#r18, requests#r1, requests#r3, supervision#r99, supervision#r104, supervision#r112, supervision#r113, supervision#r114, review#r9, supervision#r125, supervision#r126, supervision#r127, design-model-check#r120, design-model-check#r121, requests#r26, requests#r27, requests#r35, requests#r36, requests#r37, requests#r38, spec-integration#r17, work-queue#r33, supervision#r137, supervision#r138, supervision#r139, supervision#r140, requests#r46, spec-consistency#r28, spec-integration#r47, spec-integration#r48, spec-integration#r49, spec-integration#r50, spec-integration#r51, spec-integration#r52, spec-integration#r53
Drafts path: /tmp/work-run-i46-rhbgokrg/supervision-3-integrate/.shop/scratch/3-integrate/drafts
Give your change list in your result's `changes`: a list with one entry for each capability, each `{"capability": <name>, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `<capability>#r<n>`. Every term you add, change or remove goes in one entry for the glossary, `{"glossary": true, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `term/<term>`, and in no capability's entry.
Ledger: .shop/work/i46/ledger.md
Where an answer below asks for lines the request's accepted lines do not, draft those lines under the capabilities the answer names, each quoting the answer it comes from.
Base: 134745663cfa0a109b8564370c2464ef9ee9a7d5
Worktree: /tmp/work-run-i46-rhbgokrg/supervision-3-integrate
Branch: round/supervision-3-integrate
Answers the person gave, each with the question it answers:
- Question: r158: "When a change list that `work run` reads names the glossary, `work run` shall write a `drafted` glossary-proposal with the terms the change list adds, changes and removes in the glossary." Reading A: only an integrate round's change list gives a glossary-proposal, as in r159. Reading B: every change list work run reads gives one, an apply round's included (r145); then an apply round applying a glossary-proposal's drafts would give a new drafted glossary-proposal, against r166.
  Answer: 2026-10-28: r158: reading A, only an integrate round's change list gives a glossary-proposal, as in r159 (the person, 2026-10-28)
- Question: r160: "While a glossary-proposal is `awaiting-answer`, `work run` shall start no round of the kind `apply` for it." Reading A: no apply round while it is awaiting-answer and some question has no answer; once all are answered r165 starts the apply round. Reading B: no apply round while the status is awaiting-answer whatever the answers; but r169 sets that status at gate end and an answered proposal still has it, so r165 could never hold.
  Answer: 2026-10-28: r160: reading A, no apply round while the glossary-proposal is awaiting-answer and some question has no answer; once all are answered r165 starts the apply round (the person, 2026-10-28)

Read (paths in your worktree):
- .shop/work/i46/supervision.md
- .shop/work/i46/runs/supervision/1-formulate
- .shop/work/i46/runs/supervision/2-formulate
- .shop/work/i46/ledger.md

Run directory: /tmp/work-run-i46-rhbgokrg/supervision-3-integrate/.shop/scratch/3-integrate
Result file: /tmp/work-run-i46-rhbgokrg/supervision-3-integrate/.shop/scratch/3-integrate/result.json

You start in your worktree, /tmp/work-run-i46-rhbgokrg/supervision-3-integrate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
