% model.lp: docs/design-model/grammar.md (version 3) §1, §3 and §4, in clingo.
%
% Relation names, arities and constraint names follow grammar.md; "g:NN" is
% its line number. Where grammar.md does not compile as written, the clause
% carries a FIX note and the change is the smallest that keeps the stated
% intent. Facts come from `model facts`, which reads a repository's files.
% Every v_ relation must be empty; w_ relations are warnings.

% ---------------------------------------------------------------- inputs
#defined node/2.      #defined narrator/2.   #defined group/2.     #defined external/1.
#defined status/2.    #defined ikind/2.      #defined wkind/2.     #defined priority/2.
#defined summary/2.   #defined revisit_signal/2.   #defined fileset/2.   #defined escalation/2.
#defined req_id/3.    #defined retired_id/2.
#defined orders/2.    #defined in/2.         #defined seam/3.      #defined pattern/2.
#defined pins/3.      #defined has_req/2.    #defined has_sc/2.    #defined rests_on/2.
#defined supersedes/2.   #defined serves/2.  #defined using/3.     #defined source/2.
#defined part_of/2.   #defined of_job/2.     #defined enters/2.    #defined crosses/2.
#defined needs/2.     #defined from_cap/2.   #defined across/2.    #defined resolution/2.
#defined argues/2.    #defined adds/2.       #defined changes/2.   #defined removes/2.
#defined under/2.     #defined for/2.        #defined accepts/2.   #defined check/2.
#defined blocked_by/2.   #defined wi_depends/2.   #defined about/2.
% Used by grammar.md with no .decl and no §2 row:
#defined authored_depends_on/2.   % g:112 (v4); the parse of "CAP depends on X"
#defined age/2.                   % g:203 (w_stale_intake); days since an initiative was proposed

% ---------------------------------------------------------------- §1 g:9-50
standing("product-vision").  standing("job").  standing("bounded-context").  standing("context-seam").
standing("capability").  standing("capability-requirement").  standing("acceptance-scenario").  standing("design-decision").
part("job-proposal").  part("map-proposal").  part("vision-proposal").  part("job-thread").
part("capability-proposal").  part("cross-context-request").  part("map-escalation").  part("work-item").
record("observation").  record("measurement").  record("review-finding").  record("decision-argument").  record("initiative-archive").
origin("observation").  origin("measurement").  origin("review-finding").

% ---------------------------------------------------------------- §3 g:82-93
depends_on(C, D)      :- using(C, _, D).
path(J, C, D)         :- using(C, J, D).
path(J, C, E)         :- path(J, C, D), using(D, J, E).
cap_of_wi(W, C)       :- under(W, C).
cap_of_wi(W, C)       :- for(W, W2), cap_of_wi(W2, C).
root(P, I)            :- part_of(P, I), node(I, "initiative").
root(P, I)            :- part_of(P, P2), root(P2, I).
closed(P)             :- status(P, S), S = ("merged"; "built"; "delivered"; "ruled"; "green"; "refused").

% helpers for Soufflé's "!rel(X, _)"
has_part_of(P)  :- part_of(P, _).        has_root(P)    :- root(P, _).
has_about(R)    :- about(R, _).          has_narrator(C) :- narrator(C, _).
has_from(Q)     :- from_cap(Q, _).       has_cap(W)     :- cap_of_wi(W, _).
has_accepts(W)  :- accepts(W, _).        has_check(W)   :- check(W, _).
has_summary(D)  :- summary(D, _).        has_req_id(Q)  :- req_id(Q, _, _).
has_any_req(Q)  :- has_req(_, Q).        has_sc_of(S)   :- has_sc(_, S).
has_sc_q(Q)     :- has_sc(Q, _).         pinned(X, Y)   :- pins(X, Y, _).
using_any(C, D) :- using(C, _, D).       is_standing(X) :- node(X, K), standing(K).
nonstanding(X)  :- node(X, K), not standing(K).
nonorigin(X)    :- node(X, K), not origin(K).

% ---------------------------------------------------------------- §4 g:95-187
% 1. needs only on parts
v1(X) :- needs(X, _), node(X, K), not part(K).

