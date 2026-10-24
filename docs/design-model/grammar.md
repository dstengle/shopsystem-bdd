# The grammar, formally

Version 4, 2026-10-24. A machine-checkable statement of
`design-model.md`: the schema of the graph, the integrity constraints,
the lifecycles, and the sentence forms that map to facts. Notation:
Datalog (Soufflé dialect). A `v_` relation must be empty; a `w_`
relation is reported, not refused. Rules and relations marked
*(new in v4)* have no counterpart in version 3; the plugin's
`model check` does not hold them yet.

## 1. Vocabulary

```
.type Id <: symbol
.decl node(id: Id, kind: symbol)

.decl standing(kind: symbol)   .decl root(kind: symbol)   .decl part(kind: symbol)   .decl record(kind: symbol)   .decl origin(kind: symbol)

standing("product-vision").  standing("job").  standing("bounded-context").  standing("context-seam").
standing("capability").  standing("capability-requirement").  standing("acceptance-scenario").  standing("design-decision").

root("initiative").             // a bounded-context's root
root("job-thread").             // the product level's root (a part in v3)

part("job-proposal").  part("map-proposal").  part("vision-proposal").
part("capability-proposal").  part("map-escalation").  part("work-item").

node(_, "request").             // neither standing, root, part nor record: the one node that crosses a seam (new in v4)

record("observation").  record("measurement").  record("review-finding").  record("decision-argument").  record("initiative-archive").
origin("observation").  origin("measurement").  origin("review-finding").
```

Attributes read from frontmatter:

```
.decl narrator(id: Id, who: symbol)             // capability, job; a role from a job, never a bounded-context
.decl group(c: Id, g: symbol)                   // model | service | operations | guarantees
.decl external(ctx: Id)
.decl at(n: Id, ctx: Id)                        // the bounded-context (or "product") a root, part or request is kept by (new in v4)
.decl status(id: Id, s: symbol)                 // roots, parts and requests
.decl ikind(i: Id, k: symbol)                   // initiative: capability-change | defect
.decl wkind(w: Id, k: symbol)                   // work-item: capability | guarantee | enabling
.decl priority(x: Id, rank: number)             // requests and job-threads
.decl summary(d: Id, text: symbol)              // design-decision; required
.decl revisit_signal(d: Id, sig: symbol)        // "requests" | a measurement id
.decl req_id(q: Id, c: Id, n: number)            // capability-requirement q is [r<n>] of capability c
.decl retired_id(c: Id, n: number)              // ids a capability has used and retired
.decl fileset(w: Id, path: symbol)
.decl escalation(e: Id, why: symbol)            // no-seam | pattern-change | refused-still-needed | seam-decision-revisited
.decl asker(q: Id, x: Id)                       // request: a bounded-context or "product"; the upstream itself when internal (new in v4)
.decl upstream(q: Id, x: Id)                    // request: the bounded-context asked (new in v4)
.decl line(q: Id, n: number, text: symbol)      // request: the asker's proposed line, strict EARS (new in v4)
.decl outcome(q: Id, n: number, o: symbol)      // request line: accepted | rewritten | refused | question | withdrawn (new in v4)
```

## 2. Edge schema

