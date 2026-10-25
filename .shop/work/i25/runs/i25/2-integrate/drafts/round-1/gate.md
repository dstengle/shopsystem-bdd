# Gate: q2, round 1

## work-queue

Changed:
- [r14] **When** `work answer <work-item> <answer>` is run on an `awaiting-answer` work-item whose question a researcher, a planner or an implementer asked, `work` shall transition it to the status the stage that asked its question started from: `drafted` for a researcher's question, `researched` for a planner's and `ready` for an implementer's.
  Was: [r14] **When** `work answer <work-item> <answer>` is run on an `awaiting-answer` work-item, `work` shall transition it to the status the stage that asked its question started from: `drafted` for a researcher's question, `researched` for a planner's, `ready` for an implementer's and `done` for a reviewer's.

Added:
- [r26] **When** `work answer <work-item> <answer>` is run, with the flag saying that the answer asks for a change, on an `awaiting-answer` work-item whose question a reviewer asked, `work` shall transition the work-item to `ready`.
- [r27] **When** `work answer <work-item> <answer>` is run, with the flag saying that the answer accepts the work-item as it is, on an `awaiting-answer` work-item whose question a reviewer asked, `work` shall transition the work-item to `done`.

Implementation line added: r26, r27: the flag is `--change` for an answer that asks for a change and `--accept` for one that accepts the work-item as it is; the answer stays one line of free text.

## supervision

Added:
- [r98] **When** `work run` starts an implementer for a work-item that an answer to a reviewer's question returned to `ready`, `work run` shall give the implementer the reviewer's findings and the answer.

## Glossary, decisions

None.

## Questions

1. work-queue, no flag on a reviewer's question: what does `work answer` do with neither flag?
   (a) recommended (the note gives no default): refuse. Line: "**If** `work answer <work-item> <answer>` is run without the flag saying whether the answer asks for a change or accepts the work-item as it is on an `awaiting-answer` work-item whose question a reviewer asked, then `work` shall exit with an error, saying that the answer must say which, and change nothing."
   (b) acceptance by default: r27 becomes "... is run without the flag saying that the answer asks for a change ...".
2. work-queue, flag on another stage's question:
   (a) recommended: the flag is ignored and r14 holds; no new line.
   (b) refuse: "**If** `work answer <work-item> <answer>` is run with the flag saying whether the answer asks for a change or accepts the work-item as it is on a work-item whose question a reviewer did not ask, then `work` shall exit with an error, saying that the flag is for a reviewer's question, and change nothing."
3. supervision r98, what "the reviewer's findings" are and how they are given:
   (a) the brief names the findings file; Implementation line "r98: the brief names the findings file of the work-item's last review stage directory and writes the answer as r57 does." (recommended)
   (b) the findings' text is written into the brief; r98 reworded "... `work run` shall write the reviewer's findings and the answer in the implementer's brief."
   Also: r98 covers only a work-item's reviewer (recommended; a branch review's findings get a new work-item under r74), so r98 would read "... an answer to the question of a work-item's reviewer returned to `ready` ..."; or any reviewer as drafted.
4. The flag's form (`--change` / `--accept`): Implementation as drafted (recommended), or Behaviour, r26 and r27 reading "**When** `work answer <work-item> <answer> --change` is run on ..." and "... `--accept` ...".
