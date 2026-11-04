% grammar/check.lp: the check of `model logic` (design-r3 §6), a fixed meta-encoding, the same for every spec.
% It reads the facts of design-r3 §3 (one translation per fun, scripts/spec_facts.py) and the lexicon's domain, with
% one generic instance per noun phrase. A conflict is SEARCHED FOR: a witness of two requirements that fire on one
% trigger in one consistent pre-state and demand opposite things, found by one brave solve over every candidate pair.
% Shown: clash(A,B,Why) (L1), bad_set(R,A,From,To) (L3), unreachable(R,A,V) (L4), lint(R,E,T) (L5); with focus(A,B),
% pre(A,B,X,Attr,Val,Pol), the merged pre-state of one witness (a normal solve).
#defined role/3.  #defined named/3. #defined cond/5. #defined ccond/4. #defined crel/5. #defined holds/3.
#defined free/2.  #defined trig/5.  #defined resp/6. #defined oattr/4. #defined orel/4. #defined set/5.
#defined none/4.  #defined cnone/3. #defined uses/3. #defined nouse/3. #defined form/2. #defined sub/2.
#defined trans/4. #defined initial/3. #defined focus/2.

req(R) :- form(R,_).  req(R) :- role(R,_,_).  req(R) :- trig(R,_,_,_,_).  req(R) :- resp(R,_,_,_,_,_).
trg(R) :- trig(R,_,_,_,_).
universal(R) :- req(R), "U" <= R, R < "V".          % U1..U10: no capability name starts with a capital
% the terms a requirement names: its roles (v1, v2, ...) and its constants (actors, codes, value(A,V), none, ...)
term(R,X) :- role(R,X,_).      term(R,X) :- trig(R,_,_,X,_).  term(R,X) :- trig(R,_,_,_,X).
term(R,X) :- resp(R,_,_,_,X,_). term(R,X) :- resp(R,_,_,_,_,X). term(R,X) :- set(R,_,X,_,_).
term(R,X) :- uses(R,X,_).      term(R,X) :- uses(R,_,X).      term(R,X) :- nouse(R,X,_).  term(R,X) :- nouse(R,_,X).
term(R,X) :- crel(R,_,X,_,_).  term(R,X) :- crel(R,_,_,X,_).  term(R,X) :- orel(R,_,_,X).
term(R,X) :- holds(R,X,_).     term(R,X) :- holds(R,_,X).     term(R,X) :- free(R,X).
% kinds: a sub-kind is its kind (sub(K,K2): K is a kind of K2, transitively); two kinds are compatible when one is
subeq(K,K) :- role(_,_,K).  subeq(K,K) :- none(_,K,_,_).  subeq(K,K) :- cnone(_,K,_).
subeq(K,K3) :- sub(K,K2), subeq(K2,K3).
compat(K,K2) :- subeq(K,K2).  compat(K,K2) :- subeq(K2,K).

