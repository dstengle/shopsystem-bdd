% The background theory of `model logic` and of a group's trace (design-r2 §5.1, §6.2), plugin-owned. spec_logic adds
% the context's facts (value/3, attribute/2, trans/3, into/2, sub/2, relk/3, primitive/2, resource/1, capacity/2,
% start_event/1, end_event/1, free_condition/1, resource_kind/1, resource_relation/1), each statement's constraints
% guarded by on/1, the definitions' rules and one group's witness; spec_engine adds pool_size/2. Fluents (attr, rel,
% cond, given) are chosen at state 0, and later only for a thing first used at that state; after that a value
% changes only by a `set` event. Events (does, ran) are chosen; nothing happens unless a constraint asks for it or the
% minimal trace has it. A step may pass with no event (a stutter step), so a trace shorter than the horizon extends.

#program always.
% the instances: n of each kind, named o(K,1..n); a kind's supertypes hold of its instances
pool(K,1..N) :- pool_size(K,N).
kind(o(K,N),K) :- pool(K,N).
kind(X,S) :- kind(X,K), sub(K,S).
kind(R,K) :- resource(R), resource_kind(K).
thing(X) :- kind(X,_).
% a thing has at most one value of an attribute; a `set` gives it its value at the state it happens
:- attr(X,A,V), attr(X,A,W), V < W.
attr(X,A,V) :- does(_,set(A,V),X).
% the trigger forms whose subject is anyone
set_to(X,A,V) :- does(_,set(A,V),X).
done_to(E,X) :- does(_,E,X).
ran_any(C,X) :- ran(_,C,X).
% a response with an existential object holds when one of its objects does
resp(I,N,S) :- obj(I,N,S,_).
% a thing is used when anything names it, and ever used from then on; instances are used in their order
used(X) :- attr(X,_,_).
used(X) :- rel(_,X,_).
used(Y) :- rel(_,_,Y).
used(X) :- cond(_,X), thing(X).
used(X) :- does(_,_,X), thing(X).
used(X) :- does(X,_,_), thing(X).
used(X) :- ran(_,_,X), thing(X).
used(X) :- holds(X,_).
ever(X) :- used(X).
:- ever(o(K,N)), N > 1, not ever(o(K,N-1)).
% a session runs from the step something starts it until something ends it
active(X) :- does(_,E,X), start_event(E).
% a resource is over its number when more running sessions hold it than its capacity (1 when it is exclusive)
over(R) :- capacity(R,N), #count{ X : holds(X,R), active(X) } > N.
% "free" (design §8.5): a resource whose running holders, a session starting this step included, are within it
cond(C,R) :- free_condition(C), resource(R), not over(R).
% a session needs what it holds
rel(Q,X,R) :- holds(X,R), resource_relation(Q), resource(R).

#program initial.
% the first state: any value of each attribute, any relation, any primitive condition and any feature
{ attr(X,A,V) : value(K,A,V) } 1 :- thing(X), kind(X,K), attribute(K,A).
{ rel(R,X,Y) : relk(R,K1,K2), kind(Y,K2) } :- thing(X), kind(X,K1), relk(_,K1,_).
{ cond(C,X) } :- primitive(C,K), kind(X,K).
{ given(F) } :- feature(F).

#program dynamic.
% creation: a thing first used at this state may have any values, relations and primitive conditions
{ attr(X,A,V) : value(K,A,V) } 1 :- thing(X), kind(X,K), attribute(K,A), not 'ever(X).
{ rel(R,X,Y) : relk(R,K1,K2), kind(Y,K2) } :- thing(X), kind(X,K1), relk(_,K1,_), not 'ever(X).
{ cond(C,X) } :- primitive(C,K), kind(X,K), not 'ever(X).
% frame axioms: values, relations, primitive conditions, features and running sessions persist
attr(X,A,V) :- 'attr(X,A,V), not moved(X,A).
moved(X,A) :- does(_,set(A,_),X).
rel(R,X,Y) :- 'rel(R,X,Y).
cond(C,X) :- 'cond(C,X), primitive(C,_).
given(F) :- 'given(F).
ever(X) :- 'ever(X).
active(X) :- 'active(X), not ended(X).
ended(X) :- does(_,E,X), end_event(E).

#program always.
#show lab/3.
#show bind/3.
#show contrast/3.
#show attr/3.
#show rel/3.
#show cond/2.
#show given/1.
#show holds/2.
#show does/3.
#show ran/3.

% --- the minimal trace (design-r2 §7.2): read only when a trace is asked for, not by a check that needs a model
#program always.
% fewest instances, then fewest events, then fewest fluents at state 0
#minimize { 1@3,X : ever(X), thing(X) }.
#minimize { 1@2,ev,S,E,X : does(S,E,X) ; 1@2,ran,S,C,X : ran(S,C,X) }.
#program initial.
% an event at state 0 counts twice
#minimize { 1@2,first,S,E,X : does(S,E,X) ; 1@2,first,S,C,X : ran(S,C,X) }.
#minimize { 1@1,A,X,V : attr(X,A,V) ; 1@1,R,X,Y : rel(R,X,Y) ; 1@1,C,X : cond(C,X) ; 1@1,F : given(F) }.
