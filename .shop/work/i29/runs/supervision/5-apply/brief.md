# apply of supervision

Capability-proposal: .shop/work/i29/supervision.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: apply
Base: 4640ef08c740b5867638a4ae1f92e94d586c297c
Worktree: /tmp/work-run-i29-uk3_aing/supervision-5-apply
Branch: round/supervision-5-apply
Answers the person gave, each with the question it answers:
- Question: supervision r105, the term 'every raised request'. Line (added): [r105] When `work run` finds an initiative that is not `done`, whose every work-item is `green` or `withdrawn`, whose kept branch review lists nothing to fix now and whose every request kept in this context whose asker is this context and that names the initiative is `delivered`, `work run` shall set the initiative's status to `done`. Readings: (a) keep the wording, as work-queue r23 words it [recommended]; (b) 'every request that a round of the initiative raised'.
  Answer: 2026-10-25: 1: (a), keep the wording as work-queue r23 words it (the coordinator under the person's delegation 2026-10-25: "Do not involve me in fixing all of the bugs. Please get the system into a correctly working state before doing a release")
- Question: supervision r105, an initiative with no work-item. Line (added): r105 as above. As drafted it also fires for an initiative with none. Readings: (a) add 'that has at least one work-item' [recommended]; (b) as drafted.
  Answer: 2026-10-25: 2: (a), add 'that has at least one work-item' (the coordinator under the person's delegation 2026-10-25: "Do not involve me in fixing all of the bugs. Please get the system into a correctly working state before doing a release")
- Question: supervision r105 against r106 and the measure/analysis rounds, order. Line (added): r105 as above. An initiative set `done` first may never be measured or analysed (r66 skips `done`). Readings: (a) r105 adds 'and whose measurement and analysis record `work run` has committed' [recommended]; (b) as drafted.
  Answer: 2026-10-25: 3: (a), r105 adds 'and whose measurement and analysis record work run has committed' (the coordinator under the person's delegation 2026-10-25: "Do not involve me in fixing all of the bugs. Please get the system into a correctly working state before doing a release")
- Question: Commit of the `done` status. Concerns r105 and [r106] (added): When `work run` has written an initiative's measurement and its analysis record, `work run` shall commit them on the initiative branch. Readings: (a) add a line: 'When `work run` sets an initiative's status to `done`, `work run` shall commit the initiative on the initiative branch.' [recommended]; (b) add nothing.
  Answer: 2026-10-25: 4: (a), add the line committing the initiative when work run sets it done (the coordinator under the person's delegation 2026-10-25: "Do not involve me in fixing all of the bugs. Please get the system into a correctly working state before doing a release")
- Question: supervision r107, a capability the round adds. Line (added): [r107] If a change list that `work run` reads names a capability that `spec/capabilities/` does not have, then `work run` shall write no capability-proposal for it and exit with an error, naming the capability. Readings: (a) exempt it: '...neither `spec/capabilities/` nor the round's drafts have...' [recommended]; (b) refuse it too, as drafted.
  Answer: 2026-10-25: 5: (a), exempt a capability the round's drafts add (the coordinator under the person's delegation 2026-10-25: "Do not involve me in fixing all of the bugs. Please get the system into a correctly working state before doing a release")
- Question: supervision r107 and r92, what is written when one capability is missing. Line (added): r107 as above. Readings: (a) only the missing capability gets no proposal, r92 still writes the others, as drafted [recommended]; (b) none: '...shall write no capability-proposal for the change list and exit with an error, naming the capability.'
  Answer: 2026-10-25: 6: (a), only the missing capability gets no proposal; r92 still writes the others (the coordinator under the person's delegation 2026-10-25: "Do not involve me in fixing all of the bugs. Please get the system into a correctly working state before doing a release")

Read (paths in your worktree):
- .shop/work/i29/supervision.md
- .shop/work/i29/runs/supervision/1-gate
- .shop/work/i29/runs/supervision/2-answer
- .shop/work/i29/runs/supervision/3-answer
- .shop/work/i29/runs/supervision/4-answer

Run directory: /tmp/work-run-i29-uk3_aing/supervision-5-apply/.shop/scratch/5-apply
Result file: /tmp/work-run-i29-uk3_aing/supervision-5-apply/.shop/scratch/5-apply/result.json

You start in your worktree, /tmp/work-run-i29-uk3_aing/supervision-5-apply: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
