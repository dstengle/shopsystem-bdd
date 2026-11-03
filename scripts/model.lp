% model.lp: the graph of design model v5 (docs/design-model/grammar.md §1-§4), in clingo.
%
% v5 is v4 fitted to the domain model; the changes from v4 are the GF conversion design's §7.1 (C1-C32) and its rule
% codes §7.2, each with one meaning. "C<n>" below names the change a clause makes. Facts come from `model facts`, which
% reads a repository's files. Every v_ relation must be empty; w_ relations are warnings.
% Each shown relation has one plain label, label("<code>", "<label>"), written beside its rule and only here;
% `model check` and `model rules` read them from the solve (design-model-check r2, r65).
% The requirement language (GF parse, telingo) is outside this file: it joins the graph by the facts parsed/unparsed/
% ambiguous, member_of, in(G, C), generates and restates (C29). Rules over facts the codified reader emits are
% `#defined` and silent until it emits them. A file without `language: codified-1` is not read: it is v_p0.

% ---------------------------------------------------------------- inputs
#defined node/2.      #defined narrator/2.   #defined group/2.     #defined external/1.
#defined status/2.    #defined ikind/2.      #defined wkind/2.     #defined priority/2.
#defined summary/2.   #defined revisit_signal/2.   #defined fileset/2.   #defined escalation/2.
#defined req_id/3.    #defined retired_id/2.
#defined orders/2.    #defined in/2.         #defined seam/3.      #defined pattern/2.
#defined pins/3.      #defined has_req/2.    #defined rests_on/2.
#defined supersedes/2.   #defined serves/2.  #defined using/3.     #defined source/2.
#defined part_of/2.   #defined of_job/2.     #defined enters/2.    #defined crosses/2.
#defined resolution/2.   #defined at/2.
#defined argues/2.    #defined adds/2.       #defined changes/2.   #defined removes/2.
#defined under/2.     #defined for/2.        #defined accepts/2.   #defined check/2.
#defined blocked_by/2.   #defined wi_depends/2.   #defined about/2.
#defined asker/2.     #defined req_part_of/2.   #defined req_source/2.  #defined fulfils/2.
#defined date/2.      #defined foreign/1.
#defined req_thread/1.   #defined req_raised_for/2.
#defined upstream/2.  #defined line/3.       #defined outcome/3.   #defined resolution_of_line/2.   % a request (C20)
#defined authored_depends_on/2.   % the parse of "CAP depends on X" (v4)
#defined age/2.                   % days since an initiative or a request was dated
% the glossary: terms of spec/index.md and of each capability's Terms (C8, C27)
#defined term_of/2.               % term_of(T, Ctx): term T is a term of bounded-context Ctx
#defined avoid/2.                 % avoid(T, W): term T's entry lists word W after `Not:`
#defined glossary_entry/3.        % glossary_entry(T, N, W): glossary bullet N writes term T as word W
#defined mentions/2.              % mentions(X, W): X (prose, a requirement or a scenario) contains W
#defined typed/1.                 % typed(Ctx): Ctx's index is codified, so its glossary is typed
#defined category/2.              % category(T, Cat): actor, kind, attribute, value, relation, event, resource, condition
#defined value_of/3.              % value_of(V, K, A): value V belongs to attribute A of kind K
#defined linearises/2.            % linearises(T, Words): term T is written Words in the grammar
% the codified spec (C3, C5-C7, C26, C28)
#defined member_of/2.             % member_of(Q, G): requirement Q is a statement of group G
#defined generates/2.             % generates(G, S): scenario S is generated from group G
#defined restates/2.              % restates(G, Old): G replaces the 0.29 id Old, written <cap>#r<n>@0.29
#defined restated_id/1.           % restated_id(Old): spec/restated.json has Old
#defined group_id/3.              % group_id(G, C, N): G is [g<n>] of capability C
#defined retired_group/2.         % retired_group(C, N): g<n> is in C's retired:
#defined u_id/2.                  % u_id(U, N): universal condition U is [U<n>]
#defined codified/1.              % codified(C): C's file is language: codified-1
#defined uncodified/1.            % uncodified(F): spec file F has no language: codified-1
#defined logic_only/1.            % logic_only(G): G has no Steps linearisation, so no scenario
#defined pre/2.                   % pre(Q, Key): Q's trigger and condition trees, normalised (none when ubiquitous)
#defined parsed/1.  #defined unparsed/2.  #defined ambiguous/1.
#defined given_unparsed/2.        % given_unparsed(G, Line): a line of G's given block does not parse in Steps
#defined old_ref/1.               % old_ref(R): R is a 0.29 id <cap>#r<n>@0.29, resolved through spec/restated.json

