# Where the gate's questions come from (i39–i43)

Read-only analysis. Sources: `.shop/work/i39..i43/*.md`, `ledger.md`; for i40–i42 the integrate `gate.md`, gate and apply `result.json` and briefs under `runs/`; for i39 the proposals and ledger only. **i43's `runs/` was not read**; its `review.md`, `supervision.md` and `ledger.md` were. Paths below are relative to `/home/vscode/shopsystem-bdd`. "W-Qn" means a question the integrate round's writer raised in `gate.md` that the gate then dropped.

## 1. The questions, classified

Cause key: 1 request wording · 2 existing spec wording · 3 glossary/term gap · 4 brief/instruction gap · 5 genuine decision.
Where a request wording triggered something a convention already settles, the primary cause is 4 and the trigger is noted.

### i43 (q23): review and supervision proposals, all under delegation

| # | Question | Cause | Wording that caused it | Wording that would have avoided it |
|---|---|---|---|---|
| 1 | r155 "how it exited" vs "exit code". Asked **twice**: `.shop/work/i43/review.md:18` and `.shop/work/i43/supervision.md:18`. Reading A (recommended) was taken. | 4 (trigger 1) | Request: "give the branch reviewer each one's command, **exit code** and output" (`.shop/work/requests/q23.md:13`). The writer already followed the convention, which settles it: "never with a named exit code … an exit or status code … are Implementation" (`agents/capability-writer.md:30`, `docs/capability-format.md:114`, decision 0055). | Gate rule: "do not ask about a wording that `docs/capability-format.md` or a design-decision settles; note it." Request: "how it exited". |
| 2 | r33: should the request's "Where" become "When"? (`review.md:19`). Reading A (recommended) was taken. | 4 (trigger 1) | "**Where** the branch reviewer finds a behaviour…" (`q23.md:17`) is an event, not a feature. "The pattern follows what starts the behaviour, not the note's wording" (`agents/capability-writer.md:29`, `docs/capability-format.md:99`). | The same gate rule. Request guidance: use `Where` only for an option or configuration. |
| 3 | r12 ("with its reproduction") against r32/r33 (`review.md:20`). The recommended "r12 stands" was taken. | 4 | The new line already names the exception: "…marked not run, **in place of a reproduction**" (`spec/capabilities/review.md:36`). | Gate rule: when a new line states its own exception to an existing line, do not ask. |
| 4 | r7 (suite wall time) against r32 (`review.md:21`). The recommended "r7 stands" was taken. | 2 | "the branch reviewer shall write in its findings the suite's wall time" (`spec/capabilities/review.md:39`) assumes the reviewer runs the suite. r155 gives "its output" without saying it holds timing. | The request could name the wall time with the suite run. Otherwise, a gate rule against asking when the recommended reading is "no change". |
| 5 | r6 (a check the reviewer "cannot verify" fails the branch review) against r32 (`review.md:22`). The recommended "stands" was taken. | 2 | "a check a work-item names that the reviewer cannot verify" (`spec/capabilities/review.md:31`) does not say how it verifies. | The same "no change → don't ask" rule. |
| 6 | Implementation line "Probes go in the scratch directory" (`review.md:23`). The recommended "keep" was taken. | 4 | Implementation lines are not gated: the glossary says "gate: the person's approval of Behaviour lines and glossary entries" (`spec/index.md:104`). The gate asked anyway. | Gate rule: do not ask about Implementation text. The writer words it. |
| 7 | Remove the branch reviewer's Bash tool, against r32 "runs nothing" (`review.md:24`). **Not** the recommended reading. | 5 | Request: "The branch reviewer shall run nothing" (`q23.md:16`) against design-decision/the-v3-agents. | — (a real choice; it became q24) |
| 8 | r156 "each with the work-item it belongs to or none". No reading was recommended. Appears in `review.md:25` and `supervision.md:19`; the formulate round raised it (`.shop/work/i43/ledger.md:7`), not the gate. | 3 | "each with the work-item it belongs to or none" (`q23.md:14`; `spec/capabilities/supervision.md:139`). No glossary entry says when a commit belongs to a work-item. `review.md:35` (r12) says "the work-item whose commits contain it", which is just as undefined. | A glossary entry, e.g. "**work-item's commits**: the commits made on its work-item branch, its merge, and the transitions `work run` commits for it". |

### i42 (q22)

