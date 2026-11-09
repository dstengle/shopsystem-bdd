---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-09-model-logic-at-scale
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-09
---

# Keeping model logic fast as a spec grows

## The question

The owner asked whether grounding gets too expensive once a spec has thousands of lines, whether there are
alternatives to clingo such as Datalog, and said that adding dependencies is acceptable. Four studies were run to find
out and to optimise. This record gives what they found, what independent verifiers confirmed or refuted, and the
order in which to adopt the results. It serves b119 ("model logic stays near-linear as a spec grows to thousands of
lines") and is the fourth record of b112's research.

Supporting files are in the folder `2026-11-09-model-logic-at-scale/`: each study's report (`encoding-report.md`,
`architecture-report.md`, `datalog-report.md`, `entailment-report.md`), the clingo rewrite (`check_fast.lp`,
`check_fast.diff`, `spec_solve_fast.diff`), the cut encoding of the architecture study (`check_noidx.lp`) and the two
Soufflé programs (`idx2.dl`, `full2.dl`).

## 1. What was done

### The problem as measured

`model logic` parses each line, turns it into facts and checks them with clingo against `grammar/check.lp`. On scaled
copies of this repository's 265 lines, grounding took 0.05 s at 265 lines, 0.83 s at 1,045, 6.7 s at 2,605 and
27.7 s at 5,205. Solving stayed under 0.4 s. Memory reached 3.5 GB at 5,205 lines. Grounding grew about 4-6x per
doubling of the lines, so 10,000 lines would take minutes and over 10 GB. Nearly all of it was in check.lp's
candidate-pair section (lines 29-68). A first fix (a `pre(A,B)` guard, `check_spike.lp`) cut about 40% and stayed
quadratic.

The same "today" measurement differs between runs because the machine was shared: 27.7 s, 33.5 s, 38-58 s and 50 s
have all been measured for 5,205 lines. Cross-study ratios are rough for that reason; ratios inside one study are
reliable.

### The four studies

| study | question |
|---|---|
| encoding | can check.lp itself be rewritten to ground in near-linear time, in clingo alone? |
| architecture | can the work around the solver change: the candidate index in Python, pairs checked in groups, a cache for re-checks? |
| datalog | can a Datalog engine (Soufflé, Nemo) do the index, or the whole check? |
| entailment | can the planned entailed-Then check (a Then that other lines already force) scale, in clingo or Z3; and can Z3 do the clash check? |

### How correctness was required

Every variant had to give exactly today's shown atoms (the findings) at every size where today's check finishes, at
least 265, 1,045 and 2,605 lines in all three modes. A faster variant that changed one finding did not count. Each
study then had an independent verifier re-run its comparisons with its own scripts, re-time the headline numbers and
test the claims. Their verdicts are folded in below.

### The generator

All studies used one generator, `gen.py`. It makes k renamed copies of this repository's facts: 260k + 5 lines. Modes:

- `own`: each copy has its own command strings, so lines spread over many triggers;
- `shared`: copies keep the same command strings, so each trigger has k times the lines (quadratic by design);
- `mixed`: copies share command strings in groups of four (the realistic middle).

Two properties of the generator matter for reading the numbers:

- **Events are never renamed.** Lines triggered by an event (`e_write`, `e_park`, ...) share that trigger with the
  same lines in every other copy. By check.lp's own meaning these are real candidate pairs, and they grow
  quadratically: 225 at 2,605 lines and 3,900 at 10,405 (own). All four studies found this, and it is the reason no
  variant is linear in lines on this data. Whether a real spec grows like this is untested: gen.py only copies the
  same 265 lines.
- **The split-statement artefact.** gen.py renames only exact base ids, so the split line `requests#r53#1..3` keeps one
  id in every copy: k triggers and k-fold duplicate facts under one id. It barely affects timings of the clash check
  (encoding: 2.48 s to 2.39 s at 10,405 own without it; architecture and datalog: within noise). It does pad finding
  counts: at 10,405 own the encoding study's 164 findings are 125 without it. It inflates the entailment study's
  large-size timings 2-3x. Both sides of every comparison read the same facts, so no equality claim is affected.

