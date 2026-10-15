# The grammar, formally

Version 3, 2026-10-15. A machine-checkable statement of
`design-model.md`: the schema of the graph, the integrity constraints,
the lifecycles, and the sentence forms that map to facts. Notation:
Datalog (Soufflé dialect). A `v_` relation must be empty; a `w_`
relation is reported, not refused.

## 1. Vocabulary

```
.type Id <: symbol
.decl node(id: Id, kind: symbol)

.decl standing(kind: symbol)   .decl part(kind: symbol)   .decl record(kind: symbol)   .decl origin(kind: symbol)

standing("product-vision").  standing("job").  standing("bounded-context").  standing("context-seam").
standing("capability").  standing("capability-requirement").  standing("acceptance-scenario").  standing("design-decision").

node(_, "initiative").          // the root kind; neither standing nor part

part("job-proposal").  part("map-proposal").  part("vision-proposal").  part("job-thread").
part("capability-proposal").  part("cross-context-request").  part("map-escalation").  part("work-item").

record("observation").  record("measurement").  record("review-finding").  record("decision-argument").  record("initiative-archive").
origin("observation").  origin("measurement").  origin("review-finding").
```

Attributes read from frontmatter:

```
.decl narrator(id: Id, who: symbol)             // capability, job
.decl group(c: Id, g: symbol)                   // model | service | operations | guarantees
.decl external(ctx: Id)
.decl status(id: Id, s: symbol)                 // initiatives and parts
.decl ikind(i: Id, k: symbol)                   // initiative: job | job-path | capability-change | defect
.decl wkind(w: Id, k: symbol)                   // work-item: capability | guarantee | enabling
.decl priority(i: Id, rank: number)             // initiatives only
.decl summary(d: Id, text: symbol)              // design-decision; required
.decl revisit_signal(d: Id, sig: symbol)        // "requests" | a measurement id
.decl req_id(q: Id, c: Id, n: number)            // capability-requirement q is [r<n>] of capability c
.decl retired_id(c: Id, n: number)              // ids a capability has used and retired
.decl fileset(w: Id, path: symbol)
.decl escalation(e: Id, why: symbol)            // no-seam | pattern-change | refused-still-needed | seam-decision-revisited
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
| `source(I, Rec)` | initiative → origin | 0..n | intake | hand |
| `part_of(P, X)` | part → part \| initiative | exactly 1 | breakdown | the part's creator |
| `of_job(T, J)` | job-thread → job | exactly 1 | part | hand |
| `enters(T, X)` | job-thread → bounded-context | exactly 1 | part | hand |
| `crosses(T, R)` | job-thread → context-seam | 0..n | part | hand |
| `needs(P, C)` | job-thread \| cross-context-request → capability | 1..n | part | hand |
| `from_cap(Q, C)` | cross-context-request → capability | exactly 1 | part | hand |
| `across(Q, R)` | cross-context-request → context-seam | exactly 1 | part | hand |
| `resolution(Q, Rq)` | cross-context-request → capability-requirement | 0..1 | part | upstream |
| `argues(P, A)` | *-proposal → capability \| job \| bounded-context \| context-seam \| product-vision | 1..n | part | hand |
| `adds(P, Q)`, `changes(P, Q)`, `removes(P, Q)` | capability-proposal → capability-requirement | 0..n each | part | hand |
| `under(W, C)` | work-item → capability | 0..1 | part | slicer |
| `for(W, W2)` | work-item → work-item | 0..1 | part | slicer |
| `accepts(W, S)` | work-item → acceptance-scenario | 0..n | part | slicer |
| `check(W, Cmd)` | work-item → symbol | 0..1 | part | slicer |
| `blocked_by(W, W2)` | work-item → work-item | 0..n | part | slicer |
| `wi_depends(W, D)` | work-item → capability | 0..n | part | planner |
| `about(Rec, A)` | record → standing | exactly 1 | record | hand |

## 3. Derivations

```
depends_on(C, D)      :- using(C, _, D).
path(J, C, D)         :- using(C, J, D).
path(J, C, E)         :- path(J, C, D), using(D, J, E).
cap_of_wi(W, C)       :- under(W, C).
cap_of_wi(W, C)       :- for(W, W2), cap_of_wi(W2, C).
root(P, I)            :- part_of(P, I), node(I, "initiative").
root(P, I)            :- part_of(P, P2), root(P2, I).
closed(P)             :- status(P, S), (S = "merged" ; S = "built" ; S = "delivered" ; S = "ruled" ; S = "green" ; S = "refused").
```

## 4. Integrity constraints

Numbered as `design-model.md` §4.

```
// 1. needs only on parts
v1(X) :- needs(X, _), node(X, K), !part(K).

