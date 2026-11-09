# Study: the entailed-Then check, in clingo and Z3

(Saved by the session from the study agent's reply; its own write of this file was refused.)

Folder: `scratchpad/b112/scale/entailment/`. Nothing in the repository was changed.

| File | What it is |
|---|---|
| `comp.py` | Recommended: each premise compiled to one Datalog-style clingo rule; every query decided in one stratified model, no choice or search |
| `ent.lp` | First try: a fixed meta-encoding choosing how to map each premise's roles, one brave solve. Superseded |
| `cex.py` | The owner's method taken literally: one clingo counterexample search per query over a guessed world. Reference |
| `z3ent.py` | The same counterexample search in Z3, with quantified premises |
| `z3clash.py` | check.lp's per-pair L1/L6 search, one Z3 query per pair |
| `z3ordered.py` | ordered values (versions) and counts in Z3 |
| `k1_entailed.txt` | the k = 1 results with each line's text |
| `*val*.py`, `bench_*.py`, `*_final.txt`, `bench_comp.jsonl` | validation, benchmarks, outputs |

## Summary

- **This repository (k = 1):** three independent methods agree exactly on all 494 responses: the compiled forcing
  check, a literal counterexample search in clingo, and Z3. Without a refuse = exit-with-an-error rule, 17 Thens are
  entailed, all right (analysis-tools r26 and feature-file-tools r7 just restate r25 and r6 with `--json` added). With
  the rule, 52: the extra 35 are every "exit with an error ... and change nothing" line, whose change nothing follows
  from U11. The rule is best stated as a glossary definition: **refuse**: a tool refuses a command when it exits with an
  error on it.
- **Recommended build: compile each premise to one clingo rule** (`comp.py`). No new dependency, about 300 lines. Sound
  (everything it reports the other two confirm); it never reasons by cases, so it can miss an entailment, which only
  keeps a step in the scenario. Near-linear: about 6 s at 10k lines and 17 s at 20k (own), about 30 s mixed, with
  gen.py's duplicated `requests#r53` artefact left out (quadratic on its own). The first encoding (`ent.lp`, one brave
  pass) was correct but too slow: 299 s at 5k lines.
- **Z3 for the per-pair clash search:** same L1/L6 answers as check.lp on all 70 fact sets of the repository's check.lp
  tests and on every scaled size up to 5k lines; about 1.3 ms per pair, 8 s total at 5k lines against 52 s for check.lp
  to ground. Needs its own cheap pair index (here the pairs came from check.lp). Handles version order and counts
  natively (r14 and r25 come out as disjoint states). Quantified entailment queries sometimes return "unknown"; each
  query is solved separately.
- **Advice:** keep Z3 out of the main loop; use it beside clingo for ordered values and counts. Prefer a clingo-only fix
  of the pair search if another study gets the same speed.
- Side findings: (1) today's domain facts don't record each actor's `Kind of:`, so U11's "a tool" never matches `work`
  (the study adds `akind(a_work,k_tool)`); (2) gen.py copies split lines (`requests#r53#1..3`) under one id with k
  triggers and k-fold duplicate facts: quadratic by itself, and it inflates check.lp's L6 counts at scale.

## Semantics, settled by making the three checkers agree

- A premise's subject and its While/When roles are universal; a role that appears only in a positive Then is something
  the premise makes.
- A thing L's own Thens make is matched by any made thing with its kind, its restrictions and L's other Thens on it.
- An `every` object is read separately for each Then.
- "Shall not E a K" is universal: no K is E'd.
- An "If" line and a non-"If" line on the same trigger are never premises for each other.
- The refuse = exit-with-an-error rule is applied once.

Diffing the three checkers caught seven bugs in the study's own encodings, all fixed: a double negation that let U11's
own response trigger U11; mapping roles that appear only in Thens (unsound); one rule per premise over all its `every`
roles together; "the title of every item" made into one shared title; a loop in the state-1 frame rule; Z3 reading
"shall not set" as "set"; Z3 having no sub-kind axioms.

## Results on this repository (k = 1)

`comp.py`, `cex.py` (all premises, no index) and Z3 agree exactly on all 494 responses. The index asks 389 of them;
nothing outside it is entailed.

Entailed without the refuse rule (17):

| Then | Entailed by | Right? |
|---|---|---|
| backlog r18, r19, r21: "write an item that is `idea`", "commit the item" | backlog r1 | yes |
| backlog r7, r17: "print the item" | backlog r6 "print every item" | yes |
| backlog r8: "print a JSON object" | U8 | yes |
| analysis-tools r26 (both Thens) | r25 | logically yes; r26 restates r25 with `--json` added (a wording finding) |
| feature-file-tools r7 (both Thens) | r6 | as r26 |
| analysis-tools r6: print `.venv/bin/python` | r2 | yes |
| requests r8 (both Thens) | requests r6 | yes |
| requests r52, r53: "write the comment" | r32 "write every comment that is unrecorded" | yes |