% 2. standing edges only between standing artifacts. g:103 asks for one clause per relation; written out.
v2(C, J) :- serves(C, J),       nonstanding(C).    v2(C, J) :- serves(C, J),       nonstanding(J).
v2(C, D) :- using(C, _, D),     nonstanding(C).    v2(C, D) :- using(C, _, D),     nonstanding(D).
v2(C, D) :- rests_on(C, D),     nonstanding(C).    v2(C, D) :- rests_on(C, D),     nonstanding(D).
v2(C, Q) :- has_req(C, Q),      nonstanding(C).    v2(C, Q) :- has_req(C, Q),      nonstanding(Q).
v2(Q, S) :- has_sc(Q, S),       nonstanding(Q).    v2(Q, S) :- has_sc(Q, S),       nonstanding(S).
v2(A, B) :- supersedes(A, B),   nonstanding(A).    v2(A, B) :- supersedes(A, B),   nonstanding(B).
v2(A, B) :- pins(A, B, _),      nonstanding(A).    v2(A, B) :- pins(A, B, _),      nonstanding(B).
v2(V, J) :- orders(V, J),       nonstanding(V).    v2(V, J) :- orders(V, J),       nonstanding(J).

% 3. an acceptance-scenario is never on needs
v3(S) :- needs(S, _), node(S, "acceptance-scenario").
v3(S) :- needs(_, S), node(S, "acceptance-scenario").

% 4. depends_on is derived
v4(C, D) :- authored_depends_on(C, D), not using_any(C, D).

% 5. using points the way the pin points across a seam
v5(C, D) :- using(C, _, D), in(C, X), in(D, Y), X != Y, not pinned(X, Y).

% 6. crossings reference seams; mapped only then
v6(T, R)  :- crosses(T, R), not node(R, "context-seam").
v6b(T)    :- status(T, "mapped"), crosses(T, R), not node(R, "context-seam").

% 7. a cross-context-request comes from a capability, across the seam between its two contexts; upstream names no client
v7(Q)     :- node(Q, "cross-context-request"), not has_from(Q).
v7b(Q)    :- across(Q, R), from_cap(Q, C), in(C, X), needs(Q, U), in(U, Y), not seam(R, Y, X).
% FIX g:124: standing_edge is not defined in grammar.md. Read as any standing edge from an upstream capability to a downstream one.
standing_edge(U, D) :- serves(U, D).  standing_edge(U, D) :- using(U, _, D).  standing_edge(U, D) :- rests_on(U, D).
v7c(U, D) :- in(U, X), in(D, Y), pins(Y, X, _), standing_edge(U, D).

% 8. a work-item names a capability, directly or through for:
v8(W) :- node(W, "work-item"), not has_cap(W).

% 9. every part has exactly one part_of reaching an initiative; priority and source only on initiatives
v9a(P) :- node(P, K), part(K), not has_part_of(P).
v9b(P) :- part_of(P, A), part_of(P, B), A != B.
v9c(P) :- node(P, K), part(K), not has_root(P).
v9d(X) :- priority(X, _), not node(X, "initiative").
v9e(X) :- source(X, _),   not node(X, "initiative").
v9f(I) :- part_of(I, _),   node(I, "initiative").
po_tc(A, B) :- part_of(A, B).
po_tc(A, C) :- po_tc(A, B), part_of(B, C).
v9g(P) :- po_tc(P, P).

% 10. only an origin is a source; records are about standing artifacts
v10a(I, R) :- source(I, R), nonorigin(R).
v10a(I, R) :- source(I, R), not node(R, _).          % FIX g:141: a source naming nothing is read as not an origin
v10b(R)    :- node(R, K), record(K), not has_about(R).
v10c(R)    :- about(R, A), not is_standing(A).

% 11. one narrator per capability
v11(C) :- node(C, "capability"), not has_narrator(C).
v11(C) :- narrator(C, N1), narrator(C, N2), N1 != N2.

% 12. design-decisions: summary present; supersedes acyclic
v12a(D) :- node(D, "design-decision"), not has_summary(D).
sup_tc(A, B) :- supersedes(A, B).
sup_tc(A, C) :- sup_tc(A, B), supersedes(B, C).
v12b(D) :- sup_tc(D, D).

% 13. a watch condition has a reader
v13(D) :- revisit_signal(D, Sig), Sig != "requests", not node(Sig, "measurement").

% 15. requirement ids: present, unique within the capability, never reused; references by id
v15a(Q)     :- node(Q, "capability-requirement"), not has_req_id(Q).
v15b(Q1,Q2) :- req_id(Q1, C, N), req_id(Q2, C, N), Q1 != Q2.
v15c(Q)     :- req_id(Q, C, N), retired_id(C, N).
v15d(Q, C)  :- req_id(Q, C, _), not has_req(C, Q).
v15e(P, Q)  :- changes(P, Q), not has_any_req(Q).
% FIX g:161: Soufflé's disjunction in a body is split into two clauses; C is bound by has_req(C, Q).
v15f(P)     :- status(P, "formulated"), adds(P, Q),    not has_sc_q(Q), has_req(C, Q), not group(C, "guarantees").
v15f(P)     :- status(P, "formulated"), changes(P, Q), not has_sc_q(Q), has_req(C, Q), not group(C, "guarantees").

