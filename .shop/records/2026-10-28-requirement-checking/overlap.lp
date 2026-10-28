% Set-level checks over parsed Behaviour lines. Open world: two triggers overlap unless shown disjoint.
% ---- domain axioms (hand-written, small) ------------------------------------------------------
implies(gives, ends). implies(applies, ends). implies(formulates, ends). implies(drafts, ends).
ev_rel(E, E)  :- event(_, E).
ev_rel(E, F)  :- implies(E, F).
ev_rel(F, E)  :- implies(E, F).
ev_rel(E, F)  :- implies(E, ends), implies(F, ends).   % two outcomes of one round may co-occur (open world)
disjoint(question, no_question). disjoint(change_list, no_change_list). 
disjoint(fault, X) :- qual(_, X), X != fault.   % a round that ends in a fault gives nothing else
disjoint(A, B) :- disjoint(B, A).
kind_ok(A, B) :- kind(A, K), kind(B, K).
kind_ok(A, B) :- kind(A, "any"), line(B,_,_).
kind_ok(A, B) :- kind(B, "any"), line(A,_,_).
kind_ok(A, B) :- line(A,_,_), line(B,_,_), not kind(A,_), not kind(B,_).
active(L) :- line(L,_,_), not retired(L).

% ---- overlap: same system, same subject, same kind, related events, no disjoint qualifiers -------
sep(A, B) :- qual(A, X), qual(B, Y), disjoint(X, Y).
overlap(A, B) :- line(A,_,_), line(B,_,_), A < B, system(A, S), system(B, S), subject(A, H), subject(B, H),
                 kind_ok(A, B), event(A, E), event(B, F), ev_rel(E, F), not sep(A, B).

% ---- response conflicts ------------------------------------------------------------------------
clash(A, B, "two target statuses") :- resp(A, transition, O, X), resp(B, transition, O, Y), X != Y, X != "next", Y != "next".
clash(A, B, "transition vs keep status") :- resp(A, transition, O, _), resp(B, keep_status, O, _).
clash(A, B, "transition vs keep status") :- resp(A, keep_status, O, _), resp(B, transition, O, _).
clash(A, B, "transition vs no transition") :- resp(A, transition, _, _), resp(B, no_transition, _, _).
clash(A, B, "transition vs no transition") :- resp(A, no_transition, _, _), resp(B, transition, _, _).
clash(A, B, "start round vs start no round") :- resp(A, start_round, K, _), resp(B, no_round, K, _).
clash(A, B, "start round vs start no round") :- resp(A, no_round, K, _), resp(B, start_round, K, _).
same_resp(A, B) :- resp(A, V, O, X), resp(B, V, O, X).

% c1. overlapping triggers, clashing responses, neither says which wins
c1_conflict(A, B, Why) :- overlap(A, B), clash(A, B, Why), active(A), active(B).
% c2. a catch-all whose trigger covers a more specific line with a different response: B's event fires A too
ov(A, B) :- overlap(A, B). ov(B, A) :- overlap(A, B).
c2_catchall(A, B) :- ov(A, B), event(A, ends), event(B, F), implies(F, ends), not same_resp(A, B),
                     active(A), active(B), qual_count(A, N), N <= 1.
qual_count(L, N) :- line(L,_,_), N = #count { X : qual(L, X) }.
% c3. overlapping triggers with the same response: one widens/duplicates the other (retired lines included)
c3_widens(A, B) :- overlap(A, B), same_resp(A, B).
% c4. a universal prohibition of a system and a line of that system that presupposes the prohibited act
c4_presupposes(A, B) :- resp(A, runs_nothing, _, _), system(A, S), system(B, S), B != A, resp(B, presupposes_run, _, _).
c4_presupposes(A, B) :- resp(A, runs_nothing, _, _), system(A, S), system(B, S), B != A, resp(B, runs, _, _).
% per line
p1_where_event(L) :- where_event(L).
p2_many(L, N) :- many_responses(L, N).
#show c1_conflict/3. #show c2_catchall/2. #show c3_widens/2. #show c4_presupposes/2. #show p1_where_event/1. #show p2_many/2.
