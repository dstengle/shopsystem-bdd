# apply of supervision

Capability-proposal: .shop/work/i39/supervision.md
Agent: initiative-round
Scripts: /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.26.0/scripts
Kind: apply
Give the change list of what you applied in your result's `changes`: a list with one entry for each capability, each `{"capability": <name>, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `<capability>#r<n>` or `term/<term>`.
Drafts path: .shop/work/i39/runs/i39/1-integrate/drafts/round-1/
Base: b4c4ad5e86f831f3aedb0695974552aed3ba6064
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/supervision-2-apply
Branch: round/supervision-2-apply
Answers the person gave, each with the question it answers:
- Question: Delegation when the request the initiative fulfils gives none. Concerns line [r135] (new): "**When** a round of the kind `integrate` that `work run` started gives the lines of a request into an upstream, `work run` shall raise them with `work request`, raised for the request the initiative fulfils and with that request's delegation." Readings: (a) add "[r137] **Where** the request an initiative fulfils gives no delegation, **when** a round of the kind `integrate` gives the lines of a request into an upstream, `work run` shall raise them with no delegation." (recommended); (b) add a line that `work run` raises nothing and writes a question for the person under the initiative's ledger. Until you choose, r135 and the new line [r136] ("**While** a request that an initiative raised into an upstream is not `delivered`, `work run` shall draft no work-item for the capability-proposal whose lines it raised.") stand with no line for the no-delegation case.
  Answer: 2026-10-27: r135: a delegation always passes upstream as a flag; the upstream decides what to do with that fact ('I did this under delegation' is not 'we are all supposed to do this under delegation'). Whether a shop repo acts on a delegation is a setting of that repo, on to start with.

Read (paths in your worktree):
- .shop/work/i39/supervision.md
- .shop/work/i39/runs/supervision/1-gate
- .shop/work/i39/runs/i39/1-integrate/drafts/round-1/

Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/supervision-2-apply/.shop/scratch/2-apply
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/supervision-2-apply/.shop/scratch/2-apply/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/supervision-2-apply: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
