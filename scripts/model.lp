% model.lp: docs/design-model/grammar.md (version 3) §1, §3 and §4, in clingo.
%
% Relation names, arities and constraint names follow grammar.md; "g:NN" is
% its line number. Where grammar.md does not compile as written, the clause
% has a FIX note and the change is the smallest that keeps the stated
% intent. Facts come from `model facts`, which reads a repository's files.
% Every v_ relation must be empty; w_ relations are warnings.
% Each shown relation has one plain label, label("<code>", "<label>"), written beside its rule and only here;
% `model check` and `model rules` read them from the solve (design-model-check r2, r65).
% A clause marked EXTENSION is not in grammar.md v3 at all; it is proposed against
% grammar.md v3 (design-model-check r48-r54, r58-r59) and kept apart from the FIX notes.

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
#defined asker/2.     #defined req_part_of/2.   #defined req_source/2.  #defined fulfils/2.
#defined date/2.      #defined foreign/1.
#defined req_thread/1.   #defined req_raised_for/2.
% Used by grammar.md with no .decl and no §2 row:
#defined authored_depends_on/2.   % g:112 (v4); the parse of "CAP depends on X"
#defined age/2.                   % g:203 (w_stale_intake); days since an initiative was proposed
% EXTENSION (proposed against grammar.md v3): the glossary of spec/index.md.
#defined term_of/2.               % term_of(T, Ctx): term T is a term of bounded-context Ctx
#defined avoid/2.                 % avoid(T, W): term T's entry lists word W after `Not:`
#defined glossary_entry/3.        % glossary_entry(T, N, W): glossary bullet N writes term T as word W
#defined mentions/2.              % mentions(X, W): requirement or scenario X contains W, a term or avoided word

% ---------------------------------------------------------------- §1 g:9-50
standing("product-vision").  standing("job").  standing("bounded-context").  standing("context-seam").
standing("capability").  standing("capability-requirement").  standing("acceptance-scenario").  standing("design-decision").
standing("term").         % EXTENSION (proposed against grammar.md v3): a glossary term is standing
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
% FIX g:92: v3 makes `formulated` a capability-proposal's last stage (g:221-224) but closed() stops at
% `merged`. Read with the lifecycle: a capability-proposal is closed at `formulated`, any other part as listed.
closed(P)             :- status(P, S), S = ("merged"; "built"; "delivered"; "ruled"; "green"; "refused"), not node(P, "capability-proposal").
closed(P)             :- status(P, "formulated").
% design-model-check r123: `approved` closes a glossary-proposal, and no other kind.
closed(P)             :- status(P, "approved"), node(P, "glossary-proposal").
% EXTENSION (proposed against grammar.md v3; design-model-check r58): a part no longer pursued is
% `withdrawn`, and is closed.
closed(P)             :- status(P, "withdrawn").

% helpers for Soufflé's "!rel(X, _)"
has_part_of(P)  :- part_of(P, _).        has_root(P)    :- root(P, _).
has_about(R)    :- about(R, _).          has_narrator(C) :- narrator(C, _).
has_from(Q)     :- from_cap(Q, _).       has_cap(W)     :- cap_of_wi(W, _).
% FIX: accepts(W, R)'s second argument is a requirement, not grammar.md's acceptance-scenario (r106).
has_accepts(W)  :- accepts(W, _).        has_check(W)   :- check(W, _).
has_summary(D)  :- summary(D, _).        has_req_id(Q)  :- req_id(Q, _, _).
has_any_req(Q)  :- has_req(_, Q).        has_sc_of(S)   :- has_sc(_, S).
has_sc_q(Q)     :- has_sc(Q, _).         pinned(X, Y)   :- pins(X, Y, _).
using_any(C, D) :- using(C, _, D).       is_standing(X) :- node(X, K), standing(K).
nonstanding(X)  :- node(X, K), not standing(K).
nonorigin(X)    :- node(X, K), not origin(K).

% ---------------------------------------------------------------- §4 g:95-187
% 1. needs only on parts
label("v1", "needs on something that is not a part").
v1(X) :- needs(X, _), node(X, K), not part(K).

