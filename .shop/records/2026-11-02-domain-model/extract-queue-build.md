# Domain-model extraction: queue and build capabilities

Source: spec/index.md Glossary (lines 88-140) and spec/capabilities/ work-queue, requests, delivery,
role-boundaries, review, code-research, planning, red-green, as on main at 8a3d63c0. Extraction only; nothing
designed. Ids are `<capability>#rN`; `gl:<term>` cites a glossary entry. Abbreviations: wq = work-queue,
rq = requests, dl = delivery, rb = role-boundaries, rv = review, cr = code-research, pl = planning, rg = red-green.
"Impl" marks a fact stated only under "Implementation, may change", kept apart because it is not a requirement.

---

## 1. Entities

### 1.1 Initiative
- Identity: `<initiative>` (a directory name under `.shop/work/`); file `.shop/work/<initiative>/initiative.md`
  (wq#r22). Has an "id" printed by `work start` (wq#r22); form of the id not stated in these lines.
- Attributes:
  - status ∈ {proposed, started, done, abandoned} (gl:status). Lines use proposed (wq#r22), started (wq#r47),
    done (wq#r32, wq#r62), abandoned (wq#r32).
  - kind: `capability-change` is the one value written (wq#r22); value set otherwise unstated.
  - source: the request's origins (wq#r22).
  - initiative branch (wq#r36, gl:initiative branch), with base = commit it started from (gl).
  - ledger (wq#r19, gl:ledger).
- Transitions stated:
  - (none) → proposed by `work start` (wq#r22).
  - → done by any `work` command whose change makes the done-condition true (wq#r62). Condition: ≥1 work-item
    green ∧ all work-items green|withdrawn ∧ all capability-proposals formulated|withdrawn ∧ all requests kept
    here with asker = this context that name the initiative are delivered.
  - all work-items withdrawn → status unchanged (wq#r31) (consistent with r62's "at least one green").
  - stays `started` while a capability-proposal is neither formulated nor withdrawn (wq#r47) — implies the
    status was `started`, but **no line says who/what makes proposed → started**; nor → abandoned.
  - done/abandoned are terminal for `work add` (wq#r32).
- Derived display state: "waiting on <request>" while a request it raised into an upstream is not delivered
  (wq#r39). Not a status.

### 1.2 Work-item
- Identity: `w<n>`; `<n>` = 1 + max `<n>` over every work-item under `.shop/work/`, any initiative, any status
  (wq#r12). File `.shop/work/<initiative>/w<n>.md` (wq#r1). Impl: frontmatter id `work-item/<context path>/w<n>`.
  Also addressable as `<initiative>/<name>` in `work answer` (wq#r30).
- Attributes:
  - status ∈ {drafted, researched, planned, ready, claimed, done, green, awaiting-answer, failed, withdrawn}
    (gl:status). `planned` appears in no line of these files.
  - title, as its `# ` heading (wq#r1).
  - part_of, under, accepts (fields given by `--part-of`, `--under`, `--accepts`, wq#r1). `accepts` →
    scenarios/requirements (gl:work-item; rg#r1, cr#r4, cr#r5).
  - `## Answers` section (wq#r13) with dated answers.
  - open questions (wq#r36, wq#r37, dl#r6); the asking stage/role of the question (wq#r14, wq#r26).
  - file set (gl:file set; cr#r10; pl#r5; rg#r17) → becomes the claim (gl:claim; cr Purpose).
  - check (gl:check; rv#r6; rg#r3).
  - Retires list: deprecated scenarios it lists under Retires (rv#r10, rg#r2).
  - plan (pl#r1; rv#r13), notes (cr#r1), report (rg#r6), findings (rv#r1).
  - kind "fix work-item" (rv Purpose, rv#r8, rg Purpose, dl#r10) — subtype, no attribute named.
- Transitions stated (all written by `work`, logged, wq#r4, wq#r5):
  - (none) → drafted: `work add` (wq#r1).
  - failed → <status before failed per log.jsonl>: `work retry` (wq#r8).
  - X → withdrawn for X ∉ {claimed, green} (wq#r10) (also implies withdrawn → withdrawn is not excluded).
  - awaiting-answer → drafted (researcher asked) | researched (planner asked) | ready (implementer asked):
    `work answer` (wq#r14).
  - awaiting-answer (reviewer asked) → ready with `--change` (wq#r26) | → done with `--accept` (wq#r27);
    neither flag → error (wq#r28).
  - Implied by stage starts (glossary + Purpose text, not wq lines): drafted → researched (research, cr Purpose),
    researched → (planned?) (pl Purpose), ready → claimed (rg Purpose "ready work-item", rg#r3 "not yet
    claimed"), done → (review) (agent def. text), → green, → failed (gl:failed), → awaiting-answer.
    **The forward lifecycle is not stated in these capability lines** (Impl: "a transition the lifecycle does not
    allow ... is refused under r7"; lifecycle lives in design-decision/work-item-lifecycle-as-run).
  - Guard: file status must equal the last status log.jsonl gives, else refuse (wq#r6).

### 1.3 Capability-proposal
- Identity: `<name>` within an initiative (wq#r30); otherwise unnamed here.
- Attributes: status ∈ {drafted, awaiting-answer, approved, formulated, merged, withdrawn} (gl:status); lines use
  awaiting-answer (wq#r24), formulated, withdrawn (wq#r47, wq#r62). `## Answers` (wq#r24).
- Relation: part of an initiative (wq#r36, wq#r62); work-items are "under" one (gl:work-item).
- Transitions stated: none in these files; `work answer` writes an answer (wq#r24) but no transition named for it.

### 1.4 Glossary-proposal
- Only in glossary: part of an initiative beside capability-proposals; lists `term/<term>` in adds|changes|removes;
  status ∈ {drafted, awaiting-answer, approved, withdrawn} (gl:glossary-proposal, gl:status). Not in these 8 files.

### 1.5 Request
- Identity: printed id (rq#r44); Impl `.shop/work/requests/q<n>.md`, id `request/<context path>/q<n>`.
- Attributes:
  - status ∈ {open, awaiting-asker, awaiting-upstream, accepted, delivered, refused, withdrawn} (gl:status).
  - turn ∈ {asker, upstream} (gl:turn; rq#r44; Impl).
  - title (rq#r44); lines (strict EARS, rq#r2, rq#r59) — ordered, numbered n (rq#r15).
  - asker (a context, the product level, or the context itself — gl:request; rq#r32); asker id (rq#r42, rq#r57).
  - origins (`--source`) or job-thread (`--thread`) (rq#r44, rq#r45, rq#r30, rq#r31). Impl: `part_of` or `source`.
  - raised-for: the request it is raised for (rq#r29, rq#r31).
  - delegation: text, replaceable (rq#r19, rq#r65); dated person's words (rq#r72).
  - questions (rq#r20), answers (rq#r21), line outcomes (rq#r15), resolution (rq#r10).
  - "parts": asker's part = lines + answers (rq#r4); upstream's part = questions + line outcomes + resolution (rq#r5).
- Status transitions stated:
  - (none) → open, turn = upstream: `work request` (rq#r44).
  - `work turn` not setting accepted → turn flips (rq#r7).
  - turn → asker, with ≥1 line lacking outcome or with outcome ∉ {accepted, refused, withdrawn} → awaiting-asker (rq#r17).
    (Turn passed to asker with all lines decided: status not stated.)
  - turn → upstream → awaiting-upstream (rq#r18).
  - upstream ends turn, not delivered, all lines ∈ {accepted, refused, withdrawn}, ≥1 accepted → accepted; turn
    stays upstream (rq#r8, rq#r23).
  - upstream ends turn, not delivered, all lines ∈ {refused, withdrawn} → refused (rq#r9).
  - accepted → delivered by `work resolve` (rq#r10, rq#r11); turn → asker (rq#r24).
  - → withdrawn: no command (rq Not yet: `work withdraw <request>`).
  - delegation writing keeps status and turn (rq#r71).
- Derived display states: "awaiting the upstream and not yet taken in" (rq#r52); "asker has not seen it" (rq#r53).

### 1.6 Line (of a request)
- Identity: position n in the request (rq#r15).
- Attributes: text in strict EARS (rq#r2); vocabulary restricted to upstream glossary terms and Behaviour-line words
  (rq#r59); line outcome ∈ {accepted, rewritten, refused, question, withdrawn} (gl:line outcome) or none (rq#r17).
- Note: rq#r8, rq#r9, rq#r17 treat {accepted, refused, withdrawn} as decided; `rewritten` and `question` count as
  undecided.

### 1.7 Question / Answer
- Question: on a work-item (asked by researcher/planner/implementer/reviewer, wq#r14, wq#r26), on a
  capability-proposal (wq#r24), on a request line (rq#r20). Planner question has "its readings" (pl#r6).
- Answer: one line of text (wq#r15), dated (wq#r13, wq#r24), with flag `--change`/`--accept` for reviewer
  questions (wq#r26-28). Request answers: n-th answers n-th (Impl). gl:answer "in its answerer's words".

### 1.8 Delegation
- Text, non-empty (rq#r22, rq#r67), the person's words with the date (rq#r72); one per request (replaced, rq#r65).

### 1.9 Resolution
- Set of (accepted line → requirement id, version that holds it) (rq#r10, rq#r54).

### 1.10 Ledger / ledger line / note
- `.shop/work/<initiative>/ledger.md`, one line an event (gl:ledger); line = date + note (wq#r19, wq#r36);
  a note beginning `next:` is distinguished (wq#r36). Note must be one line (wq#r21).

### 1.11 Log line (log.jsonl)
- `.shop/work/<initiative>/log.jsonl`; fields time, work-item, status before, status after, who (wq#r5).

### 1.12 Observation
- Two senses: (a) a request origin printed by `work list` "that the source of no initiative and of no request
  names", with its date (rq#r64); (b) a review triage category (rv#r12, rv#r8, rv#r14). Not in glossary.

### 1.13 Session roles / agents
- person; session (gl); worker (gl); dispatch (gl); agents: initiative-round, capability-writer,
  feature-formulator, bdd-planner (planner), bdd-branch-reviewer, bdd-task-reviewer, architecture-reviewer,
  code-scout (researcher), bdd-implementer (implementer), spec-checker, trial-runner (rb#r1-r7).
- Agent attributes: model ∈ {Opus, Sonnet, Haiku} (rb#r5); tools (Edit, shell/Bash, Skill, "edit tool",
  Agent/dispatch) (rb#r1-r4, r6, r7); skills list (rb#r4).
- Skill `delivering-an-initiative` acts as an actor (dl#r4-r22).

### 1.14 Stage artefacts
- brief (gl; rv#r1, cr#r1, pl#r1, rg#r15, rg#r18); result with outcome, summary, files, questions, file set
  (gl:result; cr#r1, pl#r5, rv#r31); report (gl; rg#r6, rg#r9, rg#r10, rg#r17), with section
  `## Outside the file set` (rg#r17); notes (cr#r1, Impl `notes.md`); plan (pl#r1, Impl `plan.md`); findings file
  (rv#r1).
- outcome ∈ {DONE, DONE_WITH_CONCERNS, PARTIAL, BLOCKED, HAND-BACK, QUESTION, NEEDS_CONTEXT} (gl:outcome).
  Per role: researcher {DONE, NEEDS_CONTEXT} (cr#r12; Impl); planner {DONE, QUESTION, NEEDS_CONTEXT} (pl#r5,
  pl#r6, pl#r8); implementer {DONE, DONE_WITH_CONCERNS, PARTIAL, BLOCKED, HAND-BACK, NEEDS_CONTEXT} (rg#r16) — no
  QUESTION for implementer, yet wq#r14 has implementer's questions putting the item awaiting-answer.

### 1.15 Finding (review)
- grade ∈ {Critical, Important, Minor} (rv#r2); triage ∈ {fix now, observation, drop} (rv#r12); names the
  work-item whose commits contain it (rv#r12); reproduction, or a test "marked not run" (rv#r33); refactor
  observation with a check and the work-item it unblocks (rv#r14).
- review kinds: work-item review, branch review, architecture review (gl:review); re-review (rv#r8, rv#r30).

### 1.16 Spec objects referenced
- requirement `#r<n>` (gl), Behaviour line, capability, Purpose (rv#r5), capability's narrator (pl#r6),
  design-decision (pl#r2), scenario, deprecated scenario, feature file `.feature`, binding (rv#r11), step (rg#r5),
  Then line (rg#r3), test, suite (gl; rv#r7), check, version (rq#r10).

### 1.17 Repository-level objects
- repository (asker's, upstream's), checkout, working tree, index, HEAD, branch, current branch, remote,
  worktree, work-item branch, initiative branch, commit, green commit (rg#r9), tracked/untracked file (wq#r36),
  scratch directory (cr#r9), `CLAUDE.md` size limit (cr#r11, rg#r5), module with line count (cr#r11).

### 1.18 Bounded context / product level / upstream / asker
- context = repository; asker id registered per repository (rq#r42); upstream allows asker ids per asker (rq#r57).

---

## 2. Relations

| relation | from | to | cardinality / note | ids |
|---|---|---|---|---|
| part of | work-item | initiative | each work-item in exactly one initiative dir | wq#r1, wq#r62 |
| part of (`--part-of`) | work-item | ? (field value; not stated) | given on add | wq#r1 |
| under | work-item | capability-proposal | one (gl:work-item "under a capability-proposal") | wq#r1, gl |
| accepts | work-item | scenario(s) / requirement(s) | many | wq#r1, cr#r3-r5, rg#r1, rg#r3 |
| retires | work-item | deprecated scenario(s) | many | rv#r10, rg#r2 |
| names check | work-item | check | 0..1? | rv#r6, rg#r3, gl:check |
| has file set / claim | work-item | file paths | many; no two claims share a file | cr#r10, gl:claim |
| of (capability-proposal) | capability-proposal | initiative | many per initiative | wq#r36, wq#r62 |
| fulfils | initiative | request | initiative fulfils one request (wq#r22); request fulfilled by an initiative (rq Purpose) | wq#r22 |
| source | initiative | origins (of the request) | many | wq#r22 |
| names | request | initiative | via part_of or source (Impl) | wq#r62 |
| raised into | request | upstream (context) | one | wq#r39 |
| raised by / raised (initiative raised request) | initiative | request | many | wq#r39, wq#r62 |
| raised for | request | request (in upstream) | 0..1 | rq#r29, rq#r31 |
| asker | request | context / product level / self | exactly one | rq#r44, rq#r32 |
| upstream | request | context asked | exactly one (repository where kept, Impl) | gl:request |
| origin(s) | request | observation/origin ids | ≥1 when internal; forbidden when external | rq#r44, rq#r45, rq#r30 |
| job-thread | request | thread id | 0..1 | rq#r44, rq#r31 |
| delegation of | delegation | request | 0..1 per request | rq#r65 |
| line of | line | request | ≥1 ordered | rq#r44 |
| outcome of | line outcome | line | 0..1 | rq#r15 |
| question on | question | line (request) / work-item / capability-proposal | | rq#r20, wq#r13, wq#r24 |
| asked by | question | stage role (researcher, planner, implementer, reviewer) | one | wq#r14, wq#r26 |
| answers | answer | question | n-th answers n-th (Impl) | rq#r21 |
| holds | requirement id + version | accepted line | one per accepted line | rq#r10 |
| turn of | request | side ∈ {asker, upstream} | exactly one | gl:turn |
| registered under | repository | asker id | one | rq#r42 |
| allows | upstream | asker id for asker | many | rq#r57 |
| ledger of | ledger | initiative | 1:1 | wq#r19 |
| log of | log.jsonl | initiative | 1:1; lines per work-item transition | wq#r5 |
| initiative branch of | branch | initiative | 1:1 | wq#r36 |
| work-item branch | branch | work-item | 1, from initiative branch head, merged then deleted | gl, rg#r7 |
| brief names | brief | worktree, branch, findings/notes/plan file, result | | rv#r1, cr#r1, pl#r1, rg#r18 |
| started as | session/worker | agent | one | gl:agent |
| started on | worker | work-item in a status (researcher: drafted, planner: researched, implementer: ready/claimed, task reviewer: done) | | cr/pl/rg Purpose |
| reviews | work-item review | commits of one work-item + plan | | rv#r13 |
| reviews | branch review | initiative branch from base + every work-item | | rv#r13 |
| contains (finding) | finding | work-item whose commits contain it | one | rv#r12 |
| becomes | fix-now finding | fix work-item | | rv Purpose |
| rests on | plan decision | requirement or design-decision | | pl#r2 |
| unblocks | refactor observation | work-item | 0..1 | rv#r14 |
| replacement of | scenario | deprecated scenario | | rv#r11 |
| binds | binding (test) | scenario | | rv#r11 |

---

## 3. Events and actions

### work-queue (`work`)
| action | actor | object | pre | post | refuses |
|---|---|---|---|---|---|
| `work add <initiative> <title> --part-of --under --accepts` | person/session/script | work-item | initiative not done/abandoned (wq#r32) | new `w<n>.md`, drafted, id printed (wq#r1, wq#r12); committed with log line (wq#r9) | initiative done/abandoned, naming status (wq#r32); generic (wq#r7) |
| `work start <request>` | — | initiative | request accepted | initiative.md proposed, kind capability-change, fulfils request, source = origins; id printed (wq#r22); committed on current branch (wq#r25) | non-accepted: implied via wq#r7 |
| (any command) done-check | `work` | initiative | condition of wq#r62 newly true | status done | — (wq#r31, wq#r47 keep) |
| `work list [--json]` | — | all initiatives, work-items, requests, observations | — | prints each with status (wq#r60), JSON object (wq#r61), waiting-on (wq#r39), requests with status+turn (rq#r50), unreferenced observations with date (rq#r64) | — |
| `work show <initiative>` | — | initiative | — | prints status, proposals+status, work-items+status+open questions, branch + remote-has-all, uncommitted tracked files, untracked non-ignored files, last 10 ledger lines, last `next:` note (wq#r36) | — |
| `work show <work-item>` | — | work-item | — | status + open questions (wq#r37) | — |
| `work show <request>` | — | request | — | status, turn, lines + outcomes, questions, answers, resolution (wq#r59); side-dependent text (rq#r51-r54) | — |
| `--json` on show | | | | one JSON object (wq#r38) | |
| `work note <initiative> <line>` | session/skill | ledger | line has no mandatory line break | dated line appended (wq#r19), ledger committed (wq#r20) | line break → error "a note is one line" (wq#r21) |
| transition (internal) | `work` | work-item | file status = last log status (wq#r6) | new status in file (wq#r4), log line (wq#r5) | mismatch, naming file + both statuses (wq#r6); disallowed transition (Impl → wq#r7) |
| `work retry <work-item>` | — | work-item | failed | status before failed (wq#r8); committed (wq#r9); prints `<w> <status>` (Impl) | non-failed (implied r7) |
| `work withdraw <work-item>` | — | work-item | not claimed, not green | withdrawn (wq#r10); committed (wq#r9) | claimed/green (implied r7) |
| `work answer <target> <answer> [--change/--accept]` | person / answering session | work-item or capability-proposal (or `<initiative>/<name>`, wq#r30) | target awaiting-answer | dated answer under `## Answers` (wq#r13, wq#r24); work-item transition per asker (wq#r14, r26, r27); committed (wq#r9) | answer with line break (wq#r15); reviewer question without flag (wq#r28); not awaiting-answer (Impl→r7) |

### requests (`work`)
| action | actor | pre | post | refuses |
|---|---|---|---|---|
| `work request <title> --from <asker> --lines <file> [--source…|--thread|--raised-for] [--delegation]` | asker side, from own repo (rq#r28) | lines strict EARS (rq#r2); vocabulary (rq#r59); origin/thread/raised-for rules (rq#r45, r30, r31); asker = raising repository's context/product level (rq#r32); delegation non-empty (rq#r22) | open request, lines, asker, origins/thread, turn upstream, id printed (rq#r44); raised-for written (rq#r29); delegation (rq#r19); committed (rq#r12) | each of the above, naming line/word/asker or "because …" |
| `work outcome <request> <n> <outcome>` | upstream, in its turn | upstream's turn (rq#r16) | line outcome of line n (rq#r15); committed (rq#r12) | other side's turn (rq#r16); other side's part (rq#r55) |
| ask (question) — no command name given | upstream, in its turn | | question written (rq#r20); committed (rq#r12) | as above |
| answer (on request) — no command name given (prob. `work answer`/`reply`) | asker, in its turn, from own repo | | answer written (rq#r21); committed (rq#r12) | as above |
| `work turn <request>` | either side | its turn (implied rq#r16) | turn flips unless set accepted (rq#r7); status awaiting-asker (rq#r17) / awaiting-upstream (rq#r18); "upstream ends its turn" → accepted (rq#r8, turn kept, rq#r23) / refused (rq#r9); committed (rq#r12) | other side's turn (rq#r16) |
| `work resolve <request>` with ids + versions | upstream (rq#r5), whichever side's turn (rq#r10) | accepted | resolution written (rq#r10), delivered (rq#r11), turn → asker (rq#r24); committed (rq#r12) | not accepted (Impl→wq#r7) |
| `work delegate <request> <delegation>` | person via session (rq#r72) | request not delivered/refused/withdrawn (rq#r68); non-empty (rq#r67); any turn (rq#r70) | delegation replaced (rq#r65); status, turn kept (rq#r71); committed (rq#r66) | empty (rq#r67); terminal status, naming it (rq#r68) |
| session writes delegation (rq#r72) | session the person gave a delegation outside `work request` | — | `work delegate` called in the same reply with person's words and date | — |
| take in | upstream's `work` (at `work run` start before intake rounds, rq#r40) | — | every request/answer/turn sent before take-in began taken in (rq#r56); body read only as form fields (rq#r58) | leaves untaken those from disallowed asker id, telling upstream (rq#r57) |
| send (implicit) | asker | — | "sent" vs "taken in" (rq#r52) | — |
| raise / take in / give a line outcome / ask / answer / pass the turn / resolve / show | the command set every side gets (rq#r25) | | | |

### delivery (`delivering-an-initiative`)
| action | pre | post | refuses / never |
|---|---|---|---|
| deliver (start `work run`) | person asks (dl#r4) | `work run` started | — |
| read | while delivery lasts: nothing workers write (dl#r5); after a dispatch replied, a file it wrote only to decide what next (dl#r14) | | |
| show | `work run` exits (dl#r6) | each work-item status + open question as printed | |
| draft fix work-item | trial finds a fix to code (dl#r10) | work-item for `work run` | |
| route new scenario/example row | fix needs one (dl#r12) | sent to feature-formulator via `formulate` round of initiative-round | never to the implementer |
| ask person | worker needs disallowed tool (dl#r21, naming stage); `work run` cannot deliver a change (dl#r22) | question to person | changes nothing itself |
| dispatch an agent | (dl#r13) | asks it to reply in a few lines | |
| log answer | person gives an answer (dl#r15) | one line via `work note` | |
| fail | cannot do (dl#r7) | stop, say why, change nothing | |
| never | change code (dl#r11), start `claude -p` (dl#r19), merge a branch (dl#r20) | | |

### code-research (researcher / code-scout)
- research: started by `work run` on a drafted work-item (cr Purpose). Post: notes in notes file, file set in
  result, checkout unchanged (cr#r1). Notes contain: why each accepted scenario is red, from running it (cr#r4);
  places relying on changed/replaced requirement + their tests (cr#r3); tests made impossible to keep (cr#r5);
  refusals/effects only a skipped step produces (cr#r6); defects with reproduction (cr#r8); modules with line
  count and room under the size limit (cr#r11). Result file set: every production/test file needed (cr#r10).
  Probes in scratch dir (cr#r9). Fail: NEEDS_CONTEXT, say why, change nothing (cr#r12).

### planning (planner / bdd-planner)
- plan: started on a researched work-item (pl Purpose). Writes plan to plan file (pl#r1); names each open decision
  with what it rests on (pl#r2); lists tests each decision breaks + fate (pl#r3); no code block/file contents/diff/
  step body (pl#r4). Ends: result DONE|QUESTION + final file set (pl#r5). QUESTION when a decision changes what the
  narrator observes and nothing settles it, with readings (pl#r6). Writes only plan + result (pl#r7). Fail:
  NEEDS_CONTEXT, say why (pl#r8) — no "change nothing" here, unlike cr#r12/rv#r28/dl#r7.

### red-green (implementer / bdd-implementer)
- implement: on a ready work-item in its worktree (rg Purpose); also continuation and fix work-item.
- DONE ⇒ every accepted scenario passing (rg#r1); suite left to `work run`.
- hand back (outcome HAND-BACK, condition + evidence verbatim, work committed on work-item branch) under five
  conditions (rg#r3, rg#r7).
- BLOCKED under four conditions, naming test/step/decision/file (rg#r5).
- PARTIAL at a green commit when >15 files (rg#r9).
- NEEDS_CONTEXT when cannot do (rg#r15).
- report entries: setup-only test changes / rewrites of tests committed after base (rg#r6); silent cases as open
  questions (rg#r10); files outside file set under `## Outside the file set` before editing (rg#r17).
- never: commit to `.feature` or `.shop/work/` except `features retire` of a listed deprecated scenario (rg#r2);
  paste plan code (rg#r11); push/merge/rebase/reset (rg#r18); work outside brief's worktree/branch (rg#r18).
- every session ends with a result whose outcome ∈ 6-set (rg#r16).

### review (reviewers)
- review end: findings in findings file + result; working tree/index/HEAD/branches unchanged (rv#r1).
- read scope per kind (rv#r13); branch reviewer runs nothing (rv#r32).
- grade (rv#r2); table rows rv#r10, r3, r4, r5, r6, r11, r29; triage (rv#r12), override to fix now for
  unasked-for behaviour (rv#r30), override to observation on re-review of fix work-item (rv#r8).
- branch review end: wall time, shape vs CLAUDE.md, coupling (rv#r7); questions only for fix-now findings (rv#r31);
  run-only behaviours as findings with a test marked not run (rv#r33); dry-run/real agreement test check (rv#r34).
- architecture reviewer: refactor → observation with check + unblocked work-item (rv#r14).
- fail: stop, say why, change nothing (rv#r28).

### role-boundaries (static, about agent definitions)
- dispatch allowed only to initiative-round (rb#r1); no Edit for reviewers/researcher/planner (rb#r2); no edit/shell
  for capability-writer and feature-formulator (rb#r3); implementer skills incl. bdd-red-green + Skill tool, allowed
  only for those skills by `work run` (rb#r4); models (rb#r5); no shell for planner (rb#r6) and branch reviewer (rb#r7).

---

## 4. Exclusivity, ownership and limits

- **Sole writer of work-item status**: `work` (wq Purpose; gl:transition "written by `work`"); implementer never
  writes a transition (rg Purpose); `work run` reads results. Every transition logged with who (wq#r5).
- **File/log consistency**: transition refused when file status ≠ last log status (wq#r6).
- **Request parts owned per side**: asker owns lines + answers (rq#r4); upstream owns questions, line outcomes,
  resolution (rq#r5); cross-writes refused unless asker is the upstream itself (rq#r55); side taken from the
  repository, never an argument (rq#r33). Delegation is owned by neither part: written whichever turn (rq#r70) —
  and rq#r65/r72 say the person (through a session) writes it; side not stated.
- **Turns**: exactly one side's turn; writes other than `work resolve` refused in the other side's turn (rq#r16);
  `work resolve` and `work delegate` turn-exempt (rq#r10, rq#r70); upstream keeps turn on accepted (rq#r23); asker
  gets turn on delivered (rq#r24).
- **Asker from own repo, no upstream checkout** (rq#r28); asker identity = registered asker id (rq#r42), allowed-list
  at the upstream (rq#r57); asker given must be the raising repository's context (rq#r32).
- **Internal vs external request**: origin (`--source`) only for internal (asker = upstream itself) (rq#r30, r45);
  external needs `--raised-for` or `--thread` (rq#r31).
- **Claims**: no two claims share a file (gl:claim); file set becomes the claim (cr Purpose); `work claim` not yet
  (wq Not yet, rg Not yet).
- **Withdraw limits**: not claimed, not green (wq#r10).
- **Terminal statuses**: initiative done/abandoned refuse `work add` (wq#r32); request delivered/refused/withdrawn
  refuse `work delegate` (rq#r68).
- **Id uniqueness**: `w<n>` global across initiatives (wq#r12).
- **One-line texts**: note (wq#r21), answer (wq#r15).
- **Dispatch**: only initiative-round dispatches (rb#r1) — yet dl#r13/r14 have `delivering-an-initiative` (a skill
  in the person's session, not an agent definition) dispatching; no conflict by scope, but worth noting.
- **Read limits for delivery skill**: reads nothing workers write while delivery lasts (dl#r5); dispatch files only
  to decide next (dl#r14); never changes code/starts claude -p/merges (dl#r11, r19, r20).
- **Write limits per role**: reviewer changes nothing but findings + result (rv#r1); branch reviewer runs nothing
  (rv#r32); researcher leaves checkout unchanged, probes in scratch (cr#r1, cr#r9); planner writes only plan + result
  (pl#r7); implementer no `.feature`/`.shop/work/` commits (rg#r2), only its worktree/branch, no push/merge/rebase/
  reset (rg#r18).
- **Quantitative limits**: >15 files → PARTIAL (rg#r9); last ten ledger lines (wq#r36); size limit from CLAUDE.md
  (cr#r11, rg#r5); Impl: summary under fifteen lines (cr, rg).
- **One-at-a-time**: implementer "one scenario at a time" (rg Purpose only, no line); one task reviewer per
  work-item (rv Impl).
- **Tool/model ownership**: rb#r1-r7.

---

## 5. Repeated qualifiers (≈153 Behaviour lines incl. table rows across the 8 files; counts by grep, rough)

| qualifier | ~lines | where | note |
|---|---|---|---|
| "and change nothing" / "changing nothing" | 20 | wq#r7, r15, r21, r28, r32; rq#r2, r16, r22, r30, r31, r32, r45, r55, r59, r67, r68; dl#r7, dl#r22; cr#r12; rv#r28 | universal post-condition of every refusal/error. Absent from pl#r8 and rg#r15 (stop NEEDS_CONTEXT without "change nothing"), and from wq#r6 (refuse, no "change nothing") |
| "shall refuse" | 13 | wq#r6, r32; rq#r2, r22, r30, r31, r32, r45, r55, r59, r67, r68, r16 | refusal |
| "naming the X" (in refusal) | ~11 | wq#r6 (file + statuses), wq#r32 (status), rq#r2 (line), rq#r32 (asker), rq#r55 (side), rq#r68 (status), rq#r59 (word + why), dl#r21 (stage), rg#r5 … | refusal names its cause |
| "because <reason>" (in refusal) | 6 | rq#r16, r22, r30, r31, r45, r67 | alternative form of the same; "naming" vs "because" vs "saying that" (wq#r15, r21, r28) vs "say why" (wq#r7) — four phrasings of one pattern |
| "exit with an error, saying that …" | 4 | wq#r7, r15, r21, r28 | vs "refuse": two words for the same outcome (exit non-zero, nothing changed) |
| "cannot do what it was asked / its brief asks / its input asks, then … stop, saying why" | 6 | wq#r7, dl#r7, cr#r12, pl#r8, rg#r15, rv#r28 | universal fallback per actor; the object varies (asked / brief asks / input asks) |
| "commit … on the current branch" | 5 explicit (+ ~9 more "commit") | wq#r9, r20, r25; rq#r12, r66 | universal after-effect of any write by `work`; stated per command group instead of once |
| "shall print" | 13 | wq#r1, r22, r36-r39, r59-r61; rq#r44, r50-r54, r64 | query / id echo |
| "Where `--json` is given … one JSON object" | 2 | wq#r38, wq#r61 | |
| "with the date" | 4 | wq#r13, r19, r24; rq#r72 | |
| "mandatory line breaks U+000A … U+2029" | 2 | wq#r15, r21 | identical enumerated list; a candidate defined term "one line" |
| "in its turn" / "whichever side's turn it is" | 5 / 2 | rq#r15, r16, r20, r21; rq#r10, r70 | turn guard |
| "the outcome `X`" | 9 | cr#r12; pl#r5, r6, r8; rg#r5, r7, r9, r15, r16 | |
| "in its report" / "in the notes" | 5 / 7 | rg#r6, r9, r10, r17; cr#r3-r6, r8, r11 | per-artefact content obligations |
| "the … its brief names" | 4 | rv#r1, cr#r1, pl#r1, rg#r18 | location given by the brief |
| "only" (restriction) | 13 | rq#r4, r5, r58; rb#r1, r4; dl#r14; rv#r31, r32; pl#r7; rg#r9, r18 … | exclusivity |
| "The plugin's agent definitions shall …" | 7 | rb#r1-r7 | all of role-boundaries; static subject |
| "When <cmd> is run on a <status> <entity>" | ~10 | wq#r8, r10, r13, r14, r22, r24, r26, r27; rq#r10 | status precondition in the trigger |

---

## 6. Terms used but not defined in the glossary; inconsistencies and synonyms

### Used, not in glossary
- **asker**, **upstream** (used in gl:request, gl:turn, but no own entry; "side" is their union) — rq passim.
- **side** (rq#r16, r33, r55, r70).
- **part (of a request)**: "asker's part", "upstream's part" (rq#r4, r5, r55).
- **lines** of a request (rq#r44) and "line" vs "Behaviour line"/"requirement" — homonym.
- **origin(s)** (`--source`) (rq#r30, r44, r45; wq#r22) — no entry.
- **job-thread** (rq#r31, r44, r45).
- **asker id** (rq#r42, r57); **registered**.
- **take in / taken in / sent** (rq#r40, r52, r56, r57) — the intake mechanism.
- **resolution** (rq#r10, r11, wq#r59).
- **observation** — two senses (rq#r64 origin-like record; rv#r12 triage class).
- **initiative** — no glossary entry at all (used throughout; status in gl:status).
- **capability-proposal** — no glossary entry (status only).
- **bounded context / context / product level** (rq#r32, gl:request).
- **kind** of initiative (`capability-change`, wq#r22) and "round of the kind intake" (rq#r40) — "kind" overloaded.
- **open question(s)** (wq#r36, wq#r37, dl#r6, rg#r10) vs **question** — not distinguished.
- **finding**, **grade** (Critical/Important/Minor), **triage** (fix now/observation/drop), **re-review**,
  **fix work-item**, **reproduction**, **findings file** (rv) — none defined.
- **plan**, **notes**, **probe**, **scratch directory** (pl, cr) — `probe` is used in gl:run only as an object.
- **researcher / planner / implementer / reviewer / branch reviewer / architecture reviewer / work-item reviewer**
  roles — not defined; mapped to agents only implicitly (cr/pl/rg/rv Purpose).
- **notes file**, **plan file**, **findings file** (artefacts named by the brief).
- **worktree** (rg Purpose, rg#r18) — no entry; glossary has work-item branch only.
- **green commit** (rg#r9); status `green` exists, "green commit" is a different sense.
- **Retires** (list on a work-item) (rv#r10, rg#r2); `features retire` command.
- **binding** (rv#r11), **step** (rg#r5), **Then line** (rg#r3), **setup** (rg#r3, rg#r6, rv#r4).
- **trial's fix**, **fix** (dl#r10, r12, r22).
- **wall time** (rv#r7), **shape**, **coupling** (rv#r7), **dry-run mode / real mode / randomized test** (rv#r34).
- **version** (that holds a requirement id, rq#r10) — not the same as gl:plugin version.
- **narrator** (pl#r6) — frontmatter concept, no entry.
- **design-decision** (pl#r2).
- **current branch** (wq#r9 etc.), **checkout** (wq#r36, cr#r1), **tracked** (gl uses it too).
- **job**: "the person" (actor) — no entry.
- **`next:` note** (wq#r36).

### Inconsistencies / synonyms
- "refuse" vs "exit with an error" for the same effect (wq#r6/r32 vs wq#r7/r15/r21/r28); and rq uses "refuse" only.
- Refusal reason phrasing: "naming X" / "because X" / "saying that X" / "say(ing) why" (see §5).
- "cannot do what it was asked" (wq#r7, dl#r7, pl#r8) / "what its brief asks" (cr#r12, rg#r15) / "what its input
  asks" (rv#r28).
- "stop ... and change nothing" vs "stop" alone (pl#r8, rg#r15).
- Role names vs agent names: researcher = code-scout; planner = bdd-planner (rb#r6 uses agent name, rb#r2 role
  name); implementer = bdd-implementer; reviewer/work-item reviewer = bdd-task-reviewer; branch reviewer =
  bdd-branch-reviewer (rb#r7 agent name); "the reviewers" (rb#r5) unspecified set.
- "work-item review" (rv#r6, r13) vs glossary "work-item review" ok, vs agent "task reviewer" (rv Purpose).
- "checkout" (cr#r1) vs "working tree, index, HEAD and branches" (rv#r1) vs "worktree" (rg#r18).
- "ends its turn" (rq#r8, r9, r23) vs "passes the turn" / `work turn` (rq#r7) — whether "ends its turn" = `work turn`
  run by the upstream is not stated.
- "answers a question" (asker, rq#r21) vs `work answer` (wq) — request answers have no named command in these lines
  (the task's "reply" verb does not appear in these files).
- "ask a question" on a request has no named command here (the task's "ask" verb appears only in rq#r25 list).
- "the upstream itself" (rq#r30, r45, r55) = "the context itself" (gl:request) = asker `internal` (Impl).
- "work-items ... `done`" vs initiative `done` vs outcome `DONE` — three senses of done.
- `green` (status) vs "green commit" (rg#r9) vs "red today" (cr#r4).
- "accepted" — request status, line outcome, and "the scenarios it accepts" (work-item accepts) — three senses.
- "withdrawn" — work-item, capability-proposal, request status and line outcome.
- "delivered" (request status) vs "delivery" (gl: one invocation of `work run`) vs "deliver an initiative" (dl#r4).
- "question" — line outcome value (gl:line outcome) and a written question (rq#r20); `QUESTION` outcome (pl#r6).
- "part of" — `--part-of` field (wq#r1) and request's `part_of` = job-thread (rq Impl) vs relation "part of an
  initiative" (gl:glossary-proposal).
- "source" — initiative source (wq#r22) vs request `--source` origins (rq#r44); same word, same values?
- "the product level" (rq#r32, gl) — undefined entity.
- `planned` status in glossary has no line here that enters or leaves it; pl Purpose speaks of "researched" input
  but nothing of output status.
- `claimed` vs `ready`: rg Purpose says "ready work-item", rg#r3 "a work-item not yet claimed".
- "file set" (cr#r10, pl#r5 "final file set", rg#r17) — glossary forbids "scope"; consistent here.
- "request's origins" (wq#r22) vs "origins `--source` names" (rq#r44): same.
- "who made the transition" (wq#r5) — no value set for "who".

---

## 7. Lines packing several rules (id: rule count, what)

- wq#r1: 4 — writes file at path; status drafted; fields + title heading; prints id.
- wq#r22: 6 — writes initiative.md; status proposed; kind capability-change; fulfils request; source = origins; prints id.
- wq#r62: 5 — four conjunctive conditions + the effect (and "a `work` command's change makes it true" trigger semantics).
- wq#r36: 9 — status; proposals+status; work-items+status+open questions; branch; remote has every commit;
  uncommitted tracked files; untracked non-ignored files; last ten ledger lines; last `next:` note (plus embedded
  definition of "note").
- wq#r59: 6 — status, turn, lines+outcomes, questions, answers, resolution.
- wq#r5: 2 — append a line; its five fields.
- wq#r9: 3 — four commands; commit changed file; commit log line if any.
- wq#r14: 4 — answer writes (implicit) + three status mappings.
- wq#r21 / wq#r15: 2 each — the line-break definition (7 code points) + the refusal.
- wq#r12: 2 — numbering rule + scope (any initiative, any status).
- wq#r7: 3 — exit error, say why, change nothing.
- rq#r25: 2 — one command set (8 verbs) + one lifecycle.
- rq#r44: 7 — trigger with three alternative flags; open; lines; asker; origins/thread; turn upstream; prints id.
- rq#r59: 3 — implementation detail ban; vocabulary rule (two sources); refusal naming word + why.
- rq#r4 / rq#r5: 2 each — the partition of parts + the "only when" triggers.
- rq#r17: 2 — status rule + undecided-line condition.
- rq#r8: 3 — not delivered; all lines decided; ≥1 accepted.
- rq#r10: 3 — accepted precondition; turn-exemption; resolution content (id + version per line).
- rq#r12: 2 — five triggers; commit.
- rq#r57: 3 — leave untaken; tell upstream which; tell why.
- rq#r72: 4 — trigger outside `work request`; same reply; via `work delegate`; person's words with the date.
- rq#r56: 2 — take in everything sent before; regardless of listing lag.
- dl#r6: 2 — statuses + open questions, as printed.
- dl#r12: 3 — route to feature-formulator; via formulate round of initiative-round; never to implementer.
- rv#r1: 2 — leave findings + result; leave tree/index/HEAD/branches unchanged.
- rv#r13: 2 — work-item review scope; branch review scope.
- rv#r32: 3 — runs nothing; reads given + repository files; writes findings + result.
- rv#r6 (row): 2 — branch review fails; work-item review lists separately.
- rv#r11 (row): 3 — three different findings.
- rv#r12: 4 — naming work-item; fix now (3 triggers); observation with reproduction; drop.
- rv#r7: 3 — wall time; shape vs CLAUDE.md; coupling.
- rv#r8: 2 — three exceptions + the observation rule.
- rv#r30: 3 — scope incl. re-review; fix now; fix definition (line first or code removed) + override of r8/r12.
- rv#r34: 2 — the test ran; how many cases.
- rv#r14: 3 — observation; with check; naming unblocked work-item.
- cr#r1: 3 — notes; file set in result; checkout unchanged.
- cr#r10: 3 — production + test files; for scenarios to pass and existing to keep passing; each shown by search/read.
- pl#r5: 2 — outcome set; final file set.
- pl#r6: 3 — condition (two parts); QUESTION; with question and readings.
- rg#r1: 2 — accepted scenarios pass; suite left to `work run`.
- rg#r2: 2 — no `.feature`/`.shop/work/` commits; exception via `features retire` for listed deprecated scenario.
- rg#r3: 5 — five disjoint hand-back conditions.
- rg#r5: 5 — four BLOCKED conditions + naming obligation.
- rg#r6: 2 — setup-only change; rewrite of test committed after base.
- rg#r7: 3 — outcome HAND-BACK; condition + evidence verbatim; work committed on work-item branch.
- rg#r9: 3 — threshold 15; PARTIAL at green commit; only files named in report before first edit.
- rg#r18: 2+ — only its worktree and branch; no push, merge, rebase, reset.
- rb#r4: 3 — skills listed; bdd-red-green among them; Skill tool allowed only for those (and that last is a
  `work run` rule, not an agent-definition one).
- rb#r5: 3 — three model assignments over eleven agents.
- rb#r2, rb#r3: 2 each (several agents × tools).

## Gaps noticed (for the model, not fixes)
- No line enters `started` or `abandoned` for an initiative; no forward work-item lifecycle in wq (lives in a
  design-decision + supervision).
- `planned` status unused here; capability-proposal transitions unstated here.
- Request `withdrawn` status reachable by no command; line outcome `rewritten`/`question` have no further rule.
- Status after `work turn` to asker when every line is decided is not stated (rq#r17 covers only undecided).
- Implementer has no `QUESTION` outcome (rg#r16) though wq#r14 maps an implementer's question to `ready`.
- `work run` (supervision) is an actor in nearly every file but its capability was outside this read.
