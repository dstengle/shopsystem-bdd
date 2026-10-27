# apply of supervision

Capability-proposal: .shop/work/i41/supervision.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/.shop/scratch/runner/scripts
Kind: apply
Give the change list of what you applied in your result's `changes`: a list with one entry for each capability, each `{"capability": <name>, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `<capability>#r<n>` or `term/<term>`.
Drafts path: .shop/work/i41/runs/i41/1-integrate/drafts/round-1/
Base: c2cbb99c64349b57b8c56ef45808f0c7537b3861
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/supervision-2-apply
Branch: round/supervision-2-apply
Answers the person gave, each with the question it answers:
- Question: r147 and r132: r147 (added) reads: "**When** a round of the kind `apply` applies nothing because a capability-proposal's answers give what its drafts do not hold, `work run` shall take that as the round's output." r132 (existing, unchanged by these drafts) lists "an integrate or apply round's change list" as a stage's output, so an apply round's output would have two readings. Reading A (recommended): r147 stays and extends r132's list, r132 unchanged. Reading B: retire r132 and add a line reading "an integrate round's change list; an apply round's change list, or its finding that it applies nothing because the capability-proposal's answers give what its drafts do not hold", the rest as r132.
  Answer: 2026-10-27: r147 and r132: Reading A, recommended: r147 stays and extends r132's list, r132 unchanged (answered by the coordinator under the person's delegation of 2026-10-27).
- Question: r148 and r92: r148 (added) reads: "**When** a round of the kind `integrate` drafts a capability-proposal anew from its answers, `work run` shall write no second capability-proposal for that proposal's capability." r92 says an integrate round's change list gets a `drafted` capability-proposal for each capability it names. Reading A (recommended): r92 stays and r148 is the exception for a round started for a capability-proposal (r140). Reading B: retire r92 and add "**When** a round of the kind `integrate` that `work run` started for an initiative, not for a capability-proposal, ends with a change list, `work run` shall write a `drafted` capability-proposal for each capability the change list names, with the requirement ids and terms it adds, changes and removes on that capability."
  Answer: 2026-10-27: r148 and r92: Reading A, recommended: r92 stays and r148 is the exception for a round started for a capability-proposal (r140) (answered by the coordinator under the person's delegation of 2026-10-27).
- Question: r142 gives two responses. r142 (added) reads: "**When** a round of the kind `integrate` drafts a capability-proposal anew from its answers, `work run` shall set the capability-proposal `drafted`, its earlier drafts kept in their round's directory." Reading A (recommended): split it; r142 becomes "... `work run` shall set the capability-proposal `drafted`." and a new line is added: "**When** a round of the kind `integrate` drafts a capability-proposal anew from its answers, `work run` shall keep the proposal's earlier drafts in their round's directory." Reading B: r142 stays as drafted.
  Answer: 2026-10-27: r142: Reading B, r142 stays as drafted. Reading A adds a line the drafts do not hold, which this proposal's apply round cannot apply until the redrafting it brings in exists (the trap of i40); the split may follow later (answered by the coordinator under the person's delegation of 2026-10-27).

Read (paths in your worktree):
- .shop/work/i41/supervision.md
- .shop/work/i41/runs/supervision/1-gate
- .shop/work/i41/runs/i41/1-integrate/drafts/round-1/

Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/supervision-2-apply/.shop/scratch/2-apply
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/supervision-2-apply/.shop/scratch/2-apply/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/supervision-2-apply: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
