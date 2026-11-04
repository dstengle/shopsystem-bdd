---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-gf-conversion-design-r3
kind: design
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-04
status: draft
---

# The GF conversion, revision 3: logic and generation without the big solve

## 1. Why, in one paragraph

Revision 2 put the meaning of a requirement into one place: a `&tel` translation per grammar fun. That idea stays.
But every check and every scenario solved a whole-system model:
- a cone of about 120 statements per group;
- pools of n+1 instances for each of 31 kinds;
- free initial states and free events;
- telingo's horizon run from 0 upwards;
- on UNSAT, a retry with pools of 11.

That made `model logic supervision` take 227 s, the suite 5 minutes, and single runs 20 minutes and 1.5 GB.
`solver-research.md` (this directory) found the cause and showed the fix on a working example:
- the questions are small: two requirements, one trigger, two states, one instance per noun phrase;
- a conflict is a satisfying witness, found in one solve over every candidate pair (4 ms, 276 rules);
- a scenario is a reading of the requirement itself and needs no solver.

This revision rebuilds `model logic` and `features generate` on that. Their meaning does not change:
- the same EARS reading;
- the same checks;
- the same Steps wording;
- the same commands and reports.

## 2. Goals, non-goals, anti-goals

**Goals**
1. **One translation, read twice.** Each grammar fun has one translation into *facts* about the requirement. The
   conflict check and the Gherkin generator both read those facts. Nothing else reads a tree's meaning.
2. **Conflicts found as witnesses.** `model logic` finds two requirements that can fire on one trigger in one
   consistent pre-state and demand opposite things. It reports both ids and the unification that shows it.
3. **Lifecycle and reachability as graph checks** on the transition table.
4. **Gherkin from the facts:**
   - While/Where clauses and noun-phrase restrictions become Givens;
   - the trigger becomes the When;
   - the responses become the Thens, worded by the Steps grammar;
   - no solver; byte-stable by construction.
5. **Exceptions read right.** The live spec writes an exception as a negated existential in the condition. One
   example is supervision r27: "…`awaiting-answer` and no delegation is `written`…". The check must read "no K is v"
   as "no thing of kind K is v", so that r27 does not falsely clash with the delegation lines (§3.3).
6. **Speed.**
   - `model logic` on the whole live spec: under 2 s;
   - `features generate --check` on the whole live spec: under 5 s;
   - no test over 10 s;
   - the solver-driven part of the suite under 15 test-seconds.

**Non-goals**
- Chains: a response that triggers another requirement whose response then clashes with a third. Hanfor checks
  pairs and scales; FRET splits into components. The facts allow a depth-2 composition later (§8).
- Realizability (an environment that forces a violation) and timing ("within n steps").
- Rewording the Steps grammar or the handlers' (template, term) keys.

**Anti-goals** (a failure even if it works)
- **Any solve whose size grows with the whole spec times a pool.** No cones, no pools of more than one instance per
  noun phrase, no retries that enlarge anything.
- **A conflict reported against a group because of a fault elsewhere.** The trials r3/r6 trap blamed every group.
  Every finding names exactly the ids whose facts produce it.
- **Scenarios that change when an unrelated requirement is added.** A scenario reads only its own requirement.

## 3. The facts (one translation per fun)

`scripts/spec_facts.py` replaces the `&tel` renderer of `spec_logic.py`/`spec_logic_np.py`. `translate(vocab, ident,
tree) -> [fact]` walks the tree once, fun by fun, as today, and emits ground facts. The variables are the
requirement's own noun phrases (one generic instance each), named `v1, v2, …` in order of mention.

