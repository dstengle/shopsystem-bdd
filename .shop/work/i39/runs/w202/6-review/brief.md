# review of w202

Work-item: .shop/work/i39/w202.md
Agent: bdd-task-reviewer
Scripts: /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.26.0/scripts
Base: b4c4ad5e86f831f3aedb0695974552aed3ba6064
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/w202-6-review
Branch: none (a detached checkout)
Work-item branch: work/w202
Answers the person gave, each with the question it answers:
- Question: Important, skills/integrating-a-proposal/SKILL.md:59 (Question Template): asks the writer for request lines in the upstream's glossary terms while letting it read only spec/, features/ and docs/; the round-1 Template lacks it, and initiative-round.md has the round draft the lines itself
  Answer: 2026-10-27: A downstream writer uses whatever terminology it can; the upstream corrects the request to its own glossary terms. So the writer is not asked for request lines in the upstream's glossary terms and needs no access to the upstream's glossary. Publishing contracts and glossaries between contexts is left for later (observation 2026-10-27-published-contracts).

Read (paths in your worktree):
- .shop/work/i39/w202.md
- spec/capabilities/spec-integration.md
- .shop/work/i39/runs/w202/1-research
- .shop/work/i39/runs/w202/2-plan
- .shop/work/i39/runs/w202/3-implement
- .shop/work/i39/runs/w202/4-review
- .shop/work/i39/runs/w202/5-implement

Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/w202-6-review/.shop/scratch/6-review
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/w202-6-review/.shop/scratch/6-review/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/w202-6-review: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