% ---- candidate pairs: the shared-vocabulary index, never the cross product ---------------------------------------
% A pair can clash only when its responses can: opposite polarities of one event, two values set of one attribute,
% exit_ok with exit_error, change_nothing with a changing response, a use with a "shall not use".
quiet(print). quiet(exit_ok). quiet(exit_error). quiet(change_nothing).
changing(R) :- resp(R,_,pos,E,_,_), not quiet(E).
cc(A,B) :- resp(A,_,P,E,_,_), resp(B,_,Q,E,_,_), P != Q.
cc(A,B) :- set(A,_,_,T,V), set(B,_,_,T,W), V != W.
cc(A,B) :- resp(A,_,pos,exit_ok,_,_), resp(B,_,pos,exit_error,_,_).
cc(A,B) :- resp(A,_,pos,change_nothing,_,_), changing(B).
cc(A,B) :- uses(A,_,_), nouse(B,_,_).
can(A,B) :- cc(A,B), A != B.  can(A,B) :- cc(B,A), A != B.
% two triggers of one event, a compatible doer, objects of compatible kinds (or one constant)
cand(A,B) :- can(A,B), trig(A,P,E,D1,X), trig(B,P,E,D2,Y), kin(A,B,X,Y), doerk(A,B,D1,D2).
kin(A,B,X,Y) :- can(A,B), trig(A,_,_,_,X), trig(B,_,_,_,Y), role(A,X,K), role(B,Y,K2), compat(K,K2).
kin(A,B,X,X) :- can(A,B), trig(A,_,_,_,X), trig(B,_,_,_,X), not role(A,X,_), not role(B,X,_).
doerk(A,B,D1,D2) :- can(A,B), trig(A,_,_,D1,_), trig(B,_,_,D2,_), role(A,D1,K), role(B,D2,K2), compat(K,K2).
doerk(A,B,any,D) :- can(A,B), trig(A,_,_,any,_), trig(B,_,_,D,_).
doerk(A,B,D,any) :- can(A,B), trig(A,_,_,D,_), trig(B,_,_,any,_).
doerk(A,B,D,D) :- can(A,B), trig(A,_,_,D,_), trig(B,_,_,D,_), not role(A,D,_).
% a triggered requirement with an untriggered one that binds one of its kinds
cand(A,B) :- can(A,B), trg(A), req(B), not trg(B), role(A,_,K), role(B,_,K2), compat(K,K2).
% a requirement with a U that shares an event or an attribute; a use with a "shall not use" (static, no trigger)
names(R,E) :- resp(R,_,_,E,_,_).  names(R,E) :- trig(R,_,E,_,_).
names(R,T) :- cond(R,_,T,_,_).    names(R,T) :- set(R,_,_,T,_).
cand(A,B) :- can(A,B), universal(A), names(A,N), names(B,N).
cand(A,B) :- can(A,B), uses(A,_,_), nouse(B,_,_).
pair(A,B) :- cand(A,B), A < B.  pair(A,B) :- cand(B,A), A < B.

% ---- unification: each role of B is one of A's roles of a compatible kind, or its own instance b(Y) -------------
{ map(A,B,Y,X) : role(A,X,K), compat(K,K2) } 1 :- pair(A,B), role(B,Y,K2).
:- map(A,B,Y1,X), map(A,B,Y2,X), Y1 < Y2.
:- map(A,B,Y,X), named(A,X,C), named(B,Y,C2), C != C2.
:- map(A,B,Y,X), oattr(A,X,T,V), oattr(B,Y,T,W), V != W.
side(A,B,A) :- pair(A,B).  side(A,B,B) :- pair(A,B).
mapped(A,B,Y) :- map(A,B,Y,_).
at(A,B,A,X,X) :- pair(A,B), term(A,X).
at(A,B,B,Y,X) :- map(A,B,Y,X).
at(A,B,B,Y,b(Y)) :- pair(A,B), role(B,Y,_), not mapped(A,B,Y).
at(A,B,B,Y,Y) :- pair(A,B), term(B,Y), not role(B,Y,_).
same(A,B,X,Y) :- at(A,B,A,X,Z), at(A,B,B,Y,Z).
kindof(A,B,Z,K) :- side(A,B,S), role(S,Y,K), at(A,B,S,Y,Z).
doer(A,B,X,Y) :- same(A,B,X,Y).
doer(A,B,any,Y) :- pair(A,B), term(B,Y).  doer(A,B,X,any) :- pair(A,B), term(A,X).
% the triggers are one event: its doer and its object unify, or the pair is out under this unification
fires(A,B) :- pair(A,B), trig(A,P,E,D1,X), trig(B,P,E,D2,Y), same(A,B,X,Y), doer(A,B,D1,D2).
out(A,B) :- pair(A,B), trg(A), trg(B), not fires(A,B).

