# research of w181

Work-item: .shop/work/i29/w181.md
Agent: code-scout
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: 4640ef08c740b5867638a4ae1f92e94d586c297c
Worktree: /tmp/work-run-i29-dxw4y18k/w181-1-research
Branch: none (a detached checkout)
Work-item branch: work/w181
Accepted scenarios:
- features/supervision.feature: a change list naming a capability that neither spec/capabilities/ nor the round's drafts have gives no capability-proposal for it, and `work run` exits with an error naming it
- features/supervision.feature: the <kind> round of a capability-proposal is given the path of the kept drafts of the integrate round that wrote the proposal
- features/supervision.feature: once the initiative's measurement and analysis record are written, they are committed on the initiative branch
- features/supervision.feature: an initiative whose work-items are green or withdrawn, whose branch review lists nothing to fix now, whose measurement and analysis record are committed and whose requests are delivered is set done
- features/supervision.feature: an initiative set done is committed on the initiative branch

Read (paths in your worktree):
- .shop/work/i29/w181.md
- spec/capabilities/supervision.md

Run directory: /tmp/work-run-i29-dxw4y18k/w181-1-research/.shop/scratch/1-research
Result file: /tmp/work-run-i29-dxw4y18k/w181-1-research/.shop/scratch/1-research/result.json

You start in your worktree, /tmp/work-run-i29-dxw4y18k/w181-1-research: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
