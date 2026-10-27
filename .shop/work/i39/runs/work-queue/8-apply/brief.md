# apply of work-queue

Capability-proposal: .shop/work/i39/work-queue.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/.shop/scratch/runner/scripts
Kind: apply
Give the change list of what you applied in your result's `changes`: a list with one entry for each capability, each `{"capability": <name>, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `<capability>#r<n>` or `term/<term>`.
Drafts path: .shop/work/i39/runs/work-queue/5-integrate/drafts/round-1/
Base: b4c4ad5e86f831f3aedb0695974552aed3ba6064
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/work-queue-8-apply
Branch: round/work-queue-8-apply
Answers the person gave, each with the question it answers:
- Question: Approve the added work-queue line [r33] (new, under spec/capabilities/work-queue.md): "**While** a request that an initiative raised into an upstream is not `delivered`, `work status` shall print the initiative as waiting on that request." It pairs with supervision r136, which holds back work-items for the capability-proposal while the request is not delivered. Readings: (A) approve the line as drafted [recommended]; (B) drop it, so `work status` says nothing about such a wait; (C) reword it, in which case give the wording.
  Answer: 2026-10-27: r33: Reading (C), reworded to name the consolidated list action that replaces work status. Also folded in: work show and work status are consolidated into one action listing all work with its status and one showing the detail of an individual item.
- Question: Approve work-queue adds r34-r39 and removes r3, r11, r16, r17, r18, with decision 0072 (spec/decisions/0072-work-list-and-work-show-replace-work-status.md: `work status` and `work show` consolidated into `work list` and `work show <id>`, `work status` retired; source: the retired and new ids and design-decision/the-context-runs-without-a-coordinator; by: the person's answers of 2026-10-27)? Added lines: - [r34] **When** `work list` is run, `work` shall print each initiative, each request and each work-item under `.shop/work/` with its status. - [r35] **Where** `--json` is given, `work list` shall print its result, each initiative, request and work-item with its status, as one JSON object. - [r36] **When** `work show <initiative>` is run, `work` shall print the initiative's status, each of its capability-proposals with its status, each of its work-items with its status and its open questions, the initiative branch and whether the remote has every commit of it, each tracked file of the checkout with uncommitted changes and each untracked file of the checkout that git does not ignore, the last ten lines of the initiative's ledger, and the ledger's last line whose note, the text given to `work note` after the date `work note` writes, begins `next:`. - [r37] **When** `work show <work-item>` is run, `work` shall print the work-item's status and its open questions. - [r38] **Where** `--json` is given, `work show` shall print its result as one JSON object. - [r39] **While** a request that an initiative raised into an upstream is not `delivered`, `work list` shall print the initiative as waiting on that request. (replaces the earlier draft r33, never in spec/) Removed (retired): r3 (work show prints each work-item with its status), r11 (work show --json), r16 (work status <initiative> detail, now r36), r17 (work status with no initiative), r18 (work status --json). Readings: (A) approve as drafted [recommended]; (B) approve with changes (give them); (C) refuse.
  Answer: 2026-10-27: Names: the consolidated actions are named: work list lists all work with its status (initiatives, requests and work-items); work show <id> shows the detail of one initiative, request or work-item; work status is retired, its lines retired and replaced by lines naming work list or work show. r33 is retired and replaced by: '**While** a request that an initiative raised into an upstream is not `delivered`, `work list` shall print the initiative as waiting on that request.'
- Question: `work show <request>` has no line; r37 covers only a work-item. Readings: (A) add [r48] '**When** `work show <request>` is run, `work` shall print the request's status, whose turn it is, its lines with their line outcomes, its questions, its answers and its resolution.' and keep r37 [recommended]; (B) the detail of a work-item is more (fields, plan, stage directories), so r37 is replaced by a line naming them; (C) leave request and work-item detail to a later round.
  Answer: 2026-10-27: r33: superseded; r33 never entered spec/ and r39 replaces it, as the person's answer of 2026-10-27 has it (answered by the coordinator under the person's delegation of 2026-10-27).
- Question: work-queue r34 prints each request's status under `work list`, and requests r46 (in the requests proposal) prints the same with whose turn it is. Readings: (A) keep both as drafted; (B) retire r34 and add [r40] '**When** `work list` is run, `work` shall print each initiative and each work-item under `.shop/work/` with its status.' [recommended].
  Answer: 2026-10-27: r34-r39, removes r3 r11 r16 r17 r18, decision 0072: (A) approve as drafted, recommended (answered by the coordinator under the person's delegation of 2026-10-27).

Read (paths in your worktree):
- .shop/work/i39/work-queue.md
- .shop/work/i39/runs/work-queue/1-gate
- .shop/work/i39/runs/work-queue/2-apply
- .shop/work/i39/runs/work-queue/3-apply
- .shop/work/i39/runs/work-queue/4-apply
- .shop/work/i39/runs/work-queue/5-integrate
- .shop/work/i39/runs/work-queue/6-gate
- .shop/work/i39/runs/work-queue/7-gate
- .shop/work/i39/runs/work-queue/5-integrate/drafts/round-1/

Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/work-queue-8-apply/.shop/scratch/8-apply
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/work-queue-8-apply/.shop/scratch/8-apply/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/work-queue-8-apply: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