## 2. Results by study

### Encoding: check.lp rewritten, still clingo

**Cause.** Every slow rule joined two requirement-level facts on a word thousands of lines share (an event, a kind, a
code) before the literal that binds the pair. The grounder orders literals by domain size, so a guard written first is
not grounded first. That is why the spike stayed quadratic. Fix: join on a whole key, or copy each requirement's facts
to the pair first. Ten rule groups were rewritten (`check_fast.diff`; check.lp grows from 253 to 288 lines).

**Solving.** Once grounding was fixed, the two `#external` atoms per pair made every solve call quadratic. The witness
rules moved to a `#program witness.` part, grounded once with the chosen pairs as facts and solved once
(`spec_solve_fast.diff`).

| lines (own) | today: ground, memory | fast: ground / brave / witnesses | fast total, memory |
|---:|---|---|---|
| 2,605 | 6.7 s, 901 MB | 0.27 / 0.02 / 0.01 s | 0.30 s, 97 MB |
| 5,205 | 40 s, 3.5 GB | 0.66 / 0.10 / 0.03 s | 0.79 s, 183 MB |
| 10,405 | 143-269 s, 13.9 GB | 2.08 / 0.51 / 0.07 s | 2.7 s, 463 MB |
| 20,805 | - | 6.65 / 2.09 / 0.26 s | 9.0 s, 1.3 GB |
| 41,605 | - | 27.9 / 10.2 / 1.19 s | 39 s, 4.4 GB |

Mixed: 1.8 s at 5,205, 4.8 s at 10,405, 15 s at 20,805. Grounding costs 0.25-0.40 ms per candidate pair at every size.

**Verifier.** Confirmed: identical brave atoms, pairs and findings with their witness pre-states at k = 1, 4, 10, 20
(own, mixed); `run('.')` on the repository gives the same 8 findings; the per-pair grounding cost is flat; the
externals were the solve cost (with them, witnesses took 29.9 s at 10,405 lines against 0.14 s without). The fast
timings reproduce (3.2 s total at 10,405 own). **Refuted:** today's grounding at 10,405 own took 143 s in the
verifier's run, not 269 s, so the speed-up there is about 60-70x, not 130x. **Refuted:** "drop-in with the existing
tests". Two of the 42 tests in `tests/scripts/test_check_lp.py` fail: the focus test adds `focus` as a base fact and
the witness part is never grounded; the no-warnings test sees new "no atoms over signature" messages for `pre/6` and
`prec/5`. Both need small edits. `spec_solve_fast.py` also locates check.lp relative to its own folder and needs that
path fixed when it moves into `scripts/`. **Not fully checked:** the scaled data has no L1, L3 or L4 findings, so those
paths are compared only by fuzz, and 25-35% of fuzz seeds are unsatisfiable on both sides (a vacuous match). That the
joint witness solve picks the same witness as per-pair solves is observed everywhere, not guaranteed.

### Architecture: index in Python, pairs in bins, a cache

The candidate rules (check.lp lines 36-56) become about 150 lines of Python dictionaries. `check_noidx.lp` is check.lp
without them, fed `cand(A,B)` and `kseed` facts. Pairs share no choice or constraint in check.lp, so any set of pairs
can be checked alone. Bins of 200 pairs keep each group at 50-150 ms. Self-clash, L3 and L4 come from one program with
no pairs. L5, the only finding that crosses pairs, is about 20 lines of Python. A cache keyed by a hash of each pair's
facts re-solves only changed pairs.

| lines | mode | 1 thread | 16 workers | 1 line changed |
|---:|---|---:|---:|---:|
| 5,205 | own | 1.9 s | 0.96 s | 0.57 s |
| 10,405 | own | 5.6 s | 2.4 s | 1.1 s |
| 10,405 | mixed | 7.0 s | 2.7 s | 1.3 s |
| 20,805 | own | 16.5 s | 5.9 s | 2.8 s |
| 31,205 | own | 36 s | 10.7 s | 4.6 s |