% 2. standing edges only between standing artifacts. g:103 asks for one clause per relation; written out.
label("v2", "a standing edge touches something that is not standing").
v2(C, J) :- serves(C, J),       nonstanding(C).    v2(C, J) :- serves(C, J),       nonstanding(J).
v2(C, D) :- using(C, _, D),     nonstanding(C).    v2(C, D) :- using(C, _, D),     nonstanding(D).
v2(C, D) :- rests_on(C, D),     nonstanding(C).    v2(C, D) :- rests_on(C, D),     nonstanding(D).
v2(C, Q) :- has_req(C, Q),      nonstanding(C).    v2(C, Q) :- has_req(C, Q),      nonstanding(Q).
v2(Q, S) :- has_sc(Q, S),       nonstanding(Q).    v2(Q, S) :- has_sc(Q, S),       nonstanding(S).
v2(A, B) :- supersedes(A, B),   nonstanding(A).    v2(A, B) :- supersedes(A, B),   nonstanding(B).
v2(A, B) :- pins(A, B, _),      nonstanding(A).    v2(A, B) :- pins(A, B, _),      nonstanding(B).
v2(V, J) :- orders(V, J),       nonstanding(V).    v2(V, J) :- orders(V, J),       nonstanding(J).
v2(C, X) :- in(C, X),           nonstanding(C).    v2(C, X) :- in(C, X),           nonstanding(X).
v2(R, X) :- seam(R, X, _),      nonstanding(R).    v2(R, X) :- seam(R, X, _),      nonstanding(X).
v2(R, X) :- seam(R, _, X),      nonstanding(X).

% 3. v4 (design-model-check r116): a delivered request's resolution names only requirements the spec has
label("v3", "a delivered request's resolution names a requirement the spec does not have").
v3(Q, R) :- status(Q, "delivered"), resolution(Q, R), not node(R, "capability-requirement").

% 4. depends_on is derived
label("v4", "a depends_on that no using gives").
v4(C, D) :- authored_depends_on(C, D), not using_any(C, D).

% 5. using points the way the pin points across a seam
label("v5", "a using against the pin").
v5(C, D) :- using(C, _, D), in(C, X), in(D, Y), X != Y, not pinned(X, Y).

% 6. crossings reference seams; mapped only then
label("v6", "a crossing names no seam").
v6(T, R)  :- crosses(T, R), not node(R, "context-seam").
label("v6b", "a job-thread is mapped with a crossing that names no seam").
v6b(T)    :- status(T, "mapped"), crosses(T, R), not node(R, "context-seam").

% 7. a cross-context-request comes from a capability, across the seam between its two contexts; upstream names no client
label("v7", "a cross-context-request names no capability it comes from").
v7(Q)     :- node(Q, "cross-context-request"), not has_from(Q).
label("v7b", "a cross-context-request is across the wrong seam").
v7b(Q)    :- across(Q, R), from_cap(Q, C), in(C, X), needs(Q, U), in(U, Y), not seam(R, Y, X).
% FIX g:124: standing_edge is not defined in grammar.md. Read as any standing edge from an upstream
% capability to a downstream one; between two capabilities that is only `using` (serves ends at a job,
% rests_on at a decision, and neither has an `in`).
standing_edge(U, D) :- using(U, _, D).
label("v7c", "an upstream names a downstream client").
v7c(U, D) :- in(U, X), in(D, Y), pins(Y, X, _), standing_edge(U, D).

% 8. a work-item names a capability, directly or through for:
label("v8", "a work-item names no capability").
v8(W) :- node(W, "work-item"), not has_cap(W).

% 9. every part has exactly one part_of reaching an initiative; priority and source only on initiatives
label("v9a", "a part has no part_of").
v9a(P) :- node(P, K), part(K), not has_part_of(P).
label("v9b", "a part has two part_of").
v9b(P) :- part_of(P, A), part_of(P, B), A != B.
label("v9c", "a part reaches no initiative").
v9c(P) :- node(P, K), part(K), not has_root(P).
label("v9d", "a priority on something that is not an initiative").
v9d(X) :- priority(X, _), not node(X, "initiative").
label("v9e", "a source on something that is not an initiative").
v9e(X) :- source(X, _),   not node(X, "initiative").
label("v9f", "an initiative is part of something").
v9f(I) :- part_of(I, _),   node(I, "initiative").
po_tc(A, B) :- part_of(A, B).
po_tc(A, C) :- po_tc(A, B), part_of(B, C).
label("v9g", "a part_of cycle").
v9g(P) :- po_tc(P, P).

% 10. only an origin is a source; records are about standing artifacts
label("v10a", "a source that is not an origin").
v10a(I, R) :- source(I, R), nonorigin(R).
v10a(I, R) :- source(I, R), not node(R, _).          % FIX g:141: a source naming nothing is read as not an origin
label("v10b", "a record is about nothing").
v10b(R)    :- node(R, K), record(K), not has_about(R).
label("v10c", "a record is about something that is not standing").
v10c(R)    :- about(R, A), not is_standing(A).          % also fires on an `about` naming nothing (stricter than g:143)