| # | Question | Cause | Wording | Avoiding wording |
|---|---|---|---|---|
| 9 | spec-integration "approve as drafted?" (`.shop/work/i42/spec-integration.md:18`) | 5 (by design) | — | Under a delegation it could pass without a question. That is the person's choice. |
| 10 | r150 covers r140; retire r140? (`.shop/work/i42/supervision.md:18`). The recommended reading was taken. | 1 | q22 line 3, "**When** a round of the kind `apply` gives in its result an answer that the drafts it applied do not hold…" (`.shop/work/requests/q22.md:15`), widens r140 (q19 line 1) without naming it. | The request says "replaces supervision r140 (retired)", as q19's delegation did (`q19.md:8`). |
| 11 | r150 against r144–r146: a partial apply still counts as "having applied its drafts" (`supervision.md:19`). Recommended (b) was taken. | 2 | "ends **having applied its drafts**" (`spec/capabilities/supervision.md:62-64`) does not say whether a partial apply counts. | See Recommendation 4: a term for a redirecting result, and r144–r146 replaced to exclude it. |
| 12 | r149 against r83: a formulate round that formulates nothing is set `formulated` (`supervision.md:20`). The recommended reading was taken. | 2 | r83: "ends without giving a question" (`supervision.md:67`). | The same. |
| 13 | r149 against r131/r132: no output (`supervision.md:21`). The recommended reading was taken. | 2 | r132 is a closed list of outputs (`supervision.md:33`). Every new outcome needs a new line. | The same. |
| 14 | W-Q5: the formulation counterpart of r46 (`.shop/work/i42/runs/i42/1-integrate/drafts/round-1/gate.md:19`). The gate dropped it. | 4 (under-ask) | `scripts/supervise_brief.py:78-79`: "Ask questions only on the lines and terms listed above…" | See Recommendation 3. |
| — | apply round 2 applied nothing (`.shop/work/i42/ledger.md:7`; `runs/supervision/2-apply/result.json`). This caused a second integrate and gate. | 4 | The recommended readings of #11–#13 were "add r151…" lines that were never in the drafts. The writer may not draft a line the note does not give: "It is a question, with the line you would write" (`agents/capability-writer.md:31`). The apply round may apply only the drafts (`agents/initiative-round.md:34,37`). | See Recommendation 2. |
| 15 | Gate 4: r152 against r83 (`supervision.md:22`). The recommended "no change" was taken. | 4 (over-ask) | This repeats #12. The answer in the brief already decided it (`runs/supervision/4-gate/brief.md`, the answer to "r149 against r83"). | Gate rule: do not ask what an answer the brief gives already decides. |
| 16 | Gate 4: r150/r151 against r144/r145, keep status? (`supervision.md:23`). The recommended "meant" was taken. | 4 (over-ask) | This is option (c) of #11, which the answer already declined ("reading (b)", `supervision.md:27`). | The same rule. |

### i41 (q19)

| # | Question | Cause | Wording | Avoiding wording |
|---|---|---|---|---|
| 17 | r147 against r132 (`.shop/work/i41/supervision.md:18`). The recommended "r132 unchanged" was taken. | 2 | The closed output list in r132 (`spec/capabilities/supervision.md:33`). | Recommendation 4. |
| 18 | r148 against r92 (`supervision.md:19`). The recommended "r92 stays, r148 the exception" was taken. | 2 | r92: "**When** a round of the kind `integrate` that `work run` started ends with a change list…" (`spec/capabilities/supervision.md:46`) catches every integrate round. | Retire r92 and replace it with a line limited to rounds started for an initiative. This was reading B. |
| 19 | r142 gives two responses; split it? (`supervision.md:20`). **B (not recommended)** was taken, because A would add a line the apply round could not apply. | 1 | "…shall set the capability-proposal `drafted`, **its earlier drafts kept** in their round's directory" (`q18.md:16`, `q19.md:16`). This breaks "One 'shall', one response" (`docs/capability-format.md:104`). | One line per response in the request. |
| 20 | W-Q1: add glossary entries "capability-proposal", "drafts" and "change list" (`.shop/work/i41/runs/i41/1-integrate/drafts/round-1/gate.md:30`). The gate dropped it. | 3 | None of these terms is in `spec/index.md:88-139`, yet r92, r107, r108 and r132 use them. | Add the entries. See Recommendation 5. |
| 21 | W-Q5: give later gate and apply rounds the newest drafts? (`gate.md:34`). The writer's own answer was "No: r108 already says". | 4 | A confirmation question that the writer answered itself. | Gate rule: no confirmation questions. |

