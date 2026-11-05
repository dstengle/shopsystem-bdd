---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-03-gf-conversion-design-r2
kind: design
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-03
status: draft
---

# The GF conversion, revision 2: the written design

This design builds `revision-brief.md` (beside this file), points A–G. `brief.md` and its delegation still hold, and
`design.md` (the first design) holds wherever this one does not replace it. Replaced outright: design.md §8.1's "one
`shall`", §10.1's `Means:` and per-preposition relation entries, §12 (the logic check), §14.2 (generation) and the
`given` blocks of §10.2. `plan-r2.md` is the build plan.

## 1. What changes, in one paragraph

A requirement is parsed by GF into one tree, and the tree has one translation: into telingo temporal formulas
(`&tel{}`), one per grammar fun. That translation is the only reading of a requirement's meaning. `model logic`
solves it with telingo's own incremental loop and names conflicts by unsat cores. `features generate` asks the same
solver for a minimal trace of each group and reads the scenario off that trace: state 0 gives the Givens, the trigger
gives the When, the responses give the Thens. Every step is linearised through the Steps grammar. The grammar takes
`and` between responses, resolves a preposition by the pair of kinds it joins, and parses a condition's definition.
The lexicon then shrinks to one sentence for each term, and the spec is rewritten to all of this.

## 2. Done, as measurements (the brief's "Done means")

