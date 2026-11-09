% grammar/check.lp: the check of `model logic` (design-r3 §6), a fixed meta-encoding, the same for every spec.
% It reads the facts of design-r3 §3 (one translation per fun, scripts/spec_facts.py) and the lexicon's domain, with
% one generic instance per noun phrase. A conflict is SEARCHED FOR: a witness of two requirements that fire on one
% trigger in one consistent pre-state and demand opposite things, found by one brave solve over every candidate pair.
% Shown: clash(A,B,Why) (L1), maybe(A,B,Why,C) (L6: a clash that depends on the prose condition C), bad_set(R,A,From,To) (L3), unreachable(R,A,V) (L4), lint(R,E,T) (L5); with focus(A,B),
% pre(A,B,X,Attr,Val,Pol), the merged pre-state of one witness (a normal solve).
#defined role/3.  #defined named/3. #defined cond/5. #defined ccond/4. #defined crel/5. #defined holds/3.
#defined free/2.  #defined trig/5.  #defined resp/6. #defined oattr/4. #defined orel/4. #defined set/5.
#defined none/4.  #defined cnone/3. #defined uses/3. #defined nouse/3. #defined form/2. #defined sub/2.
#defined trans/4. #defined initial/3. #defined focus/2. #defined focusm/2. #defined rnone/4. #defined the/2.
#defined fun/1.   #defined prose/1. #defined dalt/2.  #defined dlit/5. #defined uall/3. #defined urel/4.
#defined uattr/4. #defined ucond/5. #defined uccond/4.

req(R) :- form(R,_).  req(R) :- role(R,_,_).  req(R) :- trig(R,_,_,_,_).  req(R) :- resp(R,_,_,_,_,_).
trg(R) :- trig(R,_,_,_,_).
universal(R) :- req(R), "U" <= R, R < "V".          % U1..U10: no capability name starts with a capital
% the terms a requirement names: its roles (v1, v2, ...) and its constants (actors, codes, value(A,V), none, ...)
term(R,X) :- role(R,X,_).      term(R,X) :- trig(R,_,_,X,_).  term(R,X) :- trig(R,_,_,_,X).
term(R,X) :- resp(R,_,_,_,X,_). term(R,X) :- resp(R,_,_,_,_,X). term(R,X) :- set(R,_,X,_,_).
term(R,X) :- uses(R,X,_).      term(R,X) :- uses(R,_,X).      term(R,X) :- nouse(R,X,_).  term(R,X) :- nouse(R,_,X).
term(R,X) :- crel(R,_,X,_,_).  term(R,X) :- crel(R,_,_,X,_).  term(R,X) :- orel(R,_,_,X).
term(R,X) :- holds(R,X,_).     term(R,X) :- holds(R,_,X).     term(R,X) :- free(R,X).
term(R,X) :- urel(R,_,_,X).
% kinds: a sub-kind is its kind (sub(K,K2): K is a kind of K2, transitively); two kinds are compatible when one is
subeq(K,K) :- role(_,_,K).  subeq(K,K) :- none(_,K,_,_).  subeq(K,K) :- cnone(_,K,_).
subeq(K,K3) :- sub(K,K2), subeq(K2,K3).
compat(K,K2) :- subeq(K,K2).  compat(K,K2) :- subeq(K2,K).

% ---- candidate pairs: the shared-vocabulary index, never the cross product ---------------------------------------
% A pair can clash only when its responses can: opposite polarities of one event, two values set of one attribute,
% exit_ok with exit_error, change_nothing with a changing response, a use with a "shall not use".
quiet(print). quiet(exit_ok). quiet(exit_error). quiet(change_nothing).
% "D shall do E and change nothing" changes nothing but E: a requirement's own events are excepted from its own
% change nothing, and from another's change nothing when that one names the same event
own(R,E) :- resp(R,_,pos,E,_,_).
#defined cand/2. #defined kseed/1.
subeq(K,K) :- kseed(K).
% the EARS unwanted-behaviour form ("If T, then ...") is the exception to the other requirements on its trigger: it
% wins over them, so an `if` requirement and a non-`if` one are never a pair (two of one form still are)
exc(R) :- form(R,if).  exc(R) :- form(R,while_if).  exc(R) :- form(R,where_if).
over(A,B) :- cand(A,B), exc(A), not exc(B).  over(A,B) :- cand(A,B), exc(B), not exc(A).
pair(A,B) :- cand(A,B), A < B, not over(A,B).  pair(A,B) :- cand(B,A), A < B, not over(B,A).