% ---- the two states: 0 is the pre-state (the trigger happens there), 1 is 0 with the sets of the triggered side --
% An untriggered requirement paired with a triggered one is read at state 1 (its conditions there, its responses
% with the triggered one's); any other side is read at state 0.
late(A,B,S) :- side(A,B,S), not trg(S), side(A,B,O), trg(O).
w0(A,B,Z,T,V,P) :- side(A,B,S), not late(A,B,S), cond(S,Y,T,V,P), at(A,B,S,Y,Z).
n1(A,B,Z,T,V,P) :- late(A,B,S), cond(S,Y,T,V,P), at(A,B,S,Y,Z).
put(A,B,Z,T,V) :- side(A,B,S), trg(S), set(S,_,Y,T,V), at(A,B,S,Y,Z).
moved(A,B,Z,T) :- put(A,B,Z,T,_).
w1(A,B,Z,T,V,pos) :- put(A,B,Z,T,V).
w1(A,B,Z,T,V,pos) :- w0(A,B,Z,T,V,pos), not moved(A,B,Z,T).
w1(A,B,Z,T,V,neg) :- w0(A,B,Z,T,V,neg), not put(A,B,Z,T,V).
% out when inconsistent: two values of an attribute, a literal both ways (at state 1, only what the late side needs is asked:
% two sets of one attribute are a clash, not an inconsistency)
out(A,B) :- w0(A,B,Z,T,V,pos), w0(A,B,Z,T,W,pos), V < W.
out(A,B) :- w0(A,B,Z,T,V,pos), w0(A,B,Z,T,V,neg).
out(A,B) :- n1(A,B,Z,T,V,pos), w1(A,B,Z,T,W,pos), V != W.
out(A,B) :- n1(A,B,Z,T,V,pos), n1(A,B,Z,T,W,pos), V != W.
out(A,B) :- n1(A,B,Z,T,V,pos), w1(A,B,Z,T,V,neg).  out(A,B) :- n1(A,B,Z,T,V,neg), w1(A,B,Z,T,V,pos).
out(A,B) :- n1(A,B,Z,T,V,pos), n1(A,B,Z,T,V,neg).
cw(A,B,Z,C,P) :- side(A,B,S), ccond(S,Y,C,P), at(A,B,S,Y,Z).
out(A,B) :- cw(A,B,Z,C,pos), cw(A,B,Z,C,neg).
rw(A,B,Q,Z1,Z2,P) :- side(A,B,S), crel(S,Q,Y1,Y2,P), at(A,B,S,Y1,Z1), at(A,B,S,Y2,Z2).
out(A,B) :- rw(A,B,Q,Z1,Z2,pos), rw(A,B,Q,Z1,Z2,neg).
out(A,B) :- side(A,B,S1), side(A,B,S2), free(S1,X1), holds(S2,_,X2), at(A,B,S1,X1,Z), at(A,B,S2,X2,Z).
% "no K is v" is universal over the merged state of its side (§3.3): no instance of K or a sub-kind there is v
pos(A,B,0,Z,T,V) :- w0(A,B,Z,T,V,pos).
pos(A,B,1,Z,T,V) :- w1(A,B,Z,T,V,pos).  pos(A,B,1,Z,T,V) :- n1(A,B,Z,T,V,pos).
state(A,B,S,1) :- late(A,B,S).  state(A,B,S,0) :- side(A,B,S), not late(A,B,S).
out(A,B) :- state(A,B,S,N), none(S,K,T,V), pos(A,B,N,Z,T,V), kindof(A,B,Z,K2), subeq(K2,K).
out(A,B) :- side(A,B,S), cnone(S,K,C), cw(A,B,Z,C,pos), kindof(A,B,Z,K2), subeq(K2,K).

% ---- L1: the clash of a pair, under one unification ---------------------------------------------------------------
% A pair that cannot fire together under this unification is out: soft, so that one pair never makes the program
% UNSAT and hides every other finding.
ok(A,B) :- pair(A,B), not out(A,B).
% the restrictions of B's object (its kind, its `for`) are entailed by A's object, or the other way round
gap(A,B,X,Y) :- map(A,B,Y,X), oattr(B,Y,T,W), not oattr(A,X,T,W).
gap(A,B,X,Y) :- map(A,B,Y,X), orel(B,Q,Y,Z), not relby(A,B,X,Q,Z).
relby(A,B,X,Q,Z) :- map(A,B,Y,X), orel(B,Q,Y,Z), orel(A,Q,X,X2), same(A,B,X2,Z).
pag(A,B,X,Y) :- map(A,B,Y,X), oattr(A,X,T,W), not oattr(B,Y,T,W).
pag(A,B,X,Y) :- map(A,B,Y,X), orel(A,Q,X,X2), not relof(A,B,Y,Q,X2).
relof(A,B,Y,Q,X2) :- map(A,B,Y,X), orel(A,Q,X,X2), orel(B,Q,Y,Z), same(A,B,X2,Z).
clash(A,B,pos_neg) :- ok(A,B), resp(A,_,pos,E,D1,X), resp(B,_,neg,E,D2,Y), doer(A,B,D1,D2), same(A,B,X,Y),
                      not gap(A,B,X,Y).
clash(A,B,neg_pos) :- ok(A,B), resp(A,_,neg,E,D1,X), resp(B,_,pos,E,D2,Y), doer(A,B,D1,D2), same(A,B,X,Y),
                      not pag(A,B,X,Y).
clash(A,B,set) :- ok(A,B), set(A,_,X,T,V), set(B,_,Y,T,W), same(A,B,X,Y), V != W.
clash(A,B,exit) :- ok(A,B), resp(A,_,pos,exit_ok,D1,_), resp(B,_,pos,exit_error,D2,_), doer(A,B,D1,D2).
clash(A,B,exit) :- ok(A,B), resp(A,_,pos,exit_error,D1,_), resp(B,_,pos,exit_ok,D2,_), doer(A,B,D1,D2).
clash(A,B,change) :- ok(A,B), resp(A,_,pos,change_nothing,D1,_), resp(B,_,pos,E,D2,_), not quiet(E),
                     doer(A,B,D1,D2).
clash(A,B,change) :- ok(A,B), resp(B,_,pos,change_nothing,D2,_), resp(A,_,pos,E,D1,_), not quiet(E),
                     doer(A,B,D1,D2).
clash(A,B,use) :- ok(A,B), uses(A,D1,X), nouse(B,D2,Y), doer(A,B,D1,D2), same(A,B,X,Y).
clash(A,B,use) :- ok(A,B), nouse(A,D1,X), uses(B,D2,Y), doer(A,B,D1,D2), same(A,B,X,Y).
% a requirement whose own pre-state is inconsistent, or that demands opposite things of itself
self(R) :- cond(R,X,T,V,pos), cond(R,X,T,W,pos), V < W.
self(R) :- cond(R,X,T,V,pos), cond(R,X,T,V,neg).
self(R) :- ccond(R,X,C,pos), ccond(R,X,C,neg).
self(R) :- crel(R,Q,X,Y,pos), crel(R,Q,X,Y,neg).
self(R) :- none(R,K,T,V), role(R,X,K2), subeq(K2,K), cond(R,X,T,V,pos).
self(R) :- cnone(R,K,C), role(R,X,K2), subeq(K2,K), ccond(R,X,C,pos).
self(R) :- free(R,X), holds(R,_,X).
self(R) :- set(R,_,X,T,V), set(R,_,X,T,W), V < W.
self(R) :- resp(R,_,pos,E,D,X), resp(R,_,neg,E,D,X).
clash(R,R,self) :- self(R).
#show clash/3.

% ---- L3: a set whose pre-value (its own condition, or none) has no transition to the new value -------------------
edge(T,U,V) :- trans(_,T,U,V).  moving(T) :- edge(T,_,_).  entered(T,V) :- edge(T,_,V).
bad_set(R,T,U,V) :- set(R,_,X,T,V), cond(R,X,T,U,pos), U != V, moving(T), not edge(T,U,V).
known(R,X,T) :- cond(R,X,T,_,pos).
bad_set(R,T,none,V) :- set(R,_,X,T,V), not known(R,X,T), moving(T), not entered(T,V).
#show bad_set/4.
% ---- L4: a value a requirement's pre-state needs that no path reaches from an initial value -----------------------
reach(T,V) :- initial(_,T,V).  reach(T,W) :- reach(T,V), edge(T,V,W).
unreachable(R,T,V) :- cond(R,_,T,V,pos), moving(T), not reach(T,V).
#show unreachable/3.
% ---- L5: an untriggered positive event obligation, with the triggered requirements that react to its event -------
% holding a resource is a state, not an event ("every stage shall hold the initiative lock" is no G p trap)
stative(set(T,V)) :- resp(_,_,_,set(T,V),_,_).  stative(hold(S)) :- resp(_,_,_,hold(S),_,_).  stative(change_nothing).
l5(R,E) :- resp(R,_,pos,E,_,_), not trg(R), not stative(E).
reacts(E) :- l5(_,E), trig(_,_,E,_,_).
lint(R,E,T) :- l5(R,E), trig(T,_,E,_,_).
lint(R,E,none) :- l5(R,E), not reacts(E).
#show lint/3.

% ---- the witness of one pair (a normal solve with focus(A,B)): it clashes, and its merged pre-state is shown -----
hit(A,B) :- clash(A,B,W), W != self.
:- focus(A,B), pair(A,B), not hit(A,B).
pre(A,B,Z,T,V,P) :- focus(A,B), w0(A,B,Z,T,V,P).
pre(A,B,Z,T,V,P) :- focus(A,B), n1(A,B,Z,T,V,P).
#show pre/6.