Needing the refuse rule (35, all "change nothing", all from U11): analysis-tools r21, r22, r27; backlog r3, r20;
batches r12, r13; decision-tiers r8, r9; design-model-check r51, r57; feature-file-tools r8, r13, r15, r18, r19;
intake r6; migration-tools r7, r8, r9, r12; readiness r2, r3, r6, r9, r11; requests r6, r7, r9, r15, r16, r24, r28,
r38, r40.

Correctly not entailed: analysis-tools r10 and migration-tools r14 (the success path, no error exit); U11's own
"change nothing"; every "exit with an error naming X" (U11 only guarantees *a* reason); requests r53's "not change the
status" (r53 has no error exit).

Stating the refuse rule: U11's trigger "a tool refuses a command" is produced by no line, so it needs a bridge. Cleanest:
a glossary definition, "**refuse**: a tool refuses a command when it exits with an error on it", one background rule in
the facts. Consequence to accept knowingly: a failing `tools check` or `model check` must also change nothing.

## Scaling of the entailment check (single-threaded)

`comp.py` grounds the queries in independent parts of 1,000 (queries are independent, so exact).

| k | lines | own: build / ground / solve / peak | mixed: ground / solve / peak | shared: ground / solve |
|---|---|---|---|---|
| 1 | 265 | 0.04 / 0.06 / 0.00 s / 53 MB | as own | 0.06 / 0.00 s |
| 4 | 1,045 | 0.16 / 0.31 / 0.01 s / 65 MB | 0.68 / 0.04 s / 85 MB | 0.69 / 0.04 s |
| 10 | 2,605 | 0.44 / 0.99 / 0.02 s / 105 MB | 1.56 / 0.09 s / 143 MB | 6.05 / 0.47 s |
| 20 | 5,205 | 1.03 / 3.36 / 0.12 s / 181 MB | 4.85 / 0.27 s / 242 MB | 16.2 / 1.8 s |
| 40 | 10,405 | 3.27 / 9.82 / 0.48 s / 385 MB | 19.8 / 0.85 s / 495 MB | 56.6 / 6.1 s |
| 80 | 20,805 | 6.75 / 31.0 / 1.60 s / 1.1 GB | 61.5 / 1.96 s / 1.2 GB | 250 / 22 s |

The growth is gen.py's, not the check's. With the `requests#r53` copies left out (`NO_SPLIT_ARTEFACT=1`):

| k | own: ground / solve / peak | mixed: ground / solve / peak |
|---|---|---|
| 40 | 4.7 / 0.26 s / 252 MB | 8.8 / 0.62 s / 375 MB |
| 80 | 11.3 / 0.97 s / 614 MB | 22.3 / 1.75 s / 751 MB |

About 2.4x per doubling. Shared mode is inherently quadratic: k identical lines per trigger all entail each other.

`ent.lp` (one brave solve, own): k=1 0.07/0.07 s; k=4 0.43/1.5 s; k=10 1.9/27 s; k=20 6.2/299 s. Unusable at scale.

Reference checkers: `cex.py` about 1 s per query; Z3 median 20-45 ms per query (16k queries at 10k lines: roughly 10-15
CPU-minutes).

Correctness at scale: `comp.py` = `cex.py` at k=1 and k=4 own; `comp.py` = Z3 at k=1 and k=4 own; `comp.py` = `ent.lp`
at k=4 and 10 own and mixed (before the later semantic fixes). At k=4 mixed, 4 queries differ: requests r36's "post a
comment" in each copy, which `cex.py` and Z3 find by cases (either every line is settled and a copy of r36 fires, or
some line isn't and r35 fires; both post a comment) and `comp.py` misses. Z3 also timed out on 10 queries there, all on
batches r1 (a While combining `every` with a definition).

## Z3 for the clash check

`z3clash.py`, one query per candidate pair: unification is equality (roles are constants, distinct within a side, free
to be equal across sides where kinds, codes and values agree); attributes are functions to an enum (functional
automatically), state 1 an `If` chain over the sets; conditions and relations predicates, definitions exact (iff); the
clash a disjunction of check.lp's cases; L1 = `sat(clash and not dep)`, L6 = `sat(clash and dep_C)`.

Same answers as check.lp: all 70 distinct fact sets of `tests/scripts/test_check_lp*.py` (53 pairs; 31 with an L1, 2
with an L6) identical; this repository on check.lp's own candidate pairs identical L1 (none) and L6 at every size tried
(gen.py's r53 artefact set aside; it accounts for 24-120 of check.lp's L6 findings per size).