| fact | from | meaning |
|---|---|---|
| `role(R,V,K)` | every NP | V is a thing of kind K (a `Named` code is its own constant, `named(R,V,C)`) |
| `cond(R,V,A,Val,Pol)` | While, `<attr>_Is/_IsNot`, an NP's `_Pre`/`_ThatIs`/`_Whose` modifiers | the pre-state: V's attribute A is (Pol=pos) or is not (neg) Val |
| `ccond(R,V,C,Pol)` | `<cond>_Is/_IsNot`, `<cond>_Pre` | a defined condition holds or not (opaque unless its definition parses, §3.2) |
| `crel(R,Rel,V,W,Pol)` | `rel_…_Atom`, a relation modifier | the pre-state relation |
| `feat(R,F)` | Where `FeatGiven c` | a feature given (`--json`) |
| `holds(R,V,Res)`, `free(R,Res)` | Holds, HoldsA, IsFree | resources in the pre-state |
| `trig(R,P,E,D,V)` | the trigger | the event: P ∈ {does, ran, done_to, becomes}, its event or command E, doer D (actor or role var, `any` for Undergoes/IsRun), object V (or `none`) |
| `resp(R,I,Pol,E,D,V)` | each response conjunct I | D does (pos) or does not (neg) E on V at the next state; Print, ExitOk, ExitErr, ChangeNothing, Hold are events E = print, exit_ok, exit_error, change_nothing, hold(Res) |
| `oattr(R,V,A,Val)`, `orel(R,Rel,V,W)` | the restrictions of a response's object | the new stage's kind, its `for` |
| `set(R,I,V,A,Val)` | `<attr>_Set` | V's attribute A becomes Val at the next state |
| `every(R,V)` | `_Every`, `_Pl` | V is universal (its scenario gets a contrast, §5) |
| `none(R,K,A,Val)`, `cnone(R,K,C)` | `<k>_No` in a condition ("no delegation is `written`") | no thing of kind K is Val / satisfies C in the pre-state (§3.3) |
| `count(R,Res,N)` | HoldAtMost | at most N holders at a time |
| `uses(R,D,X)` | Ubiq "D shall use X" | a static fact about a role, **not** an event at every state (§3.1) |
| `form(R,F)` | the EARS form | ubiq, when, while, where, if, while_when, … |
| `disj(R,K)` | CondOr | a disjunctive condition: the requirement is emitted once per disjunct as `R#1`, `R#2`, …, reported under R |

The lexicon's side gives `kind/1`, `sub(K,K2)`, `val(K,A,V)`, `trans(K,A,From,To)`, `initial(K,A,V)` and `actor/1`,
as `spec_logic_vocab.py` does now. The pool-size code goes.