% 11. one narrator per capability
label("v11", "a capability without exactly one narrator").
v11(C) :- node(C, "capability"), not has_narrator(C).
v11(C) :- narrator(C, N1), narrator(C, N2), N1 != N2.

% 12. design-decisions: summary present; supersedes acyclic
label("v12a", "a decision has no summary").
v12a(D) :- node(D, "design-decision"), not has_summary(D).
sup_tc(A, B) :- supersedes(A, B).
sup_tc(A, C) :- sup_tc(A, B), supersedes(B, C).
label("v12b", "a supersedes cycle").
v12b(D) :- sup_tc(D, D).

% 13. a watch condition has a reader
label("v13", "a revisit signal no one reads").
v13(D) :- revisit_signal(D, Sig), Sig != "requests", not node(Sig, "measurement").

% 15. requirement ids: present, unique within the capability, never reused; references by id
label("v15a", "a requirement has no id").
v15a(Q)     :- node(Q, "capability-requirement"), not has_req_id(Q).
label("v15b", "two requirements share an id").
v15b(Q1,Q2) :- req_id(Q1, C, N), req_id(Q2, C, N), Q1 < Q2.     % FIX g:157: Q1 < Q2, so one duplicate is one row
label("v15c", "a retired id is used again").
v15c(Q)     :- req_id(Q, C, N), retired_id(C, N).
label("v15d", "a requirement id outside its capability").
v15d(Q, C)  :- req_id(Q, C, _), not has_req(C, Q).
% FIX (design-model-check r6): only a drafted or approved proposal; a merged, formulated or withdrawn one may change a retired id.
label("v15e", "a proposal changes a requirement no capability has").
v15e(P, Q)  :- changes(P, Q), not has_any_req(Q), status(P, "drafted").
v15e(P, Q)  :- changes(P, Q), not has_any_req(Q), status(P, "approved").
% g:161's disjunction in a body is split into two clauses for clingo; C is bound by has_req(C, Q).
label("v15f", "a formulated proposal leaves a requirement without a scenario").
v15f(P)     :- status(P, "formulated"), adds(P, Q),    not has_sc_q(Q), has_req(C, Q), not group(C, "guarantees").
v15f(P)     :- status(P, "formulated"), changes(P, Q), not has_sc_q(Q), has_req(C, Q), not group(C, "guarantees").

% initiative kinds fix the first part
label("v_k1", "a job initiative's first part is not a job-proposal").
v_k1(I) :- ikind(I, "job"),               part_of(P, I), not node(P, "job-proposal").
label("v_k2", "a job-path initiative's first part is not a job-thread").
v_k2(I) :- ikind(I, "job-path"),          part_of(P, I), not node(P, "job-thread").
label("v_k3", "a capability-change initiative's first part is not a capability-proposal").
v_k3(I) :- ikind(I, "capability-change"), part_of(P, I), not node(P, "capability-proposal"), not node(P, "glossary-proposal").   % r123: a glossary-proposal is a part of one
label("v_k4", "a defect initiative's first part is not a work-item").
v_k4(I) :- ikind(I, "defect"),            part_of(P, I), not node(P, "work-item").
% FIX g:171 (design-decision/one-capability-per-proposal): a capability-change initiative may have several
% capability-proposals, one per capability; every other kind keeps one first part.
label("v_k5", "an initiative has more than one first part").
v_k5(I) :- node(I, "initiative"), part_of(P1, I), part_of(P2, I), P1 != P2, not ikind(I, "capability-change").
% FIX g:72 (same decision): `argues` is 1..n for other proposals, exactly 1 for a capability-proposal.
label("v_k6", "a capability-proposal argues more than one capability").
v_k6(P) :- node(P, "capability-proposal"), argues(P, A1), argues(P, A2), A1 < A2.

% breakdown shape: work-items only under capability-proposals (or a defect initiative)
defect_init(X) :- node(X, "initiative"), ikind(X, "defect").
% g:174's negated conjunction !(node(X, "initiative"), ikind(X, "defect")) is named defect_init.
label("v_b1", "a work-item is part of something other than a capability-proposal").
v_b1(W) :- node(W, "work-item"), part_of(W, X), not node(X, "capability-proposal"), not defect_init(X).
label("v_b2", "a cross-context-request has a part that is not a capability-proposal").
v_b2(Q) :- node(Q, "cross-context-request"), part_of(P, Q), not node(P, "capability-proposal").
label("v_b3", "a job-thread has a part of the wrong kind").
v_b3(T) :- node(T, "job-thread"), part_of(P, T), not node(P, "capability-proposal"), not node(P, "cross-context-request"), not node(P, "map-escalation").