% ---- unification: each role of B is one of A's roles of a compatible kind, or its own instance b(Y) -------------
% A `Named` code is one thing (design-r3 §3): every role of a requirement with one code is its first such role
% (`canon`), and a code both sides name is one role of the pair.
nrep(S,Y) :- named(S,Y,C), named(S,Y0,C), Y0 < Y.
canon(S,Y,Y0) :- named(S,Y,C), named(S,Y0,C), not nrep(S,Y0).  canon(S,Y,Y) :- role(S,Y,_), not named(S,Y,_).
{ map(A,B,Y,X) : role(A,X,K), compat(K,K2), not nrep(A,X) } 1 :- pair(A,B), role(B,Y,K2), not nrep(B,Y).
:- map(A,B,Y1,X), map(A,B,Y2,X), Y1 < Y2.
:- map(A,B,Y,X), named(A,X,C), named(B,Y,C2), C != C2.
:- pair(A,B), named(A,X,C), named(B,Y,C), not nrep(A,X), not nrep(B,Y), not map(A,B,Y,X).
:- map(A,B,Y,X), oattr(A,X,T,V), oattr(B,Y,T,W), V != W.
% A definite noun phrase with no antecedent (`the(R,V)`: "the work-item" never introduced) is the one thing of its
% kind: when one side has one, each role of that kind the other side's pre-state or definites name is it, or the
% pair is out under this unification.
tdef(S,K) :- the(S,X), role(S,X,K).
named1(S,Y) :- the(S,Y).  named1(S,Y) :- cond(S,Y,_,_,_).  named1(S,Y) :- ccond(S,Y,_,_).
named1(S,Y) :- crel(S,_,Y,_,_).  named1(S,Y) :- crel(S,_,_,Y,_).  named1(S,Y) :- trig(S,_,_,Y,_).
named1(S,Y) :- trig(S,_,_,_,Y).
tmap(A,B,Y) :- map(A,B,Y,X), the(A,X).
side(A,B,A) :- pair(A,B).  side(A,B,B) :- pair(A,B).
mapped(A,B,Y) :- map(A,B,Y,_).
at(A,B,A,X,Z) :- pair(A,B), term(A,X), canon(A,X,Z).
at(A,B,A,X,X) :- pair(A,B), term(A,X), not role(A,X,_).
at(A,B,B,Y,X) :- pair(A,B), canon(B,Y,Y0), map(A,B,Y0,X).
at(A,B,B,Y,b(Y0)) :- pair(A,B), canon(B,Y,Y0), not mapped(A,B,Y0).
at(A,B,B,Y,Y) :- pair(A,B), term(B,Y), not role(B,Y,_).
same(A,B,X,Y) :- at(A,B,A,X,Z), at(A,B,B,Y,Z).
kindof(A,B,Z,K) :- side(A,B,S), role(S,Y,K), at(A,B,S,Y,Z).
doer(A,B,X,Y) :- same(A,B,X,Y).
doer(A,B,any,Y) :- pair(A,B), term(B,Y).  doer(A,B,X,any) :- pair(A,B), term(A,X).
% the triggers are one event: its doer and its object unify, or the pair is out under this unification
fires(A,B) :- pair(A,B), trig(A,P,E,D1,X), trig(B,P,E,D2,Y), same(A,B,X,Y), doer(A,B,D1,D2).
out(A,B) :- pair(A,B), trg(A), trg(B), not fires(A,B).
out(A,B) :- pair(A,B), tdef(A,K), named1(B,Y), role(B,Y,K), not tmap(A,B,Y).
out(A,B) :- pair(A,B), tdef(B,K), the(B,Y), role(B,Y,K), named1(A,X), role(A,X,K), not map(A,B,Y,X).

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
% "no K is <rel> Y", "X is <rel> no K" (rnone): no instance of K is so related in the merged state
out(A,B) :- side(A,B,S), rnone(S,Q,kind(K),Y), at(A,B,S,Y,Zy), rw(A,B,Q,Z,Zy,pos), kindof(A,B,Z,K2), subeq(K2,K).
out(A,B) :- side(A,B,S), rnone(S,Q,X,kind(K)), at(A,B,S,X,Zx), rw(A,B,Q,Zx,Z,pos), kindof(A,B,Z,K2), subeq(K2,K).
% a functional relation (`fun(Q)`: a relation row of cardinality one, or a preposition, spec_logic_vocab) relates a
% thing to one thing: two images under one unification are out
redge(A,B,Q,Z1,Z2) :- rw(A,B,Q,Z1,Z2,pos).
redge(A,B,Q,Z1,Z2) :- side(A,B,S), orel(S,Q,Y1,Y2), at(A,B,S,Y1,Z1), at(A,B,S,Y2,Z2).
out(A,B) :- fun(Q), redge(A,B,Q,Z,Z1), redge(A,B,Q,Z,Z2), Z1 < Z2.