### 3.1 Two readings that change
- **"X shall use Y"** (6 lines in today's spec; 18 in the R4 numbering the research measured) was an event forced at every state. It
  becomes `uses/3`: static, cannot conflict with an event, can conflict only with "X shall not use Y".
- **An untriggered positive event obligation** ("While C, X shall do E", with E an event, not a state) is legal but
  gets warning L5 (§6). Under strong next it is the G p ∧ G(p → X q) trap whenever a triggered statement reacts to E.

### 3.2 Defined conditions
A condition whose definition parses as `Def` (13 today) is expanded into its literals inside `cond`/`crel`. Any other
defined condition is opaque: two requirements disagree on it only when one says it holds and the other says it does
not. That is sound for clashes (no false hits) and incomplete (it can miss a clash hidden in a prose definition). The
115 prose definitions are the open item they already are; each one converted to `Def` makes the check sharper with no
code change.

### 3.3 "no K is v" in a condition
`none(R,K,A,Val)` is universal over the merged pre-state. It is not a negated literal on one generic instance. After
unification, the pre-state is inconsistent if any role of kind K (or a sub-kind), A's or B's, has `cond(…,A,Val,pos)`.

Take supervision r27 ("…no delegation is `written`…") against a delegation line ("…a delegation is `written`…"). The
two cannot both fire, so they are not reported. A negated literal on a fresh instance would let the unification keep
the two delegations apart and report a false L1.

In Gherkin, a `none` condition gives no Given: the world has no such thing by default. Revision 2's trace reading did
the same.

## 4. Not in this revision: "unless"

The research proposed an "unless" form for rule-plus-exception pairs. Layer 4 rewrote the spec, and the live spec now
writes its exceptions inline as conditions (§3.3), so no live line needs the form. If one ever does, it would be:

```
Unless : Req -> Cond -> Req ;   -- <statement>, unless <condition>.
```

Example: "While a work-item is `awaiting-answer`, when the person runs `work run` on an initiative, `work run` shall
not start a stage for the work-item, unless a delegation is `written` and an answer is `--change`."

- **Meaning:** the statement applies only when the condition does not hold. The facts are the statement's own, plus
  `unless/…` for each literal.
- **Check:** a pair (A, B) is not reported when, under the clash's unification, B's pre-state entails all of A's
  `unless` literals (or the other way round). That is exactly the exception.
- **Gherkin:** A's scenario is unchanged. The exception is B's own scenario, so the unless clause adds no step.
- It would be added when two capabilities need it (the core-fun rule of design §9.5). Not now.

## 5. Gherkin from the facts

`scripts/spec_steps.py` (from `spec_trace_steps.py`, which keeps its atom table and naming) reads one requirement's
facts into `[(keyword, Steps tree)]`. `features_generate.py` linearises them through StepsEng, as now.

1. **Names:** each role variable gets its kind's letter and a counter, in order of first mention in the steps below
   (`LETTERS` as today). A `Named` code keeps its code.
2. **Givens, in this order:**
   1. `feat` facts;
   2. `cond`/`ccond`/`crel`/`holds`/`free` facts, in the order the translation numbered the clauses;
   3. each role first mentioned here, introduced with `<attr>_Given` or `<kind>_Given`.

   This is the person's point 1 ("While a work-item is drafted" → "Given a work-item w1 that is `drafted`").
3. **When:** the `trig` fact. A role first mentioned here is introduced in the When, as today.
4. **Thens:** the `resp` facts by I. Each is followed by its `oattr`/`orel` restrictions, then the `set` facts.
5. **Contrast:** for an `every` role with a restriction, one more instance of that kind that fails the restriction
   (the first value of the attribute other than the restricted one, in `val` order) is introduced as a Given. A
   `DoesNot` Then follows for it. This is a fixed rule per fun, not a solve.
6. **Example data** (given blocks) comes first, as today. Non-example given lines are left out with a line on stderr
   (v15m owns the error).
7. **Not generated:**
   - the pre-state facts that *other* requirements would need;
   - the trace's "extra Givens" of revision 2.

   A scenario states its own requirement. The world the handlers build supplies defaults: a work-item with no
   blocker, a free lock. Interactions between requirements are the checker's job, not the scenario's.

Determinism: the output is a pure function of the requirement's facts and the Steps grammar. `test_byte_stable` runs
generation twice, under two `PYTHONHASHSEED`s, on the live spec, and compares bytes (seconds, not minutes).

## 6. The checks (`model logic`)

`grammar/check.lp` is a fixed meta-encoding over the facts, built from the research example's `check.lp` and grown
to the full fact set. It runs in one `clingo` solve over the whole context:
- brave enumeration (`--enum-mode=brave`);
- the shown atoms are the findings;
- a 20 s limit, after which the findings so far are reported as partial (exit 1, "the check did not finish").

**Two states.** State 0 is the pre-state (the requirement's conditions). The trigger happens at state 0. State 1 is
state 0 with the responses' `set`s applied, and the responses happen there.

**Candidate pairs** come from a shared-vocabulary index, never the whole cross product:
- two triggered requirements whose `trig` facts have the same P and E, a compatible doer, and object kinds that are
  equal or a sub-kind;
- a triggered requirement and an untriggered one (While/Where/Ubiq) that binds a kind the triggered one binds;
- a requirement and a U whose facts share an event or an attribute.

**Unification:** a choice maps each role of B to a role of A of a compatible kind, or keeps it apart (the example's
`map/4`). The triggers must unify, and the merged pre-state must be consistent:
- no attribute with two values;
- no literal both pos and neg;
- B's unless not entailed (§4).

| code | severity | finding |
|---|---|---|
| L1 | error | `clash(A,B,Why)`: under one unification, A and B fire together and demand opposite things. The Why is one of: pos/neg of one event on one object, two `set`s of one attribute to different values, exit_ok with exit_error, change_nothing with any changing response, or "use" with "shall not use". Also `clash(A,A,self)`: a requirement whose own pre-state is inconsistent. The text names both ids and the merged pre-state: `supervision#r52 and #r72 clash: on "the person runs work run" with a work-item awaiting-answer, r52 forbids and r72 starts a stage for it` |
| L2 | warning | equal normalised trees (unchanged, no solver) |
| L3 | error | `bad_set(R,A,From,To)`: a set whose implied pre-value has no `trans` to the new value (graph rule in check.lp) |
| L4 | warning | `unreachable(K,A,V)`: a value some requirement's pre-state needs that no `trans` path reaches from an `initial` value (graph rule in check.lp) |
| L5 | warning | an untriggered positive event obligation (§3.1), naming any triggered requirement that reacts to its event |

The interface stays the same:
- `spec_solve.run(root, capability=None, extra=None)` and `report(findings, as_json)`;
- `supervise_outputs`' check of an integrate round's drafts;
- `model logic`'s exit codes (1 on L1/L3).

`capability=` filters the findings to those naming that capability. The solve is always the whole context, because
it is milliseconds.

## 7. Modules: deleted, rewritten, kept

| module | fate |
|---|---|
| `scripts/spec_engine.py`, `grammar/cone.lp`, `grammar/background.lp`, `scripts/spec_trace.py` | deleted |
| `scripts/spec_logic.py`, `scripts/spec_logic_np.py` | replaced by `scripts/spec_facts.py` (+ `spec_facts_np.py` if it passes 300 lines) |
| `scripts/spec_logic_vocab.py` | kept, less the pool sizes; the domain facts gain `initial/3` |
| `scripts/spec_solve.py` | rewritten: facts → `check.lp` → findings → report; ≤ 200 lines |
| `grammar/check.lp` | new |
| `scripts/spec_trace_steps.py` → `scripts/spec_steps.py` | kept: atom table and naming, fed facts instead of a model |
| `scripts/features_generate.py` | rewritten around `spec_steps`, no `Context` solve |
| `grammar/Req.gf`, `ReqEng.gf` | unchanged |
| CLAUDE.md module map | rows updated in the same change |
| `tools install`/`probe` | clingo kept; telingo dropped from the pins if nothing imports it (§9 Q1) |

**Tests.**
- **Deleted:** `test_spec_engine.py` and `test_spec_trace.py`.
- **Rewritten on small fixtures:** `test_spec_logic.py` becomes `test_spec_facts.py` (each fun's facts), and
  `test_spec_solve.py` runs the cluster fixture plus seeded pairs, one per clash kind, and L3/L4/L5.
- **One run over the live spec:** `test_spec_guarantees.py`, `test_revision_done.py` and `test_features_generate.py`
  share one session-scoped `model logic` run of the live spec, instead of one per capability.
- **Ceiling:** no test may take more than 10 s. A `conftest` check reports any test over it.

## 8. Later, not now
- **Depth-2 chains:** A's response is B's trigger, and B's response clashes with an untriggered C at state 2. The
  facts already carry the edges; it is one more rule set in `check.lp` with an explicit horizon of 3.
- **Prose definitions converted to `Def`** (115): sharper L1, no code.
- **"within n steps" timing,** if the grammar ever gets it.

## 9. Calls made under the delegation (the person may overturn any)

1. **clingo, not telingo, runs the check.** The two-state reading of EARS is fixed in `check.lp`:
   - "When T, R" is G(T → X R);
   - "While C, R" is G(C → R).

   Unrolling those two temporal patterns once is all a pair check needs, and it is what made the example 4 ms.
   telingo's per-requirement `&tel` formulas over an incremental horizon are what blew up. The temporal reading is
   still the semantics. It is just not handed to a general LTLf engine.
2. **Gherkin reads only its own requirement.** The revision-2 "extra Givens" go.
3. **One generic instance per noun phrase** is the cutoff, from the small-scope and cutoff results the research cites.
4. **No "unless" form.** Exceptions stay conditions; "no K is v" is read universally (§3.3).
5. **Opaque prose conditions:** sound for clashes, incomplete for them.
6. **What the build does with clashes the new check finds in the live spec.**
   - The build may edit the requirement to clear the clash when one reading is plainly the intent: a dropped
     condition, or an exception that is missing.
   - The codified spec has not been released, so the edit keeps its id, as revision 2 did. The retire-and-renumber
     rule starts at release.
   - Each edit is one commit and one line in the build's report.
   - A clash whose fix needs a product decision (which requirement wins) is not guessed. It is listed as a question
     for the person, and the live-spec "no conflict" test names it as an expected finding until it is answered.

## 10. Risks
- **Handler fallout.** Scenarios lose the extra Givens of revision 2 and gain contrasts by rule. Some handlers or
  world builders will need defaults. The build regenerates every feature and runs the scenarios. A fix goes in the
  world, never as a Given the requirement does not state.
- **Live clashes will surface.** The research's r2/r53 and r52/r72 used the R4 numbering. Layer 4 has since fixed
  both: r2 says "not waiting", r38 is the blocked rule, and r27 carries the delegation exception. How many the new
  check finds on today's spec is unknown until it runs. They are handled by §9 call 6.
- **Brave enumeration size.** The pair index keeps it small. The 20 s limit makes a blowup visible, not silent.