% scenarios: every requirement tested unless guarantees
label("v_s1", "a scenario names no requirement").
v_s1(S) :- node(S, "acceptance-scenario"), not has_sc_of(S).
% design-decision/a-scenario-names-one-requirement: a deprecated scenario has no has_sc (model facts skips it).
label("v_s2", "a scenario names more than one requirement").
v_s2(S) :- has_sc(Q1, S), has_sc(Q2, S), Q1 != Q2.
label("v_s3", "a requirement has no scenario").
v_s3(Q) :- has_req(C, Q), not has_sc_q(Q), not group(C, "guarantees").

% work-items: blocked_by acyclic; ready only when unblocked; claimed file sets disjoint; acceptance present
blk_tc(A, B) :- blocked_by(A, B).
blk_tc(A, C) :- blk_tc(A, B), blocked_by(B, C).
label("v_w1", "a blocked_by cycle").
v_w1(W)      :- blk_tc(W, W).
label("v_w2", "a ready work-item is blocked by one not green").
v_w2(W)      :- status(W, "ready"), blocked_by(W, B), not status(B, "green").
label("v_w3", "two claimed work-items claim one file").
v_w3(W1, W2) :- status(W1, "claimed"), status(W2, "claimed"), W1 < W2, fileset(W1, P), fileset(W2, P).
label("v_w4", "a work-item has no acceptance and no check").
% EXTENSION (design-model-check r106): a withdrawn work-item needs neither.
v_w4(W)      :- node(W, "work-item"), not status(W, "withdrawn"), not has_accepts(W), not has_check(W).

% initiative done only when every part is closed
% design-model-check r114: also a request this context raised to itself, whose part_of or source names the initiative.
label("v_d1", "a done initiative has a part or a request of its own open").
v_d1(I) :- status(I, "done"), root(P, I), not closed(P).
own_request(Q, I) :- req_part_of(Q, I), own_asker(Q).
own_request(Q, I) :- req_source(Q, I),  own_asker(Q).
own_asker(Q)    :- asker(Q, "internal").
own_asker(Q)    :- asker(Q, C), node(C, "bounded-context").
v_d1(I) :- status(I, "done"), own_request(Q, I), not status(Q, "delivered").
% design-model-check r119: a request is delivered only while the initiative that fulfils it is done.
label("v_d3", "a delivered request whose initiative is not done").
v_d3(Q) :- status(Q, "delivered"), fulfils(I, Q), not status(I, "done").

% requests (design-model-check r113, r115, r117)
label("v16a", "an initiative dated after 2026-10-23 that fulfils no request").
has_fulfils(I) :- fulfils(I, _).
v16a(I) :- node(I, "initiative"), date(I, D), D > "2026-10-23", not has_fulfils(I).
% r120: a job-thread is judged from the id (req_thread), and a request raised for a request is let off.
label("v17", "a request that is part of no job-thread, cites no origin and is raised for no request").
in_thread(Q)    :- req_part_of(Q, T), node(T, "job-thread").
in_thread(Q)    :- req_thread(Q).
cites_origin(Q) :- req_source(Q, O), node(O, K), origin(K).
raises_a_request(Q) :- req_raised_for(Q, _).
v17(Q) :- node(Q, "request"), not in_thread(Q), not cites_origin(Q), not raises_a_request(Q).
% r121: except a request that some request is raised for.
label("v18", "an id of a kind kept in .shop/work/ with another context's path, other than the request a request is raised for").
raised_for_any(R) :- req_raised_for(_, R).
v18(X) :- foreign(X), not raised_for_any(X).
% EXTENSION (proposed against grammar.md v3; design-model-check r59): an abandoned initiative leaves
% no part open; each is closed or withdrawn.
% CONTRACT (scripts/model --help): `withdrawn` is closed, so "not withdrawn" adds nothing to "not closed"
% today; it is written out so the rule stays valid if a later grammar stops counting withdrawn as closed.
label("v_d2", "an abandoned initiative has a part open").
v_d2(I) :- status(I, "abandoned"), root(P, I), not closed(P), not status(P, "withdrawn").