| relation | domain → range | cardinality | class | written by |
|---|---|---|---|---|
| `orders(V, J)` | product-vision → job | 0..n | standing | hand |
| `in(C, X)` | capability → bounded-context | exactly 1 | standing | hand |
| `seam(R, Up, Down)` | context-seam → bounded-context, bounded-context | exactly 1 pair | standing | hand |
| `pattern(R, P)` | context-seam → symbol | exactly 1 | standing | hand |
| `pins(Down, Up, V)` | bounded-context → bounded-context, version | 0..1 per seam | standing | hand |
| `has_req(C, Q)` | capability → capability-requirement | 1..n | standing | hand |
| `has_sc(Q, S)` | capability-requirement → acceptance-scenario | 0..n (1..n unless guarantees) | standing | formulation |
| `rests_on(C, D)` | capability → design-decision | 0..n | standing | hand |
| `supersedes(D2, D1)` | design-decision → design-decision | 0..1 | standing | hand |
| `serves(C, J)` | capability → job | 0..n | standing | **script** |
| `using(C, J, D)` | (capability, job) → capability | 0..n | standing | **script** |
| `depends_on(C, D)` | capability → capability | derived | standing | **derived** |
| `source(X, Rec)` | initiative \| request \| job-thread → origin | 0..n | intake | hand |
| `part_of(P, X)` | part → part \| root; request → job-thread | exactly 1 for a part; 0..1 for a request | breakdown | the part's creator |
| `fulfils(I, Q)` | initiative → request | exactly 1 *(new in v4)* | breakdown | the upstream |
| `raises(W, Q)` | work-item → request | 0..n *(new in v4)* | part | the asker |
| `raised_for(Q, Q0)` | request → request | 0..1 *(new in v4)* | request | the asker |
| `of_job(T, J)` | job-thread → job | exactly 1 | root | hand |
| `enters(T, X)` | job-thread → bounded-context | exactly 1 | root | hand |
| `crosses(T, R)` | job-thread → context-seam | 0..n | root | hand |
| `resolution(Q, Rq, V)` | request → capability-requirement, version | 0..n, one per accepted line | request | the upstream |
| `argues(P, A)` | *-proposal → capability \| job \| bounded-context \| context-seam \| product-vision | 1..n | part | hand |
| `adds(P, Q)`, `changes(P, Q)`, `removes(P, Q)` | capability-proposal → capability-requirement | 0..n each | part | hand |
| `under(W, C)` | work-item → capability | 0..1 | part | drafter |
| `for(W, W2)` | work-item → work-item | 0..1 | part | drafter |
| `accepts(W, S)` | work-item → acceptance-scenario | 0..n | part | drafter |
| `check(W, Cmd)` | work-item → symbol | 0..1 | part | drafter |
| `blocked_by(W, W2)` | work-item → work-item | 0..n | part | drafter |
| `wi_depends(W, D)` | work-item → capability | 0..n | part | planner |
| `about(Rec, A)` | record → standing | exactly 1 | record | hand |

Gone from version 3: `needs`, `from_cap` and `across`. A request carries
its asker and the asker's request id, not the capability that asked; the
seam is the one between `asker` and `upstream`.

## 3. Derivations

```
depends_on(C, D)      :- using(C, _, D).
path(J, C, D)         :- using(C, J, D).
path(J, C, E)         :- path(J, C, D), using(D, J, E).
cap_of_wi(W, C)       :- under(W, C).
cap_of_wi(W, C)       :- for(W, W2), cap_of_wi(W2, C).
top(P, I)             :- part_of(P, I), node(I, K), root(K).
top(P, I)             :- part_of(P, P2), top(P2, I).
raised(I, Q)          :- raises(W, Q), top(W, I).                       // new in v4
reaches(Q, T)         :- part_of(Q, T), node(T, "job-thread").          // new in v4
reaches(Q, T)         :- raised_for(Q, Q0), reaches(Q0, T).
traced(Q)             :- reaches(Q, _).
traced(Q)             :- node(Q, "request"), source(Q, _).
traced(Q)             :- raised_for(Q, Q0), traced(Q0).
internal(Q)           :- asker(Q, X), upstream(Q, X).
closed(P)             :- status(P, S), (S = "merged" ; S = "formulated" ; S = "ruled" ; S = "green").
line_final(Q, N)      :- outcome(Q, N, O), (O = "accepted" ; O = "refused" ; O = "withdrawn").
```

v3's `root(P, I)` is `top(P, I)` here, since `root` now names the kinds.

## 4. Integrity constraints

Numbered as `design-model.md` §4.

