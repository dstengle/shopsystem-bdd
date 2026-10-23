# research of w109

Work-item: .shop/work/i23-faster-batches-and-a-clean-model-check/w109.md
Agent: code-scout
Scripts: /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.24.0/scripts
Base: 1ad628182e2dd2eb91d1e0ed6e95ecb34f3bcc63
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/w109-1-research
Branch: none (a detached checkout)
Work-item branch: work/w109
Accepted scenarios:
- features/supervision.feature: `work run` pulls each work-item through research, plan, implementation and review, one worker at a time, until no work-item can make a transition (deprecated)
- features/supervision.feature: `work run` pulls each work-item through research, plan, implementation and review until no work-item can make a transition
- features/supervision.feature: when more than one work-item is drafted or researched, their research and plan stages are started at the same time
- features/supervision.feature: `work run` runs at most <limit> workers at the same time when .shop/delivery.toml <gives>
- features/supervision.feature: each stage's session.json records the path of the transcript of that stage's session
- features/supervision.feature: two ready work-items whose claims would not share a file are implemented at the same time, and merged one at a time (deprecated)
- features/supervision.feature: two ready work-items whose claims would share no file are implemented at the same time, each in its own worktree
- features/supervision.feature: two ready work-items whose claims would share a file are implemented one after the other: <how>
- features/supervision.feature: of three ready work-items whose claims would not share a file, no more than two are implemented at the same time (deprecated)
- features/supervision.feature: of three ready work-items whose claims would share no file, no more are implemented at the same time than .shop/delivery.toml's number of workers
- features/supervision.feature: implementers working at the same time that end with DONE have their branches merged one at a time, in the order they ended
- features/supervision.feature: no worker is started for a work-item whose blocked_by names a work-item that is not green

Read (paths in your worktree):
- .shop/work/i23-faster-batches-and-a-clean-model-check/w109.md
- spec/capabilities/supervision.md

Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/w109-1-research/.shop/scratch/1-research
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/w109-1-research/.shop/scratch/1-research/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/w109-1-research: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