// 2. standing edges only between standing artifacts (one clause per relation; two shown)
v2(C, J) :- serves(C, J),   (node(C, K), !standing(K) ; node(J, K2), !standing(K2)).
v2(C, D) :- rests_on(C, D), (node(C, K), !standing(K) ; node(D, K2), !standing(K2)).

// 3. an acceptance-scenario is never on needs
v3(S) :- needs(S, _), node(S, "acceptance-scenario").
v3(S) :- needs(_, S), node(S, "acceptance-scenario").

// 4. depends_on is derived
v4(C, D) :- authored_depends_on(C, D), !using(C, _, D).

// 5. using points the way the pin points across a seam
v5(C, D) :- using(C, _, D), in(C, X), in(D, Y), X != Y, !pins(X, Y, _).

// 6. crossings reference seams; mapped only then
v6(T, R) :- crosses(T, R), !node(R, "context-seam").
v6b(T)   :- status(T, "mapped"), crosses(T, R), !node(R, "context-seam").

// 7. a cross-context-request comes from a capability, across the seam between its two contexts; upstream names no client
v7(Q)     :- node(Q, "cross-context-request"), !from_cap(Q, _).
v7b(Q)    :- across(Q, R), from_cap(Q, C), in(C, X), needs(Q, U), in(U, Y), !seam(R, Y, X).
v7c(U, D) :- in(U, X), in(D, Y), pins(Y, X, _), standing_edge(U, D).

// 8. a work-item names a capability, directly or through for:
v8(W) :- node(W, "work-item"), !cap_of_wi(W, _).

// 9. every part has exactly one part_of reaching an initiative; priority and source only on initiatives
v9a(P) :- node(P, K), part(K), !part_of(P, _).
v9b(P) :- part_of(P, A), part_of(P, B), A != B.
v9c(P) :- node(P, K), part(K), !root(P, _).
v9d(X) :- priority(X, _), !node(X, "initiative").
v9e(X) :- source(X, _),   !node(X, "initiative").
v9f(I) :- part_of(I, _),   node(I, "initiative").
po_tc(A, B) :- part_of(A, B).
po_tc(A, C) :- po_tc(A, B), part_of(B, C).
v9g(P) :- po_tc(P, P).

// 10. only an origin is a source; records are about standing artifacts
v10a(I, Rec) :- source(I, Rec), node(Rec, K), !origin(K).
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

// 15. requirement ids: present, unique within the capability, never reused; references by id
v15a(Q)     :- node(Q, "capability-requirement"), !req_id(Q, _, _).
v15b(Q1,Q2) :- req_id(Q1, C, N), req_id(Q2, C, N), Q1 != Q2.
v15c(Q)     :- req_id(Q, C, N), retired_id(C, N).
v15d(Q, C)  :- req_id(Q, C, _), !has_req(C, Q).
v15e(P, Q)  :- changes(P, Q), !has_req(_, Q).
v15f(P)     :- status(P, "formulated"), (adds(P, Q) ; changes(P, Q)), !has_sc(Q, _), has_req(C, Q), !group(C, "guarantees").

// 13. a watch condition has a reader
v13(D) :- revisit_signal(D, Sig), Sig != "requests", !node(Sig, "measurement").

// initiative kinds fix the first part
v_k1(I) :- ikind(I, "job"),               part_of(P, I), !node(P, "job-proposal").
v_k2(I) :- ikind(I, "job-path"),          part_of(P, I), !node(P, "job-thread").
v_k3(I) :- ikind(I, "capability-change"), part_of(P, I), !node(P, "capability-proposal").
v_k4(I) :- ikind(I, "defect"),            part_of(P, I), !node(P, "work-item").
v_k5(I) :- node(I, "initiative"), part_of(P1, I), part_of(P2, I), P1 != P2.     // one first part

