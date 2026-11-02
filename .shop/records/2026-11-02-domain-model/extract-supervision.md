# Extraction: supervision capability (spec/capabilities/supervision.md) against the glossary (spec/index.md 88-140)

Extraction only, from the lines as written. "impl" = the `## Implementation, may change` section (not requirements).
Ids cite `supervision#rN`; glossary entries cite `gloss:<term>`. 151 live Behaviour lines read (r1..r222 less the 23 retired).

---

## 1. Entities

### 1.1 `work run` / delivery (the system actor)
- Identity: one invocation (gloss:delivery). Two modes: with an initiative (r1) or with none (r66, r81, r82).
- Attributes
  - mode: `with-initiative` | `no-initiative` (r1, r66, r81, r82, r212 vs r82)
  - started-by-worker-of-another-work-run: bool → refuse (r21)
  - exit: `success` | `error` (r10, r44, r52, r53, r81, r82, r88, r96, r101, r107, r115, r184, r212, r40, r46, r51); impl exit codes 0 / 3 (awaiting an answer) / 1.
  - printed on exit: each work-item's status (r212, r52), each fault (r52), each initiative's status (r81, r82), requests with open questions (r101), proposals/work-items with open questions (r184), round and how it ended (r88), capability named (r107), work-item and fault (r40), uncommitted paths (r46), reason (r10, r51, r53).
  - worktrees it made (r33), sessions it started (r128, r214).

### 1.2 initiative
- Identity: named `<initiative>` in paths `.shop/work/<initiative>/` (r47, r214); the id form (i<n>) is not stated in this capability.
- Attributes
  - status: `proposed` | `started` | `done` | `abandoned` (gloss:status; r66, r79, r84, r213, r161, r109). Only proposed→started (r84) and →done (r213, r161) are written here; `abandoned` only as a filter (r66).
  - fulfils: request (0..1? r79, r180, r103, r135, r141, r210); "no initiative fulfils it" (r103) implies request→initiative 0..1.
  - initiative branch (r46, r91, r100, r106, r109, r27); base (r25, r27, r156)
  - ledger (r141; gloss:ledger)
  - work-items (r1, r93, r97, r94, r213, r180)
  - capability-proposals (r180, r187, r213)
  - glossary-proposal ("its glossary-proposal" r161, singular; r180)
  - kept branch reviews (r27, r50, r75, r213)
  - measurement, analysis record (r75, r76, r106, r213)
  - raised requests: requests "an initiative raised into an upstream" (r136, r135), requests "kept in this context whose asker is this context and that names the initiative" (r213)
  - "changes only the glossary": bool (r161)
  - nodes (r28-type generic: r111, r115, r212, r81)
  - questions of the initiative (r210, r209)

### 1.3 request
- Identity: not stated here (q<n> per module map).
- Attributes
  - status: `open` | `awaiting-upstream` | `awaiting-asker` | `accepted` | `delivered` | `refused` | `withdrawn` (gloss:status); used here: `open`, `awaiting-upstream` (r67), `accepted` (r103), `delivered` (r136, r213). `awaiting-asker` not named; replaced by "in the asker's turn" (r101, r212, r82).
  - asker: this context | another context | product level (gloss:request); "whose asker is this context" (r101, r212, r82, r213); impl: `asker` = `internal` or this context's id.
  - upstream: "of which this context is the upstream" (r67, r103); "into an upstream" (r135, r136).
  - turn: `asker` | `upstream` (gloss:turn; r101, r212, r82; passed by `work turn` r67, r134).
  - lines; accepted lines (r79, r180, r141); per-line line outcome or question (r67, r100, r132).
  - delegation: optional, readable "at that moment, given before or after the initiative started" (r210, r211, r78, r118-r120).
  - open questions (r101; impl: no answer under `## Answers`).
  - kept in this context: bool (r213, r101).
  - names the initiative (r213) / raised for the request the initiative fulfils (r135).

### 1.4 capability-proposal
- Identity: not stated; one per capability per initiative implied (r159 "for each capability", r148 "no second capability-proposal for that proposal's capability", r187).
- Attributes
  - status: `drafted` | `awaiting-answer` | `approved` | `formulated` | `merged` | `withdrawn` (gloss); used: `drafted` (r159, r68, r142), `awaiting-answer` (r69, r184, r212), `approved` (r144), `formulated` (r83, r72, r122, r213), `withdrawn` (r122, r213). `merged` never used here.
  - capability: one (r159)
  - `adds`, `changes`, `removes`: sets of requirement ids (r159, r187, r145, r72, r122)
  - `## Questions` (r85, r117); answers (r70, r141, r147, r152)
  - writing integrate round + its kept drafts path (r108)
  - earlier drafts in their round's directory (r142)
  - work-items under it (r72, r74, r123)
  - lines raised into an upstream (r136)