```
// 1. retired in v4: needs is gone

// 2. standing edges only between standing artifacts (one clause per relation; two shown)
v2(C, J) :- serves(C, J),   (node(C, K), !standing(K) ; node(J, K2), !standing(K2)).
v2(C, D) :- rests_on(C, D), (node(C, K), !standing(K) ; node(D, K2), !standing(K2)).

// 3. a resolution names a capability-requirement, never a scenario (v4: replaces the needs clauses)
v3(Q, X) :- resolution(Q, X, _), !node(X, "capability-requirement").

// 4. depends_on is derived
v4(C, D) :- authored_depends_on(C, D), !using(C, _, D).

// 5. using points the way the pin points across a seam
v5(C, D) :- using(C, _, D), in(C, X), in(D, Y), X != Y, !pins(X, Y, _).

// 6. crossings reference seams; mapped only then
v6(T, R) :- crosses(T, R), !node(R, "context-seam").
v6b(T)   :- status(T, "mapped"), crosses(T, R), !node(R, "context-seam").

// 7. a request between two contexts is across a seam between them; upstream names no client
v7(Q)     :- asker(Q, X), upstream(Q, Y), X != Y, X != "product", !seam(_, Y, X), !seam(_, X, Y).
v7c(U, D) :- in(U, X), in(D, Y), pins(Y, X, _), standing_edge(U, D).

// 8. a work-item names a capability, directly or through for:
v8(W) :- node(W, "work-item"), !cap_of_wi(W, _).

// 9. every part has exactly one part_of reaching a root; priority and source only where allowed
v9a(P) :- node(P, K), part(K), !part_of(P, _).
v9b(P) :- part_of(P, A), part_of(P, B), A != B.
v9c(P) :- node(P, K), part(K), !top(P, _).
v9d(X) :- priority(X, _), !node(X, "request"), !node(X, "job-thread").
v9e(X) :- source(X, _),   node(X, K), part(K).
v9f(I) :- part_of(I, _),   node(I, K), root(K).
po_tc(A, B) :- part_of(A, B).
po_tc(A, C) :- po_tc(A, B), part_of(B, C).
v9g(P) :- po_tc(P, P).

// 10. only an origin is a source; records are about standing artifacts
v10a(X, Rec) :- source(X, Rec), node(Rec, K), !origin(K).
v10b(Rec)    :- node(Rec, K), record(K), !about(Rec, _).
v10c(Rec)    :- about(Rec, A), node(A, K), !standing(K).

// 11. one narrator per capability
v11(C) :- node(C, "capability"), !narrator(C, _).
v11(C) :- narrator(C, N1), narrator(C, N2), N1 != N2.

// 12. design-decisions: summary present; supersedes acyclic
v12a(D) :- node(D, "design-decision"), !summary(D, _).
sup_tc(A, B) :- supersedes(A, B).
sup_tc(A, C) :- sup_tc(A, B), supersedes(B, C).
v12b(D) :- sup_tc(D, D).

// 13. a watch condition has a reader
v13(D) :- revisit_signal(D, Sig), Sig != "requests", !node(Sig, "measurement").

// 15. requirement ids: present, unique within the capability, never reused; references by id
v15a(Q)     :- node(Q, "capability-requirement"), !req_id(Q, _, _).
v15b(Q1,Q2) :- req_id(Q1, C, N), req_id(Q2, C, N), Q1 != Q2.
v15c(Q)     :- req_id(Q, C, N), retired_id(C, N).
v15d(Q, C)  :- req_id(Q, C, _), !has_req(C, Q).
v15e(P, Q)  :- changes(P, Q), !has_req(_, Q).
v15f(P)     :- status(P, "formulated"), (adds(P, Q) ; changes(P, Q)), !has_sc(Q, _), has_req(C, Q), !group(C, "guarantees").

// 16. (new in v4) an initiative fulfils exactly one request, of its own context; a request has at most one initiative
v16a(I)    :- node(I, "initiative"), !fulfils(I, _).
v16b(I)    :- fulfils(I, Q1), fulfils(I, Q2), Q1 != Q2.
v16c(Q)    :- fulfils(I1, Q), fulfils(I2, Q), I1 != I2.
v16d(I, Q) :- fulfils(I, Q), at(I, X), upstream(Q, Y), X != Y.

// 17. (new in v4) every request is part of a job-thread or cites an origin, or is raised for one that is
v17(Q) :- node(Q, "request"), !traced(Q).

// 18. (new in v4) part_of never crosses a seam; a request is part of a job-thread only and has no parts; no other id crosses
v18a(P, X) :- part_of(P, X), node(P, K), part(K), at(P, C1), at(X, C2), C1 != C2.
v18b(Q, X) :- part_of(Q, X), node(Q, "request"), !node(X, "job-thread").
v18b(P, Q) :- part_of(P, Q), node(Q, "request").
v18c(A, B) :- (blocked_by(A, B) ; for(A, B)), at(A, C1), at(B, C2), C1 != C2.

// initiative kinds fix the first part (v_k1 and v_k2, for job and job-path, are gone in v4)
v_k3(I) :- ikind(I, "capability-change"), part_of(P, I), !node(P, "capability-proposal").
v_k4(I) :- ikind(I, "defect"),            part_of(P, I), !node(P, "work-item").
v_k5(I) :- node(I, "initiative"), part_of(P1, I), part_of(P2, I), P1 != P2.     // one first part

// breakdown shape: work-items only under capability-proposals (or a defect initiative); a job-thread owns neither
v_b1(W) :- node(W, "work-item"), part_of(W, X), !node(X, "capability-proposal"), !(node(X, "initiative"), ikind(X, "defect")).
v_b3(P) :- part_of(P, T), node(T, "job-thread"), (node(P, "capability-proposal") ; node(P, "work-item")).

// scenarios: exactly one requirement each; every requirement tested unless guarantees
v_s1(S) :- node(S, "acceptance-scenario"), !has_sc(_, S).
v_s2(S) :- has_sc(Q1, S), has_sc(Q2, S), Q1 != Q2.
v_s3(Q) :- has_req(C, Q), !has_sc(Q, _), !group(C, "guarantees").

// work-items: blocked_by acyclic; ready only when unblocked; claimed file sets disjoint; acceptance present
blk_tc(A, B) :- blocked_by(A, B).
blk_tc(A, C) :- blk_tc(A, B), blocked_by(B, C).
v_w1(W)      :- blk_tc(W, W).
v_w2(W)      :- status(W, "ready"), blocked_by(W, B), !status(B, "green").
v_w3(W1, W2) :- status(W1, "claimed"), status(W2, "claimed"), W1 < W2, fileset(W1, P), fileset(W2, P).
v_w4(W)      :- node(W, "work-item"), !accepts(W, _), !check(W, _).

// 19. done-ness through requests only (v_d1 extended; v_d2-v_d4 new in v4)
v_d1(I) :- status(I, "done"), top(P, I), !closed(P).
v_d1(I) :- status(I, "done"), raised(I, Q), !status(Q, "delivered").
v_d2(T) :- status(T, "built"), part_of(Q, T), node(Q, "request"), !status(Q, "delivered").
v_d3(Q) :- status(Q, "delivered"), fulfils(I, Q), !status(I, "done").
v_d4(Q, N) :- status(Q, "delivered"), outcome(Q, N, "accepted"), line(Q, N, _), !resolution_of_line(Q, N).
```

