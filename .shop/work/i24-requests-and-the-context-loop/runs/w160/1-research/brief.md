# research of w160

Work-item: .shop/work/i24-requests-and-the-context-loop/w160.md
Agent: code-scout
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: f890f2f134c30ab6fe6c80036cfd0d3e207e7d7d
Worktree: /tmp/work-run-i24-requests-and-the-context-loop-tdnk4mdl/w160-1-research
Branch: none (a detached checkout)
Work-item branch: work/w160
Accepted scenarios:
- features/work-queue.feature: a command whose change leaves every work-item of an initiative green or withdrawn, and every request this context asked naming it delivered, sets the initiative to done
- features/work-queue.feature: retry that makes an initiative's last open work-item green again sets the initiative to done

Read (paths in your worktree):
- .shop/work/i24-requests-and-the-context-loop/w160.md
- spec/capabilities/work-queue.md

Run directory: /tmp/work-run-i24-requests-and-the-context-loop-tdnk4mdl/w160-1-research/.shop/scratch/1-research
Result file: /tmp/work-run-i24-requests-and-the-context-loop-tdnk4mdl/w160-1-research/.shop/scratch/1-research/result.json

You start in your worktree, /tmp/work-run-i24-requests-and-the-context-loop-tdnk4mdl/w160-1-research: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