### 1.5 glossary-proposal
- Identity: not stated; one per initiative implied (r161).
- Attributes
  - status: `drafted` | `awaiting-answer` | `approved` | `withdrawn` (gloss); used: `drafted` (r171, r164), `awaiting-answer` (r169, r172), `approved` (r166, r161).
  - terms added / changed / removed (r171, r164, r173, r189) (gloss: `adds`/`changes`/`removes` of `term/<term>`).
  - questions; answers (r165, r172); writing integrate round + drafts path (r170).
  - its questions are never delegated (r209, r210).

### 1.6 work-item
- Identity: `<work-item>` / `<name>` (r22; gloss: `w<n>`).
- Attributes
  - status: `drafted` | `researched` | `planned` | `ready` | `claimed` | `done` | `green` | `awaiting-answer` | `failed` | `withdrawn` (gloss); used: drafted, researched, ready, done (r2, r59), planned (r31), green (r63, r75, r93, r110, r123, r212), withdrawn (r75, r93, r212, r43), awaiting-answer (r26, r36, r37, r184), failed (r34, r37, r39-r42, r45, r52, r218). `claimed` only in impl.
  - capability-proposal it is part of (r74, r123)
  - accepted requirements / scenarios (r72, r19, r22, r43, r56, r64, r65, r73)
  - check (r154; gloss:check)
  - file set / `fileset:` (r19, r31, r132, r185)
  - claim (r20; gloss:claim)
  - `blocked_by`: work-item ids (r63)
  - `## Retires`: deprecated scenarios (r73, r123)
  - `## Questions` (r36, r129, r131), answers (r57, r98), impl `## Faults`
  - plan, implementer's report, review findings (r157, r98)
  - work-item branch: kept or deleted (r4, r18, r26, r58)
  - worktree (r20, r58)
  - stage directories `runs/<work-item>/<k>-<stage>/` (r7, gloss)
  - findings file it was drafted for (r74, r110)
  - "every requirement is of a guarantees capability": bool (r56, r64, r65)

### 1.7 stage
- Identity: `<k>-<stage>` (gloss:stage directory); kinds `research` | `plan` | `implementation` | `review` (r1, r2), plus `branch-review` (r49), rounds and answering sessions (gloss:stage).
- Mapping status→stage→agent (r2): drafted→research→code-scout; researched→plan→bdd-planner; ready→implementation→bdd-implementer; done→review→bdd-task-reviewer.
- Attributes: output (r130-r132, r147, r153), where its questions go (r129), allowed tools (r30), brief, result, `session.json` (r62).
- Output per stage (r132): researcher → file set (may be empty, r185); planner → plan + file set; implementer → commits on which scenarios + whole suite pass; reviewer → findings; answering session → answer; integrate/apply round → change list; formulate round → scenario per added/changed requirement; intake round → line outcome or question per line; gate round → questions.

### 1.8 session / worker / round / branch reviewer (session subtypes)
- session (gloss): id, transcript (r62), result, end ∈ {`normal`, `error`, `turn-limit`, `no-readable-result`} (r128, r86-r88, r89, r90, r45, r42), started-for ∈ {work-item, capability-proposal, initiative, question} (r128).
- worker: `claude -p` session for one stage of one work-item (r2); agent (r2, r8, r12), plugin dir (r11), skills (r12), tools (r13, r14, r30), worktree (r17, r23, r15), turn limit (r19: researcher 80).
- round: `initiative-round` session (r67); kind ∈ {`integrate`, `gate`, `apply`, `formulate`, `intake`} (r95, r67, r68, r70, r79); for ∈ {initiative (r79), capability-proposal (r141, r187), glossary-proposal (r221, r189), request (r67)}; result, change list (r96, r159), drafts kept (r91), round's directory (r142), questions (r85, r100).
- branch reviewer: `bdd-branch-reviewer` session (r27), not a worker (gloss:worker); directory copied to `runs/branch-review/<k>/` (r47).
- answering session under a delegation (r210, r78, r89, r90, r118-r120).
- `analyzing-a-batch` session (r76).

### 1.9 result
- `result.json` (gloss): outcome (r133, r44 `PARTIAL`), questions (r129-r131; impl: string = one question), stage output (r130-r132), files named (r15), `fileset` (r31), answer (r150, r221), change-or-accept flag (r120), findings to fix now (r74).

### 1.10 brief
- Contents: work-item, files to read, where result goes (r2); plugin scripts dir, initiative branch base, worktree, work-item branch (r25); "starts in its worktree and never changes directory" (r17); write result first with `PARTIAL` (r44); answers with questions (r57); reviewer findings + answer (r98); suite outcome (r24); gate-as-questions request (r68).

### 1.11 change list
- Produced by integrate / apply round (r132). Names capabilities (r159, r107, r187), the glossary (r171), requirement ids added/changed/removed per capability (r159), terms (r171), lines of a request into an upstream (r135).

### 1.12 drafts (of an integrate round)
- kept on the initiative branch (r91); path (r108, r170); "not yet applied" (r102); add requirement ids (r102); earlier drafts kept in round's directory (r142).

### 1.13 branch review
- Identity: `<k>` (r47). Attributes: kept (r27, r50, r74, r121), commits read (r27, r50), result: findings to fix now (r74), questions (r121), "status" (r121 — undefined), commit (r53, r48).