### i40 (q18)

| # | Question | Cause | Wording | Avoiding wording |
|---|---|---|---|---|
| 22 | Keep the proposal's status during the new integrate round? (`.shop/work/i40/supervision.md:18`). The recommended reading was taken. It led to an apply that applied nothing. | 1 | q18 has no line on the status (`q18.md:13-16`). | The request carries q19 line 4 (`q19.md:17`) from the start. |
| 23 | "The apply round gave no change list" (`supervision.md:19`), a fault question from r131. | 2 | r132: "an integrate or apply round's change list" (`spec/capabilities/supervision.md:33`). | The same as #13. |
| 24 | spec-integration "approve as drafted?" (`.shop/work/i40/spec-integration.md:18`) | 5 (by design) | — | — |
| 25 | W-Q1: r80/r71/r114 fire on every apply (`.shop/work/i40/runs/i40/1-integrate/drafts/round-1/gate.md:20-21`). The gate **dropped** it (`runs/supervision/1-gate/result.json`, "outside this brief's adds"). It came back as q19 lines 5–7 and a whole initiative, i41 (`q19.md:8`). | 2 (lost by 4) | r80/r71/r114: "…**ends**, `work run` shall…" (`gate.md:35`). | Recommendations 3 and 4. |
| 26 | W-Q2: the output of an apply round that applies nothing, r131/r132 (`gate.md:23-25`). Dropped; it became q19 line 8. | 2 (lost by 4) | r132 | The same. |
| 27 | W-Q4: r92 writes a second proposal (`gate.md:29-31`). Dropped; it became q19 line 9. | 2 (lost by 4) | r92 (`gate.md:34`) | The same. |
| 28 | W-Q5: "confirm r138's round is the one r137 starts (yes: no change)" (`gate.md:32`). | 4 | A confirmation question. | Gate rule: no confirmation questions. |

### i39 (q14): a sample of 14 questions, for patterns