| k, mode | pairs | check.lp ground / solve | Z3 total | Z3 median per pair |
|---|---|---|---|---|
| 1 own | 89 | 0.05 / 0.00 s | 0.12 s | 1.2 ms |
| 4 own | 368 | 1.6 / 0.04 s | 0.63 s | 1.3 ms |
| 10 own | 1,061 | 11.3 / 0.33 s | 2.2 s | 1.5 ms |
| 10 mixed | 1,919 | 11.9 / 0.73 s | 2.6 s | 1.2 ms |
| 10 shared | 4,031 | 10.3 / 5.6 s | 8.1 s | 1.9 ms |
| 20 own | 2,616 | 54.3 / 1.3 s | 6.2 s | 1.4 ms |
| 20 mixed | 4,596 | 51.5 / 4.3 s | 8.2 s | 1.3 ms |

Per-pair cost stays flat; a replacement needs its own Python pair index (as in `comp.py`).

Better in SMT: unification needs no choice; definitions exact; `every`/`no` native; ordered values and counts free
(`z3ordered.py`, 17 ms: with versions as integer triples, migration-tools r14 ("own release", 3.2.0) and r25 ("after
1.0.0 and before 3.0.0") are disjoint, so the pair needs no L6; "hold at most 2 claims" plus a third is unsat).
Worse: quantified queries can return "unknown" (clingo never does); each query solved separately, no shared grounding;
answers harder to turn into finding text; `z3-solver` is a large dependency (about 40 MB).

## What did not work

- `ent.lp`: brave enumeration needs one model per new answer atom, so solving grows quadratically. Its role-mapping
  choice exists only because a fixed meta-encoding cannot express joins of varying width; compiling each premise to
  its own rule removes the choice.
- One `comp.py` program for all queries: grounding superlinear (87 s at k=80), the grounder matching every new atom
  against thousands of recursive rules. Fixes: two strata (premises on L's trigger; then untriggered premises and the
  refusals; chains longer than error exit -> refuse -> U11 not followed), and grounding in independent parts of 1,000
  queries.

## Recommendation

1. **Build the entailed-Then check as `comp.py` in clingo.** Sound, near-linear (about 17 s at 20k lines own, about
   30 s mixed), no new dependency, about 300 lines beside `spec_facts`; the compiler must track every new fact form, as
   check.lp does. Misses entailments by cases (safe: a step stays in). Needs actor kinds in the domain facts and the
   refuse definition in the glossary. Each finding names its premise (`ent(L,I,M)`), so the generator can say why it
   dropped a step. Estimate about 2 days with tests.
2. **Keep Z3 out of the main loop for now.** Beside clingo for ordered values (releases, versions, dates) and counts,
   where it decides r14/r25-style L6s outright; optionally an offline audit for entailments by cases. Cost: `z3-solver`
   plus about 300 lines.
3. **Z3 could replace the per-pair clash search** only with its own pair index (about 100 more lines) and the witness
   text ported from check.lp's `pre/6` to a Z3 model, an "unknown" reported as L0. Prefer a clingo-only fix if a
   parallel study reaches similar speed; choose Z3 if ordered values and counts are wanted in the clash check anyway.

## Addendum: the last ent.lp benchmarks (superseded encoding, before the later semantic fixes)

| mode | k | lines | ground | solve | peak |
|---|---|---|---|---|---|
| own | 20 | 5,205 | 6.2 s | 299 s | 1.1 GB |
| own | 40 | 10,405 | 25 s | did not finish in 600 s | 3.7 GB |
| mixed | 4 | 1,045 | 1.7 s | 96 s | 370 MB |
| mixed | 10, 20, 40 | 2,605-10,405 | 4.9-44 s | did not finish in 600 s | up to 5.8 GB |

A brave solve needs one model per new answer atom, so solving grows quadratically; mixed is worse because each command
is shared by 4 copies (more premises to map per query). At the same sizes `comp.py` solves in under 2 s (mixed 10,405
lines: 19.8 s ground, 0.85 s solve).

## Addendum 2: Z3 against comp.py at larger sizes (entailment)

- k=10 own (3,970 queries) and k=20 own (7,940): wherever Z3 answered, it matched comp.py exactly. k=10 mixed: Z3 found
  10 entailments comp.py misses, each requests r36 "post a comment" in one copy (entailment by cases, as explained).
  comp.py never claimed an entailment Z3 rejected: sound, misses entailments by cases.
- Z3 "unknown" (10 s timeouts) grows with the spec: k=4 mixed 10 and k=10 mixed 10 (batches r1 copies: a While with
  `every` and a definition); k=10 own 20 and k=20 own 40 (brainstorming r1 Then 2 and r3 Then 1, two per copy; cause
  not investigated). clingo never returns unknown.
- Z3 for the whole entailment check: median 42 ms per query at k=1 (26 s total), 54 ms at k=10 own (452 s), 114 ms at
  k=20 own (1,425 s, about 24 minutes); comp.py on the same k=20 input: about 2.8 s build+ground+solve.
- Recommendation unchanged: comp.py in clingo; Z3 for ordered values and counts, at most an offline audit for
  entailments by cases. The per-pair clash experiment stands separately: about 1.3 ms per pair, no unknown, up to
  4,596 pairs.