### 1.14 question / answer / delegation
- question: on work-item, capability-proposal, glossary-proposal, request line (r129, r85, r173, r100); "of an initiative" (r210); "reviewer's question" (r118); answered | unanswered (r89); left for the person (r209, r210).
- answer: names delegation (r78); asks-for-change | accepts-as-is (r118-r120); "that the drafts it applied do not hold" (r150, r221, r147).
- delegation: text given with request (gloss), covers / doesn't cover a question (r210).

### 1.15 git objects
- initiative branch: base, head, commits, remote (r54, r38, r35), commits read by a kept branch review (r27, r50).
- work-item branch: from initiative head (gloss), merged + deleted (r18), kept on awaiting-answer (r26).
- worktree: per worker (r20), on kept branch (r58), temp dir outside plugin dir if repo is inside it (r23), removed on exit (r33); impl `.shop/worktrees/<work-item>/`.
- main checkout, its `.shop/work/` (r46, r214, r218, r6, r34).
- remote (gloss; r35, r54).

### 1.16 files and runs
- `log.jsonl`: line = (time, work-item, stage, agent, session id) (r8, r49).
- stage directory, `session.json` (transcript path r62).
- `.shop/delivery.toml`: number of workers (r60), `[tests]` (r29), `[allowed_tools]` per stage (r30).
- suite (r4, r24, r43, r122, r154), scenario (r4, r219), check (r154), the runs `tools check`, `tools size`, `features deprecated`, `features bindings` (r154), run = (command, exit code, output, commit) (r155).
- deprecated scenario with `Deprecated for:` line, replacement, replacement's work-item (r73, r123).
- measurement, analysis record (r75, r76, r106).
- pytest option `--work-item <name>` (r22, r55, r56, r64, r65).
- capability (spec/capabilities/, r107), guarantees capability (r56, r64, r65), glossary / `spec/index.md` (r161, r171).
- fault (r128, r40, r52; gloss).
- node: generic for work-item / capability-proposal / glossary-proposal / initiative (r111, r129-r131, r212, r81); whether request is a node is not stated.

---

## 2. Relations

| relation | from | to | cardinality / note | ids |
|---|---|---|---|---|
| fulfils | initiative | request | initiative 0..1 request; request 0..1 initiative ("no initiative fulfils it") | r79, r103, r180 |
| is upstream of | this context | request | | r67, r103 |
| asker of | this context | request | | r101, r212, r213 |
| raised into | initiative | request (into upstream) | 0..* | r135, r136 |
| raised for | raised request | request the initiative fulfils | | r135 |
| names | request | initiative | | r213 |
| part of / under | work-item | capability-proposal | n..1 | r74, r123, r72 |
| holds | initiative | capability-proposal | 0..*, at most one per capability | r159, r187, r148 |
| has | initiative | glossary-proposal | 0..1 implied | r161, r171 |
| of / for | capability-proposal | capability | 1 | r159 |
| wrote | integrate round | capability-proposal / glossary-proposal | | r108, r170 |
| started for | round | initiative / capability-proposal / glossary-proposal / request | | r67, r79, r141, r187, r221 |
| adds/changes/removes | capability-proposal | requirement | n..m | r145, r159, r187 |
| adds/changes/removes | glossary-proposal | term | | r171 |
| accepts | work-item | requirement / scenario | 1..* (r72 "every requirement they name") | r72, r22, r43 |
| names (check) | work-item | check | 0..* | r154 |
| blocked_by | work-item | work-item | 0..* | r63 |
| retires | work-item | deprecated scenario | 0..* | r73, r123 |
| Deprecated for | deprecated scenario | scenario | 1 | r73 |
| replacement's work-item | deprecated scenario | work-item | | r123 |
| claims | work-item | file | no two claims share a file | r20, gloss:claim |
| has branch | work-item | work-item branch | 0..1 | r4, r26, r58 |
| merges into | work-item branch | initiative branch | | r4, r61, r18 |
| has worktree | worker | worktree | 1 | r17, r20 |
| on | worktree | work-item branch | | r58 |
| has stage | work-item | stage (stage directory) | 1..* numbered k | r7 |
| is session of | stage | session | 1 | gloss:stage, r62 |
| as agent | worker | agent | 1 (r2 mapping) | r2 |
| gives | session | result | 0..1 | r128, r42 |
| names (files) | result | file | 0..* | r15 |
| has delegation | request | delegation | 0..1 | r210 |
| answered under | answer | delegation | | r78 |
| on | question | node / request line | | r129, r100 |
| reads | branch review | commit | | r27, r50 |
| belongs to | commit | work-item | 0..1 ("or none") | r156 |
| concerns | finding | work-item | | r74 |
| rests on | capability | design-decision | | r157 |
| kept on | drafts | initiative branch | | r91 |
| is of | requirement | (guarantees) capability | | r56, r64 |
| pushes to | initiative branch | remote | | r38, r54 |
| side by side | initiative | initiative (under one `work run`) | | r66, r214-r216 |

---

