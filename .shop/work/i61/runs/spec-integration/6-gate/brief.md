# gate of spec-integration

Capability-proposal: .shop/work/i61/spec-integration.md
Agent: initiative-round
Scripts: /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.28.3/scripts
Kind: gate
Give the gate as questions in your result's `questions`, one string each: every question a decision, with its readings and the recommended reading marked.
Adds: none
Changes: spec-integration#r46
Removes: none
Ask questions only on the lines and terms listed above as adds, changes or removes, and on no other line or term.
Drafts path: .shop/work/i61/runs/spec-integration/5-integrate/drafts/round-1/
Base: 2b30178d6a0c7fa1a9a62466e6f99ddcaada2805
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/spec-integration-6-gate
Branch: round/spec-integration-6-gate
Answers the person gave, each with the question it answers:
- Question: spec-integration r58 vs r46. Line r58 (added): "When a round of the kind `apply` gives the answers its drafts do not hold, `initiative-round` shall leave out each answer that a later answer of the same proposal replaces." r46 (in spec) says: "When a round of the kind `apply` ends, `initiative-round` shall give in its result each answer of the capability-proposal that the drafts it applied do not hold." The two disagree about a replaced answer. Readings: (a) RECOMMENDED: change r46 to "...each answer of the capability-proposal that the drafts it applied do not hold and that no later answer of the same proposal replaces." and merge r58 into it; (b) keep r46 and r58, r58 an exception to r46.
  Answer: 2026-10-30: Reading (a), the recommended one, per the person's delegation of 2026-10-29 (answer every question with its recommended reading): change r46 to "...each answer of the capability-proposal that the drafts it applied do not hold and that no later answer of the same proposal replaces." and merge r58 into it. by: work run, under the delegation "The person, 2026-10-28: "i am delegating to you" and "I take recommendations"; 2026-10-29: answer every question with its recommended reading; questions of a glossary-proposal are the person's."
- Question: spec-integration r59 vs supervision r164. Line r59 (added): "When a round of the kind `gate` is started for a glossary-proposal, `initiative-round` shall ask only about the terms the glossary-proposal adds, changes and removes." supervision r164 (in spec) has `work run` ask the round only for those questions. Readings: (a) RECOMMENDED: keep r59, the round's side, beside r164, `work run`'s side (r168 and r35 are split the same way for capabilities); (b) drop r59 as given by r164.
  Answer: 2026-10-30: Reading (a): keep r59, the round's side, beside supervision r164, `work run`'s side, as r168 and r35 are split for capabilities (the person's delegation: answer with the recommended reading). by: work run, under the delegation "The person, 2026-10-28: "i am delegating to you" and "I take recommendations"; 2026-10-29: answer every question with its recommended reading; questions of a glossary-proposal are the person's."

Read (paths in your worktree):
- .shop/work/i61/spec-integration.md
- .shop/work/i61/runs/spec-integration/1-gate
- .shop/work/i61/runs/spec-integration/2-answer
- .shop/work/i61/runs/spec-integration/3-answer
- .shop/work/i61/runs/spec-integration/4-apply
- .shop/work/i61/runs/spec-integration/5-integrate
- .shop/work/i61/runs/spec-integration/5-integrate/drafts/round-1/

Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/spec-integration-6-gate/.shop/scratch/6-gate
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/spec-integration-6-gate/.shop/scratch/6-gate/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/spec-integration-6-gate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
