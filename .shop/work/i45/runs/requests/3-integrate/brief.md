# integrate of requests

Initiative: .shop/work/i45/requests.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: integrate
Request: q26
Accepted lines of the request:
- 1. The plugin shall give a skill for writing requirement lines to the `capability-writer` and to a session that writes a request's lines.
- 2. **When** `work request` takes a line that names an implementation detail or a term the glossary does not define, `work request` shall refuse the line, naming the word and why.
- 3. **When** a round of the kind `integrate` has drafted its lines, `initiative-round` shall check them against the lines of `spec/` for overlapping triggers, conflicting responses and catch-all triggers before the gate round starts.
- 4. The glossary shall define each event and each condition that a line's trigger names.
- 5. **When** a gate round finds a question whose readings differ only in wording that a convention of the spec settles, `initiative-round` shall take the reading the convention gives and note it in its result in place of asking.
- 6. **When** a round of the kind `integrate` gives a question with readings, `initiative-round` shall draft the lines of each reading.
- 7. The spec's format rules and the `capability-writer`'s instructions shall say that a changed line is retired and its replacement given a new id.
Ids drafted elsewhere (number added lines above each on the same capability): supervision#r3, supervision#r5, supervision#r16, supervision#r71, supervision#r77, supervision#r80, supervision#r92, supervision#r93, work-queue#r3, work-queue#r11, work-queue#r16, work-queue#r17, work-queue#r18, requests#r1, requests#r3, supervision#r99, supervision#r104, supervision#r112, supervision#r113, supervision#r114, review#r9, supervision#r125, supervision#r126, supervision#r127, design-model-check#r120, design-model-check#r121, requests#r26, requests#r27, requests#r35, requests#r36, requests#r37, requests#r38, spec-integration#r17, work-queue#r33, supervision#r137, supervision#r138, supervision#r139, supervision#r140, requests#r47, requests#r48, supervision#r177, supervision#r178, supervision#r179, supervision#r174, supervision#r175, supervision#r176, supervision#r181, supervision#r182, work-queue#r40, work-queue#r41, spec-integration#r57, supervision#r187, work-queue#r48, work-queue#r49, requests#r50, requests#r51, requests#r52, requests#r53, requests#r54, requests#r55, requests#r56, requests#r57, requests#r58, supervision#r184, supervision#r185, supervision#r186, work-queue#r47, requests#r49, supervision#r183, work-queue#r46, backlog#r1, backlog#r2, backlog#r3, backlog#r4, backlog#r5, backlog#r6, backlog#r7, backlog#r8, migration-tools#r35, migration-tools#r36, spec-integration#r56, work-queue#r42, work-queue#r43, work-queue#r44, work-queue#r45
Drafts path: /tmp/work-run-i45-7xftq6tl/requests-3-integrate/.shop/scratch/3-integrate/drafts
Give your change list in your result's `changes`: a list with one entry for each capability, each `{"capability": <name>, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `<capability>#r<n>`. Every term you add, change or remove goes in one entry for the glossary, `{"glossary": true, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `term/<term>`, and in no capability's entry.
Ledger: .shop/work/i45/ledger.md
Earlier drafts path (read only): .shop/work/i45/runs/i45/1-integrate/drafts/round-1/
Where an answer below asks for lines the request's accepted lines do not, draft those lines under the capabilities the answer names, each quoting the answer it comes from.
Base: 10e6a82ef18dc60fb3712e81236e2ea4da33a527
Worktree: /tmp/work-run-i45-7xftq6tl/requests-3-integrate
Branch: round/requests-3-integrate
Answers the person gave, each with the question it answers:
- Question: Q1 (requests r46): What does `work request` check for "an implementation detail or a term the glossary does not define"? Line concerned: [r46] **If** a line given to `work request` names an implementation detail or uses a word that is neither a glossary term nor a word of a Behaviour line under `spec/capabilities/`, **then** `work request` shall refuse the line, naming the word and why it is refused. (added). Readings: A (recommended, drafted): a word of a fixed list of implementation details, or a word that is neither a glossary term nor used in a Behaviour line under `spec/capabilities/` (r46 as above). B (stricter): any word that is not a glossary term: "**If** a line given to `work request` names an implementation detail or uses a word that is not a glossary term, **then** `work request` shall refuse the line, naming the word and why it is refused." (nearly every line refused unless ordinary words are exempt). C: implementation details only: "**If** a line given to `work request` names an implementation detail, **then** `work request` shall refuse the line, naming the word and why it is refused." Recommended: A.
  Answer: 2026-10-28: Q1, r46's check: reading A, a word of a fixed list of implementation details, or a word that is neither a glossary term nor used in a Behaviour line (answered by the person, 2026-10-28)
- Question: Q7 (requests r46): Which glossary does `work request` use, since it runs in the asker's repository with no checkout of the upstream's? Line concerned: [r46] **If** a line given to `work request` names an implementation detail or uses a word that is neither a glossary term nor a word of a Behaviour line under `spec/capabilities/`, **then** `work request` shall refuse the line, naming the word and why it is refused. (added). Readings: A (recommended): the upstream's glossary and `spec/capabilities/`: "...a word that is neither a term of the upstream's glossary nor a word of a Behaviour line under the upstream's `spec/capabilities/`..." (replaces r46's wording). B: the glossary and `spec/capabilities/` of the repository it runs in (r46 as drafted). Recommended: A.
  Answer: 2026-10-28: Q7, r46's glossary: reading A, the upstream's glossary and spec/capabilities/ (answered by the person, 2026-10-28)
- Question: Q12 (requests r46): Does "refuse the line" refuse the whole request? Line concerned: [r46] **If** a line given to `work request` names an implementation detail or uses a word that is neither a glossary term nor a word of a Behaviour line under `spec/capabilities/`, **then** `work request` shall refuse the line, naming the word and why it is refused. (added). Readings: A (recommended): yes, as r2: "..., **then** `work request` shall refuse, naming the word and why it is refused, and change nothing." (replaces r46's ending). B: only the line; the other lines are written: r46 as drafted, plus "**When** `work request` refuses a line, `work` shall write the request with its other lines." Recommended: A.
  Answer: 2026-10-28: Q12, r46 refusing a line: reading A, it refuses the whole request and changes nothing, as r2 (answered by the person, 2026-10-28)

Read (paths in your worktree):
- .shop/work/i45/requests.md
- .shop/work/i45/runs/requests/1-gate
- .shop/work/i45/runs/requests/2-apply
- .shop/work/i45/ledger.md
- .shop/work/i45/runs/i45/1-integrate/drafts/round-1/

Run directory: /tmp/work-run-i45-7xftq6tl/requests-3-integrate/.shop/scratch/3-integrate
Result file: /tmp/work-run-i45-7xftq6tl/requests-3-integrate/.shop/scratch/3-integrate/result.json

You start in your worktree, /tmp/work-run-i45-7xftq6tl/requests-3-integrate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