`resolution_of_line(Q, N)` holds when the resolution names line N's
requirement; how a line is tied to its requirement id is the upstream
tool's.

Warnings:

```
w_unserved_cap(C)   :- node(C, "capability"), !serves(C, _), node(_, "job").
w_unserved_job(J)   :- node(J, "job"), !serves(_, J), !of_job(_, J).
w_seam_unused(R)    :- seam(R, Up, Down), !(in(C, Down), in(D, Up), depends_on(C, D)).
w_uncited_obs(O)    :- node(O, "observation"), !source(_, O).
w_many_requests(X)  :- N = count : { upstream(Q, X), status(Q, "open") }, N > 5.
w_stale_intake(Q)   :- status(Q, "accepted"), !fulfils(_, Q), age(Q, Days), Days > 90.
```

## 5. Lifecycles

Transitions not listed are violations; guards are queries that must hold.

**request** *(new in v4)*: `open` (the asker, through the upstream's
tool; lines in strict EARS) → `awaiting-asker` (the upstream wrote an
outcome for every line and some line is not final) ⇄ `awaiting-upstream`
(the asker answered, revised, withdrew or confirmed) → `accepted` (every
line final, `line_final`, and one accepted) | `refused` (every line
final, none accepted). `withdrawn` (the asker, as a whole) from any
status before `accepted`. `accepted → delivered` (no `v_d3`, no `v_d4`).
Line outcomes: `accepted` as written; `rewritten` (the rewrite shown;
`accepted` once the asker confirms it still meets its need); `refused`
(with the reason); `question` (with its readings); `withdrawn` (the
asker).