At 5,205 lines a 1-line change re-solves 1 pair (own) or 4 (mixed) in 0.018 s of clingo time; the rest of the 0.5 s
is Python rebuilding the index. Grouping by connected components failed: universals chain the copies together.
clingo's multi-shot API was also exact but 10-40x slower per change.

**Verifier.** Confirmed: identical shown atoms for all three variants at k = 1, 4, 10 in every mode and matching
digests at k = 20. It closed the L1 gap the scaled data leaves: on all 70 fact sets of the repository's check.lp tests
(31 clashes, 3 self, 8 bad sets, 6 unreachable), the cache and bins of size 1 both matched check.lp 70 of 70. Timings
reproduced (2.18 s one thread at 5,205 own). Corrected: the 16-worker memory column counts only the parent process;
and the shared trigger behind the extra pairs is `e_write`, not the report's example `e_refuse`. **Not checked:**
witnesses (pre/prec) are not implemented in the prototype at all; the multi-shot comparison; shared mode with 16
workers. The prototype also drops an unsatisfiable group silently.

### Datalog: Soufflé for the index or the whole check

`idx2.dl` (147 lines) ports the index plus self, L3, L4 and L5 to Soufflé 2.5. `full2.dl` (378 lines) does the whole
check by listing every unification of each pair as a tuple; it is exact because pairs share no choice. A hybrid fed
Soufflé's pairs to clingo.

| lines | mode | today | hybrid (Soufflé index + clingo) | full2, 1 thread | full2, `-j16` |
|---:|---|---|---|---:|---:|
| 5,205 | own | 33.5 s, 3.5 GB | 1.9 s | 1.16 s | 0.55 s |
| 10,405 | own | - | 8.5 s, 1.2 GB | 4.35 s, 0.7 GB | 1.50 s |
| 10,405 | mixed | 230 s, 13.8 GB | 16.3 s | 4.80 s | 1.58 s |
| 20,805 | own | - | 77 s, 7.8 GB | 17.3 s, 2.7 GB | 5.08 s |

The index alone takes 0.22 s at 5,205 lines. Nemo 0.10.1 gives the same pairs at about half Soufflé's speed and ships
for every OS, with a Python wheel.

**Verifier.** Confirmed: identical pairs (idx2) and shown atoms (full2) in every mode at k = 1, 4, 10 and at k = 20;
24 new mutated specs and the repository's 68 check.lp test fact sets all identical, including `uses`/`nouse` and
`free`/`holds`, which gen.py never produces; timings within 5%. Confirmed: clingo's witness is always among Soufflé's
(the "least M" pick matched less often than reported, 85% in one run; only wording could differ). Confirmed: the
exponential bound on unifications per pair (17.6 M for two lines with 9 same-kind roles each); the guard against it is
not built. **Refuted:** "most of the gain is the engine, not the rewrite; staying in clingo is not supported". The
encoding study's clingo rewrite matches or beats full2 single-threaded (2.7-3.2 s against 4.35 s at 10,405 own). The
100-200x gap holds only for `idx2.lp`, a straight port with a bad join order. The fuzz harness also accepts "stuck and
not in the reference" as agreement and never changes a named role's kind, so it would hide global-UNSAT cases.

### Entailment: the entailed-Then check, and Z3

`comp.py` compiles each premise into one clingo rule and decides every query in one stratified model, with no search.
A literal counterexample search (`cex.py`) and Z3 served as references. On this repository, 20 Thens are entailed
(the report says 17; the verifier found 3 more on the split line) and 55 with a rule that "refuse" means "exit with an
error". The extra 35 are refusal lines whose "change nothing" follows from U11.

| lines | comp.py, own: build + ground + solve | mixed: ground + solve |
|---:|---|---|
| 5,205 | 1.0 + 2.3-3.4 + 0.1 s | 4.8 + 0.3 s |
| 10,405 | 3.3 + 9.8 + 0.5 s | 19.8 + 0.9 s |
| 20,805 (artefact out) | 6.8 + 11.3 + 1.0 s | 22.3 + 1.8 s |

