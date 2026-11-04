# The grammar, formally

Version 5, 2026-11-03, with the GF conversion's revisions 2 and 3
(`and` between responses, relations as rows, conditions defined in the
language, one translation of each fun into facts, the clingo check over
pairs, scenarios read off each requirement's facts). A
machine-checkable statement of
`design-model.md`, in two parts. The **graph** (§1–§5): the schema, the
integrity constraints, the lifecycles. Notation: Datalog (clingo
dialect, as `scripts/model.lp` runs it). A `v_` relation must be empty; a
`w_` relation is reported, not refused. The **requirement language**
(§6–§7): the requirement and step grammars, the lexicon, the guards, and
the logic check. Rules marked *(new in v5)* have no counterpart in
version 4; `design-model.md` §10 lists every change with its reason.
Each code has one meaning (`design-model.md` §10.2).

## 1. Vocabulary

```
node(Id, Kind).

standing("product-vision"). standing("job"). standing("bounded-context"). standing("context-seam").
standing("capability"). standing("requirement"). standing("requirement-group"). standing("scenario").
standing("universal-condition"). standing("term"). standing("design-decision").
generated("feature"). generated("step").            % new in v5: written by features generate, outside the graph's edges

root("initiative").  root("job-thread").             % job-thread is a root, never a part (C23)

part("job-proposal"). part("map-proposal"). part("vision-proposal"). part("map-escalation"). part("work-item").
part("capability-proposal"). part("glossary-proposal").
proposal("capability-proposal"). proposal("glossary-proposal").    % new in v5: the supertype proposal (C10)

node(_, "request").            % neither standing, root, part nor record: the one node that crosses a seam

record("observation"). record("measurement"). record("review-finding").
record("decision-argument"). record("initiative-archive"). record("design"). record("analysis").   % design, analysis new in v5
origin("observation"). origin("measurement"). origin("review-finding").
```

Attributes read from the files:

```
narrator(C, Who)          % capability, job; a role from a job, never a bounded-context
group(C, G)               % model | service | operations | guarantees
at(N, Ctx)                % the bounded-context (or "product") a root, part or request is kept by
status(N, S)              % roots, parts, requests, design-decisions
ikind(I, K)               % initiative: capability-change | defect
summary(D, Text)          % design-decision; required
revisit_signal(D, Sig)
req_id(Q, C, N)           % requirement Q is [r<n>] of capability C
group_id(G, C, N)         % requirement group G is [g<n>] of capability C              (new in v5)
u_id(U, N)                % universal condition U is [U<n>]                            (new in v5)
retired_id(C, Id)         % r<n> and g<n> a capability has used and retired
restated_0_29(Old)        % Old = <cap>#r<n> is a key of spec/restated.json            (new in v5)
category(T, Cat)          % term T: actor | kind | attribute | value | relation | event | resource | condition (new in v5)
value_of(V, K, A)         % value V belongs to attribute A of kind K                   (new in v5)
lin(T, Text)              % the text a term linearises to                              (new in v5)
fileset(W, Path)
asker(Q, X). upstream(Q, X).
line(Q, N, Text)          % request line: parses in the upstream's grammar (C20)
outcome(Q, N, O)          % request line: accepted | rewritten | refused | question | withdrawn
```

The facts that join the two languages *(new in v5)*:

```
parsed(Q)                 % requirement or universal condition Q parses to one tree, after the guards
unparsed(Q, Why)          % no tree is left; Why names the token and its position, or the guard
ambiguous(Q)              % more than one tree is left after the guards
logic_only(G)             % every statement of G is a resource statement: G has no scenario
given_unparsed(G, Line)   % a line of G's given block does not parse in the Steps grammar
given_condition(G, Line)  % a line of G's given block that is not example data, by its shape (revision 2)
pre(Q, Key)               % the normalised features, condition and trigger trees of a requirement
```

## 2. Edge schema

| relation | domain → range | cardinality | class | written by |
|---|---|---|---|---|
| `orders(V, J)` | product-vision → job | 0..n | standing | hand |
| `in(C, X)` | capability → bounded-context | exactly 1 | standing | hand |
| `member_of(Q, G)` | requirement → requirement-group | exactly 1 *(new in v5)* | standing | hand |
| `in(G, C)` | requirement-group → capability | exactly 1 *(new in v5)* | standing | hand |
| `has_req(C, Q)` | capability → requirement | **derived** from `member_of`, `in` | standing | derived |
| `generates(G, S)` | requirement-group → scenario | exactly 1 unless `logic_only(G)` *(replaces has_sc)* | standing | `features generate` |
| `restates(G, Old)` | requirement-group → 0.29 id | 0..n; a source only, `Old` is no node *(new in v5)* | standing | the conversion |
| `seam(R, Up, Down)` | context-seam → bounded-context, bounded-context | exactly 1 pair | standing | hand |
| `pins(Down, Up, V)` | bounded-context → bounded-context, version | 0..1 per seam | standing | hand |
| `rests_on(C, D)` | capability → design-decision | 0..n | standing | hand |
| `supersedes(D2, D1)` | design-decision → design-decision | 0..1 | standing | hand |
| `serves(C, J)`, `using(C, J, D)` | capability → job; (capability, job) → capability | 0..n | standing | script |
| `depends_on(C, D)` | capability → capability | derived | standing | derived |
| `avoids(T, W)` | term → word | 0..n | standing | hand |
| `source(X, Rec)` | initiative \| request \| job-thread → origin | 0..n | intake | hand |
| `part_of(P, X)` | part → part \| root; request → job-thread | exactly 1 for a part; 0..1 for a request | breakdown | the part's creator |
| `fulfils(I, Q)` | initiative → request | exactly 1 | breakdown | the upstream |
| `raises(W, Q)` | work-item → request | 0..n | part | the asker |
| `raised_for(Q, Q0)` | request → request | 0..1 | request | the asker |
| `resolution(Q, R)` | request → requirement | 0..n, one per accepted line; no version *(C19)* | request | the upstream |
| `argues(P, A)` | capability-proposal → capability | exactly 1 *(C16)*; a glossary-proposal argues the glossary | part | hand |
| `adds(P, X)`, `removes(P, X)` | capability-proposal → requirement; glossary-proposal → term | 0..n each | part | hand |
| `changes(P, X)` | capability-proposal → requirement-group; glossary-proposal → term | 0..n *(C18)* | part | hand |
| `under(W, C)` | work-item → capability | 0..1 | part | drafter |
| `accepts(W, X)` | work-item → requirement \| requirement-group (a group means its members) | 0..n *(C17)* | part | drafter |
| `check(W, Cmd)` | work-item → command | 0..1 | part | drafter |
| `blocked_by(W, W2)` | work-item → work-item | 0..n | part | drafter |
| `about(Rec, A)` | record → standing | exactly 1 | record | hand |

Gone: `needs`, `from_cap`, `across`, and the node kind
`cross-context-request` (C22).

## 3. Derivations

```
has_req(C, Q)    :- member_of(Q, G), in(G, C).
accepted_req(W, Q) :- accepts(W, Q), node(Q, "requirement").
accepted_req(W, Q) :- accepts(W, G), node(G, "requirement-group"), member_of(Q, G).
depends_on(C, D) :- using(C, _, D).
top(P, I)        :- part_of(P, I), node(I, K), root(K).
top(P, I)        :- part_of(P, P2), top(P2, I).
raised(I, Q)     :- raises(W, Q), top(W, I).
traced(Q)        :- part_of(Q, T), node(T, "job-thread").
traced(Q)        :- node(Q, "request"), source(Q, _).
traced(Q)        :- raised_for(Q, Q0), traced(Q0).
closed(P)        :- node(P, "capability-proposal"), status(P, "formulated").
closed(P)        :- node(P, "glossary-proposal"), status(P, "approved").
closed(P)        :- node(P, "work-item"), status(P, "green").
closed(P)        :- node(P, K), part(K), status(P, "withdrawn").
settled(Q, N)    :- outcome(Q, N, O), (O = "accepted" ; O = "refused" ; O = "withdrawn").
```

## 4. Integrity constraints

Numbered as `design-model.md` §4.

```
% 2. standing edges only between standing artifacts (one clause per relation)
v2(C, D) :- rests_on(C, D), (node(C, K), not standing(K) ; node(D, K2), not standing(K2)).

% 3. a resolution names a requirement (never a scenario), and the spec has it (one rule: C24)
v3(Q, X) :- resolution(Q, X), not node(X, "requirement").

% 4. depends_on is derived;  5. using points the way the pin points;  6. crossings reference seams
v4(C, D) :- authored_depends_on(C, D), not using(C, _, D).
v5(C, D) :- using(C, _, D), in(C, X), in(D, Y), X != Y, not pins(X, Y, _).
v6(T, R) :- crosses(T, R), not node(R, "context-seam").

% 7. asker and upstream sit across a seam
v7(Q) :- asker(Q, X), upstream(Q, Y), X != Y, X != "product", not seam(_, Y, X), not seam(_, X, Y).

% 8. a work-item names a capability
v8(W) :- node(W, "work-item"), not under(W, _).

% 9. every part has exactly one part_of reaching a root; priority and source only where allowed
v9a(P) :- node(P, K), part(K), not part_of(P, _).
v9b(P) :- part_of(P, A), part_of(P, B), A != B.
v9c(P) :- node(P, K), part(K), not top(P, _).
v9e(X) :- source(X, _), node(X, K), part(K).
v9f(I) :- part_of(I, _), node(I, K), root(K).

% 10. only an origin is a source; records are about standing artifacts
v10a(X, Rec) :- source(X, Rec), node(Rec, K), not origin(K).
v10b(Rec)    :- node(Rec, K), record(K), not about(Rec, _).

% 11. one narrator;  12. design-decisions: summary present, supersedes acyclic;  13. a watch has a reader
v11(C)  :- node(C, "capability"), not narrator(C, _).
v12a(D) :- node(D, "design-decision"), not summary(D, _).
v13(D)  :- revisit_signal(D, Sig), Sig != "requests", not node(Sig, "measurement").

% 15. ids: present, unique, never reused; groups and U's too; Restates: names a 0.29 id
v15a(Q)     :- node(Q, "requirement"), not req_id(Q, _, _).
v15b(Q1,Q2) :- req_id(Q1, C, N), req_id(Q2, C, N), Q1 != Q2.
v15c(Q)     :- req_id(Q, C, N), retired_id(C, N).
v15d(Q, C)  :- req_id(Q, C, _), not has_req(C, Q).
v15e(P, G)  :- changes(P, G), node(P, "capability-proposal"), not node(G, "requirement-group").
v15f(P)     :- status(P, "formulated"), adds(P, Q), member_of(Q, G), not generates(G, _), not logic_only(G),
               in(G, C), not group(C, "guarantees").
v15g(G)     :- node(G, "requirement-group"), not group_id(G, _, _).                    % new in v5
v15g(G1,G2) :- group_id(G1, C, N), group_id(G2, C, N), G1 != G2.
v15h(U1,U2) :- u_id(U1, N), u_id(U2, N), U1 != U2.                                    % new in v5
v15i(X)     :- (req_id(X, C, N) ; group_id(X, C, N)), retired_id(C, N).               % new in v5: never reused
v15j(G, O)  :- restates(G, O), not restated_0_29(O).                                  % new in v5
v15k(G)     :- member_of(Q1, G), member_of(Q2, G), pre(Q1, K1), pre(Q2, K2), K1 != K2.  % new in v5
v15l(G)     :- node(G, "requirement-group"), member_of(Q1, G), member_of(Q2, G), Q1 < Q2. % revision 2
v15m(G, L)  :- given_condition(G, L).                                                 % revision 2
v15n(G1,G2) :- group_id(G1, C, _), group_id(G2, C, _), member_of(Q1, G1), member_of(Q2, G2), % revision 2
               pre(Q1, K), pre(Q2, K), G1 < G2.

% 16. one request per initiative, one initiative per request, of its own context
v16a(I)    :- node(I, "initiative"), not fulfils(I, _).
v16c(Q)    :- fulfils(I1, Q), fulfils(I2, Q), I1 != I2.
v16d(I, Q) :- fulfils(I, Q), at(I, X), upstream(Q, Y), X != Y.

% 17. every request is traced;  18. part_of, blocked_by and for never cross a seam; no foreign work id
v17(Q)     :- node(Q, "request"), not traced(Q).
v18a(P, X) :- part_of(P, X), node(P, K), part(K), at(P, C1), at(X, C2), C1 != C2.
v18c(A, B) :- blocked_by(A, B), at(A, C1), at(B, C2), C1 != C2.

% initiative kinds fix the first part;  a capability-proposal argues one capability
v_k3(I) :- ikind(I, "capability-change"), part_of(P, I), not proposal_kind(P).
v_k4(I) :- ikind(I, "defect"), part_of(P, I), not node(P, "work-item").
v_k6(P) :- argues(P, A), argues(P, B), A != B, node(P, "capability-proposal").

% scenarios on groups (C28)
v_s1(S) :- node(S, "scenario"), not generated(S).
v_s2(S) :- generates(G1, S), generates(G2, S), G1 != G2.
v_s3(G) :- node(G, "requirement-group"), in(G, C), not has_scenario(G), not logic_only(G), not group(C, "guarantees").
v_s4(Q) :- req_id(Q, C, _), codified(C), not grouped(Q).
v_s4(Q) :- member_of(Q, G1), member_of(Q, G2), G1 != G2.

% work-items
v_w1(W)      :- blk_tc(W, W).
v_w2(W)      :- status(W, "ready"), blocked_by(W, B), not status(B, "green").
v_w3(W1, W2) :- status(W1, "claimed"), status(W2, "claimed"), W1 < W2, fileset(W1, P), fileset(W2, P).
v_w4(W)      :- node(W, "work-item"), not status(W, "withdrawn"), not accepts(W, _), not check(W, _).

% 19. done-ness through requests only
v_d1(I) :- status(I, "done"), top(P, I), not closed(P).
v_d1(I) :- status(I, "done"), raised(I, Q), not status(Q, "delivered").
v_d2(T) :- status(T, "built"), part_of(Q, T), node(Q, "request"), not status(Q, "delivered").
v_d3(Q) :- status(Q, "delivered"), fulfils(I, Q), not status(I, "done").
v_d5(I) :- status(I, "abandoned"), top(P, I), not closed(P).                          % LP's old v_d2 (C24)

% the parse (C25, new in v5)
v_p1(Q, Why) :- unparsed(Q, Why).
v_p2(Q)      :- ambiguous(Q).
v_p3(G, L)   :- given_unparsed(G, L).

% terms (C27, new in v5)
v_t1(X, W, T) :- mentions_prose(X, W), avoids(T, W).            % prose sections only: a parsed line uses lexicon words
v_t2(T)       :- glossary_entry(T, N1), glossary_entry(T, N2), N1 < N2.
v_t3(W)       :- avoids(_, W), lin(_, W).
v_t4(T)       :- node(T, "term"), not category(T, _).
v_t5(V)       :- category(V, "value"), not value_of(V, _, _).
v_t5(V)       :- value_of(V, K1, A1), value_of(V, K2, A2), (K1, A1) != (K2, A2).
v_t6(T1, T2)  :- lin(T1, X), lin(T2, X), T1 < T2, category(T1, C), category(T2, C).
```

The lexicon's own problems, reported by `model lexicon --check` and by
`model check` *(revision 2)*: **v_t7** a term entry whose gloss is more
than one sentence (§6.2's count), **v_t8** a relation entry (a relation
is a row of `## Relations`), **v_t9** a `Means` field, **v_t10** two rows of
`## Relations` with one (from, word, to).

Warnings:

```
w_unserved_cap(C)   :- node(C, "capability"), not serves(C, _), node(_, "job").
w_uncited_obs(O)    :- node(O, "observation"), not source(_, O).
w_many_requests(X)  :- upstream(_, X), #count { Q : upstream(Q, X), status(Q, "open") } > 5.
w_stale_intake(Q)   :- status(Q, "accepted"), not fulfils(_, Q), age(Q, Days), Days > 90.
w_stale_proposed(I) :- status(I, "proposed"), age(I, Days), Days > 90.               % LP's old w_stale_intake
```

Gone: v1, v7 and v7b in their LP meaning, v_b2, v_k1, v_k2, v_e1 and
v_e2 (the regex check, replaced by v_p1 and v_p2), and the inputs `needs`,
`from_cap`, `across`.

## 5. Lifecycles

Transitions not listed are violations. The glossary's attribute entries
(`spec/index.md`) give each as a row `from → to: event`, and
`model logic` reports a status set along no row (L3).

**request**: `open` → `awaiting-asker` (the upstream wrote an outcome for
every line and some line is not settled) ⇄ `awaiting-upstream` →
`accepted` (every line settled, one accepted) | `refused` (every line
settled, none accepted). `withdrawn` from any status before `accepted`.
`accepted → delivered` (no `v_d3`). The turn passes by `work turn`.

**initiative** (C15): `proposed → started` by `work start`;
`started → done` when it is complete (no `v_d1`); `started → abandoned`
by `work abandon` (no `v_d5`).

**capability-proposal** (C11): `drafted → awaiting-answer` (a question) →
`drafted` (`work answer`); `drafted → approved` (the person) →
`formulated` (its groups' scenarios generated and committed; no `v15f`);
`withdrawn` from any open status. `merged` is gone.

**glossary-proposal**: as the capability-proposal, without `formulated`.

**work-item** (C13): `drafted → researched → planned → ready → claimed →
done → green`, each by its stage's result (`planned → ready` and
`ready → claimed` by `work`, when no `v_w2` or `v_w3` would result); any
stage → `awaiting-answer` on a question, back to the stage's starting
status by `work answer`; any stage → `failed` when the stage is
discarded (U6), back by `work retry`; any open status → `withdrawn`.

**design-decision** (C14): `proposed → accepted | rejected`;
`accepted → superseded` when a later decision supersedes it.

**job-thread**: `proposed → mapped → accepted` (the person) → `built`
(no `v_d2`).

## 6. The requirement language

### 6.1 The grammars

- `grammar/Req.gf`, `grammar/ReqEng.gf`: the core requirement grammar,
  plugin-owned. The six EARS forms (`design-model.md` §2), each taking
  `Resps`; triggers and conditions not tied to a kind (`Runs`, `RunsOn`,
  `IsRun`, `Happens`, `HappensI`, `Undergoes`, `Holds`, `HoldsA`,
  `IsFree`), verb phrases (`Do`, `DoTo`, `Print`, `ExitOk`, `ExitErr`,
  `ChangeNothing`, `Hold`, `HoldA`, `HoldAtMost`), and untyped noun
  phrases (codes, quoted strings, numbers, lists, `only`).
- The funs of revision 2, each with a corpus line:

  | fun | type | English |
  |---|---|---|
  | `Shall` | `Subj -> VPs -> Resp` | `work run` shall A, B and C |
  | `ShallNot` | `Subj -> VPor -> Resp` | `work run` shall not A or B (neither) |
  | `OneVP`, `AndVP` | `VP -> VPs`, `VP -> VPs -> VPs` | A / A and B / A, B and C |
  | `OneVPor`, `OrVP` | `VP -> VPor`, `VP -> VPor -> VPor` | A / A or B |
  | `OneResp`, `AndResp` | `Resp -> Resps`, `Resp -> Resps -> Resps` | R1, and R2 (responses whose subjects differ) |
  | `CondOr` | `Atom -> Cond -> Cond` | A or B (beside `CondOne`, `CondAnd`) |
  | `rel_<k1>_<w>_<k2>` | `<k1>_CN -> <k2>_NP -> <k1>_CN` | a stage for the work-item (generated, one for each relation row) |
  | `rel_<k1>_<w>_<k2>_Atom` | `<k1>_NP -> <k2>_NP -> Atom` | the stage is for the work-item; the initiative fulfils the request (generated) |
  | `c_<cond>_<kind>_Def` | `Cond -> Def` | a <kind> is <cond> when C (generated, in `Def`) |

  `RefuseErr` and `CommitPush` are gone: they were `and` written as single
  funs, and are now `AndVP (ExitErr x) (OneVP ChangeNothing)` ("exit with
  an error naming X and change nothing") and `AndVP (Do commit x) (OneVP
  (Do push the_commit))`. Verb phrases are not noun phrases, so "print
  the file and the line count and exit successfully" has one tree. A
  response's conjuncts are read in their spoken order.
- `grammar/Steps.gf`, `grammar/StepsEng.gf`: the step grammar, one
  template for each Gherkin use of a category (Given a kind with a value,
  a relation, a resource held; When a command runs, an event happens, a
  value is reached; Then a value, an action, a print, an exit).
- `Lex` and `Typed`, generated for each context from its glossary and
  its `## Relations` rows, and never tracked: the words, and one typed
  block for each kind, attribute and relation row. The typed slots are
  what make "an initiative that is `drafted`" fail to parse.
- `Def` and `DefEng`, generated beside them: `abstract Def = Req ** {
  flags startcat = Def ; ... }`, one fun for each (condition, kind) of
  the lexicon. `model parse --grammar Req|Steps|Def` parses in any of the
  three. A definition that says "it" is refused: it names its subject as
  "the <kind>" (`Cond` is not indexed by kind, so `it` would fill any
  typed atom whose kind has the word).
- The Steps grammar is additive: each conjunct of a response is its own
  Then (`SDoes`, `SAtom`, ...), and a relation atom is an `Atom`, so
  `SAtom` gives "the stage s1 is for the work-item w1". A commit and its
  push are two conjuncts, so two Thens (`SDoes`); there is no `SCommits`.
- `grammar/corpus/*.txt`: sentences that must parse with exactly one tree,
  one file per capability; `grammar/corpus/refused.txt`: sentences that
  must be refused.

### 6.2 The lexicon

A term entry is
`- **term** (category): one sentence. Plural: … . Forms: … . Kind of: … . Not: … .`
The glossary is the union of `spec/index.md`'s `## Glossary` and each
capability's `## Terms`. For an attribute or a condition its kind
follows the category (`attribute of initiative`). An attribute gives
`Values:` and `Transitions:`; a kind may give `Kind of:` (its
supertype); a resource is `exclusive` or `counted by <code>`. A term
maps to a GF identifier by its category's letter and its lower-cased
spelling (`k_work_item`, `a_work_run`).

- **One sentence** (v_t7): the gloss is the text after the `:` and before
  the first field. Code spans, quoted strings, `e.g.`, `i.e.`, `etc.` and
  `vs.` are blanked; a sentence ends at `.`, `!` or `?` before a space or
  the end, and at `;`; a `:` ends none. What a thing contains or does is
  a requirement, never a gloss.
- **Relations are rows**, not entries: `## Relations` in `spec/index.md`
  (and a capability's own), `| from kind | word | to kind |` with an
  optional cardinality. A row on a supertype expands to every subkind
  and keeps its own fun, under the one relation id. A preposition between
  two kinds means the one row for that pair; the attachment of a
  prepositional phrase is typed, so a line where two attachments
  typecheck is refused and reworded. `Lexicon.relations()` gives the
  expanded rows `(k1, word, k2, rid)`.
- **A condition** is a definition or primitive. A definition is one
  sentence that parses in `Def` (`An initiative is open when the
  initiative is not `done` and the initiative is not `abandoned`.`); its
  logic is a rule. A primitive condition's sentence is a gloss; the logic
  treats it as a fluent, free when its thing is created and inertial
  after. There is no `Means` field (v_t9).

### 6.3 Guards and tokens

GF's types alone accept repeated list members and an `it` with no
antecedent, so the parse is followed by a check on each tree: a value
list has no repeats, `it` follows a noun phrase of the same sentence (and
never stands in a definition), and
a literal is a literal only when it is no lexicon word (a backticked
lexicon word parses only as the word). A tree that fails is dropped;
ambiguity (v_p2) is counted after the guards. The tokeniser splits off
punctuation and keeps a backticked span, a double-quoted string and a
number as one token each.

### 6.4 Growth

A core fun is added only for a construct that recurs in at least two
capabilities; otherwise the line is reworded. Grammar changes are plugin
changes, made with a corpus line for each new fun. A target project grows
its language by glossary entries only.

### 6.5 The reading form of the graph

The sentence forms of version 4 stay as a non-normative way to read the
graph aloud (`ecommerce-example.md`): *capability-proposal P argues C
adds r3, r4, part of I*, *request Q from X to Y, raised for Q0: lines*.
No parser reads them; `LINE = EARS` and "formulated as" are gone (C30).
A line is a sentence of §6.1.

## 7. The logic check and the tooling

- **`model check`** reads the facts of §1–§3 and holds §4 with clingo
  (`scripts/model.lp`). It reads the parse facts, and never solves over
  time.
- **`model logic`** translates each requirement's tree, one translation
  for each abstract fun, into ground facts about the requirement, its
  noun phrases one generic instance each (`v1`, `v2`, … in order of
  mention): `role` for each noun phrase, `cond`, `ccond` and `crel` for
  the pre-state (a `Def` condition expanded into its literals, a prose
  one opaque), `none` for "no K is v" (read over every thing of kind K),
  `trig` for the trigger, `resp` for each conjunct of `and`, `set` for
  an attribute set, `every`, `uses` for "X shall use Y" (static, not an
  event), and `form`; a choice is split into `R#1`, `R#2`, … reported
  under R. The lexicon adds the domain facts: kinds, sub-kinds, values,
  transition rows and initial values. The whole context is checked in
  one brave clingo solve of these facts with the fixed encoding
  `grammar/check.lp`, over two states: state 0 is the pre-state, the
  trigger happens there, and state 1 is state 0 with the sets applied,
  where the responses happen (`When T, R` is G(T → X R); `While C, R` is
  G(C → R)). Candidate pairs come from a shared-vocabulary index, never
  the cross product: two triggered requirements with one trigger, a
  triggered and an untriggered one over a shared kind, a requirement and
  a U that share an event or an attribute. A unification maps each role
  of one requirement to a role of the other of a compatible kind, or
  keeps it apart; the triggers must unify and the merged pre-state must
  be consistent. The shown atoms are the findings:
  - **L1** (error): a clash: under one unification, two requirements
    fire together and demand opposite things (one event done and not
    done on one object, one attribute set to two values, `exit_ok` with
    `exit_error`, `change_nothing` with a change, "use" with "shall not
    use"), named both, with the merged pre-state of the witness; or one
    requirement whose own pre-state is inconsistent;
  - **L2** (warning): two requirements with equal normalised trees;
  - **L3** (error): a set whose implied pre-value has no transition row
    to the new value;
  - **L4** (warning): a value some pre-state needs that no transition
    path reaches from an initial value;
  - **L5** (warning): an untriggered positive event obligation ("While
    C, X shall do E"), naming the triggered requirements that react to
    its event;
  - **L0** (error): the solve did not finish within its 20 s limit; the
    findings so far are listed.
- **`model parse`**, **`model lexicon`** and **`model restates`** report a
  line's tree or refusal (with the longest parsed prefix and the nearest
  lexicon words), the lexicon by category, and the coverage of the 0.29
  ids.
- **`features generate`** writes one scenario for each group, read off
  its requirements' facts with no solver: the `feat` facts, then the
  pre-state facts in clause order, then each instance first mentioned
  there give the Givens, the `trig` fact the When, each `resp` fact with
  its object's restrictions and then the `set` facts the Thens, each
  linearised through the Steps grammar; instances are named by their
  kind's letter in order of first mention. An `every` role with a
  restriction gets a contrast: one more instance that fails it, as a
  Given, and a `does not` Then for it. A `none` condition gives no
  Given. A scenario states only its own requirements; the world the
  handlers build supplies the defaults. A given block gives only example
  data, first; a given line that is not example data is left out with a
  line on stderr (v15m is its error). The same spec gives the same
  bytes. A group with a fact no step words gets no scenario and a line
  on stderr. `features vocab` reads the step grammar's typed funs as
  step patterns.
- The grammar tools are GF 3.12 with the pgf runtime and clingo,
  installed by `tools install`.
