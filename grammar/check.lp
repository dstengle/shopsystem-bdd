% grammar/check.lp: the check of `model logic` (design-r3 §6), a fixed meta-encoding, the same for every spec.
% It reads the facts of design-r3 §3 (one translation per fun, scripts/spec_facts.py) and the lexicon's domain, with
% one generic instance per noun phrase. A conflict is SEARCHED FOR: a witness of two requirements that fire on one
% trigger in one consistent pre-state and demand opposite things, found by one brave solve over every candidate pair.
% Shown: clash(A,B,Why) (L1), maybe(A,B,Why,C) (L6: a clash that depends on the prose condition C),
% forbid(A,B) (L7: a "shall not" line that forbids what a "may" line permits), bad_set(R,A,From,To) (L3), unreachable(R,A,V) (L4), lint(R,E,T) (L5), coded(A,B) and fit(A,B) (a pair set aside);
% in the part `witness`, with focus(A,B), pre(A,B,X,Attr,Val,Pol), the merged pre-state of one witness.
% THE RULE OF THIS FILE: never join two requirement-level facts on a vocabulary word (an event, a kind, a code, an
% attribute); copy each to the pair, or join on a whole key, first. The grounder orders a body's literals by their
% domains, not as written, so a guard written first does not keep such a join from ranging over all pairs of lines:
% it passes at a few hundred lines and grounds for minutes at thousands (tests/scripts/test_check_scale.py).
#defined role/3.  #defined named/3. #defined cond/5. #defined ccond/4. #defined crel/5. #defined holds/3.
#defined free/2.  #defined trig/5.  #defined resp/6. #defined oattr/4. #defined orel/4. #defined set/5.
#defined none/4.  #defined cnone/3. #defined uses/3. #defined nouse/3. #defined form/2. #defined sub/2.
#defined trans/4. #defined initial/3. #defined focus/2. #defined focusm/2. #defined rnone/4. #defined the/2.
#defined fun/1.   #defined prose/1. #defined dalt/2.  #defined dlit/5. #defined uall/3. #defined urel/4.
#defined uattr/4. #defined ucond/5. #defined uccond/4. #defined pre/6. #defined prec/5.
#defined each/2.   #defined only/5. #defined rattr/4.  #defined rrel/4.  #defined akind/2.
#defined cnl4/1.  #defined cmp/5.  #defined count/7.  #defined nec/5.  #defined necsub/2.

req(R) :- form(R,_).  req(R) :- role(R,_,_).  req(R) :- trig(R,_,_,_,_).  req(R) :- resp(R,_,_,_,_,_).
trg(R) :- trig(R,_,_,_,_).
universal(R) :- req(R), "U" <= R, R < "V".          % U1..U10: no capability name starts with a capital
% the terms a requirement names: its roles (v1, v2, ...) and its constants (actors, codes, value(A,V), none, ...)
term(R,X) :- role(R,X,_).      term(R,X) :- trig(R,_,_,X,_).  term(R,X) :- trig(R,_,_,_,X).
term(R,X) :- resp(R,_,_,_,X,_). term(R,X) :- resp(R,_,_,_,_,X). term(R,X) :- set(R,_,X,_,_).
term(R,X) :- uses(R,X,_).      term(R,X) :- uses(R,_,X).      term(R,X) :- nouse(R,X,_).  term(R,X) :- nouse(R,_,X).
term(R,X) :- crel(R,_,X,_,_).  term(R,X) :- crel(R,_,_,X,_).  term(R,X) :- orel(R,_,_,X).
term(R,X) :- holds(R,X,_).     term(R,X) :- holds(R,_,X).     term(R,X) :- free(R,X).
term(R,X) :- urel(R,_,_,X).    term(R,X) :- count(R,_,_,X,_,_,_).
term(R,X) :- cmp(R,X,_,_,_).  term(R,C) :- cmp(R,_,_,C,_).
% kinds: a sub-kind is its kind (sub(K,K2): K is a kind of K2, transitively); two kinds are compatible when one is
subeq(K,K) :- role(_,_,K).  subeq(K,K) :- none(_,K,_,_).  subeq(K,K) :- cnone(_,K,_).
subeq(K,K3) :- sub(K,K2), subeq(K2,K3).
compat(K,K2) :- subeq(K,K2).  compat(K,K2) :- subeq(K2,K).