% initiative kinds fix the first part
v_k1(I) :- ikind(I, "job"),               part_of(P, I), not node(P, "job-proposal").
v_k2(I) :- ikind(I, "job-path"),          part_of(P, I), not node(P, "job-thread").
v_k3(I) :- ikind(I, "capability-change"), part_of(P, I), not node(P, "capability-proposal").
v_k4(I) :- ikind(I, "defect"),            part_of(P, I), not node(P, "work-item").
v_k5(I) :- node(I, "initiative"), part_of(P1, I), part_of(P2, I), P1 != P2.

% breakdown shape: work-items only under capability-proposals (or a defect initiative)
defect_init(X) :- node(X, "initiative"), ikind(X, "defect").
v_b1(W) :- node(W, "work-item"), part_of(W, X), not node(X, "capability-proposal"), not defect_init(X).
v_b2(Q) :- node(Q, "cross-context-request"), part_of(P, Q), not node(P, "capability-proposal").
v_b3(T) :- node(T, "job-thread"), part_of(P, T), not node(P, "capability-proposal"), not node(P, "cross-context-request"), not node(P, "map-escalation").

% scenarios: exactly one requirement each; every requirement tested unless guarantees
v_s1(S) :- node(S, "acceptance-scenario"), not has_sc_of(S).
v_s2(S) :- has_sc(Q1, S), has_sc(Q2, S), Q1 != Q2.
v_s3(Q) :- has_req(C, Q), not has_sc_q(Q), not group(C, "guarantees").

% work-items: blocked_by acyclic; ready only when unblocked; claimed file sets disjoint; acceptance present
blk_tc(A, B) :- blocked_by(A, B).
blk_tc(A, C) :- blk_tc(A, B), blocked_by(B, C).
v_w1(W)      :- blk_tc(W, W).
v_w2(W)      :- status(W, "ready"), blocked_by(W, B), not status(B, "green").
v_w3(W1, W2) :- status(W1, "claimed"), status(W2, "claimed"), W1 < W2, fileset(W1, P), fileset(W2, P).
v_w4(W)      :- node(W, "work-item"), not has_accepts(W), not has_check(W).

% initiative done only when every part is closed
v_d1(I) :- status(I, "done"), root(P, I), not closed(P).

% ---------------------------------------------------------------- warnings g:193-204
w_unserved_cap(C)  :- node(C, "capability"), not serves(C, _).
w_unserved_job(J)  :- node(J, "job"), not serves(_, J), not of_job(_, J).
% FIX g:200: Soufflé has no negation of a conjunction; named as seam_used.
seam_used(R)       :- seam(R, Up, Down), in(C, Down), in(D, Up), depends_on(C, D).
w_seam_unused(R)   :- seam(R, _, _), not seam_used(R).
w_uncited_obs(O)   :- node(O, "observation"), not source(_, O).
w_many_requests(R) :- across(_, R), #count{ Q : across(Q, R), status(Q, "open") } > 5.
w_stale_intake(I)  :- status(I, "proposed"), age(I, Days), Days > 90.

#show.
#show v1/1.  #show v2/2.  #show v3/1.  #show v4/2.  #show v5/2.  #show v6/2.  #show v6b/1.
#show v7/1.  #show v7b/1. #show v7c/2. #show v8/1.  #show v9a/1. #show v9b/1. #show v9c/1.
#show v9d/1. #show v9e/1. #show v9f/1. #show v9g/1. #show v10a/2. #show v10b/1. #show v10c/1.
#show v11/1. #show v12a/1. #show v12b/1. #show v13/1.
#show v15a/1. #show v15b/2. #show v15c/1. #show v15d/2. #show v15e/2. #show v15f/1.
#show v_k1/1. #show v_k2/1. #show v_k3/1. #show v_k4/1. #show v_k5/1.
#show v_b1/1. #show v_b2/1. #show v_b3/1. #show v_s1/1. #show v_s2/1. #show v_s3/1.
#show v_w1/1. #show v_w2/1. #show v_w3/2. #show v_w4/1. #show v_d1/1.
#show w_unserved_cap/1. #show w_unserved_job/1. #show w_seam_unused/1. #show w_uncited_obs/1.
#show w_many_requests/1. #show w_stale_intake/1.
