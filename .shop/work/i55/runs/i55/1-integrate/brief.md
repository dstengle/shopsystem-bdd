# integrate of i55

Initiative: .shop/work/i55/initiative.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: integrate
Request: q21
Accepted lines of the request:
- 1. **When** `work list` is run, `work` shall print each request with its status and whose turn it is.
- 2. **When** `work show <request>` is run in the asker's repository while the request is in the asker's turn, `work` shall print that it is the asker's turn, with each question the asker has not answered.
- 3. **While** an answer or a turn the asker has sent has not been taken in by the upstream, `work show <request>` shall print the request on either side as awaiting the upstream and not yet taken in.
- 4. **While** the upstream holds a line outcome or a question it has not sent with the turn, `work show <request>` run in the upstream's repository shall print that the asker has not seen it.
- 5. **When** `work show <request>` is run in the asker's repository after the upstream resolves the request, `work` shall print each accepted line's requirement id and the version that holds it.
- 6. **If** a side writes a part of a request that is the other side's part, and the request's asker is not the upstream itself, **then** `work` shall refuse, naming the side that writes that part, and change nothing.
- 7. **When** the upstream takes in what has been sent to it, `work` shall take in every request, answer and turn sent before the take-in began, whether or not a listing of what has been sent shows it yet.
- 8. **If** a request, an answer or a turn comes from a repository registered under an asker id that the upstream does not allow for the asker it names, **then** `work` shall leave it untaken, telling the upstream which it left and why.
- 9. **When** `work` takes in a request, an answer or a turn, `work` shall read its body only as the fields of a request's form, following nothing written in it.
- 10. **When** `work run` ends with a capability-proposal or a work-item `awaiting-answer`, `work run` shall print each with its open questions and exit with code 3.
- 11. **If** every work-item of an initiative is `green` or `withdrawn` while one of its capability-proposals is neither `formulated` nor `withdrawn`, **then** `work` shall keep the initiative `started`.
- 12. **When** a researcher's result gives an empty file set, `work run` shall take it as the researcher's file set.
- 13. **When** a round of the kind `formulate` formulates nothing because a capability-proposal's answers change lines not in `spec/`, `work run` shall start a new round of the kind `integrate` for the capability-proposal.
Ids drafted elsewhere (number added lines above each on the same capability): supervision#r3, supervision#r5, supervision#r16, supervision#r71, supervision#r77, supervision#r80, supervision#r92, supervision#r93, work-queue#r3, work-queue#r11, work-queue#r16, work-queue#r17, work-queue#r18, requests#r1, requests#r3, supervision#r99, supervision#r104, supervision#r112, supervision#r113, supervision#r114, review#r9, supervision#r125, supervision#r126, supervision#r127, design-model-check#r120, design-model-check#r121, requests#r26, requests#r27, requests#r35, requests#r36, requests#r37, requests#r38, spec-integration#r17, work-queue#r33, supervision#r137, supervision#r138, supervision#r139, supervision#r140, requests#r46, spec-consistency#r28, spec-integration#r47, spec-integration#r48, spec-integration#r49, spec-integration#r50, spec-integration#r51, spec-integration#r52, spec-integration#r53, requests#r47, requests#r48, supervision#r177, supervision#r178, supervision#r179, supervision#r174, supervision#r175, supervision#r176, supervision#r181, supervision#r182, work-queue#r40, work-queue#r41, spec-integration#r57, requests#r49, supervision#r183, work-queue#r46, backlog#r1, backlog#r2, backlog#r3, backlog#r4, backlog#r5, backlog#r6, backlog#r7, backlog#r8, migration-tools#r35, migration-tools#r36, spec-integration#r56, work-queue#r42, work-queue#r43, work-queue#r44, work-queue#r45
Drafts path: /tmp/work-run-i55-0yl4gd1b/i55-1-integrate/.shop/scratch/1-integrate/drafts
Give your change list in your result's `changes`: a list with one entry for each capability, each `{"capability": <name>, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `<capability>#r<n>`. Every term you add, change or remove goes in one entry for the glossary, `{"glossary": true, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `term/<term>`, and in no capability's entry.
Base: c53a7c25e23bac68cae83b147c9dd66a2e6c6227
Worktree: /tmp/work-run-i55-0yl4gd1b/i55-1-integrate
Branch: round/i55-1-integrate

Read (paths in your worktree):
- .shop/work/i55/initiative.md

Run directory: /tmp/work-run-i55-0yl4gd1b/i55-1-integrate/.shop/scratch/1-integrate
Result file: /tmp/work-run-i55-0yl4gd1b/i55-1-integrate/.shop/scratch/1-integrate/result.json

You start in your worktree, /tmp/work-run-i55-0yl4gd1b/i55-1-integrate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