% ---- candidate pairs: the shared-vocabulary index, never the cross product ---------------------------------------
% A pair can clash only when its responses can: opposite polarities of one event, two values set of one attribute,
% exit_ok with exit_error, change_nothing with a changing response, a use with a "shall not use". Each requirement's
% clash keys (`key`) and the keys another needs to clash with it (`dem`) are found first; then every join below is on
% a whole shared key (trigger and key, or an untriggered or universal requirement's own keys), so no rule ranges over
% all pairs of requirements, and no join is bound on a word only (an event, a kind) that thousands of lines share.
quiet(print). quiet(exit_ok). quiet(exit_error). quiet(change_nothing).
% "D shall do E and change nothing" changes nothing but E: a requirement's own events are excepted from its own
% change nothing, and from another's change nothing when that one names the same event
own(R,E) :- resp(R,_,pos,E,_,_).
key(R,ev(P,E)) :- resp(R,_,P,E,_,_).  key(R,at(T,V)) :- set(R,_,_,T,V).
key(R,use) :- uses(R,_,_).  key(R,nouse) :- nouse(R,_,_).
vals(T,V) :- set(_,_,_,T,V).  posev(E) :- resp(_,_,pos,E,_,_).
dem(R,ev(neg,E)) :- key(R,ev(pos,E)).  dem(R,ev(pos,E)) :- key(R,ev(neg,E)).
dem(R,at(T,W)) :- key(R,at(T,V)), vals(T,W), V != W.
dem(R,ev(pos,exit_error)) :- key(R,ev(pos,exit_ok)).  dem(R,nouse) :- key(R,use).
% a permission is forbidden by a "shall not" of its act, and nothing else (L7)
dem(R,ev(neg,E)) :- key(R,ev(may,E)).  dem(R,ev(may,E)) :- key(R,ev(neg,E)).
dem(R,ev(pos,E)) :- key(R,ev(pos,change_nothing)), posev(E), not quiet(E), not own(R,E).
% "D shall V only Ks that P" (`only`, spec_lf_facts) obliges no V: it can clash only with a V, by the V's keys
key(R,ev(only,E)) :- only(R,_,E,_,_).  dem(R,ev(pos,E)) :- key(R,ev(only,E)).  dem(R,ev(only,E)) :- key(R,ev(pos,E)).
% a count (`count(R,I,E,D,X,B,N)`, CNL 4's call 4, I15) can clash only with a count of its act E
key(R,ev(cnt,E)) :- count(R,_,E,_,_,_,_).  dem(R,ev(cnt,E)) :- key(R,ev(cnt,E)).
% cc(A,B) holds exactly when dem(A,K), key(B,K) for some K; a pair can clash when either way holds.
% (1) two triggers of one event: joined on the trigger and the key at once
tdem(A,P,E,K) :- trig(A,P,E,_,_), dem(A,K).  tkey(B,P,E,K) :- trig(B,P,E,_,_), key(B,K).
tc(A,B,P,E) :- tdem(A,P,E,K), tkey(B,P,E,K), A != B.  tc(B,A,P,E) :- tdem(A,P,E,K), tkey(B,P,E,K), A != B.
tp(A,B,X,Y,D1,D2) :- tc(A,B,P,E), trig(A,P,E,D1,X), trig(B,P,E,D2,Y).
% a compatible doer, objects of compatible kinds (or one constant)
kin(A,B,X,Y) :- tp(A,B,X,Y,_,_), role(A,X,K), role(B,Y,K2), compat(K,K2).
kin(A,B,X,X) :- tp(A,B,X,X,_,_), not role(A,X,_), not role(B,X,_).
doerk(A,B,D1,D2) :- tp(A,B,_,_,D1,D2), role(A,D1,K), role(B,D2,K2), compat(K,K2).
doerk(A,B,any,D) :- tp(A,B,_,_,any,D).
doerk(A,B,D,any) :- tp(A,B,_,_,D,any).
doerk(A,B,D,D) :- tp(A,B,_,_,D,D), not role(A,D,_).
cand(A,B) :- tp(A,B,X,Y,D1,D2), kin(A,B,X,Y), doerk(A,B,D1,D2).
% (2) a triggered requirement with an untriggered one that binds one of its kinds: from the untriggered one's keys
ureq(B) :- req(B), not trg(B).
ukey(B,K) :- ureq(B), key(B,K).  udem(B,K) :- ureq(B), dem(B,K).
uc(B,A) :- udem(B,K), key(A,K), trg(A).  uc(B,A) :- ukey(B,K), dem(A,K), trg(A).
ukind(B,K) :- ureq(B), role(B,_,K2), compat(K,K2).
cand(A,B) :- uc(B,A), role(A,_,K), ukind(B,K).
% (3) a requirement with a U that shares an event or an attribute; a use with a "shall not use" (static, no trigger)
names(R,E) :- resp(R,_,_,E,_,_).  names(R,E) :- trig(R,_,E,_,_).
names(R,T) :- cond(R,_,T,_,_).    names(R,T) :- set(R,_,_,T,_).
unames(A,N) :- universal(A), names(A,N).
ukeyu(A,K) :- universal(A), key(A,K).  udemu(A,K) :- universal(A), dem(A,K).
unc(A,B) :- udemu(A,K), key(B,K), A != B.  unc(A,B) :- ukeyu(A,K), dem(B,K), A != B.
cand(A,B) :- unc(A,B), unames(A,N), names(B,N).
cand(A,B) :- uses(A,_,_), nouse(B,_,_), A != B.
% (4) a permission (`resp(R,I,may,E,D,X)`, spec_lf_modal) with a "shall not" of its act, both untriggered: on the key
mkey(A,K) :- ureq(A), key(A,K), K = ev(may,_).
cand(A,B) :- mkey(A,K), udem(B,K), A != B.
% The If tag (CNL 4's call 12): the EARS unwanted-behaviour form ("If T, then ...") takes precedence over a line of
% another form on its own trigger: where its state holds its response replaces the other's, and where it does not it
% does not fire, so the two are never a pair (two of one form still are). A universal condition holds in every trace:
% it takes no precedence and none is taken over it, so it is paired with each line it bears on, If or not (b117).
% A pair of two codified-1 lines (`cnl4(R)`: a codified-2 line, spec_lf_facts) keeps the reading it had until its
% files are reworded: an If line is never paired with a line of another form.
exc(R) :- form(R,if).  exc(R) :- form(R,while_if).  exc(R) :- form(R,where_if).
four(A,B) :- cand(A,B), cnl4(A).  four(A,B) :- cand(A,B), cnl4(B).
lone(A,B) :- cand(A,B), not four(A,B).
lone(A,B) :- four(A,B), tc(A,B,_,_), not universal(A), not universal(B).
over(A,B) :- lone(A,B), exc(A), not exc(B).  over(A,B) :- lone(A,B), exc(B), not exc(A).
pair(A,B) :- cand(A,B), A < B, not over(A,B).  pair(A,B) :- cand(B,A), A < B, not over(B,A).

% ---- unification: each role of B is one of A's roles of a compatible kind, or its own instance b(Y) -------------
% A `Named` code is one thing (design-r3 §3): every role of a requirement with one code is its first such role
% (`canon`), and a code both sides name is one role of the pair.
nrep(S,Y) :- named(S,Y,C), named(S,Y0,C), Y0 < Y.
canon(S,Y,Y0) :- named(S,Y,C), named(S,Y0,C), not nrep(S,Y0).  canon(S,Y,Y) :- role(S,Y,_), not named(S,Y,_).
{ map(A,B,Y,X) : role(A,X,K), compat(K,K2), not nrep(A,X) } 1 :- pair(A,B), role(B,Y,K2), not nrep(B,Y).
:- map(A,B,Y1,X), map(A,B,Y2,X), Y1 < Y2.
% (a side's codes and object attributes lifted to the pair first: never joined on a code or an attribute alone)
% A unification that breaks a code is `unfit`: soft, so a pair whose shared code no unification keeps one thing (its
% roles of incompatible kinds) sets only itself aside. `coded(A,B)`, a pair that shares a code, and `fit(A,B)`, one
% that some unification keeps, are shown: a coded pair never fit is set aside (spec_solve).
na(A,B,X,C) :- pair(A,B), named(A,X,C).  nb(A,B,Y,C) :- pair(A,B), named(B,Y,C).
unfit(A,B) :- map(A,B,Y,X), na(A,B,X,C), nb(A,B,Y,C2), C != C2.
unfit(A,B) :- na(A,B,X,C), nb(A,B,Y,C), not nrep(A,X), not nrep(B,Y), not map(A,B,Y,X).
coded(A,B) :- na(A,B,_,C), nb(A,B,_,C).  fit(A,B) :- coded(A,B), not unfit(A,B).
#show coded/2.  #show fit/2.
oa(A,B,X,T,V) :- pair(A,B), oattr(A,X,T,V).  ob(A,B,Y,T,W) :- pair(A,B), oattr(B,Y,T,W).
:- map(A,B,Y,X), oa(A,B,X,T,V), ob(A,B,Y,T,W), V != W.
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
% an actor is a doer a role of its kind or a kind above it stands for (`akind`, the actor's Kind of:, b121)
aterm(A,B,S,Y,K) :- side(A,B,S), term(S,Y), not role(S,Y,_), akind(Y,K).
doer(A,B,X,Y) :- pair(A,B), role(A,X,K), aterm(A,B,B,Y,K2), subeq(K2,K).
doer(A,B,X,Y) :- pair(A,B), role(B,Y,K), aterm(A,B,A,X,K2), subeq(K2,K).
% the triggers are one event: its doer and its object unify, or the pair is out under this unification
ta(A,B,P,E,D,X) :- pair(A,B), trig(A,P,E,D,X).  tb(A,B,P,E,D,Y) :- pair(A,B), trig(B,P,E,D,Y).
fires(A,B) :- ta(A,B,P,E,D1,X), tb(A,B,P,E,D2,Y), same(A,B,X,Y), doer(A,B,D1,D2).
out(A,B) :- pair(A,B), trg(A), trg(B), not fires(A,B).
nk(S,Y,K) :- named1(S,Y), role(S,Y,K).  thek(S,Y,K) :- the(S,Y), role(S,Y,K).
tda(A,B,K) :- pair(A,B), tdef(A,K).  tdb(A,B,K) :- pair(A,B), tdef(B,K).
out(A,B) :- tda(A,B,K), nk(B,Y,K), not tmap(A,B,Y).
out(A,B) :- tdb(A,B,K), thek(B,Y,K), nk(A,X,K), not map(A,B,Y,X).

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
fr(A,B,Z) :- side(A,B,S), free(S,X), at(A,B,S,X,Z).  hd(A,B,Z) :- side(A,B,S), holds(S,_,X), at(A,B,S,X,Z).
out(A,B) :- fr(A,B,Z), hd(A,B,Z).
% "no K is v" is universal over the merged state of its side (§3.3): no instance of K or a sub-kind there is v
pos(A,B,0,Z,T,V) :- w0(A,B,Z,T,V,pos).
pos(A,B,1,Z,T,V) :- w1(A,B,Z,T,V,pos).  pos(A,B,1,Z,T,V) :- n1(A,B,Z,T,V,pos).
state(A,B,S,1) :- late(A,B,S).  state(A,B,S,0) :- side(A,B,S), not late(A,B,S).
% (each `no` lifted to the pair, and an instance's kinds closed upwards per pair: `kup`)
kup(A,B,Z,K) :- kindof(A,B,Z,K2), subeq(K2,K).
nonep(A,B,N,K,T,V) :- state(A,B,S,N), none(S,K,T,V).
out(A,B) :- nonep(A,B,N,K,T,V), pos(A,B,N,Z,T,V), kup(A,B,Z,K).
cnonep(A,B,S,K,C) :- side(A,B,S), cnone(S,K,C).
out(A,B) :- cnonep(A,B,_,K,C), cw(A,B,Z,C,pos), kup(A,B,Z,K).
% "no K is <rel> Y", "X is <rel> no K" (rnone): no instance of K is so related in the merged state
out(A,B) :- side(A,B,S), rnone(S,Q,kind(K),Y), at(A,B,S,Y,Zy), rw(A,B,Q,Z,Zy,pos), kup(A,B,Z,K).
out(A,B) :- side(A,B,S), rnone(S,Q,X,kind(K)), at(A,B,S,X,Zx), rw(A,B,Q,Zx,Z,pos), kup(A,B,Z,K).
% time (CNL 4's I16, call 9): a history ("has ended a stage", spec_lf_time) is a state relation `hist(E)`, set by its
% event and unset by nothing, read as any `crel`. A comparison `cmp(R,X,Op,C,P)` puts a bound on the moment X: C a
% moment of the line (a code among them) or `ago(S)`, now less S seconds ("within the last 7 days"). Over the
% constants named, exactly: X above C (after, or not before) and below C (before, or not after) is out, unless both
% are weak (not before C and not after C: X is C); and so is X above a bound later than a bound it is below.
cw2(A,B,Z,O,Zc,P) :- side(A,B,S), cmp(S,Y,O,C,P), at(A,B,S,Y,Z), at(A,B,S,C,Zc).
lo(A,B,Z,C,s) :- cw2(A,B,Z,after,C,pos).   lo(A,B,Z,C,w) :- cw2(A,B,Z,before,C,neg).
hi(A,B,Z,C,s) :- cw2(A,B,Z,before,C,pos).  hi(A,B,Z,C,w) :- cw2(A,B,Z,after,C,neg).
later(A,B,ago(N2),ago(N1)) :- lo(A,B,_,ago(N2),_), hi(A,B,_,ago(N1),_), N2 < N1.
out(A,B) :- lo(A,B,Z,C,s), hi(A,B,Z,C,_).  out(A,B) :- lo(A,B,Z,C,_), hi(A,B,Z,C,s).
out(A,B) :- lo(A,B,Z,C2,_), hi(A,B,Z,C1,_), later(A,B,C2,C1).
% a functional relation (`fun(Q)`: a relation row of cardinality one, or a preposition, spec_logic_vocab) relates a
% thing to one thing: two images under one unification are out
redge(A,B,Q,Z1,Z2) :- rw(A,B,Q,Z1,Z2,pos).
redge(A,B,Q,Z1,Z2) :- side(A,B,S), orel(S,Q,Y1,Y2), at(A,B,S,Y1,Z1), at(A,B,S,Y2,Z2).
out(A,B) :- fun(Q), redge(A,B,Q,Z,Z1), redge(A,B,Q,Z,Z2), Z1 < Z2.

% ---- a necessity (`nec`, `necsub`: spec_lf_modal) is a premise of every pair, in both states: "a K1 never Qs a K2"
% puts out a pair whose merged state relates a K1 to a K2 so; "a K1 always Qs a K2" one whose side says a K1 is so
% related to no K2 (or to no kind above it). (A necessity is joined with a pair's own facts on its relation: a
% context has few necessities, so this is no join of two requirement-level facts.)
subeq(K,K) :- nec(_,_,_,K,_).  subeq(K,K) :- nec(_,_,_,_,K).
out(A,B) :- nec(_,never,Q,Kx,Ky), rw(A,B,Q,Z1,Z2,pos), kup(A,B,Z1,Kx), kup(A,B,Z2,Ky).
out(A,B) :- nec(N,always,Q,Kx,Ky), necsub(N,1), side(A,B,S), rnone(S,Q,X,kind(K)), at(A,B,S,X,Z), kup(A,B,Z,Kx),
            subeq(Ky,K).
out(A,B) :- nec(N,always,Q,Kx,Ky), necsub(N,2), side(A,B,S), rnone(S,Q,kind(K),Y), at(A,B,S,Y,Z), kup(A,B,Z,Ky),
            subeq(Kx,K).

% ---- a defined condition read through its definition (`dalt(C,N)`, `dlit(C,N,Attr,Val,Pol)`: the ways through a
% Def whose literals are all on its own subject, spec_facts.def_facts) under `no`, `every` and a negation --------
has(A,B,0,Z,T,V,P) :- w0(A,B,Z,T,V,P).
has(A,B,1,Z,T,V,P) :- w1(A,B,Z,T,V,P).  has(A,B,1,Z,T,V,P) :- n1(A,B,Z,T,V,P).
% the instances a definition is asked of: (side's state N, instance Z, condition C)
ask(A,B,N,Z,C) :- cnonep(A,B,S,K,C), state(A,B,S,N), kup(A,B,Z,K), dalt(C,_).
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
out(A,B) :- cnonep(A,B,S,K,C), state(A,B,S,N), kup(A,B,Z,K), ent(A,B,N,Z,C).
out(A,B) :- side(A,B,S), state(A,B,S,N), ccond(S,Y,C,neg), at(A,B,S,Y,Z), ent(A,B,N,Z,C).
% "every K <restrictions> is C" (uall, urel, uattr; ucond, uccond): each instance of K with the restrictions is C
ucand(A,B,S,U,Z) :- side(A,B,S), uall(S,U,K), kup(A,B,Z,K).
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
% A pair that cannot fire together under this unification is out, or unfit: soft, so that one pair never makes the
% program UNSAT and hides every other finding.
ok(A,B) :- pair(A,B), not out(A,B), not unfit(A,B).
% the restrictions of B's object (its kind, its `for`) are entailed by A's object, or the other way round
% (an obligation on every K, `each(R,X)` of a codified-2 line (spec_lf_facts), binds each K its restrictions allow:
% what the other side says of its K need only agree with them, which the unification already asks. A codified-1
% line's `every(R,X)` is left unread, as it was, until its files are reworded: its findings stay as they were.)
gap(A,B,X,Y) :- map(A,B,Y,X), oattr(B,Y,T,W), not oattr(A,X,T,W), not each(A,X).
gap(A,B,X,Y) :- map(A,B,Y,X), orel(B,Q,Y,Z), not relby(A,B,X,Q,Z), not each(A,X).
relby(A,B,X,Q,Z) :- map(A,B,Y,X), orel(B,Q,Y,Z), orel(A,Q,X,X2), same(A,B,X2,Z).
pag(A,B,X,Y) :- map(A,B,Y,X), oattr(A,X,T,W), not oattr(B,Y,T,W), not each(B,Y).
pag(A,B,X,Y) :- map(A,B,Y,X), orel(A,Q,X,X2), not relof(A,B,Y,Q,X2), not each(B,Y).
relof(A,B,Y,Q,X2) :- map(A,B,Y,X), orel(A,Q,X,X2), orel(B,Q,Y,Z), same(A,B,X2,Z).
% each side's responses lifted to the pair first (`ra`, `rb`, `sa`, `sb`, `ua`, `ub`, `xa`, `xb`), so a clash is joined on the pair and the
% event at once, never on an event (print, exit_error) that thousands of lines share
ra(A,B,P,E,D,X) :- pair(A,B), resp(A,_,P,E,D,X).  rb(A,B,P,E,D,Y) :- pair(A,B), resp(B,_,P,E,D,Y).
sa(A,B,X,T,V) :- pair(A,B), set(A,_,X,T,V).        sb(A,B,Y,T,W) :- pair(A,B), set(B,_,Y,T,W).
cl(A,B,pos_neg) :- ok(A,B), ra(A,B,pos,E,D1,X), rb(A,B,neg,E,D2,Y), doer(A,B,D1,D2), same(A,B,X,Y),
                      not gap(A,B,X,Y).
cl(A,B,neg_pos) :- ok(A,B), ra(A,B,neg,E,D1,X), rb(A,B,pos,E,D2,Y), doer(A,B,D1,D2), same(A,B,X,Y),
                      not pag(A,B,X,Y).
cl(A,B,set) :- ok(A,B), sa(A,B,X,T,V), sb(A,B,Y,T,W), same(A,B,X,Y), V != W.
cl(A,B,exit) :- ok(A,B), ra(A,B,pos,exit_ok,D1,_), rb(A,B,pos,exit_error,D2,_), doer(A,B,D1,D2).
cl(A,B,exit) :- ok(A,B), ra(A,B,pos,exit_error,D1,_), rb(A,B,pos,exit_ok,D2,_), doer(A,B,D1,D2).
cl(A,B,change) :- ok(A,B), ra(A,B,pos,change_nothing,D1,_), rb(A,B,pos,E,D2,_), not quiet(E),
                     not own(A,E), doer(A,B,D1,D2).
cl(A,B,change) :- ok(A,B), rb(A,B,pos,change_nothing,D2,_), ra(A,B,pos,E,D1,_), not quiet(E),
                     not own(B,E), doer(A,B,D1,D2).
% only: a V by its agent of a thing known to fall outside its restrictor (an attribute of another value there)
oa1(A,B,E,D,X) :- pair(A,B), only(A,_,E,D,X).  ob1(A,B,E,D,Y) :- pair(A,B), only(B,_,E,D,Y).
zval(A,B,Z,T,W) :- side(A,B,S), oattr(S,Y,T,W), at(A,B,S,Y,Z).  zval(A,B,Z,T,W) :- pos(A,B,_,Z,T,W).
outside(A,B,S,Z) :- side(A,B,S), rattr(S,X,T,V), at(A,B,S,X,Z), zval(A,B,Z,T,W), V != W.
cl(A,B,only) :- ok(A,B), oa1(A,B,E,D1,X), rb(A,B,pos,E,D2,Y), doer(A,B,D1,D2), same(A,B,X,Y),
                   at(A,B,A,X,Z), outside(A,B,A,Z).
cl(A,B,only) :- ok(A,B), ob1(A,B,E,D2,Y), ra(A,B,pos,E,D1,X), doer(A,B,D1,D2), same(A,B,X,Y),
                   at(A,B,B,Y,Z), outside(A,B,B,Z).
% counts: two counts of one act by one doer on one thing, alike restricted, that no number of things meets both of
% (`adm(R,I,M)`: the count of act I of R admits M things; the numbers from 0 to one past the largest count's)
num(0..M) :- M = #max{ N+1 : count(_,_,_,_,_,_,N) }, M >= 0.
adm(R,I,M) :- count(R,I,_,_,_,least,N), num(M), M >= N.    adm(R,I,M) :- count(R,I,_,_,_,most,N), num(M), M <= N.
adm(R,I,N) :- count(R,I,_,_,_,exactly,N).                 adm(R,I,M) :- count(R,I,_,_,_,more,N), num(M), M > N.
adm(R,I,M) :- count(R,I,_,_,_,fewer,N), num(M), M < N.
ka(A,B,I,E,D,X) :- pair(A,B), count(A,I,E,D,X,_,_).  kb(A,B,J,E,D,Y) :- pair(A,B), count(B,J,E,D,Y,_,_).
cl(A,B,count) :- ok(A,B), ka(A,B,I,E,D1,X), kb(A,B,J,E,D2,Y), doer(A,B,D1,D2), same(A,B,X,Y), not gap(A,B,X,Y),
                    not pag(A,B,X,Y), #count{ M : adm(A,I,M), adm(B,J,M) } = 0.
ua(A,B,D,X) :- pair(A,B), uses(A,D,X).   ub(A,B,D,Y) :- pair(A,B), uses(B,D,Y).
xa(A,B,D,X) :- pair(A,B), nouse(A,D,X).  xb(A,B,D,Y) :- pair(A,B), nouse(B,D,Y).
cl(A,B,use) :- ok(A,B), ua(A,B,D1,X), xb(A,B,D2,Y), doer(A,B,D1,D2), same(A,B,X,Y).
cl(A,B,use) :- ok(A,B), xa(A,B,D1,X), ub(A,B,D2,Y), doer(A,B,D1,D2), same(A,B,X,Y).
% a clash whose witness merges onto an instance a prose condition one side states (`prose(C)`: no Def) and something
% the other side states of it that the first does not: a definition of C could refute it, so it is L6, not L1
lit(A,B,S,Z,c(T,V,P)) :- side(A,B,S), cond(S,Y,T,V,P), at(A,B,S,Y,Z).
lit(A,B,S,Z,k(C,P)) :- side(A,B,S), ccond(S,Y,C,P), at(A,B,S,Y,Z).
lit(A,B,S,Z1,r(Q,Z2,P)) :- side(A,B,S), crel(S,Q,Y1,Y2,P), at(A,B,S,Y1,Z1), at(A,B,S,Y2,Z2).
lit(A,B,S,Z2,i(Q,Z1,P)) :- side(A,B,S), crel(S,Q,Y1,Y2,P), at(A,B,S,Y1,Z1), at(A,B,S,Y2,Z2).
dep(A,B,C) :- lit(A,B,S,Z,k(C,_)), prose(C), side(A,B,S2), S2 != S, lit(A,B,S2,Z,L), not lit(A,B,S,Z,L).
depends(A,B) :- dep(A,B,_).
% L7: a "shall not" that forbids what a "may" permits, of one doer and one thing, where both fire; not a clash
cl(A,B,may) :- ok(A,B), ra(A,B,may,E,D1,X), rb(A,B,neg,E,D2,Y), doer(A,B,D1,D2), same(A,B,X,Y), not gap(A,B,X,Y).
cl(A,B,may) :- ok(A,B), ra(A,B,neg,E,D1,X), rb(A,B,may,E,D2,Y), doer(A,B,D1,D2), same(A,B,X,Y), not pag(A,B,X,Y).
forbid(A,B) :- cl(A,B,may).
#show forbid/2.
clash(A,B,W) :- cl(A,B,W), not depends(A,B), W != may.
maybe(A,B,W,C) :- cl(A,B,W), dep(A,B,C), W != may.
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
% The pairs a witness is asked of are facts focus(A,B) (an L1) and focusm(A,B) (an L6: a witness that clashes and
% depends on a prose condition) of the part `witness`, ground on the same Control after the check's brave solve, for
% every such pair at once: pairs share no atom, so one model holds a witness of each. (Externals, one per pair of
% each kind, made every solve call cost the whole set of them.)
hit(A,B) :- clash(A,B,W), W != self.  hitm(A,B) :- maybe(A,B,_,_).
#program witness.
:- focus(A,B), pair(A,B), not hit(A,B).
:- focusm(A,B), pair(A,B), not hitm(A,B).
foc(A,B) :- focus(A,B).  foc(A,B) :- focusm(A,B).
pre(A,B,Z,T,V,P) :- foc(A,B), w0(A,B,Z,T,V,P).
pre(A,B,Z,T,V,P) :- foc(A,B), n1(A,B,Z,T,V,P).
prec(A,B,Z,C,P) :- foc(A,B), cw(A,B,Z,C,P).
#show pre/6.  #show prec/5.