The first encoding (`ent.lp`, one brave solve) took 299 s at 5,205 lines and was dropped. Z3 for the clash check gave
check.lp's L1/L6 on all 70 test fact sets at about 1.3 ms per pair (6.2 s at 5,205 own); it needs its own pair index.
Z3 answers "unknown" on some quantified entailment queries; clingo never does.

**Verifier.** Confirmed: the three methods agree on all 494 responses at k = 1; `comp.py` is sound and misses only
entailments that need reasoning by cases (requests r36); timings reproduce; Z3's clash results match. Weaker than
claimed: the three methods share one fact parser and compiler, so a shared misreading would not show; and "comp.py
equals ent.lp" holds in own mode only (at k=4 mixed, 5,916 triples against 5,808). **Refuted:** "the growth is
gen.py's, not the check's". The artefact is real, but premises on a shared event trigger such as `e_write` also grow
quadratically, and in a real spec that growth is genuine. The cross-check also removes Z3's speed case: its 6-8 s were
measured against today's unfixed check.lp, not against the rewrite.

## 3. Comparison

Single-threaded, own mode, unless noted. "Today" for reference: 27.7-58 s at 5k lines, 143-269 s and 13.9 GB at 10k.

| option | ~5k lines | ~10k | ~20k | exact? | dependencies | code to keep in step | risks |
|---|---:|---:|---:|---|---|---|---|
| clingo rewrite (`check_fast.lp` + spec_solve change) | 0.8 s | 2.7-3.2 s | 9 s | yes, incl. witnesses; verified | none (clingo 5.8) | none: one encoding | join order can regress silently (cause 7 appeared only at 20k); two test edits; witness pick empirical |
| Python index + bins + cache (`check_noidx.lp`) | 1.9 s (0.96 s ×16; re-check 0.57 s) | 5.6 s (2.4 s; 1.1 s) | 16.5 s (5.9 s; 2.8 s) | yes; verified on 70 test sets | none (standard library) | Python index mirrors check.lp lines 36-56 | witnesses not built; UNSAT group dropped silently; cache on disk not built |
| Soufflé index + clingo (hybrid) | 1.9 s | 8.5 s | 77 s, 7.8 GB | yes | Soufflé 2.5 | index in `.dl` and check.lp | clingo part still grows faster than pairs |
| Soufflé whole check (`full2.dl`) | 1.2 s (0.55 s ×16) | 4.4 s (1.5 s) | 17 s (5.1 s), 2.7 GB | yes; verified incl. fuzz | Soufflé 2.5: Linux x86_64 deb, macOS Homebrew; no Windows, no aarch64 deb, no PyPI wheel | whole check twice if clingo is kept | exponential unifications per pair; guard and fallback not built |
| Z3 per-pair clash search | 6.2 s (+ pair index) | not measured | not measured | yes on 70 test sets; L1 at scale vacuous | `z3-solver` (~40 MB wheel) | whole clash check in Python/Z3 | "unknown" answers; witness text to port |

The entailment check is a new check, not an alternative: `comp.py` in clingo, about 5 s at 5k lines (mixed), about
20 s at 10k mixed, 19 s at 20k own without the artefact.

What the table shows:

- The clingo rewrite is the fastest single-threaded option at every size measured, with no new dependency and no
  second copy of the rules.
- Soufflé is ahead only with 16 threads (5 s against 9 s at 20k lines). Single-threaded it is slower than the rewrite.
- Only the architecture study offers fast re-checks after small edits. Its cold check is slower than the rewrite.
- All options leave the same floor: the candidate pairs. Every exact option is roughly constant per pair (0.25-0.5 ms in
  clingo); the pairs grow faster than the lines only where many lines share an event trigger.

## 4. Recommendation

The expectation tested was: the clingo rewrite first, the per-pair cache for re-checks, the entailment check as
`comp.py` in clingo, Z3 only beside clingo for ordered values and counts, Soufflé later if clingo's per-pair cost
becomes the limit. The evidence supports it, with one change of emphasis: the cache is not needed until specs reach
roughly 10,000 lines.

