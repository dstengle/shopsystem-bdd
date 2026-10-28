# apply of supervision

Capability-proposal: .shop/work/i48/supervision.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: apply
Give the change list of what you applied in your result's `changes`: a list with one entry for each capability, each `{"capability": <name>, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `<capability>#r<n>`. Every term you add, change or remove goes in one entry for the glossary, `{"glossary": true, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `term/<term>`, and in no capability's entry.
Compare each answer below with the drafts you applied, and give each answer they do not hold in your result's `unheld_answers`, a list of the answers' texts, also when you applied some of the drafts; leave out an answer they hold.
Drafts path: .shop/work/i48/runs/i48/1-integrate/drafts/round-1/
Base: 6cf63096ec9edd7f549d3452dfc0408f53453906
Worktree: /tmp/work-run-i48-89bbkiac/supervision-2-apply
Branch: round/supervision-2-apply
Answers the person gave, each with the question it answers:
- Question: r179, "terms of the proposal": a capability-proposal lists requirement ids, and terms are listed by a glossary-proposal. Line: [r179] **When** a round of the kind `integrate` redrafts some of the lines of a capability-proposal it was started for, `work run` shall keep the requirement ids and terms of the proposal that the round's change list does not name. Reading A: split it into r179 (requirement ids of the capability-proposal) and r180 "**When** a round of the kind `integrate` redrafts some of the terms of a glossary-proposal it was started for, `work run` shall keep the terms of the glossary-proposal that the round's change list does not name." Reading B: drop "terms", so r179 reads "...shall keep the requirement ids of the capability-proposal that the round's change list does not name." Reading C: keep the line as drafted. Recommended: A.
  Answer: 2026-10-28: r179's terms: reading A, split into r179 (a capability-proposal's requirement ids) and r180 (a glossary-proposal's terms) (answered by the person, 2026-10-28)
- Question: r179, what "keep" means for the ids. Line: [r179] **When** a round of the kind `integrate` redrafts some of the lines of a capability-proposal it was started for, `work run` shall keep the requirement ids and terms of the proposal that the round's change list does not name. Reading A: the ids stay in the `adds`, `changes` and `removes` that `work run` writes for the proposal (r159, r145), with the line as drafted. Reading B: the apply round is also given the earlier round's drafts of the lines not named, so the line reads "...`work run` shall give the round of the kind `apply` the kept drafts of the earlier round for each line the redraft's change list does not name." Recommended: A.
  Answer: 2026-10-28: r179's keep: reading A, the ids stay in the adds, changes and removes work run writes for the proposal (answered by the person, 2026-10-28)
- Question: r179, which redraft the line covers. Line: [r179] **When** a round of the kind `integrate` redrafts some of the lines of a capability-proposal it was started for, `work run` shall keep the requirement ids and terms of the proposal that the round's change list does not name. Reading A: any round of the kind `integrate` started for a capability-proposal (r141, r150, r149) that redrafts a subset of its lines, as drafted. Reading B: only a redraft from answers (r142, r148). Recommended: A.
  Answer: 2026-10-28: r179's redrafts: reading A, any integrate round started for a capability-proposal that redrafts a subset of its lines (answered by the person, 2026-10-28)

Read (paths in your worktree):
- .shop/work/i48/supervision.md
- .shop/work/i48/runs/supervision/1-gate
- .shop/work/i48/runs/i48/1-integrate/drafts/round-1/

Run directory: /tmp/work-run-i48-89bbkiac/supervision-2-apply/.shop/scratch/2-apply
Result file: /tmp/work-run-i48-89bbkiac/supervision-2-apply/.shop/scratch/2-apply/result.json

You start in your worktree, /tmp/work-run-i48-89bbkiac/supervision-2-apply: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
