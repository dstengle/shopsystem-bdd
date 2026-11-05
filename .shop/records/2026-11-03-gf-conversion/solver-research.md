I couldn't write REPORT.md: the harness refused the Write ("subagents should return findings as text"). The report is below, after a short summary. The scripts, extracted programs and the working example are in `/tmp/claude-1000/-home-vscode-shopsystem-bdd/248cf039-6f1c-44df-97a2-339ab46c8793/scratchpad/solver-research/`.

## Summary

1. **Both goals are small problems.** Conflict finding asks: is there one state and trigger where two requirements both fire and clash? That needs two states and one generic instance per noun phrase (a cutoff). Lifecycle and reachability are graph questions. Gherkin is a direct reading of the parse tree and needs no solver.
2. **We feed the solver a whole-system model instead.**
   - Per group, a "cone" of 122–131 statements over 12 capabilities, for a group of 1–2 statements.
   - Pools of n+1 instances for each of 31 kinds.
   - Free choice of every initial attribute, relation and condition, and free events at every step.
   - telingo's horizon run from 0 upwards, so every short horizon is a full UNSAT proof.
   - On UNSAT, a re-solve with pools at n×imax+1 (= 11).
3. **The pool retry is the main cause** (`spec_engine.py:102`, used at `spec_solve.py:157,160`). The real g50 conflict, r72 against r52 alone:

   | pool | rules | time | memory |
   |---|---|---|---|
   | 1 | 4.3 k | 0.10 s | 19 MB |
   | 2 | 8.6 k | 0.16 s | 20 MB |
   | 6 | 206 k | 3.5 s | 68 MB |
   | 11 (the retry) | 3.2 M | 54 s | 829 MB |

   The core is the same at every size, found with 0 solver conflicts. On the 122-statement cone the same retry is the observed 20+ min and 1.5 GB.
4. **Why pools hurt so much:** each `&tel` constraint with k noun phrases is grounded over the pool cross product, P^k per step (`spec_logic.py:182`); r72 has k=4. On g50's cone at H=2, a 2.5× larger pool gives 18× more rules (43 k at pool 2, 748 k at pool 6). Horizon 0→5 takes the cone from 12 k to 100 k rules. The number of requirements grows it only roughly linearly.
5. **The cones are not small.** `cone.lp:109-112` admits any untriggered statement whose kinds are covered; a statement that uses no kind is covered vacuously.
   - 23 statements are in all 424 cones, including trials r3 (its "only a measurement" variable has no kind, `spec_logic_np.py:247`), 17 role-boundaries statements and U1.
6. **Why trials r3/r6 was the core of every batch-measurement group:** two faults combined, neither about batch-measurement.
   - r3 was in every cone (point 5). At the time an effect did not name its doer, so every batch-measurement "writes a measurement" pulled r6 into the cone; R4 later fixed this.
   - Read as "at every state", r3 obliged a write at every state. I infer "only" was lost; that version can't be recovered. With r6's "when it writes, next name it", that is G write ∧ G(write → X name), which no finite trace satisfies. `example/ltlf_trap.lp` reproduces it through the plugin's own engine: UNSAT at every horizon, core [r3, r6].
   - Because L1 asks whether the whole cone can happen, a fault present in every cone is blamed on every group.
7. **Earlier attempts made the same mistake at larger scale.** The first build solved the whole spec (about 640 statements) once per group at horizon 3, which is the 5.6 minutes. The cs-spike put many groups' witnesses into one program: 20 groups took 7–11 s, all groups ran long.
8. **Tools that scale don't do this.** NASA FRET checks connected components over shared variables (one case went from 1525 s to under 7 s). Hanfor checks every pair of requirements, plus the invariants, with 300 s each. EARS formalisations, SpeAR and ARSENAL all model signals as variables, never instance pools. Small-scope and cutoff results support one instance per role.
9. **Recommended approach, with a working example** in `example/`. Requirements become facts, checked by one fixed meta-encoding, on pairs that share a trigger. A conflict is a satisfiable witness, not an UNSAT proof.
   - Seven requirements: r2, r3, r52, r53, r72, r16, plus seeded r99 and r98.
   - Found: `clash(r2,r53)`, `clash(r52,r72)`, `clash(r16,r99,set)` and `bad_set(r98, drafted→done)`. No false hits.
   - 4 ms, 276 ground rules.
   - Gherkin is printed from the same facts with no solver (`example/gherkin.py`).
