% grammar/entail.lp: the background of the entailment check (L8, the CNL 4 design's I13a; scripts/spec_entail.py).
% Each query q(L,I) asks whether response I of requirement L is entailed by other requirements. Its world (facts
% under Q) holds only what L states: its terms, antecedent, trigger and other responses; each premise M is one rule
% over Q (scripts/spec_entail_rules.py) that forces M's responses, tagged M, where its antecedent and trigger hold.
% No choice and no search: one stratified model. A premise's negative literal needs a stated or entailed negation,
% never a missing fact. Shown: ent(L,I,M), response I of L forced by M; self_ent(L,I), forced by L's own others.
% The strata: A, the premises on L's own trigger, over the world; B, the untriggered premises and those on the
% bridge's refusal (an error exit on a run is a refusal of its command, the CLI pack's definition of refuse), over
% the world and A.
#defined a0/4. #defined na0/4. #defined k/3. #defined nk/3. #defined rel/4. #defined nrel/4. #defined feat/2.
#defined code/3. #defined ev/5. #defined r/6. #defined setv/4. #defined prop/4. #defined lnone/4. #defined hit/2.
#defined isk/3. #defined rA/6. #defined rB/6. #defined iskA/3. #defined iskB/3. #defined propA/4. #defined propB/4.
#defined relA/4. #defined relB/4. #defined setvA/4. #defined evB/5. #defined lcnone/3. #defined lrnone/4.
#defined bridgecmd/2. #defined tq/5. #defined dask/2. #defined use/2. #defined kind/1. #defined sub/2.
#defined val/3. #defined dalt/2. #defined dlit/5.
isk2(Q,Z,K) :- isk(Q,Z,K).  isk2(Q,Z,K) :- iskA(Q,Z,K).  rel2(Q,R,X,Y) :- rel(Q,R,X,Y).  rel2(Q,R,X,Y) :- relA(Q,R,X,Y).
prop2(Q,Z,T,V) :- prop(Q,Z,T,V).  prop2(Q,Z,T,V) :- propA(Q,Z,T,V).
setv2(Q,Z,T,V) :- setv(Q,Z,T,V).  setv2(Q,Z,T,V) :- setvA(Q,Z,T,V).
rall(Q,P,E,D,X,M) :- r(Q,P,E,D,X,M).  rall(Q,P,E,D,X,M) :- rA(Q,P,E,D,X,M).  rall(Q,P,E,D,X,M) :- rB(Q,P,E,D,X,M).
iskall(Q,Z,K) :- isk2(Q,Z,K).  iskall(Q,Z,K) :- iskB(Q,Z,K).
propall(Q,Z,T,V) :- prop2(Q,Z,T,V).  propall(Q,Z,T,V) :- propB(Q,Z,T,V).
relall(Q,R,X,Y) :- rel2(Q,R,X,Y).  relall(Q,R,X,Y) :- relB(Q,R,X,Y).
evB(Q,does,e_refuse,D,C) :- bridgecmd(Q,C), r(Q,pos,exit_error,D,_,_).
evB(Q,does,e_refuse,D,C) :- bridgecmd(Q,C), rA(Q,pos,exit_error,D,_,_).
% entailed negations: another value of a functional attribute
na0(Q,Z,T,V) :- a0(Q,Z,T,W), val(_,T,V), V != W.
% state 1: after L's own (other) sets and the sets forced
moved(Q,Z,T) :- setv2(Q,Z,T,_).
a1(Q,Z,T,V) :- setv2(Q,Z,T,V).
a1(Q,Z,T,V) :- a0(Q,Z,T,V), not moved(Q,Z,T).
na1(Q,Z,T,V) :- na0(Q,Z,T,V), not moved(Q,Z,T).
na1(Q,Z,T,V) :- a1(Q,Z,T,W), val(_,T,V), V != W.
% a defined condition: one way's literals all stated; refuted when each way has one contradicted
term(Q,Z) :- isk(Q,Z,_).
dno(Q,Z,C,W) :- dask(Q,C), term(Q,Z), dlit(C,W,T,V,pos), not a0(Q,Z,T,V).
dno(Q,Z,C,W) :- dask(Q,C), term(Q,Z), dlit(C,W,T,V,neg), not na0(Q,Z,T,V).
k(Q,Z,C) :- dask(Q,C), term(Q,Z), dalt(C,W), not dno(Q,Z,C,W).
dbr(Q,Z,C,W) :- dask(Q,C), term(Q,Z), dlit(C,W,T,V,pos), na0(Q,Z,T,V).
dbr(Q,Z,C,W) :- dask(Q,C), term(Q,Z), dlit(C,W,T,V,neg), a0(Q,Z,T,V).
dlv(Q,Z,C) :- dask(Q,C), term(Q,Z), dalt(C,W), not dbr(Q,Z,C,W).
nk(Q,Z,C) :- dask(Q,C), term(Q,Z), dalt(C,_), not dlv(Q,Z,C).
subeq(K,K) :- kind(K).  subeq(K,K3) :- sub(K,K2), subeq(K2,K3).
lnone2(Q,K,T,V) :- lnone(Q,K2,T,V), subeq(K,K2).
lcnone2(Q,K,C) :- lcnone(Q,K2,C), subeq(K,K2).
lrnone2(Q,R,kind(K),Y) :- lrnone(Q,R,kind(K2),Y), subeq(K,K2).
lrnone2(Q,R,X,kind(K)) :- lrnone(Q,R,X,kind(K2)), subeq(K,K2).
% the query's response (generic rules: a rule per query in a recursive component would slow the grounder)
hit(Q,M) :- tq(Q,P,E,D,X), rall(Q,P,E,D,X,M).
hit(Q,M) :- tq(Q,neg,e_change,D,_), rall(Q,pos,change_nothing,D,none,M).
ent(L,I,M) :- hit(q(L,I),M), M != self.
self_ent(L,I) :- hit(q(L,I),self).
#show ent/3. #show self_ent/2.
