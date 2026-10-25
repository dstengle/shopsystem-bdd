# research of w139

Work-item: .shop/work/i24-requests-and-the-context-loop/w139.md
Agent: code-scout
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: f890f2f134c30ab6fe6c80036cfd0d3e207e7d7d
Worktree: /tmp/work-run-i24-requests-and-the-context-loop-n2el5fjl/w139-2-research
Branch: none (a detached checkout)
Work-item branch: work/w139
Accepted scenarios:
- features/supervision.feature: when every work-item is green or withdrawn and the kept branch review lists nothing to fix now, `measure initiative` is run on the initiative
- features/supervision.feature: once `measure initiative` has written the initiative's measurement, a session of analyzing-a-batch writes its analysis record

Read (paths in your worktree):
- .shop/work/i24-requests-and-the-context-loop/w139.md
- spec/capabilities/supervision.md
- .shop/work/i24-requests-and-the-context-loop/runs/w139/1-research

Run directory: /tmp/work-run-i24-requests-and-the-context-loop-n2el5fjl/w139-2-research/.shop/scratch/2-research
Result file: /tmp/work-run-i24-requests-and-the-context-loop-n2el5fjl/w139-2-research/.shop/scratch/2-research/result.json

You start in your worktree, /tmp/work-run-i24-requests-and-the-context-loop-n2el5fjl/w139-2-research: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