10. **Changes, ordered by value:**
    1. Delete the pool retry.
    2. Use one instance per noun phrase.
    3. Check pairs (or small sets) from a shared-vocabulary index instead of cones.
    4. Make L1 a search for a clash instead of "the group cannot happen".
    5. Stop reading "X shall use Y" as an event at every state (18 statements are read that way now), and lint for the G p ∧ G(p → X q) trap.
    6. Make L3 and L4 graph checks again.
    7. Leave labels and optimisation out of the check.
    8. Generate Gherkin from the tree.
    9. Add an "unless"/priority construct to the grammar: r52/r72 is a real logical conflict only because r72 is meant as an exception.

---

# Report

The code read:
- **R4:** `.claude/worktrees/wf_a8bccdd0-2c9-8` (gfr/R4, 8b222524).
- **Latest engine:** `wf_a8bccdd0-2c9-21` (d388ca5f). Its `spec_engine.py` is identical to R4's; its `spec_solve.py` differs only in the core's horizon. Line numbers below refer to it.
- **First build:** `wf_bbfe2b24-5b0-7` (P6).

Every solver call had a 60 s limit. No whole-spec or whole-capability solve was run; for cones I only grounded, with a conflict limit of 1.

## 1. The goals, stated precisely

**Conflict finding** covers four checks:
- **(a)** Under one trigger and a consistent pre-state, A obliges what B forbids, or A and B set one attribute of one thing to different values.
- **(b)** A set that no lifecycle transition allows from the value the condition implies.
- **(c)** A pre-state value no transition path reaches.
- **(d)** A requirement that breaks one of U1–U10.

Formally:
- (a) and (d) are satisfiability questions over pairs or small sets of requirements that share vocabulary, one or two steps deep. The things involved are the requirements' own noun phrases, a fixed number. No pools and no incremental horizon are needed.
- (b) and (c) are graph questions on `trans/3`.

**Gherkin** maps While/Where/restrictions to Given, the trigger to When and the responses to Then, worded by the Steps grammar. It is a deterministic function of the tree, so no solver is needed. Made-up example data at most needs a horizon-1 call over the group's own facts.

## 2. Diagnosis

### What is fed, per group
`spec_solve.solve` (`spec_solve.py:142-160`):
1. Draws the cone over the whole spec.
   - Supervision g2's cone: 72 supervision, 17 role-boundaries, 7 red-green, 5 code-research, 4 planning, 4 review, 4 spec-integration, 3 delivery, 2 trials, 1 spec-migration, and U1, U4, U10.
2. Builds a program with:
   - `background.lp`: free choice of every attribute, relation and condition of every instance at state 0 and at creation (lines 47-56), plus frame axioms;
   - pools of n+1 instances for each of the 31 kinds the cone touches (`spec_logic_vocab.py:166`);
   - 249 `&tel` constraints, 90 event choice rules and 126 `on/1` externals.
3. Runs `telingo.imain` with `imin=0` (`spec_engine.py:86`). imax is 5 for supervision.
4. If UNSAT: minimises the core with one solve per id (`:108-117`), re-solves the core program, and retries with pools at n×imax+1 (`:102`). If the core is SAT under the bigger pools, it re-solves the whole cone with them (`spec_solve.py:160`).

The first build (P6 `spec_solve.py:125-127, 250-251`) put all about 640 statements into every group's program at fixed horizon 3: the 5.6 minutes. The cs-spike `solve.py` put many groups' witnesses into one program, with pools growing with the number of witnesses: 20 groups gave 16 k atoms and took 7–11 s; `all.lp` ran long.

### Measurements
From `groundsize.py`, which grounds like `imain`, and `solve_small.py`, which runs the plugin's own `_run` and `minimal_core`.