% ---------------------------------------------------------------- §1 kinds (C1, C3, C7, C8, C10, C21, C23)
standing("product-vision").  standing("job").  standing("bounded-context").  standing("context-seam").
standing("capability").  standing("requirement").  standing("requirement-group").  standing("scenario").
standing("design-decision").  standing("term").  standing("universal-condition").
root_kind("initiative").  root_kind("job-thread").                                         % C23
part("job-proposal").  part("map-proposal").  part("vision-proposal").  part("map-escalation").
part("capability-proposal").  part("glossary-proposal").  part("work-item").
proposal("capability-proposal").  proposal("glossary-proposal").                          % C10: proposal's sorts
record("observation").  record("measurement").  record("review-finding").
record("decision-argument").  record("initiative-archive").  record("design").  record("analysis").   % C21
origin("observation").  origin("measurement").  origin("review-finding").

% ---------------------------------------------------------------- §3 derivations
has_req(C, Q)         :- member_of(Q, G), in(G, C), node(G, "requirement-group").          % C5
depends_on(C, D)      :- using(C, _, D).
cap_of_wi(W, C)       :- under(W, C).
cap_of_wi(W, C)       :- for(W, W2), cap_of_wi(W2, C).
top(P, I)             :- part_of(P, I), node(I, K), root_kind(K).
top(P, I)             :- part_of(P, P2), top(P2, I).
root(P, I)            :- top(P, I), node(I, "initiative").
% A capability-proposal is closed at `formulated`, a glossary-proposal at `approved` (r123), any part at
% `withdrawn` (r58); `merged` closes only the product proposals (C11).
closed(P)             :- status(P, S), S = ("merged"; "built"; "delivered"; "ruled"; "green"; "refused"), not node(P, "capability-proposal").
closed(P)             :- status(P, "formulated").
closed(P)             :- status(P, "approved"), node(P, "glossary-proposal").
closed(P)             :- status(P, "withdrawn").

has_part_of(P)  :- part_of(P, _).        has_top(P)     :- top(P, _).
has_about(R)    :- about(R, _).          has_narrator(C) :- narrator(C, _).
has_cap(W)      :- cap_of_wi(W, _).      has_check(W)   :- check(W, _).
has_accepts(W)  :- accepts(W, _).        % C17: a requirement or a group (a group means its members)
has_summary(D)  :- summary(D, _).        has_req_id(Q)  :- req_id(Q, _, _).
generated(S)    :- generates(_, S).      has_scenario(G) :- generates(G, _).
grouped(Q)      :- member_of(Q, _).
has_any(X)      :- has_req(_, X).        has_any(G)     :- node(G, "requirement-group"), in(G, _).
group_of(Q, G)  :- member_of(Q, G).      group_of(G, G) :- node(G, "requirement-group").
has_group_id(G) :- group_id(G, _, _).    has_u_id(U)    :- u_id(U, _).
has_category(T) :- category(T, _).       has_value_of(V) :- value_of(V, _, _).
pinned(X, Y)    :- pins(X, Y, _).        using_any(C, D) :- using(C, _, D).
is_standing(X)  :- node(X, K), standing(K).
nonstanding(X)  :- node(X, _), not is_standing(X).
nonorigin(X)    :- node(X, K), not origin(K).