## 3. Events and actions
(actor is `work run` unless said; Pre = what must hold, Post = what holds after)

| action | object | pre | post | ids |
|---|---|---|---|---|
| start (delivery) | initiative / all | not started by a worker of another work run (r21); `.shop/work/` clean (r46); can start (r10) | — | r1, r66, r10, r21, r46 |
| refuse / exit with error, change nothing | delivery | cannot start / dirty `.shop/work/` / started by worker | nothing changed | r10, r21, r46 |
| push first | initiative branch | branch has commits remote lacks, at start | remote has them | r54 |
| pull through stages | work-items | — | until no work-item can transition | r1 |
| take through transitions | node | transition left node able to transition | done before end | r111 |
| start intake round | request | this context upstream; request `open`/`awaiting-upstream` | round writes outcomes/questions, `work turn` | r67 |
| write question in request | request | intake gave a question on a line | — | r100; impl before `work turn` |
| leave status | request | intake gave question | status as `work turn` wrote | r134 |
| `work start` | initiative of request | request `accepted`, no initiative fulfils it | initiative exists (proposed) | r103 |
| start integrate round | initiative | `proposed` (r79) or `started` & fulfils request & no proposal/work-item (r180); for a proposal after apply/formulate redraft (r150, r221, r186) | given accepted lines (r79, r180), other initiatives' unapplied ids (r102), questions+answers+ledger (r141) | r79, r180, r102, r141 |
| transition initiative → started | initiative | integrate round of `proposed` initiative starts | `started` | r84 |
| keep proposal status | capability-proposal | integrate round for it started | unchanged until round ends | r143 |
| keep drafts | drafts | integrate round ends | on initiative branch | r91 |
| write drafted capability-proposal | change list | integrate ends with change list; capability exists (r107) | one `drafted` proposal per capability with ids | r159, r148 |
| merge ids into existing proposal | capability-proposal | integrate for proposal names another capability already held | ids added, held ids kept | r187 |
| keep unnamed ids / terms | proposal | integrate redrafts some lines/terms | unnamed kept | r188, r189 |
| set drafted (redraft) | capability-proposal | integrate drafts anew from answers | `drafted`, earlier drafts kept | r142 |
| write drafted glossary-proposal | change list | names the glossary | `drafted` glossary-proposal | r171 |
| raise | request lines into upstream | integrate gives such lines | `work request` with fulfilled request's delegation | r135 |
| exit with error | — | integrate without change list (r96); unknown capability (r107) | no proposal written (r107) | r96, r107 |
| start gate round | capability-proposal / glossary-proposal | `drafted` | asked only for questions on its lines/terms; given drafts path | r68, r164, r168, r108, r170 |
| write questions | proposal `## Questions` | gate ended | questions; or one approval question if none | r85, r117, r173 |
| transition → awaiting-answer | proposal | gate ended | `awaiting-answer` | r69, r169 |
| start apply round | proposal | every gate question answered | given answers, drafts path | r70, r165, r108, r170; blocked by r172 |
| transition → approved | proposal | apply applied drafts | `approved` | r144, r166 |
| write adds/changes/removes | capability-proposal | apply applied | from applied change list | r145 |
| start formulate round | capability-proposal | apply applied (r146); every formulate question answered (r116) | — | r146, r116; never for glossary r167; blocked r151 |
| (apply output = nothing applied) | apply round | answers give what drafts don't hold | taken as output; new integrate started | r147, r150, r221 |
| transition → formulated | capability-proposal | formulate ended without question | `formulated` | r83 |
| (formulate nothing) | formulate round | answers change lines not in `spec/` | output; status kept; new integrate | r152, r153, r186 |
| round fault | round for proposal/initiative | error / turn limit / no result | status kept, no transition, other nodes first, exit error naming round | r86, r87, r88, r115 |
| draft work-items (`work add`) | capability-proposal | `formulated`; no raised request undelivered (r136) | one per capability in adds+changes, accepting every named requirement; `## Retires` filled (r73) | r72, r136, r73 |
| draft retiring work-item | deprecated scenarios | all initiative's work-items green/withdrawn; replacement's work-item green | one work-item under last-drafted's proposal | r123, r124 |
| draft fix work-item | branch review findings | kept review lists fix-now findings | one work-item naming findings file | r74 |
| start stage worker | work-item | status drafted/researched/ready/done; not awaiting-answer/failed (r37); blocked_by all green (r63); push verify ok (r35) | new `claude -p` session, one brief | r2, r35, r37, r63 |
| run suite first | implementer worktree | before implementer starts | brief says how it ended | r24 |
| read result / route questions | session result | session ended | questions to planner brief or `## Questions` + awaiting-answer | r129, r36 |
| next transition | node | result has no question and has output | next status | r130 |
| missing-output question | node | no question, no output | question naming output; awaiting-answer | r131 |
| merge | work-item branch → initiative branch | implementer result no question; scenarios pass; suite passes but for r43/r122 expected; flaky rerun (r219, r222) | merged, branch deleted (r18) | r4, r18, r61, r219, r222 |
| rerun once | failing scenario | failure would block r4 merge | second run alone; both runs into r131 question if fail | r219, r220 |
| keep branch | work-item branch | transition to awaiting-answer | kept; next implementer worktree on it | r26, r58 |
| write fileset | work-item | planner result gives `fileset` | `fileset:` written at → planned | r31 |
| commit transition | work-item file, stage dirs, log.jsonl | work-item transition | committed, nothing else | r7 |
| push | initiative branch | after every commit | on remote | r38 |
| append log line | log.jsonl | worker/branch reviewer starts or ends | line | r8, r49 |
| record transcript path | session.json | writing it | path | r62 |
| copy named files | stage directory | before removing worktree | copied | r15 |
| put back | `.shop/work/` file | worker changed it outside stage dir (r6, r218), not other side-by-side initiative's paths (r214, r215) | restored; work-item `failed` (r34, r218) | r6, r34, r218, r214-r216 |
| transition → failed | work-item | push verify fails (r39), git fails (r41), no readable result (r42), session error/turn limit/no JSON (r45), `.shop/work/` changed (r34, r218) | `failed`, reason recorded; exit error (r40) | r34, r39-r42, r45, r218, r40 |
| start branch review | initiative branch | all work-items green/withdrawn; an unread commit (r27); not all read (r50); has work-items (r94); retiring item drafted (r124); push verify ok (r51, r35) | runs (r154) given (r155), commits + diff (r156), files (r157) | r27, r50, r94, r124, r154-r157 |
| copy & commit review dir | branch reviewer dir | session ended | `runs/branch-review/<k>/` committed | r47, r48 |
| next branch review | initiative | fix work-item turns green | started before exit | r110 |
| `measure initiative` | initiative | all green/withdrawn, ≥1 green, kept review nothing to fix (r75); has work-item (r97); retiring item drafted (r124) | measurement | r75, r97, r124 |
| start analysis | analyzing-a-batch session | measurement written | analysis record | r76 |
| commit measurement + analysis | initiative branch | both written | committed | r106 |
| set done | initiative | r213 conjunction, or r161 glossary-only | `done`, committed | r213, r161, r109 |
| delegate question | question of initiative (not glossary-proposal) | request gives delegation | own session given delegation + named files only; answers or leaves | r210, r211, r209 |
| write answer naming delegation | answer | delegated session answered | `by` = delegation (impl) | r78 |
| transition after delegated reviewer answer | work-item | answer asks change → `ready`; accepts → `done` | | r118, r119, r120 |
| delegated session fault | question | error / turn limit / no result | unanswered; stage dir + log committed | r89, r90 |
| remove worktrees | worktrees | on exit | all removed | r33 |
| exit successfully | delivery | r212 / r82 conjunction | statuses printed | r212, r82 |
| exit with error | delivery | r101, r184, r52, r81, r40, r53, r51, r88, r96, r107, r10, r46 | printed | (listed) |
| `--work-item` option: keep/refuse/deselect/exit 0 | pytest collection | non-scenario test; none accepted & not guarantees; none accepted & all guarantees; left with no test | keep / refuse / deselect / success | r55, r56, r64, r65 |