**A. Horizon** (g50's cone, pool 2):

| H | rules | atoms | ground time |
|---|---|---|---|
| 0 | 12 k | 6.5 k | 0.3 s |
| 1 | 27 k | 14 k | 0.8 s |
| 2 | 43 k | 24 k | 1.5 s |
| 3 | 60 k | 35 k | 2.5 s |
| 5 | 100 k | 61 k | 4.8 s |

The group's own statement alone at H=5 is 8 k rules.

**B. Pool size** (g50's cone, H=2). Pool 11 is the retry size and was not attempted; it extrapolates to about 10 M rules.

| pool | rules | ground time | memory |
|---|---|---|---|
| 1 | 17 k | 0.3 s | 34 MB |
| 3 | 96 k | 2.4 s | 59 MB |
| 4 | 202 k | 5.2 s | 90 MB |
| 6 | 748 k | 18.8 s | 262 MB |

**C. The two-requirement core** (r72, r52 and g50's witness, imax 5):

| pool | rules | time | memory |
|---|---|---|---|
| 1 | 4.3 k | 0.10 s | 19 MB |
| 2 | 8.6 k | 0.16 s | 20 MB |
| 3 | 18 k | 0.33 s | 23 MB |
| 6 | 206 k | 3.5 s | 68 MB |
| 11 | 3.2 M | 54 s | 829 MB |

The result is the same core every time, found with 0 solver conflicts: the conflict is propositional.

**D. Number of statements** (g50's cone, pool 2, H=3), rules: 1 → 6.6 k, 10 → 15 k, 40 → 22 k, 122 → 62 k. Roughly linear.

**E. What the grounding is made of** (pool 4, H=2):

| part | rules | ground time |
|---|---|---|
| background with free choices only | 65 k | 0.18 s |
| + `&tel` constraints | +66 k | 3.4 s |
| + labels | +70 k | 5.1 s |

The labels exist only for Gherkin.

### The constructs that explode, by measured damage
1. **The pool retry n×imax+1** (`spec_engine.py:102`; `spec_solve.py:157,160`). Conflicts among universally quantified requirements already show at one instance per noun phrase. Bigger pools only add ways to satisfy a requirement through fresh objects.
2. **Noun-phrase variables bound only by `kind/2`** (`spec_logic.py:182`). This gives P^k ground instances per step, each with its translated `&tel` subformulas (telingo `Theory.translate`).
3. **The horizon search from `imin=0`.** Strong next makes every horizon below the chain length UNSAT, so the solver proves UNSAT over free initial states and free events (`spec_logic.py:164,184`) at H=0, 1, … first.
   - The UNSAT groups (g2, g6, g34, g35, g40, g42) took 171–197 s each.
   - g1 was SAT at horizon 1 after 809 s. It is an inference that this was the H=0 proof.
4. **Cone rule 2 admits kindless statements vacuously** (`cone.lp:109-112`). 23 statements are in all 424 cones: U1, red-green r2 and r4, role-boundaries r6–r23, supervision r139, trials r2 and r3. Trigger edges then pull whole capabilities into g2.
5. **The minimal-core loop on the big program,** which multiplies the retry's cost.
6. **Ubiquitous actions read as "at every state"** (`spec_logic.py:181` in `#program always`). 18 statements, such as role-boundaries r11–r20 ("the implementer shall use `bdd-red-green`") and review r10–r13, force an event at every state of every trace.
7. **Labels in the check:** a third of the grounding, for Gherkin only. The labels' past formulas (`spec_logic.py:196`) cost as much as the constraints.
8. **One solve per group over almost the same cone.** The 72 supervision groups ground nearly the same 122-statement program 72 times, and several UNSAT groups blame the same pair: r2/r53 is the core of g2, g6, g34 and g40.

### trials r3/r6
- **r3 is in every cone.** Its only variable has no kind (`spec_logic_np.py:247`), so its `uses` is empty and cone rule 2 admits it.
- **r6 was in every batch-measurement cone.** In the `live40.txt` version, an effect's signature had no doer. So every batch-measurement "writes a measurement" (by `measure`) had an edge into r6's trigger ("When `trial-runner` writes a measurement…"). R4 fixed this later (`spec_logic.py:102-103`); today r6 is in only 2 cones.
- **Together they are UNSAT at every horizon.** Read as an obligation at every state, r3 required a write at every state; I infer "only" was lost in that version, which can't be recovered. With r6's strong-next response, that is G p ∧ G(p → X q), which no finite trace satisfies. `example/ltlf_trap.lp` gives UNSAT up to horizon 7 with core [r3, r6]; each one alone is SAT.
- **Why it appeared everywhere:** L1 asks whether the whole cone can happen, so an inconsistency present in every cone is reported for every group.
- **The same risk exists today:** if any triggered strong-next statement reacts to one of the "shall use" events, every group in the spec becomes an L1.

## 3. Literature and tools
- **NASA FRET** compositional realizability (Mavridou et al., FM 2021; https://ntrs.nasa.gov/citations/20210015352, https://arxiv.org/abs/2205.09082).
  - Requirements are connected when they share a state variable (inputs excluded), and each connected component is checked separately. The whole set is realizable if and only if each component is.
  - One spec went from 1525 s to under 7 s; a 9-requirement set that timed out at 12 h whole split into 7 components.
  - The failure mode they name is ours: mode variables connect everything, and they advise checking the mode logic separately.
  - Diagnosis gives all minimal conflicting sets.
- **Hanfor / Ultimate** (Langenfeld et al., RE 2019, https://nicolas.markey.fr/cnrs/PDF/Papers/re2019-LDWHP.pdf). Requirements become phase event automata. rt-inconsistency is checked on every subset of c requirements (c=2 in practice), together with the untimed invariants, with 300 s per subset, so partial results always exist.
- **EARS formalisations:** EARS-CTRL (Lúcio et al.) and "Formalizing EARS – First Impressions" (EARS→LTL templates); FRET's scope/condition/timing/response templates (https://arxiv.org/pdf/2110.09277). All use propositional signals, not instances.
- **SpeAR** (pLTL→Lustre→JKind, https://github.com/lgwagner/spear) and **ARSENAL** (NL→LTL, Büchi emptiness, https://arxiv.org/abs/1403.3142). Both use signal variables.
- **telingo** (LPNMR 2019; TEL on finite traces https://arxiv.org/abs/1804.10227; survey https://arxiv.org/abs/2009.06544).
  - It makes one copy of the program per step. Future operators unfold at quadratic to exponential cost; past operators stay linear.
  - Its benchmarks are planning problems, not satisfiability over free initial states.
  - With strong next on finite traces, G(p → X q) is unsatisfiable whenever p can hold at the last state.
- **Dedicated LTLf satisfiability:** aaltaf/CDLSC (https://ojs.aaai.org/index.php/AAAI/article/view/4150), BLACK, and ASP-based minimal-unsat-core enumeration (https://ceur-ws.org/Vol-3904/paper6.pdf). All propositional.
- **Grounding advice:** domain predicates, lower arity, aggregates, symmetry breaking, no unrestricted choices (Potassco guide https://www.cs.utexas.edu/~vl/teaching/378/guide-2.0.pdf; IJCAI 2022 https://www.ijcai.org/proceedings/2022/0353.pdf).
- **Bounded instance counts:** Alloy's small-scope hypothesis and parameterized-verification cutoffs (Emerson & Kahlon, https://www.cs.utexas.edu/ftp/techreports/tr00-03.pdf). Both support one generic instance per role.
- **SMT-based consistency:** PROPAS (patterns→FOL→Z3, unsat core as the conflict) and GE ASSERT (conflict analysis plus test generation, https://khoury.northeastern.edu/~pete/pub/re-2018.pdf).
- **Gherkin:** EARS→Gherkin practice is a direct mapping without a solver. I found no solver-based work; FRET's test generation exists, but I didn't verify which solver it uses.

**Fit:** the tools that scale all decompose by shared vocabulary (FRET's components, Hanfor's small subsets), give each check its own budget, and model signals propositionally. Our requirements are first-order but monadic in practice, each over a few noun phrases, so one generic instance per role is the cutoff.

## 4. The recommended approach and the working example
**Conflict finding:**
1. One translation per GF fun, emitting facts: `role/3`, `cond/4`, `trig/4`, `resp/5` with `oattr` and `orel`, `set/4`.
2. One fixed meta-encoding (`example/check.lp`):
   - candidate pairs where the trigger's event and doer match;
   - a choice that unifies B's roles with A's same-kind roles, or keeps them apart;
   - the triggers must unify and the pre-state must be consistent;
   - `clash/3` when B's prohibition is entailed by A's obligation, or when A and B set different values.
3. Brave enumeration lists every clashing pair, with its ids and the unification that shows it, in one solve.
4. Lifecycle and reachability as graph rules (`bad_set/4`).
5. Each U paired only with the requirements that share its vocabulary.
6. Chains composed along the trigger graph to depth 2–3 at an explicit horizon, one component at a time, each with its own timeout.

**Run** (`cd example && python3 run.py`), on seven requirements: the real r2, r3, r52, r53, r72, r16, plus seeded r99 (a different status on r16's trigger) and r98 (drafted → done, which no transition allows):
```
bad_set(r98,status,drafted,done)
clash(r16,r99,set)
clash(r2,r53,pos_neg)
clash(r52,r72,neg_pos)
ground 0.003s total 0.004s  lp atoms 249 rules 276  choices 45
```
r2/r3, r3/r53 and r53/r72 are correctly not reported. The plugin's path needs 8.6 k rules and 0.16 s for the r52/r72 pair alone at pool 2, and 3.2 M rules and 54 s at its retry pool.

r52/r72 is a real logical conflict, but only because r72 is meant as an exception under a delegation. The remedy belongs in the language (an "unless" or priority construct), not the solver.

**Gherkin:** `example/gherkin.py` prints scenarios from the same facts with no solver, byte-stable by role order. The plugin would keep its Steps grammar for the wording. Requirement A's scenario also serves as the witness shown for a clash.

## 5. What to change in the plugin, by value
1. Delete the pool retry (`spec_engine.py:102`, `spec_solve.py:157-160`). A 2-requirement core goes from 54 s and 829 MB to 0.1 s.
2. Use one instance per noun phrase of the statements under test, instead of n+1 per kind over a cone (`spec_logic_vocab.py:164-166`, `spec_logic.py:294-298`).
3. Draw pairs or small sets from a shared-vocabulary index (FRET-style components) instead of cones. Remove cone rule 2's vacuous admission. Give each check its own timeout and report partial results.
4. Make L1 "a reachable state where A and B fire and clash", found by SAT, instead of "the group cannot happen".
5. Stop reading "X shall use Y" as an event at every state. Lint the 18 untriggered positive event obligations, and check strong-next obligations against untriggered obligations of their trigger event (the G p ∧ G(p → X q) trap).
6. Make L3 and L4 graph checks on `trans/3`.
7. Leave labels, witnesses and optimisation out of the check.
8. Generate Gherkin from the tree; drop `optN`, `CAP` and `least`.
9. Add "unless"/priority to the grammar for rule-plus-exception pairs like r52/r72.

**Stop doing:**
- the incremental horizon from 0 as a conflict detector;
- free initial states and free events over every kind in every check;
- the whole spec, or everything, in one program (the first build, the cs-spike);
- one solve per group over overlapping cones;
- minimising cores on big programs;
- enlarging pools on UNSAT;
- measuring on the whole spec to find these problems.

## Files
In `/tmp/claude-1000/-home-vscode-shopsystem-bdd/248cf039-6f1c-44df-97a2-339ab46c8793/scratchpad/solver-research/`:

| File | What it does |
|---|---|
| `extract.py` | writes a group's cone program through the plugin's own code path, without solving |
| `dump_rules.py` | dumps every statement's translation and every group's cone to `out/r4_rules.json` |
| `compose.py` | builds a program from chosen statement ids and a witness at a chosen pool |
| `groundsize.py` | grounds like `imain` to horizon H and reports the ground size |
| `solve_small.py` | runs the plugin's `_run` and `minimal_core` on a small program |
| `out/` | the extracted programs, e.g. `r4_supervision_g50.lp`, `c_g50_core11.lp` |
| `example/` | `domain.lp`, `reqs.lp`, `check.lp`, `run.py`, `ltlf_trap.lp`, `gherkin.py` |