**initiative**: `proposed` (its request `accepted`; no `v16`) →
`started` (owner; a first part exists) → `done` (no `v_d1`) |
`abandoned`. On `done`: archive; measure; its request may be delivered.

**job-thread**: `proposed → mapped` (no `v6b`) → `accepted` (the person)
→ `built` (no `v_d2`; the entry scenario green). On a request's
`delivered`, the upstream writes `serves … using` on its own capabilities
for the job the request reaches, from its work-items' `wi_depends`.

**capability-proposal**: `drafted → approved` (the person, on the ids in
`adds`, `changes`, `removes`) → `merged` (the requirements present with
those ids; removed ids retired) → `formulated` (no `v15f`). The product
proposals: `drafted → approved → merged`.

**map-escalation**: `open → ruled` (product role; a map-proposal or a
ruling recorded).

**work-item**: as the model's §3; `planned → awaiting-ruling → planned`
on a question; `ready → claimed` only when no `v_w3` would result;
`done → green` on a clean review or the initiative's branch review.

## 6. Sentence forms

```
statement = standing_stmt | root_stmt | request_stmt | part_stmt | record_stmt ;

standing_stmt =
    CAP "serves" JOB "using" ( CAPLIST | "nothing" )            → serves, using
  | CAP "has requirement" RID ":" TEXT ("formulated as" SCEN)?  → has_req, req_id, has_sc
  | CAP "rests on" DECLIST                                       → rests_on
  | DEC "supersedes" DEC                                         → supersedes
  | DEC ":" SUMMARY ("revisit when" TEXT ("signal" SIG)?)?       → summary, revisit_signal
  | CTX "pins" CTX "at" VER                                      → pins
  | "seam" CTX "–" CTX "is" PATTERN                              → seam, pattern
  | "the product-vision orders" JOB "before" JOB                 → orders
  | "job" JOB ":" "when" TEXT "," NARR "wants" TEXT              → node(JOB,"job"), narrator
  ;

root_stmt =
    "initiative" I "(" IKIND ")" "in" CTX "fulfils" REQ ":" SUMMARY ("; sources" RECLIST)?
                                                                 → ikind, at, fulfils, source
  | "job-thread" T "of" JOB "enters" CTX ("crosses" SEAM)* "; priority" N ("; sources" RECLIST)?
                                                                 → of_job, enters, crosses, priority, source
  ;

request_stmt =
    "request" REQ "from" ASKER "to" CTX ( ", part of" T | ", raised for" REQ | "; sources" RECLIST ) ":" LINELIST
                                                                 → asker, upstream, part_of | raised_for | source, line
  | "line" REQ "#" N "is" OUTCOME (":" TEXT)?                    → outcome
  | "request" REQ "is" RSTATUS                                   → status
  | "request" REQ "is resolved by" RID "at" VER ("," RID "at" VER)*
                                                                 → resolution
  ;

part_stmt =
    "job-proposal" P "argues job" JOB ", part of" X              → argues, part_of
  | "capability-proposal" P "argues" CAP ("adds" REQLIST)? ("changes" REQLIST)? ("removes" REQLIST)? ", part of" X
                                                                 → argues, adds, changes, removes, part_of
  | "map-escalation" E WHY ", part of" X                         → escalation, part_of
  | "work-item" W "is" WKIND ("accepts" SCENLIST | "check" TEXT) ("blocked by" WLIST)?
                 ("depends on" CAPLIST)? ("for" W2)? ("raises" REQLIST)? ", part of" X
                                                                 → wkind, accepts|check, blocked_by, wi_depends, for, raises, part_of
  ;

record_stmt =
    "observation" O "about" ANY ":" TEXT                         → node(O,"observation"), about
  ;

IKIND = "capability-change" | "defect" ;
ASKER = CTX | "the product level" | "itself" ;
OUTCOME = "accepted" | "rewritten" | "refused" | "a question" | "withdrawn" ;
RSTATUS = "open" | "awaiting-asker" | "awaiting-upstream" | "accepted" | "delivered" | "refused" | "withdrawn" ;
LINELIST = LINE (";" LINE)* ;   LINE = EARS ;
CAP = CTX "/" NAME ;   RID = CAP "#r" DIGITS ;   REQLIST = RID ("," RID)* ;   REQ = CTX "/q" DIGITS ;   SCEN = '"' TEXT '"' ;
```