---

## 4. Exclusivity, concurrency and limits

| rule | what runs together / waits | real resource | ids |
|---|---|---|---|
| initiatives side by side | all open initiatives concurrently under one `work run` | process scheduling across initiatives | r66 |
| one session of an initiative at a time, except r20/r59 workers | serialisation within an initiative | the initiative's files and branch (commit sequencing on initiative branch, the main checkout's `.shop/work/<initiative>/`) | r66 |
| integrate/apply/formulate rounds of different initiatives one at a time | global mutex over spec-writing rounds | `spec/` (and the drafts/requirement-id space: r102 gives integrate the ids other initiatives' drafts add) | r95, r66, r102 |
| research/plan stages of several work-items at the same time | parallel | none shared but worker slots | r59 |
| ready work-items implemented at the same time if claims share no file | parallel, each its own worktree | tracked files (claim), worktrees | r20, gloss:claim |
| at most N workers at the same time, N = delivery.toml or 4 | global counting semaphore | worker processes / cost | r60, r59, r20 |
| merges one at a time in the order implementers ended | serialise | initiative branch head | r61 |
| no nested `work run` | refuse | the repository / supervisor | r21 |
| side-by-side initiatives' `.shop/work/<other>/` paths excluded from checks, not put back, no fault | partition of the main checkout | main checkout `.shop/work/` | r214, r215, r216, r218 |
| worker may not change `.shop/work/` outside stage dir | isolation | main checkout `.shop/work/` | r6, r34, r218 |
| worktree outside plugin directory if repo inside it | isolation | filesystem / plugin dir | r23 |
| worker never changes directory | isolation | worktree | r17 |
| no bare Write/Edit; Bash limited | capability restriction | the checkout/system | r13, r14, r30 |
| researcher limit 80 turns | limit | round trips (gloss:round trip) | r19 |
| turn limit generally (unquantified) | fault condition | session round trips | r128, r86-r89, r45 |
| no worker while awaiting-answer/failed | wait | work-item | r37 |
| no worker while blocked_by not green | wait (dependency) | work-item ordering | r63 |
| no apply while glossary questions unanswered | wait | glossary-proposal | r172 (and r70/r165 positively) |
| no formulate until new integrate applied | wait | capability-proposal | r151 |
| status held during integrate | lock-like hold | capability-proposal status | r143 |
| no work-items while raised request not delivered | wait (cross-context) | capability-proposal → upstream | r136 |
| retiring work-item before branch review / measure | ordering | — | r124 |
| suite before implementer | ordering | worktree | r24 |
| runs before branch review | ordering | initiative head | r154 |
| push verify before worker/branch reviewer | ordering | remote | r35, r39, r51 |
| push after every commit | ordering | remote | r38, r54 |
| copy files before worktree removal | ordering | worktree contents | r15 |
| other nodes before fault exit | ordering | — | r115 |
| next branch review before exit | ordering | — | r110 |
| no branch review while all read / no work-item | guard | — | r50, r94 |
| no measure while no work-item | guard | — | r97 |
| rerun scenario once, alone | limit 1 retry; "alone" = no concurrency | test isolation | r219 |
| a request turn: one side writes next | turn-taking | request | r67, r101, gloss:turn |
| Not yet: "the lock", time and spending limits | explicitly absent | — | Not yet |

Note: "one session of an initiative at a time" (r66) and "integrate/apply/formulate one at a time across initiatives" (r95) are both about sessions, but r95 is really about `spec/` as a shared resource; r66's exception is really about worker slots (r60) and claims (r20).

---

## 5. Repeated qualifiers (candidate universal conditions)

| phrase | ~lines | note |
|---|---|---|
| "that `work run` started" / "`work run` started" (on a session or round) | 31 | always true of any session `work run` reacts to; candidate universal: scope of all session/round rules |
| "a round of the kind X" | ~47 occurrences in ~50 lines | type tag; could be `X round` |
| "ends in an error or at its turn limit, or leaves no result `work run` can read" | 7–8 (r128, r86, r87, r88, r115, r89, r90; r45 variant "exits with an error, or leaves output that holds no JSON result"; r42 "without a result file") | = definition of *fault* end (gloss:fault); r128 already generalises it |
| "exit with an error" (+ "naming ..." / "printing ..." / "saying why") | 12 (+r40 "naming the work-item and its fault") | exit contract; payload varies |
| "exit successfully, printing ..." | 3 (r212, r82, r65) | |
| "naming ..." | 10 | exit/question payload |
| "and change nothing" | 2 (r10, r46) | pre-start refusal |
| commit / "on the initiative branch" | ~20 mentions; "on the initiative branch" 7 | r38 universalises push after commit |
| "every work-item ... is `green` or `withdrawn`" | 7 (r75, r93, r123, r124, r27, r212, r213) | initiative "work complete" predicate |
| "kept branch review lists nothing to fix now" | 3 (r75, r213, r121 variant) | |
| "Where the request an initiative fulfils gives a delegation" | 5 (r210, r78, r118, r119, r120) | |
| "under a delegation" / "under it" | 7 | |
| "transition the work-item to `failed`, recording ..." | 6 (r34, r39, r41, r42, r45, r218) | with r40 always exit with error |
| "under the node's/proposal's/work-item's `## Questions`" + awaiting-answer | 8 | question-writing pattern |
| "within the number of workers r60 gives" | 2 (r59, r20) | could be universal for all worker starts |
| "When `work run` writes a worker's brief" | 4 (r17, r25, r44, r57) | brief contents split over lines |
| "When `work run` starts a branch review" | 4 (r154-r157) | |
| "ends having applied its drafts" | 5 (r144, r166, r167, r145, r146) | |
| "the drafts it applied do not hold" | 3 (r150, r221, r151) + r147 variant | |
| "formulates nothing because a capability-proposal's answers change lines not in `spec/`" | 3 (r186, r152, r153) | same trigger, three responses |
| "the path of the kept drafts of the round of the kind `integrate` that wrote the proposal" | 2 (r108, r170) | cap vs glossary duplicate |
| "given the accepted lines of the request it fulfils" | 3 (r79, r180, r141) | |
| "whose asker is this context ... in the asker's turn" | 3–5 (r101, r212, r82, r213) | |
| "a path under `.shop/work/<initiative>/` of another initiative that `work run` is running side by side" | 4 (r214, r215, r216, r218) | |
| "a pytest command given `--work-item <name>` collects scenarios and none that the work-item accepts" | 2 (r56, r64) | |
| "keep(s) ... status" | r86, r143, r152 (3) | |
| "first" (ordering prefix) | 6 (r54, r15, r24, r35, r154, r10 implicit) | |

Pairs that differ only by node kind (capability-proposal vs glossary-proposal) — candidates for one rule over a supertype "proposal": r68/r164, r168/r164, r108/r170, r69/r169, r117/r173, r70/r165, r144/r166, r150/r221, r188/r189, r159/r171.

---

## 6. Terms not in the glossary; inconsistent use and synonyms

### 6.1 Used, not defined in the glossary
- **initiative** (no glossary entry at all, though it has statuses in gloss:status), **capability-proposal** (none), **node** (used r111, r129-r131, r212, r81; gloss:status mentions "a node's place" without defining node), **capability**, **design-decision**, **bounded context / this context** (Purpose, r67), **upstream / asker** (only inside gloss:request), **change list** (r132, r159...), **drafts / kept drafts** (r91, r102, r108), **drafts path** (only in gloss:round), **kind** (of a round), **intake / integrate / gate / apply / formulate** as round kinds, **branch review** (only inside gloss:review), **branch reviewer**, **findings / findings to fix now / findings file** (r74, r121), **plan** (r132, r157), **researcher / planner / implementer / reviewer** as roles (gloss:hand-back mentions implementer only), **answering session**, **output** (of a stage; r130-r132 — gloss:outcome exists, output does not), **turn limit** (vs gloss:round trip / `--max-turns`), **main checkout** (r46, r214, r218), **worktree** (no entry; used in brief, work-item branch), **base / head** of initiative branch (base only in gloss:initiative branch), **push verification** (r35, r51, r39 "the verification"), **side by side** (r66, r214), **fulfils** (r79), **raise / raised** (r135, r136), **accepted lines** (r79), **accepts** (work-item → requirement; in gloss:work-item only), **retires / `## Retires` / replacement** (r73, r123; gloss:deprecated scenario has "replacement"), **`blocked_by`** (r63), **`fileset`** (r31 — glossary *forbids* "fileset" as a synonym of file set, but r31 uses it as the result key), **`work add`, `work start`, `work request`, `work turn`, `measure initiative`** (commands), **analysis record**, **`analyzing-a-batch`** (a skill, named as "a session of"), **log.jsonl** (only in gloss:transition), **session.json**, **transcript**, **agent names** (code-scout etc.), **the person** (narrator), **the whole suite** vs gloss:suite, **expected (failing)** (r43, r122), **pass/fail of a scenario run**, **`initiative-round`** (agent), **fault** used as verb "fault no session" (r216).

### 6.2 Inconsistent use / synonyms
- **stage kinds**: "research, plan, implementation and review" (r1, gloss:stage) vs roles "researcher, planner, implementer, reviewer" (r129, r132) vs agents (r2) vs statuses (drafted/researched/ready/done) — three namings of one thing; "implementation" (noun) vs "implemented" (r20) vs "implementer".
- **session vs stage vs worker vs round**: r66 "one session of an initiative", r128 "a session that work run started for ... a question", r129-r131 "its stage's questions/output" applied to all sessions incl. rounds; gloss:stage includes rounds and answering sessions but r2/r8 use stage only for worker stages; branch reviewer is "not a worker" (gloss) yet r35 lists "a worker or the branch reviewer" and r49 gives it a "stage `branch-review`".
- **round end vocabulary**: "ends", "gives", "ends with", "ends without", "gives in its result", "applies nothing", "formulates nothing", "drafts anew", "redrafts" — the same event (round result read) under many verbs.
- **"gives"** is overloaded: a result gives (r129), a request gives a delegation (r210), delivery.toml gives (r29, r60), r60 gives a number (r59), a round gives questions (r100), a round gives lines into an upstream (r135).
- **"kept"**: kept drafts (r91), kept branch review (r27, r74 — meaning "copied and committed" r47-48?), kept work-item branch (r26), keep status (r86), "kept in this context" for a request (r213), keep ids (r187) — six senses.
- **"take"**: take through transitions (r66, r111), take as fault (r128), take as output (r147, r153, r185), take as passing (r222), take as listing nothing (r121).
- **"answer"**: an answer to a question; "an answer that asks for a change" (r118); "answers give what its drafts do not hold" (r147) vs "an answer that the drafts it applied do not hold" (r150) — same condition worded two ways.
- **awaiting-asker** status vs "in the asker's turn" (r101, r212) — status and turn both used.
- **fault** (gloss: failure outside a session's work) vs **failed** status vs "ends in an error" vs r128 "take the session's end as a fault" — fault for rounds keeps status (r86) while for work-items it transitions to failed (r45): same event, different effect by node kind.
- **verification**: "push verification" (r51), "the verification before a worker starts" (r39), "verify that it can push" (r35).
- **"the initiative"** without antecedent in r59, r212 (`work run` with initiative mode assumed) vs r81/r82 for no-initiative mode.
- **file set / fileset / file set of a researcher** (r19 given to researcher; r132 researcher outputs one; r31 planner's `fileset`).
- **scenario / requirement** linkage: "a scenario of a requirement" (r73), "scenario whose requirement" (r43), "accepted scenarios" (r19) vs "requirement it accepts" (r56).
- **glossary vs `spec/index.md`**: both used (r161, r171).
- **capability-proposal "part of" vs "under"** (r74 both).
- **status of a branch review** (r121 "whatever its status") — branch reviews have no status in gloss:status.
- **"done"** for work-item status and initiative status and "what it delivers is closed" (Purpose).
- **turn** (gloss: request side) vs **turn limit** (session round trips) — same word, two concepts.

---

## 7. Lines packing several rules

| id | rules | what's packed |
|---|---|---|
| r66 | 5 | scope (every non-done/abandoned initiative); every transition; initiatives side by side; one session per initiative at a time except r20/r59; r95 rounds one at a time |
| r213 | 7 | done condition: not done; ≥1 green; all green/withdrawn; every proposal formulated/withdrawn; kept review nothing to fix; measurement+analysis committed; every own request naming it delivered |
| r132 | 9 | output definition per stage kind (9 kinds) |
| r212 | 5 | four-part exit condition + printing |
| r82 | 4 | no-initiative mode, no transition, none awaiting/failed, no asker-turn request + print |
| r81 | 3 | mode, no transition, one awaiting/failed → exit error + print |
| r210 | 5 | delegation scope excludes glossary questions; one session per question; given delegation + named files only ("nothing else"); answers if covered; leaves otherwise; "whatever words it uses" |
| r129 | 3 | researcher's questions → planner brief; others → `## Questions`; transition awaiting-answer |
| r131 | 2 | write missing-output question; transition awaiting-answer |
| r4 | 3 | merge condition: no question; scenarios pass; suite passes modulo r43 |
| r2 | 4 | status→agent mapping; new `claude -p` session; one brief; brief contents |
| r14 | 3 | Bash allowed: pytest, plugin scripts by path, needed git |
| r20 | 3 | parallel implement when claims disjoint; own worktree each; within r60 |
| r59 | 3 | research/plan in parallel; when >1 drafted/researched; within r60 |
| r60 | 2 | max = toml value; default 4 |
| r61 | 2 | one at a time; in order ended |
| r72 | 3 | draft with `work add`; one per capability in adds+changes; accepts every named requirement |
| r123 | 4 | trigger (all green/withdrawn + replacement green, any initiative); one work-item; under last-drafted's proposal; retires each such scenario |
| r124 | 2 | ordering before branch review and before measure |
| r74 | 3 | one work-item; naming findings file; under proposal of concerned work-item |
| r75 | 3 | conjunction (all green/withdrawn, ≥1 green, nothing to fix) → measure |
| r27 | 4 | all green/withdrawn; unread commit other than review's own; start bdd-branch-reviewer; over branch from base, one brief |
| r154 | 7 | runs: suite, each work-item's scenarios, each check, tools check, tools size, features deprecated, features bindings; at head |
| r155 | 4 | each run with command, exit, output, commit |
| r156 | 3 | commits base→head; each with work-item or none; diff less `.shop/` |
| r157 | 3+ | capabilities, their design-decisions, per work-item plan/report/findings |
| r7 | 2 | commit these three things; nothing else |
| r8 | 2 | on start and end; five fields |
| r25 | 4 | brief names scripts dir, base, worktree, branch |
| r44 | 2 | write result first as PARTIAL; keep it current |
| r34 | 3 | transition failed; record files; branch unmerged |
| r218 | 4 | exclusion of other initiatives' paths; compare to last commit at worker end; put back; failed naming files |
| r45 | 3 end conditions | error / turn limit / exits with error / no JSON → failed recording |
| r128 | 3 | three end conditions → fault, "whatever its result says" |
| r86/r87/r88/r115 | 1 each (same trigger, 4 consequences split) | already split |
| r88 | 2 | exit error; naming round and how it ended |
| r135 | 3 | raise with `work request`; raised for fulfilled request; with its delegation |
| r141 | 4 | give questions, answers, ledger, accepted lines |
| r142 | 2 | set drafted; earlier drafts kept |
| r159 | 2 | one proposal per capability; with added/changed/removed ids |
| r187 | 2 | add ids to existing proposal; keep held ids |
| r107 | 2 | write no proposal; exit with error naming capability |
| r68 | 3 | gate as questions; each a decision with readings; recommended marked |
| r67 | 3 | start intake given request; writes outcome/question per line; passes turn |
| r161 | 3-part trigger | glossary-only, approved, committed → done |
| r30 | 2 | replace allowed_tools; less bare Write/Edit |
| r23 | 1 conditional | — |
| r19 | 3 | file set; accepted scenarios; 80-turn limit |
| r10 | 3 | exit error; say why; change nothing |
| r46 | 3 | exit error; naming; change nothing |
| r51 | 2 | exit error saying why; no branch review |
| r184, r101, r52 | 2 each | exit error + print payload |
| r219 | 3 | rerun once; alone; before refusing merge |
| r90 | 2 | commit stage dir and log lines |
| r211 | 2 | at that moment; before or after start |
| r120 | 1 (a rule on the session, not on `work run`) | subject is "the session", unlike the rest |
| r55, r56, r64, r65 | 1–2 each | subject is "the option"/"the command", not `work run` |

Also: Purpose paragraph packs ~12 responsibilities in one sentence (intake, `work start`, integrate, keep drafts, write proposals, gate/apply/formulate, draft and deliver, fresh worker per stage, read result, write status, measurement+analysis commit, set done).
