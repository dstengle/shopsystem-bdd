# formulate of work-queue

Capability-proposal: .shop/work/i25/work-queue.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: formulate
Base: f582b1bb522f819e5b2c7ff1d38707beafcc63fe
Worktree: /tmp/work-run-i25-3zfrxbbu/work-queue-3-formulate
Branch: round/work-queue-3-formulate
Answers the person gave, each with the question it answers:
- Question: work-queue r26/r27, no flag on a reviewer's question: what does `work answer` do with neither flag? Lines drafted (work-queue): changed r14, now "**When** `work answer <work-item> <answer>` is run on an `awaiting-answer` work-item whose question a researcher, a planner or an implementer asked, `work` shall transition it to the status the stage that asked its question started from: `drafted` for a researcher's question, `researched` for a planner's and `ready` for an implementer's." (was the same line without 'a researcher, a planner or an implementer asked' and ending "..., `ready` for an implementer's and `done` for a reviewer's."); added r26 "**When** `work answer <work-item> <answer>` is run, with the flag saying that the answer asks for a change, on an `awaiting-answer` work-item whose question a reviewer asked, `work` shall transition the work-item to `ready`."; added r27 "**When** `work answer <work-item> <answer>` is run, with the flag saying that the answer accepts the work-item as it is, on an `awaiting-answer` work-item whose question a reviewer asked, `work` shall transition the work-item to `done`." Readings: (a) RECOMMENDED, refuse (the note gives no default): new line "**If** `work answer <work-item> <answer>` is run without the flag saying whether the answer asks for a change or accepts the work-item as it is on an `awaiting-answer` work-item whose question a reviewer asked, then `work` shall exit with an error, saying that the answer must say which, and change nothing." (b) accept by default: r27 becomes "**When** `work answer <work-item> <answer>` is run, without the flag saying that the answer asks for a change, on an `awaiting-answer` work-item whose question a reviewer asked, `work` shall transition the work-item to `done`."
  Answer: 2026-10-25: 1: (a), refuse: work answer without the flag on a reviewer's question exits with an error saying the answer must say which, and changes nothing (the coordinator under the person's delegation 2026-10-25)
- Question: work-queue, the flag given on a work-item whose question a researcher, planner or implementer asked (r14 sends those to drafted, researched, ready). Readings: (a) RECOMMENDED, the flag is ignored and r14 holds; no new line. (b) refuse: "**If** `work answer <work-item> <answer>` is run with the flag saying whether the answer asks for a change or accepts the work-item as it is on a work-item whose question a reviewer did not ask, then `work` shall exit with an error, saying that the flag is for a reviewer's question, and change nothing."
  Answer: 2026-10-25: 2: (a), the flag is ignored on a researcher's, planner's or implementer's question and r14 holds; no new line (the coordinator under the person's delegation 2026-10-25)
- Question: supervision r98, added: "**When** `work run` starts an implementer for a work-item that an answer to a reviewer's question returned to `ready`, `work run` shall give the implementer the reviewer's findings and the answer." Two decisions. How the findings are given: (a) RECOMMENDED, the brief names the findings file; Implementation line "r98: the brief names the findings file of the work-item's last review stage directory and writes the answer as r57 does."; (b) the findings' text is written into the brief, r98 reading "... `work run` shall write the reviewer's findings and the answer in the implementer's brief." Whose reviewer: (i) RECOMMENDED, only a work-item's reviewer (a branch review's findings get a new work-item under r74), r98 reading "**When** `work run` starts an implementer for a work-item that an answer to the question of a work-item's reviewer returned to `ready`, `work run` shall give the implementer the reviewer's findings and the answer."; (ii) any reviewer, as drafted.
  Answer: 2026-10-25: 3: (a) the brief names the findings file, and (i) only a work-item's reviewer, as answered on i25/supervision (the coordinator under the person's delegation 2026-10-25)
- Question: work-queue r26/r27, the form of the flag (`--change` / `--accept`): (a) RECOMMENDED, it stays an Implementation line as drafted ("r26, r27: the flag is `--change` for an answer that asks for a change and `--accept` for one that accepts the work-item as it is; the answer stays one line of free text."); (b) it is Behaviour: r26 reads "**When** `work answer <work-item> <answer> --change` is run on an `awaiting-answer` work-item whose question a reviewer asked, `work` shall transition the work-item to `ready`." and r27 the same with `--accept` and `done`.
  Answer: 2026-10-25: 4: (a), the flag's form --change / --accept stays an Implementation line as drafted (the coordinator under the person's delegation 2026-10-25)

Read (paths in your worktree):
- .shop/work/i25/work-queue.md
- .shop/work/i25/runs/work-queue/1-gate
- .shop/work/i25/runs/work-queue/2-apply

Run directory: /tmp/work-run-i25-3zfrxbbu/work-queue-3-formulate/.shop/scratch/3-formulate
Result file: /tmp/work-run-i25-3zfrxbbu/work-queue-3-formulate/.shop/scratch/3-formulate/result.json

You start in your worktree, /tmp/work-run-i25-3zfrxbbu/work-queue-3-formulate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