`EARS` is the strict form `model check` already holds for proposed lines
(one of EARS's patterns, one "shall", one sentence: `v_e1`, `v_e2`).

Refusals, as the checker sees them:

| sentence | parses to | fails |
|---|---|---|
| *request Q … needs TEXT* | no production | parse error (v4: `needs` is gone) |
| *initiative I (job) …* | no production | parse error (v4: a job is a job-thread) |
| *initiative I (capability-change) in account* with no "fulfils" | no production | parse error; as facts, v16a |
| *request Q from shopping to account* with no thread, request or sources | `traced(Q)` absent | v17 |
| *capability-proposal P (kept by account) … part of request Q* | `part_of(P, Q)` | v18b: a request has no parts |
| *work-item account/… part of capability-proposal P* where P is shopping's | `part_of(W, P)` across contexts | v18a |
| *request Q from shopping to sharing* (no such seam) | `asker`, `upstream` | v7 |
| *request Q is resolved by "saving follows the shopper…"* (a scenario) | `resolution(Q, S, V)` | v3 |
| *work-item W serves JOB* | no production | parse error |
| *CAP depends on X* with no `using` | `authored_depends_on` | v4 |
| *work-item W … part of job-thread T* | `part_of(W, T)` | v_b1, v_b3 |
| *initiative I … part of X* | `part_of(I, X)` | v9f |
| *initiative I sources decision-argument A* | `source(I, A)` | v10a |
| *catalog/item-lookup serves J using shopping/saved-items* | `using` against the pin | v5 |
| *job-thread T crosses shopping–sharing* (no such seam) | `crosses(T, r)` | v6 |
| *capability-proposal P changes "When a signed-in shopper saves…"* (by text) | no production | parse error |
| *capability-proposal P adds r3* where r3 is retired | `adds(P, Q)`, `req_id(Q, C, 3)` | v15c |

## 7. Tooling

- **§2** as kb types: each relation a `ref` with `targets` and
  `cardinality`; kb refuses dangling and wrong-typed references at write
  time, which covers v6, v8's first half, v9a/b, v10b and the structural
  rows for free.
- **§3–4** as a Datalog program over facts exported from frontmatter, or
  as SQL recursive CTEs against kb's SQLite; run in CI and at every
  transition in §5. The plugin's `model check` (`scripts/model.lp`) is
  such a program; it holds the version 3 rules until a later release
  implements these.
- **§5** as the `status` field's allowed values plus one guard query per
  transition, enforced by the scripts that move roots, parts and
  requests.
- **§6** as a parser of a few hundred lines; `ecommerce-example.md` should
  be run through it, not read.
- If the store becomes RDF: §2 is SHACL shapes, §4 is SHACL-SPARQL, and
  kb's IRIs are already the node ids.
