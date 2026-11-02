# formulate of supervision

Capability-proposal: .shop/work/i62/supervision.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: formulate
Where the answers below change lines that are not in spec/, so that you formulate nothing, give in your result `nothing_formulated`, a sentence saying so, and no `questions`: `work run` then starts an integrate round for the proposal.
Base: 955ad466c30a8e870af65b406cdd4b241699f24e
Worktree: /tmp/work-run-i62-cldtsv95/supervision-14-formulate
Branch: round/supervision-14-formulate
Answers the person gave, each with the question it answers:
- Question: r213, "its question". Line (added): [r213] **If** the second run of a scenario that r212 makes also fails, **then** `work run` shall give both runs of the scenario in the question r131 writes for the work-item. Readings: (a, recommended, as drafted) the question r131 writes under the work-item's `## Questions`; (b) a question of its own: "[r213] **If** the second run of a scenario that r212 makes also fails, **then** `work run` shall write under the work-item's `## Questions` a question that gives both runs of the scenario and transition the work-item to `awaiting-answer`."
  Answer: 2026-10-30: Reading (a), as recommended and drafted: `work run` gives both runs of the scenario in the question r131 writes under the work-item's `## Questions`, per the person's delegation of 2026-10-28 and 2026-10-29 (answer every question with its recommended reading). by: work run, under the delegation "The person, 2026-10-28: "i am delegating to you" and "I take recommendations"; 2026-10-29: answer every question with its recommended reading; questions of a glossary-proposal are the person's."
- Question: r213, what "both runs" give. Line (added): [r213] **If** the second run of a scenario that r212 makes also fails, **then** `work run` shall give both runs of the scenario in the question r131 writes for the work-item. Readings: (a, recommended, as drafted) both runs, without saying what each gives; (b) each run with its command, how it ended and its output: "... give both runs of the scenario, each with its command, how it ended and its output, in the question r131 writes for the work-item."
  Answer: 2026-11-02: Reading (a), as recommended and drafted, on each open question: (2) both runs, without saying what each gives; (3) no line for a passing second run; (4) every failure that would refuse the merge gets one more run; (5) the second run is of that scenario by itself; (6) scenarios only, in both runs r4 makes. The ids r212 and r213 are already taken in spec/capabilities/supervision.md (it now goes to r218): the two lines take the next free ids, r219 and r220, the references between them renumbered to match (the person, 2026-11-02).
- Question: After a passing second run. Lines (added): r212 and r213 (q41 does not say the merge goes ahead). Readings: (a, recommended, as drafted) add no line; (b) add a line: "[r214] **When** the second run of a scenario that r212 makes passes, `work run` shall take the scenario as passing for r4's merge."
  Answer: 2026-11-02: (3) After a passing second run: reading (a), add no line (the person, 2026-11-02).
- Question: r212's condition. Line (added): [r212] **If** a scenario fails in a run that `work run` makes before a merge and its failure would keep r4 from merging the work-item branch, **then** `work run` shall run that scenario again once, alone, before it refuses the merge. Readings: (a, recommended, as drafted) every failure that would refuse the merge gets one more run; the rerun is how `work run` finds whether it repeats; (b) only failures `work run` can tell in advance are not the work-item's (q41 gives no list): "[r212] **If** a scenario fails in a run that `work run` makes before a merge, for a reason that `work run` takes as not caused by the work-item, **then** `work run` shall run that scenario again once, alone, before it refuses the merge."
  Answer: 2026-11-02: (4) r212's condition: reading (a), every failure that would refuse the merge gets one more run (the person, 2026-11-02).
- Question: r212, "alone". Line (added): r212 as in the previous question. Readings: (a, recommended, as drafted) the second run is of that scenario by itself; (b) the same run is made again: "[r212] **If** a scenario fails in a run that `work run` makes before a merge and its failure would keep r4 from merging the work-item branch, **then** `work run` shall make that run again once before it refuses the merge."
  Answer: 2026-11-02: (5) r212, alone: reading (a), the second run is of that scenario by itself (the person, 2026-11-02).
- Question: r212, reach. Line (added): r212 as above. Readings: (a, recommended, as drafted) scenarios only, in both runs r4 makes; (b) a failing non-scenario test of the suite gets a second run too: "[r212] **If** a scenario or test fails in a run ..."
  Answer: 2026-11-02: (6) r212, reach: reading (a), scenarios only, in both runs r4 makes (the person, 2026-11-02).
- Question: r219: Reading 1: the merge is refused whatever the second run gives; reading 2: refused only if the second run also fails, and a passing second run lets the merge go ahead.
  Answer: 2026-11-02: r219: reading 2. The merge is refused only if the second run also fails; a passing second run lets the merge go ahead. This replaces my earlier answer (3), 'add no line for a passing second run': r219 is to say so itself, or a further line beside it (the person, 2026-11-02).
- Question: r222, the line for a passing second run. Line (added): [r222] **When** the second run of a scenario that r219 makes passes, `work run` shall take the scenario as passing in r4's merge of the work-item branch. (You answered 2026-11-02: reading 2, a passing second run lets the merge go ahead; r219 is to say so itself, or a further line beside it.) Readings: (a, recommended, as drafted) a further line beside r219, r222 as above; r219 and r220, already in spec/, stay as they are; (b) r219 says it itself: r219 is retired and a new line takes its place, "**If** a scenario fails in a run that `work run` makes before a merge and its failure would keep r4 from merging the work-item branch, **then** `work run` shall run that scenario again once, alone, and refuse the merge only if the second run also fails.", with r220 reworded to name the new id.
  Answer: 2026-11-02: r222: reading (a), as recommended and drafted: a further line beside r219; r219 and r220 stay as they are (the person's delegation: answer every question with its recommended reading; 2026-11-02).

Read (paths in your worktree):
- .shop/work/i62/supervision.md
- .shop/work/i62/runs/supervision/1-gate
- .shop/work/i62/runs/supervision/10-formulate
- .shop/work/i62/runs/supervision/11-integrate
- .shop/work/i62/runs/supervision/12-gate
- .shop/work/i62/runs/supervision/13-apply
- .shop/work/i62/runs/supervision/2-answer
- .shop/work/i62/runs/supervision/3-answer
- .shop/work/i62/runs/supervision/4-answer
- .shop/work/i62/runs/supervision/5-answer
- .shop/work/i62/runs/supervision/6-answer
- .shop/work/i62/runs/supervision/7-answer
- .shop/work/i62/runs/supervision/8-apply
- .shop/work/i62/runs/supervision/9-formulate

Run directory: /tmp/work-run-i62-cldtsv95/supervision-14-formulate/.shop/scratch/14-formulate
Result file: /tmp/work-run-i62-cldtsv95/supervision-14-formulate/.shop/scratch/14-formulate/result.json

You start in your worktree, /tmp/work-run-i62-cldtsv95/supervision-14-formulate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