1. **Adopt the clingo rewrite now.** Bring in `check_fast.lp` as `grammar/check.lp` and the `spec_solve_fast.diff`
   changes into `scripts/spec_solve.py` (about 204 lines, under the size limit). Cost: the two test edits in
   `tests/scripts/test_check_lp.py` (ground the witness part in the focus test; declare `pre/6` and `prec/5` with
   `#defined` or accept the info messages); the check.lp path; `_solve`'s unused `focus`/`external` parameters
   removed. Add the rule to check.lp's header: *never join two requirement-level facts on a vocabulary word; copy each
   to the pair, or join on a whole key, first.* Add a test that grounds a 4x scaled spec within a time limit, since a
   bad join can pass at today's size and fail at 20k lines. Fix b120 in the same work: the rewrite touches the named-code
   constraints (`na`/`nb`) anyway.
2. **Build the entailed-Then check as `comp.py` in clingo** when b112's design calls for it. About 300 lines, no new
   dependency, sound. It needs the actor `Kind of:` facts and the refuse definition (section 5). Its own growth is
   partly quadratic on shared event triggers, as the clash check's is.
3. **Add bins and the per-pair cache when re-checks at 10k+ lines become slow.** At 5k lines the rewritten check takes
   0.8 s cold, so a cache saves little. At 20k lines (9 s cold) it would. Open: the cache was built over the Python
   index, not over the rewrite. Bins are exact for any encoding, and the rewrite's pair section could produce the pairs
   instead of a Python copy; this is untested. Witnesses per bin must be built.
4. **Use Z3 only beside clingo,** for ordered values (versions, dates) and counts, where it settles cases like
   migration-tools r14/r25 outright. It offers no speed gain over the rewrite for the clash check.
5. **Keep Soufflé as a later option.** It becomes worth its platform cost only if clingo's per-pair cost becomes the
   limit and multi-threading is wanted. It would need the role-count guard with a clingo fallback, and a Windows answer
   (Nemo is pip-installable, at half the speed, but was tried only on the index).

**What stays open.**

- The pair count. It is the floor for every option. The next lever is in the language, not the engine: for example,
  scoping an event trigger by what it acts on, so that unrelated lines on `write` are not paired.
- Whether a real spec grows like gen.py's copies is unknown. A real spec that adds vocabulary with its lines should
  have far fewer pairs per line.
- L1, L3 and L4 at scale were tested only through fuzz and the repository's test fact sets. A quarter to a third of
  fuzz seeds were unsatisfiable on both sides.
- The rewrite's joint witness solve matches per-pair witnesses in every run, but is not guaranteed to.
- The exponential unification case (many same-kind roles in one line) is not exercised by gen.py for any engine.
- Today's numbers above 10,405 lines and the encoding study's 20,805 and 41,605 points were not re-run by the
  verifiers.

## 5. Bugs and backlog

| finding | where it stands |
|---|---|
| One unsatisfiable pair hides every finding: check.lp's hard named-code constraints (l.69-71) make the whole program UNSAT, and `model logic` prints no findings and no L0. 14 of 40 fuzz seeds in the encoding study; 10 of 40 and 2 of 12 in the verifier's re-run; both encodings. | b120. Fix with step 1: make the constraint soft (the pair marked out) and report an unsatisfiable solve as an error. The architecture prototype and Soufflé's `stuck` show the same gap in their own forms. |
| The domain facts do not record an actor's `Kind of:`, so U11's "a tool" never matches `work` (the study added `akind(a_work,k_tool)` by hand). | b121. Prerequisite of the entailed-Then check. |
| U11's trigger "a tool refuses a command" is produced by no line. The 35 refusal entailments need a glossary definition: **refuse**: a tool refuses a command when it exits with an error on it. Consequence to accept knowingly: a failing `tools check` or `model check` must also change nothing. | b122. Related to b117 (U11 is never paired with any line). |
| analysis-tools r26 restates r25, and feature-file-tools r7 restates r6, each with `--json` added: their Thens are entailed. | Added to b118. Each reworded line gets a new id. |
| check.lp's join order can regress without any test failing. | Part of step 1: the header rule and the scaled-spec timing test. |
| gen.py's split-statement artefact and unrenamed events. | A study tool, not repository code. Any later measurement should rename split ids per copy and report pairs per line next to its timings. |
