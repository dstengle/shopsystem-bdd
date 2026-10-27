# formulate of design-model-check

Capability-proposal: .shop/work/i39/design-model-check.md
Agent: initiative-round
Scripts: /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.26.0/scripts
Kind: formulate
Base: b4c4ad5e86f831f3aedb0695974552aed3ba6064
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/design-model-check-3-formulate
Branch: round/design-model-check-3-formulate
Answers the person gave, each with the question it answers:
- Question: design-model-check r120, r121 against table rows r115 (v17) and r117 (v18). Lines: [r120] **When** `model check` reads a request whose `part_of` names a job-thread kept in another repository, `model check` shall print no `v17` for the request. [r121] **When** `model check` reads a request raised for a request of another context, `model check` shall print neither `v17` nor `v18` for the request. Readings: (a) as drafted, standalone lines that override the rows for these requests (recommended, since the lines are what q14 accepted); (b) the rows change instead: "| [r115] | v17 | a request neither is part of a job-thread, cites an origin nor is raised for a request |" and "| [r117] | v18 | ... judged from the id alone, other than the request a request is raised for |", with lines 8 and 9 citing them.
  Answer: 2026-10-27: r120, r121: no requirement edits or overrides another. Rows r115 (v17) and r117 (v18) are retired and replaced by new rows with new ids covering q14 lines 8 and 9; r120 and r121 are dropped. Also folded in: a retired requirement is a node labelled retired, not returned by queries about the current spec; closed records (a delivered request, a done work-item, a merged, formulated or withdrawn proposal, ledgers, decisions, measurements) may name one; the current spec (scenario tags, live lines and rows) and open work naming one is an error; v3 becomes a resolution naming a requirement that never existed.

Read (paths in your worktree):
- .shop/work/i39/design-model-check.md
- .shop/work/i39/runs/design-model-check/1-gate
- .shop/work/i39/runs/design-model-check/2-apply

Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/design-model-check-3-formulate/.shop/scratch/3-formulate
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/design-model-check-3-formulate/.shop/scratch/3-formulate/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/design-model-check-3-formulate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
