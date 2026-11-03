% The cone of a group (design-r2 §5.7, §6.3), from the translation's signature facts:
%   trig(Id,P,E,K) eff(Id,P,E,K) uses(Id,K) untriggered(Id), sub(Kind,Super), own(G,Id); start(G) names the group,
%   whose witness's facts carry G as their id.
% Kinds match when equal or one is a subkind of the other.
kindof(K) :- uses(_,K). kindof(K) :- trig(_,_,_,K). kindof(K) :- eff(_,_,_,K).
kindof(K) :- sub(K,_). kindof(K) :- sub(_,K).
above(K,S) :- sub(K,S). above(K,T) :- above(K,S), sub(S,T).
match(K,K) :- kindof(K). match(K,S) :- above(K,S). match(S,K) :- above(K,S).
% an effect of S matches a trigger of T; the witness's trigger is an effect of the group at state 0
edge(S,T) :- eff(S,P,E,K), trig(T,P,E,L), match(K,L).
edge(G,T) :- start(G), trig(G,P,E,K), trig(T,P,E,L), match(K,L), T != G.
% rule 1: reachable by edge/2 from the witness or a statement in the cone
node(G) :- start(G).
node(T) :- node(S), edge(S,T).
in_cone(G,I) :- start(G), own(G,I).
in_cone(G,I) :- start(G), node(I), I != G.
% rule 2: a statement with no trigger enters exactly when every kind it binds is one the cone already uses; of the
% sets closed so, the least is kept (a statement may not enter on the strength of its own kinds alone)
used(G,K) :- start(G), uses(G,K).
used(G,K) :- in_cone(G,I), uses(I,K).
covered(G,K) :- used(G,L), match(K,L).
missing(G,I) :- start(G), untriggered(I), uses(I,K), not covered(G,K).
{ in_cone(G,I) } :- start(G), untriggered(I), I != G.
:- in_cone(G,I), untriggered(I), missing(G,I), not own(G,I).
:- start(G), untriggered(I), I != G, not in_cone(G,I), not missing(G,I).
node(I) :- in_cone(_,I).
#minimize { 1,I : in_cone(G,I) }.
#show in_cone/2.
#show edge/2.