// breakdown shape: work-items only under capability-proposals (or a defect initiative)
v_b1(W) :- node(W, "work-item"), part_of(W, X), !node(X, "capability-proposal"), !(node(X, "initiative"), ikind(X, "defect")).
v_b2(Q) :- node(Q, "cross-context-request"), part_of(P, Q), !node(P, "capability-proposal").
v_b3(T) :- node(T, "job-thread"), part_of(P, T), !node(P, "capability-proposal"), !node(P, "cross-context-request"), !node(P, "map-escalation").

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

// initiative done only when every part is closed
v_d1(I) :- status(I, "done"), root(P, I), !closed(P).
```

Warnings:

```
w_unserved_cap(C)   :- node(C, "capability"), !serves(C, _).
w_unserved_job(J)   :- node(J, "job"), !serves(_, J), !of_job(_, J).
w_seam_unused(R)    :- seam(R, Up, Down), !(in(C, Down), in(D, Up), depends_on(C, D)).
w_uncited_obs(O)    :- node(O, "observation"), !source(_, O).
w_many_requests(R)  :- N = count : { across(Q, R), status(Q, "open") }, N > 5.
w_stale_intake(I)   :- status(I, "proposed"), age(I, Days), Days > 90.
```

## 5. Lifecycles

Transitions not listed are violations; guards are queries that must hold.

**initiative**: `proposed → started` (owner; a first part exists) → `done`
(no `v_d1`) | `abandoned`. On `done`: archive; measure.

**job-thread**: `proposed → mapped` (no `v6b`) → `accepted` (the person)
→ `built` (every part under it closed; the entry scenario green). On
`built`: write `serves … using` from the work-items' `wi_depends`.

**cross-context-request**: `open → accepted` (upstream owner) | `refused`
(upstream owner; a map-escalation may follow) → `delivered` (`resolution`
present; the capability-proposal under it merged).

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
statement = standing_stmt | initiative_stmt | part_stmt | record_stmt ;

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

initiative_stmt =
    "initiative" I "(" KIND ")" ":" SUMMARY "; priority" N "; sources" RECLIST
                                                                 → ikind, priority, source
  ;

part_stmt =
    "job-proposal" P "argues job" JOB ", part of" X              → argues, part_of
  | "job-thread" T "of" JOB "enters" CTX ("crosses" SEAM "needing" TEXT)* ", part of" X
                                                                 → of_job, enters, crosses, needs, part_of
  | "capability-proposal" P "argues" CAP ("adds" REQLIST)? ("changes" REQLIST)? ("removes" REQLIST)? ", part of" X
                                                                 → argues, adds, changes, removes, part_of
  | "cross-context-request" Q "from" CAP "across" SEAM "needs" TEXT ", part of" X
                                                                 → from_cap, across, needs, part_of
  | "map-escalation" E WHY ", part of" X                         → escalation, part_of
  | "work-item" W "is" WKIND ("accepts" SCENLIST | "check" TEXT) ("blocked by" WLIST)?
                 ("depends on" CAPLIST)? ("for" W2)? ", part of" X
                                                                 → wkind, accepts|check, blocked_by, wi_depends, for, part_of
  ;

record_stmt =
    "observation" O "about" ANY ":" TEXT                         → node(O,"observation"), about
  ;

CAP = CTX "/" NAME ;   RID = CAP "#r" DIGITS ;   REQLIST = RID ("," RID)* ;   SCEN = '"' TEXT '"' ;
```

Refusals, as the checker sees them:

| sentence | parses to | fails |
|---|---|---|
| *acceptance-scenario S needs CAP* | `needs(S, CAP)` | v3 |
| *cross-context-request Q depends on CAP* | no production | parse error |
| *work-item W serves JOB* | no production | parse error |
| *CAP depends on X* with no `using` | `authored_depends_on` | v4 |
| *CAP needs CAP′* | `needs(CAP, CAP′)` | v1 |
| *job-thread T … (no "part of")* | `part_of` absent | v9a |
| *work-item W … part of job-thread T* | `part_of(W, T)` | v_b1 |
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
  transition in §5.
- **§5** as the `status` field's allowed values plus one guard query per
  transition, enforced by the scripts that move initiatives and parts.
- **§6** as a parser of a few hundred lines; `ecommerce-example.md` should
  be run through it, not read.
- If the store becomes RDF: §2 is SHACL shapes, §4 is SHACL-SPARQL, and
  kb's IRIs are already the node ids.