% ---- a defined condition read through its definition (`dalt(C,N)`, `dlit(C,N,Attr,Val,Pol)`: the ways through a
% Def whose literals are all on its own subject, spec_facts.def_facts) under `no`, `every` and a negation --------
has(A,B,0,Z,T,V,P) :- w0(A,B,Z,T,V,P).
has(A,B,1,Z,T,V,P) :- w1(A,B,Z,T,V,P).  has(A,B,1,Z,T,V,P) :- n1(A,B,Z,T,V,P).
% the instances a definition is asked of: (side's state N, instance Z, condition C)
ask(A,B,N,Z,C) :- side(A,B,S), state(A,B,S,N), cnone(S,K,C), kindof(A,B,Z,K2), subeq(K2,K), dalt(C,_).
ask(A,B,N,Z,C) :- side(A,B,S), state(A,B,S,N), ccond(S,Y,C,neg), at(A,B,S,Y,Z), dalt(C,_).
ask(A,B,N,Z,C) :- umatch(A,B,S,U,Z), state(A,B,S,N), uccond(S,U,C,_), dalt(C,_).
% a way through C is entailed on Z when each of its literals is; broken when one is contradicted. What a side's
% "every K ... is v" says of Z (`ucond`) counts as Z's own value here (hasu): "every line is `refused`" makes a line
% settled, so "a line is not settled" is out (requests r20, r22)
hasu(A,B,N,Z,T,V,P) :- has(A,B,N,Z,T,V,P).
hasu(A,B,N,Z,T,V,pos) :- umatch(A,B,S,U,Z), state(A,B,S,N), ucond(S,U,T,V,pos).
unent(A,B,N,Z,C,W) :- ask(A,B,N,Z,C), dlit(C,W,T,V,pos), not hasu(A,B,N,Z,T,V,pos).
negd(A,B,N,Z,T,V) :- has(A,B,N,Z,T,V,neg).
negd(A,B,N,Z,T,V) :- hasu(A,B,N,Z,T,W,pos), dlit(_,_,T,V,_), V != W.
unent(A,B,N,Z,C,W) :- ask(A,B,N,Z,C), dlit(C,W,T,V,neg), not negd(A,B,N,Z,T,V).
ent(A,B,N,Z,C) :- ask(A,B,N,Z,C), dalt(C,W), not unent(A,B,N,Z,C,W).
brk(A,B,N,Z,C,W) :- ask(A,B,N,Z,C), dlit(C,W,T,V,pos), negd(A,B,N,Z,T,V).
brk(A,B,N,Z,C,W) :- ask(A,B,N,Z,C), dlit(C,W,T,V,neg), hasu(A,B,N,Z,T,V,pos).
live(A,B,N,Z,C) :- ask(A,B,N,Z,C), dalt(C,W), not brk(A,B,N,Z,C,W).
refuted(A,B,N,Z,C) :- ask(A,B,N,Z,C), not live(A,B,N,Z,C).
out(A,B) :- side(A,B,S), state(A,B,S,N), cnone(S,K,C), kindof(A,B,Z,K2), subeq(K2,K), ent(A,B,N,Z,C).
out(A,B) :- side(A,B,S), state(A,B,S,N), ccond(S,Y,C,neg), at(A,B,S,Y,Z), ent(A,B,N,Z,C).
% "every K <restrictions> is C" (uall, urel, uattr; ucond, uccond): each instance of K with the restrictions is C
ucand(A,B,S,U,Z) :- side(A,B,S), uall(S,U,K), kindof(A,B,Z,K2), subeq(K2,K).
umiss(A,B,S,U,Z) :- ucand(A,B,S,U,Z), urel(S,Q,U,W), at(A,B,S,W,Zw), not rw(A,B,Q,Z,Zw,pos).
umiss(A,B,S,U,Z) :- ucand(A,B,S,U,Z), state(A,B,S,N), uattr(S,U,T,V), not has(A,B,N,Z,T,V,pos).
umatch(A,B,S,U,Z) :- ucand(A,B,S,U,Z), not umiss(A,B,S,U,Z).
out(A,B) :- umatch(A,B,S,U,Z), state(A,B,S,N), ucond(S,U,T,V,pos), has(A,B,N,Z,T,W,pos), V != W.
out(A,B) :- umatch(A,B,S,U,Z), state(A,B,S,N), ucond(S,U,T,V,pos), has(A,B,N,Z,T,V,neg).
out(A,B) :- umatch(A,B,S,U,Z), state(A,B,S,N), ucond(S,U,T,V,neg), has(A,B,N,Z,T,V,pos).
out(A,B) :- umatch(A,B,S,U,Z), uccond(S,U,C,pos), cw(A,B,Z,C,neg).
out(A,B) :- umatch(A,B,S,U,Z), uccond(S,U,C,neg), cw(A,B,Z,C,pos).
out(A,B) :- umatch(A,B,S,U,Z), state(A,B,S,N), uccond(S,U,C,pos), refuted(A,B,N,Z,C).
out(A,B) :- umatch(A,B,S,U,Z), state(A,B,S,N), uccond(S,U,C,neg), ent(A,B,N,Z,C).

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
cl(A,B,pos_neg) :- ok(A,B), resp(A,_,pos,E,D1,X), resp(B,_,neg,E,D2,Y), doer(A,B,D1,D2), same(A,B,X,Y),
                      not gap(A,B,X,Y).
cl(A,B,neg_pos) :- ok(A,B), resp(A,_,neg,E,D1,X), resp(B,_,pos,E,D2,Y), doer(A,B,D1,D2), same(A,B,X,Y),
                      not pag(A,B,X,Y).
cl(A,B,set) :- ok(A,B), set(A,_,X,T,V), set(B,_,Y,T,W), same(A,B,X,Y), V != W.
cl(A,B,exit) :- ok(A,B), resp(A,_,pos,exit_ok,D1,_), resp(B,_,pos,exit_error,D2,_), doer(A,B,D1,D2).
cl(A,B,exit) :- ok(A,B), resp(A,_,pos,exit_error,D1,_), resp(B,_,pos,exit_ok,D2,_), doer(A,B,D1,D2).
cl(A,B,change) :- ok(A,B), resp(A,_,pos,change_nothing,D1,_), resp(B,_,pos,E,D2,_), not quiet(E),
                     not own(A,E), doer(A,B,D1,D2).
cl(A,B,change) :- ok(A,B), resp(B,_,pos,change_nothing,D2,_), resp(A,_,pos,E,D1,_), not quiet(E),
                     not own(B,E), doer(A,B,D1,D2).
cl(A,B,use) :- ok(A,B), uses(A,D1,X), nouse(B,D2,Y), doer(A,B,D1,D2), same(A,B,X,Y).
cl(A,B,use) :- ok(A,B), nouse(A,D1,X), uses(B,D2,Y), doer(A,B,D1,D2), same(A,B,X,Y).
% a clash whose witness merges onto an instance a prose condition one side states (`prose(C)`: no Def) and something
% the other side states of it that the first does not: a definition of C could refute it, so it is L6, not L1
lit(A,B,S,Z,c(T,V,P)) :- side(A,B,S), cond(S,Y,T,V,P), at(A,B,S,Y,Z).
lit(A,B,S,Z,k(C,P)) :- side(A,B,S), ccond(S,Y,C,P), at(A,B,S,Y,Z).
lit(A,B,S,Z1,r(Q,Z2,P)) :- side(A,B,S), crel(S,Q,Y1,Y2,P), at(A,B,S,Y1,Z1), at(A,B,S,Y2,Z2).
lit(A,B,S,Z2,i(Q,Z1,P)) :- side(A,B,S), crel(S,Q,Y1,Y2,P), at(A,B,S,Y1,Z1), at(A,B,S,Y2,Z2).
dep(A,B,C) :- lit(A,B,S,Z,k(C,_)), prose(C), side(A,B,S2), S2 != S, lit(A,B,S2,Z,L), not lit(A,B,S,Z,L).
depends(A,B) :- dep(A,B,_).
clash(A,B,W) :- cl(A,B,W), not depends(A,B).
maybe(A,B,W,C) :- cl(A,B,W), dep(A,B,C).
#show maybe/4.
% a requirement whose own pre-state is inconsistent, or that demands opposite things of itself
cd(R,Z,T,V,P) :- cond(R,X,T,V,P), canon(R,X,Z).  ccd(R,Z,C,P) :- ccond(R,X,C,P), canon(R,X,Z).
self(R) :- cd(R,X,T,V,pos), cd(R,X,T,W,pos), V < W.
self(R) :- cd(R,X,T,V,pos), cd(R,X,T,V,neg).
self(R) :- ccd(R,X,C,pos), ccd(R,X,C,neg).
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
% focus/2 is an external, false unless a witness solve assigns it true, so the check and every witness share one grounding
% (focusm/2 the same for an L6: a witness that clashes and depends on a prose condition)
#external focus(A,B) : pair(A,B).  #external focusm(A,B) : pair(A,B).
hit(A,B) :- clash(A,B,W), W != self.  hitm(A,B) :- maybe(A,B,_,_).
:- focus(A,B), pair(A,B), not hit(A,B).
:- focusm(A,B), pair(A,B), not hitm(A,B).
foc(A,B) :- focus(A,B).  foc(A,B) :- focusm(A,B).
pre(A,B,Z,T,V,P) :- foc(A,B), w0(A,B,Z,T,V,P).
pre(A,B,Z,T,V,P) :- foc(A,B), n1(A,B,Z,T,V,P).
prec(A,B,Z,C,P) :- foc(A,B), cw(A,B,Z,C,P).
#show pre/6.  #show prec/5.