% ---------------------------------------------------------------- §4 integrity constraints
% 1 (needs) is retired in v4 (C22).
% 2. standing edges only between standing artifacts, one clause per relation
label("v2", "a standing edge touches something that is not standing").
v2(C, J) :- serves(C, J),       nonstanding(C).    v2(C, J) :- serves(C, J),       nonstanding(J).
v2(C, D) :- using(C, _, D),     nonstanding(C).    v2(C, D) :- using(C, _, D),     nonstanding(D).
v2(C, D) :- rests_on(C, D),     nonstanding(C).    v2(C, D) :- rests_on(C, D),     nonstanding(D).
v2(C, Q) :- has_req(C, Q),      nonstanding(C).    v2(C, Q) :- has_req(C, Q),      nonstanding(Q).
v2(Q, G) :- member_of(Q, G),    nonstanding(Q).    v2(Q, G) :- member_of(Q, G),    nonstanding(G).
v2(G, S) :- generates(G, S),    nonstanding(G).    v2(G, S) :- generates(G, S),    nonstanding(S).
v2(A, B) :- supersedes(A, B),   nonstanding(A).    v2(A, B) :- supersedes(A, B),   nonstanding(B).
v2(A, B) :- pins(A, B, _),      nonstanding(A).    v2(A, B) :- pins(A, B, _),      nonstanding(B).
v2(V, J) :- orders(V, J),       nonstanding(V).    v2(V, J) :- orders(V, J),       nonstanding(J).
v2(C, X) :- in(C, X),           nonstanding(C).    v2(C, X) :- in(C, X),           nonstanding(X).
v2(R, X) :- seam(R, X, _),      nonstanding(R).    v2(R, X) :- seam(R, X, _),      nonstanding(X).
v2(R, X) :- seam(R, _, X),      nonstanding(X).

