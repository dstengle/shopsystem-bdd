# research of w198

Work-item: .shop/work/i37/w198.md
Agent: code-scout
Scripts: /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.26.0/scripts
Base: 94be81b4c7efa16e4b751858da00db485be242d1
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/w198-1-research
Branch: none (a detached checkout)
Work-item branch: work/w198
Accepted scenarios:
- features/supervision.feature: a kept branch review whose result gives <outcome> and no question is taken as listing nothing to fix now
- features/supervision.feature: when every work-item is green or withdrawn and the kept branch review lists nothing to fix now, `measure initiative` is run on the initiative (deprecated)
- features/supervision.feature: an initiative whose work-items are <work-items> and whose kept branch review lists nothing to fix now <measured>
- features/supervision.feature: an initiative whose work-items are green or withdrawn, whose branch review lists nothing to fix now, whose measurement and analysis record are committed and whose requests are delivered is set done (deprecated)
- features/supervision.feature: an initiative whose work-items are <work-items>, its delivery otherwise closed, <set>
- features/supervision.feature: under a delegation, the session answering a reviewer's question is asked to say in its result whether its answer asks for a change or accepts the work-item as it is

Read (paths in your worktree):
- .shop/work/i37/w198.md
- spec/capabilities/supervision.md

Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/w198-1-research/.shop/scratch/1-research
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/w198-1-research/.shop/scratch/1-research/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/w198-1-research: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
