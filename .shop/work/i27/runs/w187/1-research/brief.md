# research of w187

Work-item: .shop/work/i27/w187.md
Agent: code-scout
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: 3cbd0c528b0bd62d10ca4b2453f47921f76c1c6e
Worktree: /tmp/work-run-i27-0cbctcft/w187-1-research
Branch: none (a detached checkout)
Work-item branch: work/w187
Accepted scenarios:
- features/supervision.feature: an initiative with no work-item gets no branch review, though its branch holds a commit no kept branch review has read
- features/supervision.feature: `work run` started with no initiative runs the integrate, apply and formulate rounds of different initiatives one at a time
- features/supervision.feature: an initiative with no work-item is not measured
- features/supervision.feature: `work run` started with no initiative takes every initiative that is neither done nor abandoned through its transitions, the initiatives side by side and one session of an initiative at a time
- features/supervision.feature: a started initiative with neither a capability-proposal nor a work-item is given to an integrate round with the accepted lines of the request it fulfils
- features/supervision.feature: an integrate round that ends DONE without a change list ends `work run` with an error naming the round
- features/supervision.feature: the drafts of an integrate round that <ending> are kept on the initiative branch
- features/supervision.feature: an integrate round's change list gives one drafted capability-proposal for each capability it names, with what it adds, changes and removes on that capability
- features/supervision.feature: the change lists of two initiatives that name the same capability give two drafted capability-proposals with different ids

Read (paths in your worktree):
- .shop/work/i27/w187.md
- spec/capabilities/supervision.md

Run directory: /tmp/work-run-i27-0cbctcft/w187-1-research/.shop/scratch/1-research
Result file: /tmp/work-run-i27-0cbctcft/w187-1-research/.shop/scratch/1-research/result.json

You start in your worktree, /tmp/work-run-i27-0cbctcft/w187-1-research: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