% 3. a resolution names a requirement (never a scenario), and the spec has it (§7.2: v4's and the live clause, one rule)
label("v3", "a request's resolution names something that is not a requirement of the spec").
v3(Q, R) :- resolution(Q, R), not node(R, "requirement"), not old_ref(R).      % a 0.29 id is history (§13.4)

label("v4", "a depends_on that no using gives").
v4(C, D) :- authored_depends_on(C, D), not using_any(C, D).
label("v5", "a using against the pin").
v5(C, D) :- using(C, _, D), in(C, X), in(D, Y), X != Y, not pinned(X, Y).
label("v6", "a crossing names no seam").
v6(T, R)  :- crosses(T, R), not node(R, "context-seam").
label("v6b", "a job-thread is mapped with a crossing that names no seam").
v6b(T)    :- status(T, "mapped"), crosses(T, R), not node(R, "context-seam").

% 7. a request between two contexts is across a seam between them (§7.2: v4's); judged once the repository maps
% seams, as w_unserved_cap is once it maps jobs. upstream names no client (v7c).
label("v7", "a request between two contexts is across no seam between them").
maps_seams :- node(_, "context-seam").
across_seam(X, Y) :- seam(_, X, Y).     across_seam(X, Y) :- seam(_, Y, X).
v7(Q) :- asker(Q, X), upstream(Q, Y), X != Y, X != "internal", not product_asker(Q), not across_seam(X, Y), maps_seams.
product_asker(Q) :- asker(Q, X), X = "product".
product_asker(Q) :- asker(Q, X), X >= "product/", X < "product0".   % "product/<path>"
standing_edge(U, D) :- using(U, _, D).
label("v7c", "an upstream names a downstream client").
v7c(U, D) :- in(U, X), in(D, Y), pins(Y, X, _), standing_edge(U, D).

label("v8", "a work-item names no capability").
v8(W) :- node(W, "work-item"), not has_cap(W).

% 9. every part has exactly one part_of reaching a root (C23); priority and source only where v4 allows them
label("v9a", "a part has no part_of").
v9a(P) :- node(P, K), part(K), not has_part_of(P).
label("v9b", "a part has two part_of").
v9b(P) :- part_of(P, A), part_of(P, B), A != B.
label("v9c", "a part reaches no root").
v9c(P) :- node(P, K), part(K), not has_top(P).
label("v9d", "a priority on something that is not an initiative, a request or a job-thread").
v9d(X) :- priority(X, _), not node(X, "initiative"), not node(X, "request"), not node(X, "job-thread").
label("v9e", "a source on a part").
v9e(X) :- source(X, _), node(X, K), part(K).
label("v9f", "a root is part of something").
v9f(I) :- part_of(I, _), node(I, K), root_kind(K).
po_tc(A, B) :- part_of(A, B).
po_tc(A, C) :- po_tc(A, B), part_of(B, C).
label("v9g", "a part_of cycle").
v9g(P) :- po_tc(P, P).

label("v10a", "a source that is not an origin").
v10a(I, R) :- source(I, R), nonorigin(R).
v10a(I, R) :- source(I, R), not node(R, _).          % a source naming nothing is not an origin
label("v10b", "a record is about nothing").
v10b(R)    :- node(R, K), record(K), not has_about(R).
label("v10c", "a record is about something that is not standing").
v10c(R)    :- about(R, A), not is_standing(A).

label("v11", "a capability without exactly one narrator").
v11(C) :- node(C, "capability"), not has_narrator(C).
v11(C) :- narrator(C, N1), narrator(C, N2), N1 != N2.

label("v12a", "a decision has no summary").
v12a(D) :- node(D, "design-decision"), not has_summary(D).
sup_tc(A, B) :- supersedes(A, B).
sup_tc(A, C) :- sup_tc(A, B), supersedes(B, C).
label("v12b", "a supersedes cycle").
v12b(D) :- sup_tc(D, D).

label("v13", "a revisit signal no one reads").
v13(D) :- revisit_signal(D, Sig), Sig != "requests", not node(Sig, "measurement").

% 15. ids: present, unique within the capability, never reused (C26)
label("v15a", "a requirement has no id").
v15a(Q)     :- node(Q, "requirement"), not has_req_id(Q).
label("v15b", "two requirements share an id").
v15b(Q1,Q2) :- req_id(Q1, C, N), req_id(Q2, C, N), Q1 < Q2.
label("v15c", "a retired id is used again").
v15c(Q)     :- req_id(Q, C, N), retired_id(C, N).
label("v15d", "a requirement id outside its capability").
v15d(Q, C)  :- req_id(Q, C, _), not has_req(C, Q).
% Only a drafted or approved proposal; a formulated or withdrawn one may name a retired id. `changes` applies to groups
% and terms: a changed requirement is `removes` old and `adds` new (C18), judged where it sits in a group.
label("v15e", "a proposal changes a requirement no capability has, or a requirement of a group").
v15e(P, Q)  :- changes(P, Q), not has_any(Q), status(P, S), S = ("drafted"; "approved").
v15e(P, Q)  :- changes(P, Q), grouped(Q), status(P, S), S = ("drafted"; "approved").
label("v15f", "a formulated proposal leaves a group without a scenario").
named(P, X) :- adds(P, X).   named(P, X) :- changes(P, X).
v15f(P)     :- status(P, "formulated"), named(P, X), group_of(X, G), in(G, C), not has_scenario(G), not logic_only(G),
               not group(C, "guarantees").
label("v15g", "a group has no id, or shares one").
v15g(G)     :- node(G, "requirement-group"), not has_group_id(G).
v15g(G)     :- group_id(G, C, N), group_id(G2, C, N), G != G2.
label("v15h", "a universal condition has no id, or shares one").
v15h(U)     :- node(U, "universal-condition"), not has_u_id(U).
v15h(U)     :- u_id(U, N), u_id(U2, N), U != U2.
label("v15i", "an id is used again: retired, or added though live").
v15i(G)     :- group_id(G, C, N), retired_group(C, N).
v15i(X)     :- adds(P, X), status(P, S), S = ("drafted"; "awaiting-answer"), group_of(X, G), in(G, C), codified(C).
label("v15j", "a group restates an id 0.29 did not have").
v15j(G, O)  :- restates(G, O), not restated_id(O).
label("v15k", "the statements of a group differ in trigger or condition").
v15k(G)     :- member_of(Q1, G), member_of(Q2, G), pre(Q1, K1), pre(Q2, K2), K1 != K2.

% initiative kinds fix the first part (the rules of the job and job-path kinds are gone: C22)
label("v_k3", "a capability-change initiative's first part is not a proposal").
v_k3(I) :- ikind(I, "capability-change"), part_of(P, I), node(P, K), not proposal(K).
label("v_k4", "a defect initiative's first part is not a work-item").
v_k4(I) :- ikind(I, "defect"),            part_of(P, I), not node(P, "work-item").
% A capability-change initiative may have several proposals, one per capability; every other kind one first part.
label("v_k5", "an initiative has more than one first part").
v_k5(I) :- node(I, "initiative"), part_of(P1, I), part_of(P2, I), P1 != P2, not ikind(I, "capability-change").
label("v_k6", "a capability-proposal argues more than one capability").                 % C16
v_k6(P) :- node(P, "capability-proposal"), argues(P, A1), argues(P, A2), A1 < A2.

% breakdown shape: work-items only under capability-proposals (or a defect initiative); a job-thread owns neither
defect_init(X) :- node(X, "initiative"), ikind(X, "defect").
label("v_b1", "a work-item is part of something other than a capability-proposal").
v_b1(W) :- node(W, "work-item"), part_of(W, X), not node(X, "capability-proposal"), not defect_init(X).
label("v_b3", "a job-thread has a capability-proposal or a work-item as a part").
v_b3(T) :- node(T, "job-thread"), part_of(P, T), node(P, K), K = ("capability-proposal"; "work-item").

% scenarios: one per group, generated (C4, C6, C28)
label("v_s1", "a scenario names no group").
v_s1(S) :- node(S, "scenario"), not generated(S).
label("v_s2", "a scenario is generated from more than one group").
v_s2(S) :- generates(G1, S), generates(G2, S), G1 != G2.
label("v_s3", "a group has no scenario").
v_s3(G) :- node(G, "requirement-group"), in(G, C), not has_scenario(G), not logic_only(G), not group(C, "guarantees").
label("v_s4", "a requirement of a codified capability is in no group, or in two").
v_s4(Q) :- req_id(Q, C, _), codified(C), not grouped(Q).
v_s4(Q) :- member_of(Q, G1), member_of(Q, G2), G1 != G2.

blk_tc(A, B) :- blocked_by(A, B).
blk_tc(A, C) :- blk_tc(A, B), blocked_by(B, C).
label("v_w1", "a blocked_by cycle").
v_w1(W)      :- blk_tc(W, W).
label("v_w2", "a ready work-item is blocked by one not green").
v_w2(W)      :- status(W, "ready"), blocked_by(W, B), not status(B, "green").
label("v_w3", "two claimed work-items claim one file").
v_w3(W1, W2) :- status(W1, "claimed"), status(W2, "claimed"), W1 < W2, fileset(W1, P), fileset(W2, P).
label("v_w4", "a work-item has no acceptance and no check").
v_w4(W)      :- node(W, "work-item"), not status(W, "withdrawn"), not has_accepts(W), not has_check(W).

% 19. done-ness (r114: a request this context raised to itself, whose part_of or source names the initiative)
label("v_d1", "a done initiative has a part or a request of its own open").
v_d1(I) :- status(I, "done"), root(P, I), not closed(P).
own_request(Q, I) :- req_part_of(Q, I), own_asker(Q).
own_request(Q, I) :- req_source(Q, I),  own_asker(Q).
own_asker(Q)    :- asker(Q, "internal").
own_asker(Q)    :- asker(Q, C), node(C, "bounded-context").
v_d1(I) :- status(I, "done"), own_request(Q, I), not status(Q, "delivered").
label("v_d2", "a built job-thread has a request not delivered").                            % §7.2: v4's
v_d2(T) :- status(T, "built"), node(T, "job-thread"), req_part_of(Q, T), node(Q, "request"), not status(Q, "delivered").
label("v_d3", "a delivered request whose initiative is not done").
v_d3(Q) :- status(Q, "delivered"), fulfils(I, Q), not status(I, "done").
label("v_d4", "a delivered request has an accepted line its resolution does not name").
v_d4(Q, N) :- status(Q, "delivered"), outcome(Q, N, "accepted"), line(Q, N, _), not resolution_of_line(Q, N).
label("v_d5", "an abandoned initiative has a part open").                                   % §7.2: the live v_d2
v_d5(I) :- status(I, "abandoned"), root(P, I), not closed(P).

% 16-18. requests (r113, r115, r117, r121). §7.2 drops v16a's date cutoff once old initiatives are compacted; until
% then it stays, so that the initiatives from before requests existed are not reported (the release compacts them).
label("v16a", "an initiative dated after 2026-10-23 that fulfils no request").
has_fulfils(I) :- fulfils(I, _).
v16a(I) :- node(I, "initiative"), date(I, D), D > "2026-10-23", not has_fulfils(I).
label("v17", "a request that is part of no job-thread, cites no origin and is raised for no request").
in_thread(Q)    :- req_part_of(Q, T), node(T, "job-thread").
in_thread(Q)    :- req_thread(Q).
cites_origin(Q) :- req_source(Q, O), node(O, K), origin(K).
raises_a_request(Q) :- req_raised_for(Q, _).
v17(Q) :- node(Q, "request"), not in_thread(Q), not cites_origin(Q), not raises_a_request(Q).
label("v18a", "a part is part of something kept by another context").
v18a(P, X) :- part_of(P, X), node(P, K), part(K), at(P, C1), at(X, C2), C1 != C2.
label("v18b", "a part is part of a request").
v18b(P, Q) :- part_of(P, Q), node(Q, "request").
label("v18c", "a blocked_by or for across contexts").
v18c(A, B) :- blocked_by(A, B), at(A, C1), at(B, C2), C1 != C2.
v18c(A, B) :- for(A, B), at(A, C1), at(B, C2), C1 != C2.
label("v18d", "an id of a kind kept in .shop/work/ with another context's path, other than the request a request is raised for").
raised_for_any(R) :- req_raised_for(_, R).
v18d(X) :- foreign(X), not raised_for_any(X).

% ---------------------------------------------------------------- terms (C8, C27)
% A requirement is in its capability's context; a scenario in its group's or requirement's. A scenario that names
% neither (v_s1 reports it) is read in the repository's own, the one bounded-context.
ctx_of(Q, X) :- has_req(C, Q), in(C, X).
ctx_of(S, X) :- generates(G, S), in(G, C), in(C, X).
ctx_of(S, X) :- node(S, "scenario"), not generated(S), node(X, "bounded-context").
label("v_t1", "a word the glossary avoids").
v_t1(X, W, T) :- mentions(X, W), avoid(T, W), term_of(T, Ctx), ctx_of(X, Ctx).
label("v_t2", "a term has two entries").
v_t2(T)       :- glossary_entry(T, N1, _), glossary_entry(T, N2, _), N1 < N2.
label("v_t3", "an avoided word is a term").
v_t3(W)       :- avoid(T, W), term_of(T, Ctx), glossary_entry(T2, _, W), term_of(T2, Ctx).
label("v_t4", "a term of a typed glossary has no category").
v_t4(T)       :- node(T, "term"), term_of(T, Ctx), typed(Ctx), not has_category(T).
label("v_t5", "a value names no attribute, or more than one").
v_t5(V)       :- category(V, "value"), not has_value_of(V).
v_t5(V)       :- value_of(V, K1, A1), value_of(V, K2, A2), (K1, A1) < (K2, A2).
label("v_t6", "two terms are written the same").
v_t6(T1, T2)  :- linearises(T1, L), linearises(T2, L), T1 < T2.

% ---------------------------------------------------------------- the parse (C2, C25)
% Every file of the spec is codified (§13.4): the 0.29 reader is gone, so `migrate upgrade` converts one that is not.
label("v_p0", "a spec file is not codified (no `language: codified-1`): run `migrate upgrade`").
v_p0(F)      :- uncodified(F).
% `model` parses every statement of a codified capability and of spec/universal.md in the context's grammar.
label("v_p1", "a requirement does not parse").
v_p1(Q, Why) :- unparsed(Q, Why).
label("v_p2", "a requirement parses to more than one tree").
v_p2(Q)      :- ambiguous(Q).
label("v_p3", "a line of a group's given block does not parse in the step grammar").
v_p3(G, L)   :- given_unparsed(G, L).

% ---------------------------------------------------------------- warnings
label("w_unserved_cap", "a capability serves no job").
w_unserved_cap(C)  :- node(C, "capability"), not serves(C, _), node(_, "job").
label("w_unserved_job", "a job nothing serves").
w_unserved_job(J)  :- node(J, "job"), not serves(_, J), not of_job(_, J).
seam_used(R)       :- seam(R, Up, Down), in(C, Down), in(D, Up), depends_on(C, D).
label("w_seam_unused", "a seam nothing crosses").
w_seam_unused(R)   :- seam(R, _, _), not seam_used(R).
label("w_uncited_obs", "an observation no initiative cites").
w_uncited_obs(O)   :- node(O, "observation"), not source(_, O).
label("w_many_requests", "more than five open requests to one upstream").                 % §7.2: v4's
w_many_requests(X) :- upstream(_, X), #count{ Q : upstream(Q, X), status(Q, "open") } > 5.
label("w_stale_intake", "a request accepted more than 90 days ago that no initiative fulfils").   % §7.2: v4's
w_stale_intake(Q)  :- status(Q, "accepted"), node(Q, "request"), not fulfilled(Q), age(Q, Days), Days > 90.
fulfilled(Q)       :- fulfils(_, Q).
label("w_stale_proposed", "an initiative proposed more than 90 days ago").                 % §7.2: the live w_stale_intake
w_stale_proposed(I) :- status(I, "proposed"), node(I, "initiative"), age(I, Days), Days > 90.

#show.
#show label/2.
#show v2/2.  #show v3/2.  #show v4/2.  #show v5/2.  #show v6/2.  #show v6b/1. #show v7/1.  #show v7c/2.
#show v8/1.  #show v9a/1. #show v9b/1. #show v9c/1. #show v9d/1. #show v9e/1. #show v9f/1. #show v9g/1.
#show v10a/2. #show v10b/1. #show v10c/1. #show v11/1. #show v12a/1. #show v12b/1. #show v13/1.
#show v15a/1. #show v15b/2. #show v15c/1. #show v15d/2. #show v15e/2. #show v15f/1.
#show v15g/1. #show v15h/1. #show v15i/1. #show v15j/2. #show v15k/1.
#show v_k3/1. #show v_k4/1. #show v_k5/1. #show v_k6/1. #show v_b1/1. #show v_b3/1.
#show v_s1/1. #show v_s2/1. #show v_s3/1. #show v_s4/1.
#show v_w1/1. #show v_w2/1. #show v_w3/2. #show v_w4/1.
#show v_d1/1. #show v_d2/1. #show v_d3/1. #show v_d4/2. #show v_d5/1.
#show v16a/1. #show v17/1. #show v18a/2. #show v18b/2. #show v18c/2. #show v18d/1.
#show v_t1/3. #show v_t2/1. #show v_t3/1. #show v_t4/1. #show v_t5/1. #show v_t6/2.
#show v_p0/1. #show v_p1/2. #show v_p2/1. #show v_p3/2.
#show w_unserved_cap/1. #show w_unserved_job/1. #show w_seam_unused/1. #show w_uncited_obs/1.
#show w_many_requests/1. #show w_stale_intake/1. #show w_stale_proposed/1.