| # | the person's point | measured by (plan-r2 R14 runs each) |
|---|---|---|
| 1 | no given block that is not example data | `model check`: rule **v15m** ("a given line that is not example data") has no rows. A given line is example data only by its shape (§9.1): `the <words> <name> holds:` followed by a docstring or a table, or `the <words> <name> holds` followed by one code span or quoted string. The shape test is in `spec_read_given.py`; no grammar is compiled for it |
| 2 | statements that repeat a trigger are combined with "and" | `model check`: rules **v15l** ("a group has more than one statement") and **v15n** ("two groups of one capability whose statements share features, condition and trigger") have no rows. v15k stays. Together: one statement per (features, condition, trigger) in a capability |
| 3 | terms: no logic in definitions, no per-preposition meanings | lexicon problems **v_t7** (a term entry over one sentence, counted by §8's rule), **v_t8** (a relation entry that only names a preposition), **v_t9** (a `Means:` field) and **v_t10** (a duplicate relation row) have no rows; `grep -rn 'Means:' spec/` prints nothing. What the rows mean for the person's point is reported to the person (§13, call 16) |
| 4 | GF to telingo; the solver finds conflicts | named tests, not greps: `test_spec_logic.py::test_statement_is_a_tel_constraint` (the emitted text of a `When` statement is `:- on(id), …, &tel{ … & ~ > … }`), `test_spec_engine.py::test_stops_at_horizon_1`, `::test_chained_stops_at_horizon_2` and `::test_engine_uses_imain` (telingo's own `imain` sets the horizon), and `test_spec_solve.py::test_seeded_conflict` (a requirement contradicting a live one, built from the live spec, gives an L1 naming both ids). `! grep -rn 'HORIZON = ' scripts/` |
| 5 | Gherkin read from traces, byte-stable | `features generate --check` exits 0 for every service capability; `test_features_generate.py::test_byte_stable` generates twice, under two `PYTHONHASHSEED`s, and after adding two unrelated requirements (§7.4), and compares bytes |
| 6 | new requests go through it | `tests/scripts/test_e2e_codified.py` (P15) passes, and q47's six lines parse (`model parse`) |
| 7 | — | full suite green; `tools size --limit 300` exits 0 |

## 3. The spike (done before this design; the result it rests on)

**Where it is:** `.shop/scratch/spike-tel/` (gitignored, readable on disk). It holds `spike.py` (334 lines),
`run_spike.py` and `spike-output.txt`. It was run with clingo 5.8.2 and telingo 2.1.3 under `python3`.

**What it did.** It took the real trees from `spec_grammar.parse` on the live branch: supervision g2 (r2), and g13
(r16 and r17), with g13's two statements merged into one requirement whose response conjoins the two VPs, as point C
asks. It translated each tree, fun by fun, into `&tel` constraints guarded by `#external on(id)`. It added a witness
for each group (its condition and trigger hold at state 0) and solved with `telingo.imain` through a Control proxy.
It then read a minimal trace with fixed tie-breaks into Given/When/Then.

The translation it produced (r2, and the merged g13 as r13):

```
resp("r2",0,X1) :- does(a_work_run,e_start,S), attr(S,t_kind,v_research_2), rel(r_for_7,S,X1), kind(S,k_stage), kind(X1,k_work_item).
:- on("r2"), kind(X1,k_work_item), kind(X2,k_initiative),
   &tel{ attr(X1,t_status_6,v_drafted_3) & ran(a_the_person,a_work_run,X2) & ~ > (resp("r2",0,X1)) }.
:- on("r13"), kind(X1,k_result), kind(X2,k_session), kind(X3,k_stage), kind(X4,k_work_item),
   &tel{ cond(c_outputless,X1) & attr(X3,t_kind,v_plan_2) & rel(r_for_7,X3,X4) & rel(r_with,X3,X1) & does(X2,e_end,X3)
         & ~ > (does(a_work_run,set(t_status_6,v_awaiting_answer_3),X4) & resp("r13",0,X4)) }.
```

**Results** (`spike-output.txt`; the whole run takes 0.8 s for 8 solves):

| run | horizon telingo stopped at | optimal models | Gherkin |
|---|---|---|---|
| g2 alone | 1 | 2 | `Given the work-item w1 whose status is drafted` / `When the person runs work run on the initiative i1` / `Then work run starts the stage s1 [research, for w1]` |
| g2 again | 1 | 2 | identical bytes |
| g2 + merged g13 (unrelated) | 1 | 2 | identical bytes |
| g2 + r8 (chained: "when `work run` starts a research stage, it logs the stage") | **2** | 32 | identical Givens and When |
| g13 merged, alone / again / + r2 | 1 | 5 | identical bytes: `Given the result r1 is outputless` / `When the session e1 ends the stage s1 [plan, for w1, with r1]` / `Then work run asks the question q1 [on w1]` / `And work run sets the status of w1 to awaiting-answer` |
| seeded conflict: merged g13 and r99 "… `work run` shall not ask a question on the work-item", r2 also on | UNSAT up to the bound | — | **unsat core = [r13, r99]** (r2 not named) |

**What the spike settled** (each is a rule of this design):

1. `&tel{}` may appear only in a constraint, under `not`, or in a head (telingo raises "temporal formulas not
   supported in this context" otherwise). So a requirement becomes a constraint, a witness becomes `:- …, not &tel{…}`
   in `#program initial`, and a condition's definition (which is not temporal) becomes a plain rule.
2. `&tel` has no quantifier. A response's existential object ("start **a** stage for the work-item") becomes an
   auxiliary atom `resp(id, i, <shared variables>)`, defined by a rule in the always part, and the formula says
   `~ > resp(…)`.
3. **Strong next (`>`) drives the horizon.** A trigger at the last state violates `~ > R`, so telingo's own `imain`
   (istop SAT) stops at the first horizon where every obligation is met. g2 stopped at 1, and at 2 once a chained
   requirement was added. No fixed horizon is needed.
4. **The `on/1` externals have to be set free right after each ground.** With the externals left at their default of
   false and passed as assumptions, every solve was UNSAT. Calling `assign_external(sym, None)` after each `ground`
   fixed it. The proxy does this, so `imain` is used as it is and its loop is not copied.
5. A minimal trace gives values to things it creates that nothing asked for (the spike's `rel(r_for_3,s1,i1)`). The
   spike worded the Thens from the trees to avoid them. **This design does not** (check point 5): the translation
   labels the atoms each clause asks for (§5.7), the scenario is read from the labelled atoms of the trace and the
   state-0 fluents, and each atom has one Steps fun by its predicate (§7.3). An unlabelled value of a created thing
   is never read, so the spike's stray relation does not reach the text.
6. The tie-break is exhaustive. clingo enumerates every optimal model (`--opt-mode=optN`), and Python takes the least
   by its sorted atom strings. With the instance pool's symmetry broken (`o(K,2)` only if `o(K,1)`), the spike saw
   between 2 and 42 optimal models.
7. Solver reachability also works. A test program with transitions a→b→c reached `c` at horizon 2 through
   `:- not &tel{ >? v(c) }`, and `d` was UNSAT at every horizon up to the number of values.

## 4. The grammar (points C, D, E)

Files: `grammar/Core.gf`, `CoreEng.gf`, `Req.gf`, `ReqEng.gf`, `Steps.gf`, `StepsEng.gf`, and the generated `Lex`/
`Typed`/`StepsTyped` (from `spec_typed.py` and `features_vocab.py`). A tree stays unambiguous: `spec_grammar.parse`
already refuses a line with two trees, and every change below is checked against the corpus (`grammar/corpus/*.txt`)
for one tree per line.

### 4.1 `and` between responses (C)

| fun | type | English |
|---|---|---|
| `Shall` | `Subj -> VPs -> Resp` | `work run` shall A, B and C |
| `ShallNot` | `Subj -> VPor -> Resp` | `work run` shall not A or B (neither) |
| `OneVP`, `AndVP` | `VP -> VPs`, `VP -> VPs -> VPs` | `A` / `A and B` / `A, B and C` (the `MoreNP` pattern) |
| `OneVPor`, `OrVP` | `VP -> VPor`, `VP -> VPor -> VPor` | `A` / `A or B` |
| `OneResp`, `AndResp` | `Resp -> Resps`, `Resp -> Resps -> Resps` | `R1, and R2`: responses whose subjects differ |
| the forms | `… -> Resps -> Req` | every form takes `Resps` in place of `Resp` |
| `CondOr` | `Atom -> Cond -> Cond` | `A or B` (CondAnd stays) |

**Deleted:** `RefuseErr` ("exit with an error naming X and change nothing") and `CommitPush` ("commit X and push the
commit"). They were `and` written as single funs, and are now `AndVP (ExitErr x) (OneVP ChangeNothing)` and
`AndVP (Do commit x) (OneVP (Do push the_commit))`. Both must be deleted in the same change that adds `AndVP`:
with both present, the 50 spec lines that use them would have two trees and be refused. "push the commit" needs the
event **push**, which today is local to `role-boundaries.md`. The orchestrator moves that entry, unchanged, to
`spec/index.md` before layer 1 (a shared change between layers), so the 50 lines keep parsing once R1 lands. "the
commit" has no antecedent in its statement. A `<k>_The` with no antecedent is translated as `<k>_An` (§5.4).

**Ambiguity:** `print X and exit successfully` could be read as a list of noun phrases or a list of verb phrases. VPs
are not NPs, so GF gives one tree. The corpus gets one line for each new fun, plus the risky cases (`print the file
and the line count and exit successfully`). `spec_tree.parts(tree)` returns `resp` as a list of `(polarity, subject,
VP)` conjuncts, in their spoken order.

### 4.2 Prepositions resolved by the kinds they join (D)

- There is no `Prep` category (check point 3). Each typed relation fun carries its own word, so a closed class of
  prepositions would be unused. `spec_typed.PREPOSITIONS` stays only to tell a preposition row from a verb row.
- The relations of a context are one table, `## Relations`, in `spec/index.md`, and optionally in a capability file
  for its own local relations. Each row is `| from kind | word | to kind |`, with an optional fourth column for
  cardinality. The word is a preposition or a verb (with `Forms:` given only when it is irregular). This is the
  domain model's §4 table.
- A kind entry may say `Kind of: node`. A row whose from or to kind is a supertype expands to every subkind, so
  domain model §4's "for | stage → node" is one row, not six. **The supertype keeps its own fun too** (check point
  12): (stage, for, node) and (stage, for, work-item), … are all generated, with the one relation id of the row.
  This gives no second tree, because the grammar has no coercion from `k_work_item_NP` to `k_node_NP`: "a stage for
  the work-item w1" typechecks only against the work-item fun, and "a stage for a node" only against the node fun.
  R1's corpus has one line of each with its expected tree. In the logic, `kind(X,node) :- kind(X,K), sub(K,node).`,
  so a node variable ranges over the subkinds. supervision.md's local `for` entries (lines 26–31) duplicate
  `spec/index.md`'s "for (stage → node)" once expanded. R5 deletes the local ones, and v_t10 catches any left.
- `spec_typed.py` generates one typed fun for each expanded row: `rel_<k1>_<word>_<k2> : <k1>_CN -> <k2>_NP ->
  <k1>_CN` (a modifier: "a stage for the work-item"). It also generates `rel_<k1>_<word>_<k2>_Atom : <k1>_NP ->
  <k2>_NP -> Atom` (a clause: "the stage is for the work-item", "the initiative fulfils the request").
- **The resolution rule:** a preposition between two kinds means the one relation its row gives for that pair. Two
  rows with the same (from, to, word) are lexicon problem v_t10. Two relations on one kind pair need distinct words
  (adds/changes/removes already have them). PP attachment is typed, so "a `plan` stage for a work-item with the
  result" has one tree only because (work-item, with, result) has no row. Where both attachments typecheck, the line
  is refused as ambiguous and is reworded. q47's line 4 ("an `integrate` stage for an initiative with a result that
  is `DONE`") is the same case for (initiative, with, result). It goes into `grammar/corpus/core.txt` as a guarded
  line: R1's test shows one tree today and a refusal once a stub row (initiative, with, result) is added. Since the
  corpus test is in the suite, whoever adds such a row later sees the refusal and rewords the corpus line and the
  spec line together.
- **Removed:** every term entry `**for** (relation …)` or `**on** (relation …)`, and every other relation entry that
  only names a preposition (v_t8). A relation's meaning is its row.

### 4.3 Conditions defined in the language (E)

- A condition entry is one sentence. Either the sentence parses as a **`Def`**, or the condition is **primitive**.
- `Def` is a **new generated module pair, `Def.gf`/`DefEng.gf`** (check point 2): `abstract Def = Req ** { flags
  startcat = Def ; cat Def ; fun … }`. `spec_typed_def.py` (new, beside `spec_typed.py`) writes it next to the
  generated `Lex`/`Typed` modules, with one fun for each (condition, kind) the lexicon gives:
  `c_<cond>_<kind>_Def : Cond -> Def`, English `a <kind> is <cond> when <Cond>`. `spec_grammar.load(root, "Def")`
  then compiles `DefEng.gf` by the mechanism it already has, and `model parse --grammar` takes `Req`, `Steps` or
  `Def`. The condition then has a definition, and its translation is a rule (§5.6).
- **A definition names its subject as "the <kind>", never "it"** (check point 11). `Cond` is not indexed by kind,
  so `k_<kind>_It` could fill any typed atom whose kind has the word, and give several trees. `the <kind>` is
  `k_<kind>_The`, typed to its kind, and binds to the head by the anaphora rule of statements. `spec_grammar.parse`
  with `grammar="Def"` refuses a tree that holds any `_It` fun, with the hint "a definition names its subject as the
  <kind>". A coordination across kinds ("no question and no output") is written as two clauses. The corpus lines and
  their expected trees (R1, with stub rows (result, gives, question) and (result, gives, output)):

  | line | tree |
  |---|---|
  | A result is outputless when the result gives no question and the result gives no output. | `c_outputless_k_result_Def (CondAnd (rel_result_gives_question_Atom (k_result_The k_result) (k_question_No k_question)) (CondOne (rel_result_gives_output_Atom (k_result_The k_result) (k_output_No k_output))))` |
  | An initiative is open when the initiative is not `done` and the initiative is not `abandoned`. | `c_open_k_initiative_Def (CondAnd (t_status_<n>_IsNot (k_initiative_The k_initiative) v_done) (CondOne (t_status_<n>_IsNot (k_initiative_The k_initiative) v_abandoned)))` |
  | A result is outputless when it gives no question. | refused: "a definition names its subject as the result" |

  (`<n>` is the attribute's generated index, as in `t_status_6`.)
- A condition whose sentence does not parse as a `Def` is primitive. Its sentence is a gloss, like a kind's, and the
  logic treats the condition as a fluent: free when its thing is created, and inertial after that. A step definition
  builds it. Most of design-model-check's 40 file-shape conditions (unnumbered, renumbered, reusing, …) are
  primitive, because their words (a bullet, a bracket) are not kinds.
- The rule for choosing between the two: a condition is defined when every word of its sentence is in the lexicon
  and the sentence parses. Otherwise it is primitive. A condition that is a value test (`open`: its status is neither
  `done` nor `abandoned`) is always defined. The rewrite packages (§9) choose the wording for each condition.
- Words the definitions need that the grammar lacks: relation atoms (§4.2), `CondOr`, and `No` in a clause object
  ("it gives no question"). `No` already exists as a determiner.

### 4.4 The Steps grammar

The Steps grammar is additive, so every step text that parses today still parses. There is no `SRelAtom` (check
point 3): a relation atom `rel_<k1>_<w>_<k2>_Atom` is an `Atom`, so the existing `SAtom` already gives "the stage s1
is for the work-item w1". A condition's Given is `SAtom` over `<cond>_Is` ("the result r1 is outputless"). Each
conjunct of a response is its own Then (`SDoes`, `SAtom`, …).

**`SCommits` stays until R14** (check point 1). `features/supervision.feature` (lines 257, 395, 440) has "… and pushes
the commit" steps, and `features_vocab.py` maps `SCommits` to `ThenCommits`; the scenario suite must stay green in
every layer. The new generator (R6, layer 3) writes a commit-and-push response as two Thens, `SDoes` commit and
`SDoes` push. Layer 4 regenerates the features, so no step uses `SCommits` after it. R14 (layer 5) deletes `SCommits`
from `Steps.gf`/`StepsEng.gf`, its mapping in `features_vocab.py` and the `ThenCommits` handler, and checks with
`features vocab --check --tests tests/scenarios`. `RefuseErr`'s Thens were already two (`SExitsErr` +
`SChangesNothing`).

## 5. The &tel translation (point A)

`scripts/spec_logic.py` has one translation per fun (the core funs and the typed patterns). It has two renderers:
`&tel` text for statements, and a plain ASP body for definitions. Nothing else in the plugin reads a requirement's
meaning.

### 5.1 Atoms

| atom | kind of atom | written by |
|---|---|---|
| `kind(X,K)` | static | the pool (§6.2) |
| `attr(X,A,V)` | fluent: at most one V for each (X,A), inertial | creation, or `does(_,set(A,V),X)` |
| `rel(R,X,Y)` | fluent, inertial | creation, or a response |
| `cond(C,X)` | derived (defined condition) or fluent (primitive) | its rule, or creation |
| `does(S,E,X)` | event: true at the state it happens, not inertial | a trigger or a response; S is an actor or a thing |
| `ran(S,C,X)` | event: S runs command C (on X, or `none`) | Runs, RunsOn, IsRun |
| `given(F)` | static | Where F |
| `holds(X,R)`, `active(X)`, `over(R)` | as in today's background (resources) | |
| `used(X)` | derived: X appears in any of the above | the pool's minimality |

### 5.2 Statement forms (B is the static binding literals of the clause's noun phrases, `kind(X,K)`)

| form | constraint guarded by `on(id)` |
|---|---|
| `Ubiq R` | `:- on(id), B, used(X…), &tel{ ~ R }` (same state; quantified NPs range over used things) |
| `When T R`, `IfThen T R` | `:- on(id), B, &tel{ T & ~ > R }` |
| `While C R` | `:- on(id), B, &tel{ C & ~ R }` |
| `Where F R` | `:- on(id), B, &tel{ F & ~ R }` |
| `WhileWhen C T R`, `WhileIf C T R` | `&tel{ C & T & ~ > R }` |
| `WhereWhen F T R`, `WhereIf F T R` | `&tel{ F & T & ~ > R }` |
| `WhereWhile F C R` | `&tel{ F & C & ~ R }` |
| `ShallNot` | the same, with `~ R` written `R` (the constraint fires when the forbidden response happens) |
| `Resps` / `VPs` with n conjuncts | n constraints under the same `on(id)`, one per conjunct (the same as `~ > (R1 & … & Rn)`, and each Then is one conjunct) |
| `VPor` under `ShallNot` | n constraints `… & > Ri` |

Triggers are read at state t and responses at t+1. Conditions and features are read at t.

### 5.3 Clause funs

| fun | formula |
|---|---|
| `Runs S C` / `RunsOn S C X` / `IsRun C` | `ran(S,C,none)` / `ran(S,C,X)` / `ran_any(C,none)` (aux `ran_any(C,X) :- ran(_,C,X).`) |
| `Happens S E X` / `HappensI S E` | `does(S,E,X)` / `does(S,E,none)` |
| `Undergoes X E` | `done_to(E,X)` (aux `done_to(E,X) :- does(_,E,X).`) |
| `<attr>_Becomes X v` | `set_to(X,A,v)` (aux from `does(_,set(A,v),X)`); the source value comes from the transition constraint (§6.4) |
| `CondOne` / `CondAnd` / `CondOr` | `A` / `A & C` / `A \| C` |
| `<attr>_Is X v` / `_IsNot` | `attr(X,A,v)` / `~ attr(X,A,v)` |
| `<cond>_Is X` / `_IsNot` | `cond(C,X)` / `~ cond(C,X)` |
| `rel_…_Atom X Y` | `rel(R,X,Y)` |
| `Holds X R`, `HoldsA X R` / `IsFree R` | `holds(X,R) & active(X)` / `~ over(R)` |
| `FeatGiven c` / `FeatAtom A` | `given(c)` / A |

### 5.4 Noun phrases

| fun | in a clause | as a response's object |
|---|---|---|
| `<k>_An`, `_One`, `_Every`, `_Pl` | a fresh variable X, `kind(X,K)` in B, and its modifiers conjoined into the clause | an existential: the aux atom of §3 rule 2 (`_Every`/`_Pl`: universal, so X is bound in B and the response is per X) |
| `<k>_The`, `_It`, `_Its` | the variable bound before for K (anaphora); a `_The` with no antecedent in its statement is read as `_An` | the same |
| `<k>_Every`/`_Pl` with a restriction, **in a witness** | the witness also asks for one K that fails the restriction at state 0 (`contrast(id,i,Y)`), and labels its absent response `lab(id, not(i), …)` (§5.7) | |
| `<k>_No` | `~ some_<id>_<i>(…)` (an aux for "there is one") | the response's polarity flipped: `> resp` |
| `<k>_AtMostOne` | an aux defined by a `#count` rule (no aggregate inside `&tel`) | the same |
| `<k>_Named c` | the constant `c`, with `kind(c,K)` a fact | the same |
| `<k>_NumberOf`, `<attr>_Of X` | the terms `number(K)`, `value(A,X)`, as today | |
| `Only X`, `CodeNP`, `QuotedNP` | X; a quoted constant | |
| modifiers: `<attr>_Pre v`, `_ThatIs`/`_Whose v1..vn`, `_ThatIsNot`/`_WhoseNot` | `attr(X,A,v)`; `attr(X,A,v1) \| …`; `~ attr(X,A,v1) & …` | inside the aux body |
| `<cond>_Pre`, `_ThatIs`, `_ThatIsNot` | `cond(C,X)` / `~ cond(C,X)` | inside the aux body |
| `rel_<k1>_<w>_<k2> CN NP` | `rel(R,X,Y)` and the NP's own formula | inside the aux body |

### 5.5 Verb phrases (one conjunct each)

`Do E X` → `does(S,E,X)`. `DoTo E X Y` → `does(S,E,pair(X,Y))`. `Print NPs` → one `does(S,print,Xi)` for each
member (a conjunct each). `ExitOk`, `ExitErr X` and `ChangeNothing` → `does(S,exit_ok,none)`,
`does(S,exit_error,X)` and `does(S,change_nothing,none)`. `<attr>_Set X v` → `does(S,set(A,v),X)`, with the effect
rule `attr(X,A,V) :- does(_,set(A,V),X).` `Hold R`, `HoldA R` → `holds(S,R)`. `HoldAtMost n R` → an aggregate
constraint in the always part: `:- on(id), #count{Y : holds(Y,R), active(Y)} > n.` Aggregates are not allowed in
`&tel`, so count statements stay plain ASP.

### 5.6 Definitions, universal conditions, choices

- **A defined condition** `a K is c when Cond`: `cond(c,X) :- kind(X,K), <Cond as an ASP body>.` (`~` becomes `not`,
  `|` becomes one rule per disjunct, `No` becomes `not` of an aux.) A definition is not guarded. If it is wrong, its
  condition is wrong everywhere, and model check's term rules own it.
- **U1–U10** are statements, translated by the same table and guarded by `on("U<n>")`. U3 and U4 become
  coordinations: "exit with an error naming the reason and change nothing", and "commit every transition and push
  the commit".
- **Choices.** Every response head pattern (`does(S,E,_)` with the object's kind) and every trigger pattern of the
  program gets a choice rule `{ … }`. Fluents are free only when their thing is created (§6.2). So the solver can do
  what a statement asks, and minimisation (§7.2) removes anything that nothing asks for.

### 5.7 Labels and signatures: what the rest of the plugin reads (check points 5–8)

The translation emits two more outputs beside the constraints, from the same per-fun code that writes each formula.
Nothing downstream walks a tree.

- **Labels.** For each clause and each response conjunct, a shown atom `lab(Id, Part, Atom)`, where `Part` is
  `feat(i)`, `cond(i)`, `trig`, `resp(i)`, `mod(i,j)` (the j-th restriction of conjunct i's object) or `not(i)` (a
  contrast's absent response). Each is a rule in the always part, bound to the instances of the witness or of the
  firing: for example `lab("r13",resp(1),does(a_work_run,e_ask,Q)) :- resp("r13",1,X4,Q), does(a_work_run,e_ask,Q).`
  The witness's clauses label at state 0, the trigger at the state it happens, and the responses at the next state.
- **Signatures.** For each statement, ASP facts: `trig(Id,P,E,K)` (its trigger's predicate, event or `set` value, and
  object kind), `eff(Id,P,E,K)` for each response conjunct, `uses(Id,K)` for each kind its noun phrases bind, and
  `untriggered(Id)` for Ubiq/While/Where/WhereWhile. `grammar/cone.lp` (new, about 20 lines) derives `edge(S,T)` (an
  effect of S matches a trigger of T: the same predicate and event or value, and kinds equal or one a subkind of the
  other) and `in_cone(G,Id)` (§6.3). `spec_engine.cone(facts, gid)` grounds and solves it once; the horizon bound is
  the longest path over the `edge/2` atoms it returns.

## 6. The program and the solve

### 6.1 Modules

| module | concern | about |
|---|---|---|
| `scripts/spec_logic.py` (rewritten) | the per-fun translation of §5: `translate(vocab, ident, tree) -> Rules`, `witness(vocab, gid, tree) -> Rules`, `definition(vocab, term, tree) -> Rules` | ≤ 300 lines; the NP/CN half in `spec_logic_np.py` |
| `scripts/spec_logic_vocab.py` | the lexicon side: fun → entry, the domain facts (`kindname`, `val`, `trans`, `relk`, `initial_value`, resources), the pool sizes | `means_values` goes |
| `grammar/background.lp` (rewritten) | pool, `used`, symmetry, creation, frame axioms, guarded transitions, resources, minimisation | |
| `scripts/spec_engine.py` (new) | the solver: `telingo.imain` through `Proxy`, cores, optimal models, the horizon bound, the cone | ≤ 200 lines |
| `scripts/spec_solve.py` (rewritten) | `model logic`'s checks L1–L4 and their report; `run(root, capability=None, extra=None)` and `report(findings, as_json)` keep their signatures | |
| `grammar/cone.lp` (new) | `edge/2` and `in_cone/2` from the translation's signatures (§5.7) | |
| `scripts/spec_trace.py` (new) | a group's minimal trace read into Steps trees by the atom table (§7.3) | reads atoms, never trees |
| `scripts/features_generate.py` (rewritten) | the feature file: header, scenarios, tags, example-data blocks; it calls `spec_trace` | ≤ 120 lines |

### 6.2 Instances, creation, frame (background.lp)

- `pool(K,1..n)`, where n is the number of noun phrases of kind K in the cone's statements and witness, plus 1. There
  is no fixed cap (check point 10). When a program is UNSAT at imax, the engine solves it once more with each pool at
  n × imax + 1, the most instances a trace of imax states can introduce (each noun phrase at most one new instance
  per state). Only UNSAT under that bound is an L1, so a pool too small is never reported as a conflict. Each
  `o(K,i)` has `kind(o(K,i),K)`. Symmetry: `:- used(o(K,N)), N > 1, not used(o(K,N-1)).`
- At state 0, any value of each attribute, any relation and any primitive condition may be chosen. At a later state,
  only for a thing **first used** at that state (`not 'used(X)`). Otherwise values change only by `set` events.
  Relations, primitive conditions and values persist.
- Events at state 0 other than the witness's trigger cost extra (§7.2), so nothing happens before the When.

### 6.3 The engine: incremental horizon and cores

- `Proxy(ctl, on_ids)` wraps a `clingo.Control` for `telingo.imain`. Its `ground` grounds and then frees every `on/1`
  external (§3 rule 4). Its `solve` adds the `on/1` literals to imain's future assumptions and passes `on_core`. It
  keeps the optimal models (`optimality_proven`) and maps the core's literals to ids. imain runs as telingo ships it,
  with `istop="SAT"`. The copied grounding loop and its MIT notice are deleted.
- **Horizon bound (imax).** The trigger graph is the `edge/2` relation `cone.lp` derives from the translation's
  signatures (§5.7), not a walk over trees. Let D be the longest path in the cone from the witness. Then imax = D + 2. Every obligation of a statement in the cone falls due by state D+1, so a
  horizon beyond that adds only stutter states. UNSAT at imax is therefore UNSAT at every horizon. A cycle in the
  cone makes a finite trace impossible under strong next, and that is a real finding (an L1 whose core is the
  cycle). In that case imax = (statements in the cone) + 2.
- **The cone** of a group is taken over **the whole spec**, every capability and the U's (check point 9), because
  triggers cross capabilities (a `work run` response triggers a work-queue statement). It is the least set that
  holds the group's own statement and is closed under two rules:
  1. a statement whose trigger is reachable by `edge/2` from the witness's trigger or from a statement in the cone;
  2. a statement with no trigger (Ubiq, While, Where, WhereWhile) **all of whose `uses` kinds** are kinds the cone
     already uses (its witness and statements), subkinds included.

  The U's follow the same two rules; they are not in every cone by default. This is sound for UNSAT. A triggered
  statement outside the cone has a trigger that nothing forces, so the solver satisfies it by not triggering it. A
  trigger-less statement that binds a kind no cone statement uses can only be made true by instances the minimal
  trace never creates. Pool sizes follow the cone (§6.2), so they too change only when the cone does.
- **Cores.** On UNSAT at imax, the core over the `on/1` assumptions is minimised as today (one id dropped at a time,
  kept when the rest is SAT). Transition constraints are guarded by `on("T:<attribute>@<kind>")`, so a core can name
  them too.

### 6.4 The checks (`model logic`)

| code | what | how |
|---|---|---|
| L1 (error) | a group cannot happen | its program (cone + U's + witness) is UNSAT at imax. The core names the requirement and U ids: `supervision#g13 (r13) cannot happen: conflicts with supervision#r99` |
| L2 (warning) | two statements say the same thing | equal normalised trees, as today |
| L3 (error) | a `Set` no transition allows | an L1 whose core holds a `T:` guard is reported as L3, naming the statement, the attribute and the value. The tree walk (`_edges`, `l3`) is deleted |
| L4 (warning) | a pre-state value no trace reaches | asked of the solver, once for each (kind, attribute, value) a group's pre-state needs. Those values are read from the solver's own output, not from trees (check point 8): the `lab(gid, cond(i), attr(X,A,V))` and `lab(gid, feat(i), attr(…))` atoms at state 0 of the group's SAT model, with X's kind. For each: state 0 holds an initial value (one that no transition enters, or any value when all are entered), the guarded transition constraints, `:- not &tel{ >? attr(x,A,v) }` at initial, and imax = the number of values. UNSAT means L4. `_reachable` is deleted |

The integrate round's check (`supervise_outputs`, "unparsing") keeps calling `spec_solve.run(root, extra=drafts)`.

**Cost.** Today `model logic supervision` takes 74 s. Each cone is small (the spike's solves took 0.1 s), and a
group's L1 needs only SAT, not optimisation. The budget is under 60 s for the whole spec. It can only be measured on
a merged spec, so the layer 2 gate measures it (check point 20); R4 reports its own time on its base. If it is
exceeded, the engine caches results by the sha of (program text, ids), as `spec_grammar` caches the PGF.

## 7. Gherkin read from the trace (point B)

### 7.1 The scenario solve

For a group G of a service capability that is not logic-only, the program is the background, the facts, G's cone,
the U's, and G's witness: its features, condition and trigger hold at state 0 for the bound instances `bind(var, X)`.
It runs on the same engine with `--opt-mode=optN` and `--project=show`, showing `lab` and the state-0 `attr`, `rel`,
`cond`, `given` and `holds`. telingo stops at the first SAT horizon. If G's program is UNSAT, that is an L1,
and `features generate` refuses G with the L1's text.

### 7.2 Minimal and deterministic

- **Minimal**, by lexicographic priority:
  1. fewest instances used (@3);
  2. fewest events, with an event at state 0 other than the trigger counted twice (@2);
  3. fewest fluents at state 0, then fewest fluents set at creation (@1).
- **Fixed tie-breaks:** every optimal model is enumerated, and the least by its sorted atom strings is taken. Pool
  symmetry is broken (§6.2). More than 10 000 optimal models refuses the group with "the group's trace is not
  determined", which is deterministic too.
- **Fixed instance naming:** each instance is renamed in order of first mention in the output (Givens, When, Thens),
  by its kind's letter and a counter per letter (`LETTERS` as today: i, w, p, q; otherwise the kind's first letter).
  A `Named` code keeps its code. The solver's `o(K,i)` numbers never reach the text.
- **Sorted output:** Givens by label part (`feat(i)` then `cond(i)` in i order, the order the translation numbered
  the clauses), then extra fluents by sorted atom. Then the When. Then the Thens by `resp(i)`, each followed by its
  `mod(i,j)`, then the `not(i)` Thens.
- **Test:** `test_byte_stable` generates every service capability twice, in two processes with different
  `PYTHONHASHSEED`, and once more after adding an unrelated requirement to another capability. It compares bytes.

### 7.3 Reading the trace into steps

`spec_trace.read(model, vocab) -> [(keyword, Steps tree)]` reads atoms only. It takes no requirement tree (check
point 5): the trees reach it only through the translation's labels.

- **The atom table.** Each atom predicate has one Steps fun, the one the Steps grammar already has for that shape:

  | atom | Given | When | Then |
  |---|---|---|---|
  | `attr(X,A,V)` | `<attr>_Given` at X's first mention ("a work-item w1 that is `drafted`"), else `SAtom (<attr>_Is …)` | `STrig (<attr>_Becomes …)` | `SAtom (<attr>_Is …)` (a Set) |
  | `cond(C,X)` / its absence under `~` | `SAtom (<cond>_Is …)` / `_IsNot` | | |
  | `rel(R,X,Y)` | `SAtom (rel_<k1>_<w>_<k2>_Atom …)` | | `SAtom` |
  | `does(S,E,X)`, `ran(S,C,X)` | | `STrig (Happens/Runs/RunsOn …)` | `SDoes`/`SDoesTo`/`SPrints`/`SExitsOk`/`SExitsErr`/`SChangesNothing` by E |
  | `lab(_, not(i), does(…))` | | | `SDoesNot`/`SPrintsNot` |
  | `given(F)`, `holds(X,R)` | `SFeat`, `SAtom (Holds …)` | | `SAtom (Holds …)` |
  | `<kind>_Given` | an instance with no labelled atom at its first mention ("a result r1") | | |

  The table is a mapping from a predicate to a fun, as `features_vocab`'s `THEN` and `TRIG` maps are today. Choosing
  `_Given` at a first mention is linearisation (it depends only on the order of mention), not a rule about meaning.
- **Givens:** the `lab(gid, feat(i), A)` and `lab(gid, cond(i), A)` atoms, then the **extra Givens**: each state-0
  fluent of the model that no `lab(gid, …)` atom names (check point 7). That is a set difference on atoms. Since the
  solve minimises state-0 fluents (§7.2), every fluent left is one some statement in the cone needs. This is the
  person's point 1: "While a work-item is `drafted`" becomes "Given a work-item w1 that is `drafted`" through the
  translation, with no given block.
- **When:** the `lab(gid, trig, A)` atom. A noun phrase the trigger introduces is named in it.
- **Thens:** the `lab(id, resp(i), A)` atoms of the group's statement, each followed by its `lab(id, mod(i,j), A)`
  restriction atoms (the new stage's kind and `for`), then the `not(i)` atoms. A `ShallNot` conjunct is labelled
  `not(i)` directly.
- **Contrast instances** are no longer a Python rule (check point 6). They are part of the witness that the
  translation of `_Every`/`_Pl` with a restriction emits (§5.4): one solve, and the contrast's Then is its `not(i)`
  label. `features_generate.choose` and its "one more solve" are gone.
- **Example data:** a group's given block, when it has one, comes first, as today. Its lines are read by shape (§9.1)
  and parsed by the Steps grammar as `<kind>_HoldsText`/`_HoldsBlock`. The instance it names (a `Named` code) is the
  same constant in the trace. A given line that is not example data is not refused by the generator: it is left out
  of the scenario with a line on stderr, and `model check`'s v15m is the error that names it (check point 4). One
  owner for the rule, and layer 3 can generate the live supervision file, which keeps 65 such blocks until layer 4.

### 7.4 What makes it deterministic, stated once

The program depends only on the group's cone, and the cone depends only on the signatures (§5.7) by the two rules of
§6.3. The solve is exhaustive over optimal models, and the choice among them is a total order on strings. Naming is
by order of mention in a fixed step order. So the same spec gives the same bytes.

What "unrelated" means is stated, not assumed (check point 9): a requirement is outside a group's cone when its
trigger is not reachable from the group and, if it has no trigger, it binds a kind the cone does not use. Such a
requirement changes neither the cone nor the pools, so it changes no byte. A trigger-less statement over kinds the
cone uses does enter it and may change the scenario. That is intended: it constrains every such trace.

`test_byte_stable` therefore adds, to a temp copy of the spec, (a) a `When` statement in `analysis-tools.md` whose
trigger is `the person runs \`tools probe\`` (no response produces it), and (b) a new local kind **widget** in
`trials.md` with "While a widget is `broken`, `tools` shall print the widget." It asserts the supervision and
work-queue features are byte-identical, and a second test asserts that (c) a While over **work-item** does enter
g2's cone. That was the untested worry behind "the solver breaks determinism" in design.md §14.2.

### 7.5 What stays

The feature header, the `@g<n> @r<n>` tags, sorting by group, logic-only groups (`spec_tree.logic_only`), `--check`
and `--preview`, and formulate as a script (`supervise_formulate.py` calls `features_generate`). Handlers stay keyed
by (template, term).

## 8. The lexicon (points D, E, F)

- **What counts as one sentence** (v_t7; check point 13). The gloss is the text after the entry's `:` and before
  its first field (`Values:`, …). Code spans (`` `…` ``) and quoted strings are blanked first, then `e.g.`, `i.e.`,
  `etc.` and `vs.` are blanked. A sentence ends at `.`, `!` or `?` followed by a space or the end, and at `;`. The
  gloss is one sentence when exactly one end is found at its end and none before. A `:` inside the gloss does not end
  a sentence. R2 tests each: a code span holding `.` (`spec/index.md`), `e.g.`, a `:` gloss and a field all pass; two
  sentences and a `;` fail.
- **One sentence for each entry** (v_t7). A kind: "**worker brief** (kind): the brief `work run` gives a worker." What
  a brief, list or log contains or does is not in the term. It becomes requirements of the capability, for example
  "When `work run` starts a stage for a work-item, `work run` shall give the stage a worker brief that names the
  work-item." Supervision's worker brief, tool list, round brief, review brief, output and log entries become such
  requirements in its rewrite package.
- **Fields kept:** `Values:` and `Transitions:` (an attribute), `Forms:` and `Plural:` (where English is irregular),
  `Not:` (avoided words) and `Kind of:` (new; a kind's supertype). These are data, not sentences, and v_t7 counts
  only the gloss.
- **Removed:** `Means:` (v_t9), and relation entries that only name a preposition (v_t8). A relation is a row of
  `## Relations`.
- **Lexicon API** (`spec_lexicon`): `Term` keeps its fields and gains `supertype`, and `means` is kept only until
  R14 deletes it. `Lexicon.relations()` returns the expanded rows `(k1, word, k2, rid)`, the supertype's own row
  included (§4.2). `Lexicon.definition(term)` returns the gloss sentence of a condition, which
  `spec_grammar.parse(root, text, grammar="Def")` parses. New problems: v_t7, v_t8, v_t9 and v_t10 (two rows with
  one (from, word, to)).
- **Modules** (check point 18): `spec_lexicon.py` (192 lines) keeps terms, fields, v_t4–v_t7 and v_t9. The
  `## Relations` table, `Kind of:` expansion, v_t8 and v_t10 go into **`scripts/spec_relations.py`** (new), which
  `spec_lexicon.read` calls. `spec_read.py` (234) gets its given-block reading and the example-data shape test moved
  into **`scripts/spec_read_given.py`** (new). `spec_typed.py` (189) gets the `Def` module in
  **`scripts/spec_typed_def.py`** (new). `features_vocab.py` (299) has its `modules(lex)` (the generated StepsTyped
  grammar text, lines 41–123 with `attributes` and `_relation_text`) moved into **`scripts/features_vocab_gf.py`**
  (new) by R6, before R6 adds anything.

## 9. The spec, rewritten (point G)

### 9.1 The format

```
### [g13] A result with no output makes the work-item await an answer
Restates: r131@0.29, r132@0.29.
- [r13] While a result is outputless, when a session ends a `plan` stage for a work-item with the result, `work run`
  shall set the status of the work-item to `awaiting-answer` and ask a question on the work-item.
```

- **One statement for each group** (v15k + v15l). The statements of a group that share a trigger and condition
  become one statement, with `and` between the VPs, or `, and` between responses whose subjects differ. The
  `Restates:` lines are merged into one, sorted, with no repeats.
- **One statement for each (features, condition, trigger) in a capability** (v15n). Two groups whose statements
  share all three are merged into one group, keeping the clearer title. Across capabilities this is accepted: two
  capabilities may each respond to one trigger, and merging them would cross files that different packages own.
- **Given blocks** remain only for example data (v15m). Example data is known by the line's shape, tested in
  `spec_read_given.py` without any grammar (check point 14): `the <words> <name> holds:` with a docstring or table
  after it, or `the <words> <name> holds` followed by exactly one code span or quoted string. A line such as `a result r1` / `the result r1 is outputless`
  is deleted: the condition is already in the statement. Where deleting one changes the scenario today, the condition
  was missing from the statement, and it is written into the statement (the 169 cases the revision brief measured).
  Where a deletion made `features generate` crash (63 cases), the new generator introduces the instance from the
  While clause.
- **Renumbering.** The codified ids were never released, so each capability is renumbered in file order. With one
  statement for each group, **g<n> and r<n> share n**. `retired: []` stays empty, because nothing released is
  retired. `restates` must still cover every 0.29 id: `model restates` reports 0 missing for each capability, and
  dropped ids keep their `## Dropped` entry.
- **References** (check point 19). No open work item references a codified id (q47's lines name none, and i67 exists
  only on the scratch branch). The search is every tracked file, not only `.shop/work/`:
  `git grep -nE '\b<cap>#[rg][0-9]+\b' -- ':!spec/capabilities' ':!features' ':!.shop/records'`. At 5d6cd4c8 it
  finds, outside `.shop/work/` (whose hits are 0.29 ids, already in `baseline-model-check.txt`):
  - `spec/restated.json`, `docs/design-model/design-model.md`, `tests/scripts/test_spec_read.py`: 0.29 ids, which
    renumbering does not touch;
  - `tests/scripts/test_spec_solve.py`: ids of the frozen fixture `tests/scripts/fixtures/logic/cluster/`, not of the
    live spec;
  - `tests/scenarios/supervision_build.py:59` (`work-queue#r1`), `tests/scripts/test_e2e_codified.py`,
    `test_supervise_formulate.py`, `test_supervise_outputs.py`, `test_migrate_upgrade_codified.py`: ids inside
    specs each test writes itself, not the live spec. `work-queue#r1` exists in any renumbered capability. R8 owns
    `supervision_build.py` and its scenarios prove it;
  - `spec/decisions/0072-work-list-and-work-show-replace-work-status.md`: `work-queue#r34–r39`, dated 2026-10-27,
    before the conversion, so they are 0.29 ids. Today `work-queue#r34` resolves by accident to the codified r34.
    **R12 owns this file** and writes its six sources with `@0.29`.

  Each layer-4 package writes `ids-<cap>.tsv` (old codified id, new id) beside its report. The layer 4 gate reruns
  the grep and checks that every hit is one listed above or mapped through those files.

### 9.2 The procedure for each capability (one rewrite package does this for each of its capabilities)

1. Rewrite `## Terms`: one sentence each; conditions as `Def` sentences or primitive glosses; content kinds moved
   into requirements; local relation rows in the capability's `## Relations`.
2. Rewrite `## Behaviour`: merge groups that share a trigger and condition (§9.1). Move a given-block condition into
   the statement. Delete non-example given blocks. Renumber.
3. Make each line parse with exactly one tree (`model parse --file`), and add one corpus line for each new construct
   to `grammar/corpus/<cap>.txt`.
4. `model logic <cap>` reports no L1 or L3. Each L4 is either fixed or listed in the package report.
5. `features generate <cap>` (service capabilities), then make the scenarios pass by updating
   `tests/scenarios/<cap>_*handlers*.py` and the capability's world modules. Handler keys are (template, term), so most
   handlers stay.
6. `model restates <cap>`: 0 missing. `model check`: no v15k, v15l, v15m, v15n, v_t7, v_t8, v_t9 or v_t10 rows for
   the capability. `ids-<cap>.tsv` written (§9.1).

`spec/universal.md` is rewritten by the guarantees package. U3 and U4 use VP coordination, and U7 may use `or` now
(worktree or stage directory).

## 10. Code deleted, rewritten, kept

| file | what happens |
|---|---|
| `scripts/spec_solve.py` | `_ground` (the copied imain and its MIT notice), `HORIZON`, `_edges`, `l3`, `_reachable`, `l4`'s graph search: deleted. L1–L4 on the engine (§6.4) |
| `scripts/spec_logic.py` | rewritten as §5: the `Sentence` class with its `'` (previous) translation, `_prime`, `witness`'s `wit(0)`/`wit(1)`, and `ACTIONS` for RefuseErr/CommitPush are deleted |
| `scripts/spec_logic_vocab.py` | `means_values`, `Vocab._means` and `cond_attr` deleted; facts rewritten for the relations table and the pool |
| `grammar/background.lp` | rewritten (§6.2); the stutter-step comment and `start_event`/`end_event` kept for resources |
| `scripts/features_generate.py` | `Inst`, `Scenario` (`given_block`'s non-example lines, `constraints`, `condition` (the reader of `Means:` English), `choose`, `resolve`, `subst`, `precondition`, `becomes`, `then`, `lines`): deleted, about 230 lines. What is left writes the file |
| `scripts/features_vocab.py` | `modules(lex)` moved to `features_vocab_gf.py` (new); given-block templates narrowed to `_HoldsText`/`_HoldsBlock`; `_relation_text` replaced by the relations table. `SCommits` deleted by R14 only |
| `scripts/spec_lexicon.py`, `scripts/spec_relations.py` (new) | the `Means` field (after R14), preposition relation entries; adds the relations table and `Kind of:` (in `spec_relations`), the definition sentence and v_t7–v_t10 |
| `scripts/spec_typed.py`, `scripts/spec_typed_def.py` (new) | `_relation` from rows (modifier and atom funs, supertype rows included); the generated `Def`/`DefEng` module |
| `scripts/spec_read.py`, `scripts/spec_read_given.py` (new) | given blocks moved out; the example-data shape test (v15m's facts) |
| `scripts/model_spec.py`, `scripts/model.lp` | facts and rules for v15l, v15m, v15n, v_t7–v_t10 |
| `grammar/Req.gf`, `ReqEng.gf` | VPs/VPor/Resps/CondOr added; RefuseErr, CommitPush deleted. `Def` is a generated module (§4.3); relation atoms are generated typed funs. `Steps.gf`/`StepsEng.gf`: `SCommits` deleted by R14 |
| `tests/scripts/test_spec_logic.py`, `test_spec_solve.py`, `test_features_generate.py` | rewritten to the new behaviour, test first |
| `docs/design-model/grammar.md`, `docs/capability-format.md`, `agents/capability-writer.md`, `agents/spec-checker.md`, `skills/formulating-features/SKILL.md`, `skills/checking-spec-consistency/SKILL.md` | the format: one sentence for each term, relations table, definitions, `and`, given blocks only for example data |

## 11. Calls made under the delegation

1. **Keep groups and requirement ids both**, with one statement per group and the same number. Groups carry the
   title, `Restates:` and example data, and `accepts` names requirements. Collapsing the two would touch `work`,
   `model` and the queue for no gain the person asked for.
2. **A conjunct is its own constraint under one guard.** This is equivalent to `~ > (A & B)`, it gives one Then for
   each conjunct, and the core still names one id.
3. **The cone, not the whole program, for each solve.** The cone is drawn over the whole spec by the two rules of
   §6.3. It is sound for UNSAT, fast, and makes stability under additions outside the cone true by construction,
   with "outside" defined (§7.4). `model logic` with no capability still checks every group, so every
   statement is in some cone.
4. **Primitive conditions are allowed.** Point E asks for no prose `Means:`, not for every file-shape test to be
   expressible in the language. A primitive condition is one sentence with no logic, built by a step definition.
5. **L3 is folded into the solve** through guarded transition constraints, and reported under its own code. L4 is
   asked of the solver once for each (kind, attribute, value).
6. **Relations live in a table in `spec/index.md`**, and a capability may add local rows in its own `## Relations`.
   Rewrite packages in one layer then never share `spec/index.md`.

## 12. Risks

- **Solve cost on supervision's cones.** Mitigations: the cone, SAT-only for L1, a cache keyed by sha. R4 measures
  the cost, and so does the R14 gate.
- **Ambiguity from `and`/`or` and typed PP attachment.** The corpus and the one-tree guard catch it at parse time,
  and the rewrite rewords.
- **Handlers whose text changes.** Givens now come from the statement rather than from a block, but they are the
  same step funs as the block lines (`<attr>_Given`, `<cond>_Is`), so most handlers stay. Rewrite packages own their
  handler modules.
- **Optimal-model counts.** The spike saw up to 42. The 10 000 cap refuses rather than guesses.

## 13. Calls made in the check

The builder check of this design and plan (`builder-check-r2.md`, beside this file, not committed) raised 23 points.
Each was settled under the delegation. The section named is where the design now says it, and the plan's packages
carry it.

| # | point | the call | where |
|---|---|---|---|
| 1 | R1 deletes `CommitPush`, but the scenario suite and `features_vocab` still use `SCommits` | `RefuseErr`/`CommitPush` leave Req in R1, since keeping them beside `AndVP` gives two trees. `SCommits` stays in the Steps grammar, `features_vocab` and the handlers until R14 deletes it in layer 5, after layer 4 regenerated the features. The orchestrator moves **push** (event) to `spec/index.md` before layer 1. In layer 4, `grammar/*.gf` and `scripts/` are frozen: a line that needs a new fun is reworded, or is handed back for R14 | §4.1, §4.4; plan R1, R14, layer 0 |
| 2 | `Def` would load a `DefEng.gf` that does not exist | A generated module pair `Def.gf`/`DefEng.gf` (`abstract Def = Req ** …`), written by `spec_typed_def.py`. `spec_grammar.load` needs no start-category argument. `model parse --grammar` takes `Req`, `Steps` or `Def` | §4.3 |
| 3 | `Prep` and `SRelAtom` are unused | Both dropped | §4.2, §4.4 |
| 4 | R6 refuses non-example given lines, yet must generate the live supervision file | The generator never refuses them. It leaves them out with a line on stderr. v15m in `model check` is the only error. Layer 3 tolerates them, and layer 4 deletes them | §7.3; plan R6 |
| 5 | The wording came from the trees, with Python choosing templates | The trace reader takes no trees. It reads `lab/3` atoms and state-0 fluents, and maps each atom predicate to its one Steps fun by a fixed table, the way `features_vocab`'s `THEN`/`TRIG` maps do today | §3 rule 5, §5.7, §7.3 |
| 6 | Contrast instances were a Python rule | They are part of the witness the translation of `_Every`/`_Pl` with a restriction emits, with a `not(i)` label. One solve; `choose` is gone | §5.4, §7.3 |
| 7 | Extra Givens needed atoms matched back to clauses | The translation emits `lab(Id, Part, Atom)` for each clause and conjunct. Extra Givens are the state-0 fluents no `lab(gid, …)` names: a set difference on atoms | §5.7, §7.3 |
| 8 | The cone, the horizon edges and L4's needed values came from tree walks | The translation emits signature facts (`trig`, `eff`, `uses`, `untriggered`). `grammar/cone.lp` derives `edge/2` and `in_cone/2`, and the horizon is the longest path over `edge/2`. L4's values are the labelled state-0 `attr` atoms of each group's SAT model | §5.7, §6.3, §6.4 |
| 9 | Cone scope; trigger-less statements in every cone undo byte-stability | The whole spec, closed under reachability and, for trigger-less statements and U's, under "every kind it binds is already used by the cone". "Unrelated" is defined, and `test_byte_stable` adds one requirement of each unrelated kind plus a test that a related While does enter | §6.3, §7.4 |
| 10 | A pool cap of 3 gives false conflicts | No cap. On UNSAT the engine re-solves with each pool at n × imax + 1, a sound bound. Only UNSAT under it is an L1 | §6.2 |
| 11 | `it` in a definition has several trees | A definition names its subject "the <kind>". `parse(grammar="Def")` refuses any `_It`. Coordination across kinds is two clauses. Three corpus lines are given with their expected trees | §4.3 |
| 12 | `Kind of:`: does the supertype row get its own fun? | Yes. There is no second tree, because the grammar has no subkind-to-supertype coercion. Both cases are corpus lines. supervision.md's local `for` entries are deleted by R5 and v_t10 guards it | §4.2 |
| 13 | v_t7 has no counting rule | A rule is given (blank code spans, quotes and the abbreviations; `.!?` before a space or the end, and `;`, end a sentence; `:` does not), with R2's tests | §8 |
| 14 | v15m by Steps parsing pulls the Steps grammar into `model check` | A shape test in `spec_read_given.py`, with no grammar | §2, §9.1 |
| 15 | Point 2 measured only inside a group | v15n: two groups of one capability with equal (features, condition, trigger) is an error, and they are merged. Across capabilities it is accepted (ownership, and different subjects) | §2, §9.1 |
| 16 | Relations rows still list each meaning of "on"/"for" | Rows are kept. They carry no prose (a row is three or four cells, no gloss column), and they are the domain model's relation table, which both typed PP attachment and the logic's `rel/3` need. Letting any preposition join any two kinds would make every PP attachment ambiguous. With `Kind of:`, supervision's six `for` entries become one row. The substance is **reported to the person**: R5 counts preposition entries before and rows after, and the words with more than one row, and R14 puts these and this reasoning in `gate-r2-done.md` as an open point for the person | §4.2; plan R5, R14 |
| 17 | q47 line 4 becomes ambiguous with an (initiative, with, result) row | A guarded corpus line, with a test that the stub row makes it refused | §4.2; plan R1 |
| 18 | No split modules named | `spec_relations.py`, `spec_read_given.py`, `spec_typed_def.py` and `features_vocab_gf.py` (new) | §8, §10 |
| 19 | Renumbered ids cross packages, and 0072 has no owner | The search is every tracked file. Each hit is classified (§9.1). R12 owns 0072 and writes its sources as `@0.29` ids. Each layer-4 package writes `ids-<cap>.tsv`, and the layer 4 gate rechecks the grep | §9.1; plan R8, R12, layer 4 gate |
| 20 | R4's 60 s limit is on a spec R4 cannot see | The layer 2 gate measures it. R4 reports its own time on its base | §6.4; plan R4, L2 gate |
| 21 | 0.29 had no `model logic` | The baseline is `model logic --json` at 5d6cd4c8 (code as 7e0684d2), recorded by the orchestrator before layer 1 as `logic-baseline-r2.json` | plan layer 0, R4 |
| 22 | Positive greps pass on a comment | Named tests replace them (`test_statement_is_a_tel_constraint`, `test_stops_at_horizon_1`, `test_chained_stops_at_horizon_2`, `test_seeded_conflict`, `test_engine_uses_imain`). Negative greps stay, since a comment can only make them stricter | §2; plan R3, R4, R14 |
| 23 | R5's "every line that parsed before" is not encoded | The orchestrator saves the unparsed Behaviour and U lines at layer 0 and after the layer 1 gate (`unparsed-L0.txt`, `unparsed-L1.txt`), with the plan's `unparsed.sh`. Each later accept compares its own run with `comm -13` | plan layer 0, L1 gate, R5, layer 4 |