% ---------------------------------------------------------------- EXTENSION: terms
% Proposed against grammar.md v3 (design-model-check r52-r54); grammar.md has no terms yet.
% A requirement is in its capability's context; a scenario in its requirement's. A scenario that
% names no requirement (v_s1 reports it) is read in the repository's own, the one bounded-context.
ctx_of(Q, X) :- has_req(C, Q), in(C, X).
ctx_of(S, X) :- has_sc(Q, S), ctx_of(Q, X).
ctx_of(S, X) :- node(S, "acceptance-scenario"), not has_sc_of(S), node(X, "bounded-context").
% t1. a requirement or scenario uses no word its context's glossary avoids
label("v_t1", "a word the glossary avoids").
v_t1(X, W, T) :- mentions(X, W), avoid(T, W), term_of(T, Ctx), ctx_of(X, Ctx).
% t2. one entry per term
label("v_t2", "a term has two entries").
v_t2(T)       :- glossary_entry(T, N1, _), glossary_entry(T, N2, _), N1 < N2.
% t3. no term avoids a term of its context, itself included
label("v_t3", "an avoided word is a term").
v_t3(W)       :- avoid(T, W), term_of(T, Ctx), glossary_entry(T2, _, W), term_of(T2, Ctx).

% ---------------------------------------------------------------- EXTENSION: EARS lines
% Proposed against grammar.md v3 (design-model-check r103-r104; design-decision/behaviour-lines-are-ears).
% scripts/model matches each Behaviour line (a table row by its lead sentence) and gives ears_other(Q) for a line
% in none of EARS's patterns and ears_many(Q) for one with more than one "shall" or more than one sentence.
label("v_e1", "a Behaviour line is not in one of EARS's patterns").
label("v_e2", "a Behaviour line has more than one \"shall\" or more than one sentence").
v_e1(Q) :- ears_other(Q).
v_e2(Q) :- ears_many(Q).

% ---------------------------------------------------------------- warnings g:193-204
label("w_unserved_cap", "a capability serves no job").
w_unserved_cap(C)  :- node(C, "capability"), not serves(C, _), node(_, "job").
label("w_unserved_job", "a job nothing serves").
w_unserved_job(J)  :- node(J, "job"), not serves(_, J), not of_job(_, J).
% FIX g:200: Soufflé has no negation of a conjunction; named as seam_used.
seam_used(R)       :- seam(R, Up, Down), in(C, Down), in(D, Up), depends_on(C, D).
label("w_seam_unused", "a seam nothing crosses").
w_seam_unused(R)   :- seam(R, _, _), not seam_used(R).
label("w_uncited_obs", "an observation no initiative cites").
w_uncited_obs(O)   :- node(O, "observation"), not source(_, O).
label("w_many_requests", "more than five open requests across one seam").
w_many_requests(R) :- across(_, R), #count{ Q : across(Q, R), status(Q, "open") } > 5.
label("w_stale_intake", "an initiative proposed more than 90 days ago").
w_stale_intake(I)  :- status(I, "proposed"), age(I, Days), Days > 90.

#show.
#show label/2.
#show v1/1.  #show v2/2.  #show v3/2. #show v4/2.  #show v5/2.  #show v6/2.  #show v6b/1.
#show v7/1.  #show v7b/1. #show v7c/2. #show v8/1.  #show v9a/1. #show v9b/1. #show v9c/1.
#show v9d/1. #show v9e/1. #show v9f/1. #show v9g/1. #show v10a/2. #show v10b/1. #show v10c/1.
#show v11/1. #show v12a/1. #show v12b/1. #show v13/1.
#show v15a/1. #show v15b/2. #show v15c/1. #show v15d/2. #show v15e/2. #show v15f/1.
#show v_k1/1. #show v_k2/1. #show v_k3/1. #show v_k4/1. #show v_k5/1. #show v_k6/1.
#show v_b1/1. #show v_b2/1. #show v_b3/1. #show v_s1/1. #show v_s2/1. #show v_s3/1.
#show v_w1/1. #show v_w2/1. #show v_w3/2. #show v_w4/1. #show v_d1/1. #show v_d3/1.
#show v16a/1. #show v17/1. #show v18/1.      % requests (design-model-check r113, r115, r117)
#show v_t1/3. #show v_t2/1. #show v_t3/1.    % EXTENSION (proposed against grammar.md v3)
#show v_e1/1. #show v_e2/1.                  % EXTENSION (proposed against grammar.md v3)
#show v_d2/1.                                 % EXTENSION (proposed against grammar.md v3)
#show w_unserved_cap/1. #show w_unserved_job/1. #show w_seam_unused/1. #show w_uncited_obs/1.
#show w_many_requests/1. #show w_stale_intake/1.