| # | Question | Cause | Wording | Avoiding wording |
|---|---|---|---|---|
| 29 | requests r3 "changed", narrowed (`.shop/work/i39/requests.md:2`) | 5 (content); 4 (form) | The writer drafted a "changed" line keeping its id, as the instructions say ("A line you change keeps its id", `agents/capability-writer.md:22`; `docs/capability-format.md:162`). The person ruled the opposite (`.shop/work/i39/ledger.md:83-84`). | See Recommendation 4b. |
| 30 | r43 "contract's form" (`requests.md:3`) | 1 | "the fields of the contract's form" (`q14.md:22`; the number is q14's own line number) | Use the glossary's term, or leave it to the upstream. |
| 31 | term/carrier (`requests.md:6`) | 1 | "keep the carrier of a request behind one port, with a file … and an issue…" (`q14.md:2`). Storage was put into a line. | The person's own rule: storage and transport stay out of lines (ledger `:77`). |
| 32 | r41 allow list, where it is kept (`requests.md:5`) | 1 | "an identity the upstream does not allow" (`q14.md:20`) | The same. |
| 33 | r35–r38: which command shows the state (`requests.md:4`) | 2 | `work show` and `work status` overlapped (ledger `:78`). | The spec consolidation done in i39. |
| 34 | r25 "one set of commands", asked twice (`requests.md:7,10`) | 1 | "(raise, take in, give a line outcome, …) and one lifecycle" (`q14.md:1`) | Name the actions as the spec's commands, or leave the names to the upstream. |
| 35 | r33/r34: which side writes on an internal request (`requests.md:8`) | 5 | — | — |
| 36 | "message" is undefined (`requests.md:9`) | 3 | "a request or a message" (`q14.md:18,20,22`) | A glossary entry. |
| 37 | supervision r135: delegation passes upstream (`.shop/work/i39/supervision.md:18`) | 5 | — | — |
| 38 | r136: which proposals are held. No reading was recommended (`supervision.md:19`). The formulate round raised it. | 4 | The answer quotes the request, which already said it: "the capability-proposal whose lines it raised" (`q14.md:25`). | The request already settled it. |
| 39 | spec-integration r44: how the index names an upstream (`.shop/work/i39/spec-integration.md:41`). The recommended "Implementation only" was taken. | 4 | A format or implementation question. | The convention: format is Implementation (`agents/capability-writer.md:30`). |
| 40 | design-model-check r120/r121 against rows r115/r117 (`.shop/work/i39/design-model-check.md:62`) | 4 | The writer drafted standalone lines that "override the rows". The person: "no requirement edits or overrides another" (ledger `:67,:81`). No instruction says so. | Recommendation 4b. |
| 41 | r121 (v18), two readings, asked twice (`design-model-check.md:63-64`). Formulation raised it. | 1 | "a request raised for a request of another context" (`q14.md:9`) | — |
| 42 | work-queue r33 approve/reword (`.shop/work/i39/work-queue.md:18`) | 2 | `work status`/`work show` overlap | — |

i39 also had apply rounds that applied nothing three times (`.shop/work/i39/ledger.md:94,99,100`), from the same cause as Recommendation 2.

## 2. Counts (42 rows)

| Cause | Rows | i40–i43 only |
|---|---|---|
| 1 request wording | 8 (#10, 19, 22, 30, 31, 32, 34, 41) | 3 |
| 2 existing spec wording | 13 (#4, 5, 11, 12, 13, 17, 18, 23, 25, 26, 27, 33, 42) | 11 |
| 3 glossary/term gap | 3 (#8, 20, 36) | 2 |
| 4 brief/instruction gap | 12 (#1, 2, 3, 6, 14, 15, 16, 21, 28, 38, 39, 40) | 9 |
| 5 genuine decision | 6 (#7, 9, 24, 29, 35, 37), of which 2 are bare "approve as drafted" | 3 |

Plus apply rounds that applied nothing: i40 ×1, i42 ×1, i39 ×3. All have cause 4 (Recommendation 2).

Of the 28 questions in i40–i43, only 3 are genuine, and two of those are plain approvals.

## 3. Recommendations (ranked by questions or rounds avoided)

### 1. Gate rule: decide and note, don't ask

Change `scripts/supervise_brief.py:74-79` and `agents/initiative-round.md:32`, and the writer's `agents/capability-writer.md:74`. Proposed text:

> "Do not ask a question when (a) its recommended reading is 'no change', 'as drafted', 'stands' or 'meant'; (b) `docs/capability-format.md` or a design-decision settles it (EARS keyword, exits in words, Implementation wording); (c) an answer this brief gives already decides it; (d) it only confirms. Write such cases under 'Decided without asking' in the result, with the convention or answer that settles each."

- **Would remove 15 asks:** #1 (×2), 2, 3, 4, 5, 6, 15, 16, 17, 18, 21, 28, 38, 39.
- **Caveat that needs the person:** readings like "r148 is the exception to r92" or "r152 is the exception to r83" (#15, #17, #18) conflict with the person's i39 ruling that "no requirement edits or overrides another" (`.shop/work/i39/ledger.md:67,81`). Under delegation the coordinator took the "exception" readings anyway. The person should decide once which holds:
  - if a specific line may stand as an exception, rule (a) holds;
  - if not, the integrate round should draft the retire-and-replace of the general line itself, not ask.

### 2. Draft the recommended reading's lines so apply can apply them

Today the writer must not draft a line the note does not give (`agents/capability-writer.md:31`), and apply applies only the drafts (`agents/initiative-round.md:34,37`). So every "add a line" answer forces a nothing-applied apply, a new integrate round and a new gate. Proposed text for the writer:

> "For each question whose reading adds, retires or replaces a line, draft that reading's lines under `round-<n>/readings/<question>/`, and name that path in the question."

The apply round then applies the drafts of the chosen reading.

- **Would remove:** the i40 apply-nothing round, and with it all of q19 and i41's integrate and gate, which re-asked i40's dropped questions. Also the i42 apply-nothing round with integrate round 3 and gate 4 (#15, #16), the i39 work-queue apply-nothing rounds ×3, and the forced non-recommended choice in #19.
- **That is 5 nothing-applied applies, 2 extra integrate rounds and 2 extra gates.**

### 3. Fix the gate's scope sentence

The sentence "Ask questions only on the lines and terms listed above as adds, changes or removes, and on no other line or term" (`scripts/supervise_brief.py:78-79`) made the i40 and i41 gates drop the writer's collision questions (#25, 26, 27, 20; #14 in i42). The i40 ones came back as a whole new request and initiative (`q19.md:8`). Yet the i43 review gate still asked about the supervision lines r155 and r156, so the same questions were answered twice.

Proposed: "Ask on the listed lines, including each existing line or term they collide with or rely on; a question on another proposal's listed line belongs to that proposal, not this one."

- **Would have prevented:** losing 5 collision questions (i40's three cost q19 lines 5–9 and i41), and the 2 duplicate asks in i43.

### 4. Spec and instruction wording, as proposals

**(a) The redirect family.**
- Add a term, e.g. **unheld answer**: "an answer of a capability-proposal that the drafts or `spec/` a round was given do not hold".
- Retire r83, r144, r145, r146 and r132, and add replacement lines whose triggers exclude a round that gives an unheld answer. For example: "When a round of the kind `apply` … ends having applied every answer of its proposal, `work run` shall transition the proposal to `approved`." And an output list that counts "an unheld answer" as the output of any round.
- Retire r92 for a line limited to rounds started for an initiative.
- Every new outcome of a round currently needs three companion lines, which is why these collisions keep happening.
- **Would remove 11 asks:** #11, 12, 13, 17, 18, 23, 25, 26, 27, plus #15 and #16 again.

**(b) Retire-not-edit is in no instruction.**
- `docs/capability-format.md:162`, `agents/capability-writer.md:22`, `skills/integrating-a-proposal/SKILL.md:26`, `skills/formulating-features/SKILL.md:28` and `skills/checking-spec-consistency/SKILL.md:52` all still say "a changed line keeps its id".
- No spec line records the person's rule (`.shop/work/i39/ledger.md:83-84`); a grep for "in place" or "keeps its id" in `spec/capabilities/` finds none.
- Proposal: a new spec-integration line, "When a line or table row is changed, `integrating-a-proposal` shall retire it and add the changed line with a new id, and no line shall override another", plus matching instruction text.
- **Would remove:** #29's form and #40. It also explains why the i40 writer drafted "(ids kept: changed lines r80, r71, r114)".

### 5. Request-writing guidance and glossary entries

There is no request-writing guidance anywhere. The only check is strict form (`spec/capabilities/requests.md:27`, v_e1/v_e2). Proposed checklist, in a skill or the `work request` help:
- one response per line;
- the EARS keyword follows what starts the behaviour;
- exits in words, no codes;
- no carrier or storage;
- glossary terms only;
- name every existing id a line supersedes, narrows, or depends on (for example q23 line 4 against review r6, r7 and r12).

Proposed glossary entries: **capability-proposal**, **drafts**, **change list**, **work-item's commits** (or "belongs to"), **message**, and **run** as a noun (r155 says "each run r154 names", but the entry at `spec/index.md:123` defines only the verb). Also note that the **check** entry says "exit code 0" (`spec/index.md:93`), against decision 0055.

**Would remove 10:** #8 (×2), 10, 19, 20, 30, 31, 32, 34, 36, and the triggers of #1 and #2.

## 4. Over-asking vs under-asking

**Over-asking (strong signal).** In i40–i43, 21 questions had a recommended reading, and 19 of those were answered with it. The 2 exceptions:
- #19, where the recommended reading was rejected only because apply could not hold it (Recommendation 2);
- #7, a genuine decision.

At least 10 of the 19 recommended readings were "no change", "stands" or "meant" (#3, 4, 5, 6, 15, 16, 17, 18, and #1 ×2). Gate 4 of i42 re-asked two collisions that the answers in its own brief had decided.

**Under-asking (also real).**
- The scope sentence made gates drop 5 writer questions in i40–i42. The i40 ones cost a whole further request and initiative.
- Three questions with no reading recommended reached formulation instead of the gate: i43 r156 (#8), i39 r136 (#38) and r121 (#41).

So the gate both over-asks on settled matters and under-asks on collisions with existing lines.

## 5. What I could not determine

- i43's gate results and the integrate `gate.md` (under `runs/`, not read). The ledger says "7 questions" (`.shop/work/i43/ledger.md:3`), but `review.md` holds 8. I infer that the 8th, r156, came from formulate round 3 (`ledger.md:7`), but did not verify it.
- I did not check the i39 gate results under `runs/` per proposal.
- What any question cost in tokens or time.
