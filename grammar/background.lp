% The background theory of `model logic` (design §12.2), plugin-owned. spec_logic adds the context's facts from its
% lexicon (value/3, attribute/2, resource/1, capacity/2, start_event/1, end_event/1, free_condition/1,
% resource_kind/1, resource_relation/1, the rule of each condition's Means:), each statement's constraint guarded by
% on/1, and one group's witness. A step may pass with no event (a stutter step), so a trace shorter than the horizon
% extends to it.

#program always.
% a thing has at most one value of an attribute
:- attr(X,A,V), attr(X,A,W), V < W.
% a session runs from the step something starts it until something ends it
active(X) :- does(_,E,X), start_event(E).
% a resource is over its number when more running sessions hold it than its capacity (1 when it is exclusive)
over(R) :- capacity(R,N), #count{ X : holds(X,R), active(X) } > N.
% "free" (design §8.5): a resource whose running holders, a session starting this step included, are within it
cond(C,R) :- free_condition(C), resource(R), not over(R).
% a resource of the lexicon is a thing of the kind `resource`, and a session needs what it holds
kind(R,K) :- resource(R), resource_kind(K).
rel(Q,X,R) :- holds(X,R), resource_relation(Q), resource(R).

#program initial.
% the first state: any value of each attribute of each thing, and any of the features given
{ attr(X,A,V) : value(K,A,V) } 1 :- thing(X), kind(X,K), attribute(K,A).
{ given(C) } :- feature(C).

#program dynamic.
% frame axioms: a value, a feature and a running session persist unless a step changes them
attr(X,A,V) :- 'attr(X,A,V), not moved(X,A).
moved(X,A) :- attr(X,A,W), 'attr(X,A,V), W != V.
given(C) :- 'given(C).
active(X) :- 'active(X), not ended(X).
ended(X) :- does(_,E,X), end_event(E).
