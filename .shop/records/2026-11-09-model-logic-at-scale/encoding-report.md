# Study: grammar/check.lp grounded in near-linear time, in clingo

(Saved by the session from the study agent's reply; its own write of this file was refused.)

Files in `scratchpad/b112/scale/encoding/`: `check_fast.lp`, `check_fast.diff` (204 lines), `spec_solve_fast.py`,
`spec_solve_fast.diff`, `variants/` (v1-v6, `check_fast8_externals.lp`), `out/` (every log and compared output),
profiling scripts `sections.py`, `prefix_cost.py`, `prof.py`, `solvestats.py`, `wprobe.py`, `solveoverhead.py`,
`assignprobe.py`, `fuzz.py`.

## Summary

`check_fast.lp` gives exactly the same findings and witnesses as `grammar/check.lp`, and its grounding grows only with
the number of candidate pairs. At 10,405 lines (own) grounding takes 2.1 s instead of 269 s, memory 463 MB instead of
13.9 GB; at 41,605 lines it grounds in 28 s.

- **Grounding.** Every slow rule had the same cause: the grounder joins two requirement-level facts on a word thousands
  of lines share (an event, a kind, a code), and only then meets the literal that binds the pair. A guard written first
  does not help: the grounder orders literals by domain size (why the spike stayed quadratic). Fix: join on a whole key
  (trigger plus clash key), or copy each requirement's facts to the pair first. Ten rule groups rewritten.
- **Solving.** Once grounding was fixed, solving was the quadratic part: the two `#external` atoms per pair, which every
  solve call paid for (1.39 s per call at 20,805 lines, clasp itself solving 0.03 s).
- **Witnesses.** The witness rules move to a `#program witness.` part; `spec_solve` adds the chosen pairs as facts of
  that part, grounds it once and runs one normal solve for all witnesses (`spec_solve_fast.py`: `_clashes` and a new
  `_witnesses`, 204 lines in all).
- **Totals.** Ground + brave + witnesses: 2.7 s at 10,405 lines and 9 s at 20,805 (own); 15 s at 20,805 (mixed).
- **What remains.** The pairs themselves grow faster than the lines in gen.py's data (copies share events like
  `e_write`, so lines in different copies on one event trigger are real candidate pairs). No encoding removes them
  without changing findings.
- **Correctness.** Brave atoms match today's check up to 5,205 lines (own, mixed), at 10,405 own, and in shared up to
  2,605. Witnesses match, and end-to-end findings through `spec_solve._findings`. A 40-seed fuzz (with `pair`/`ok`/`cl`/
  `out` shown too) found no difference. `run('.')` on the repository gives the same 8 findings.
- **Side finding.** The hard named-code constraints can make the whole program unsatisfiable; `model logic` then reports
  no findings and no L0. It happened on 14 of 40 fuzz seeds, with both encodings.

## Results

| lines (own) | today: ground | today: memory | fast: ground | brave | witnesses | total | fast: memory | pairs |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 265 | 0.05 s | 52 MB | 0.03 | 0.00 | 0.00 | 0.03 s | 53 MB | 89 |
| 1,045 | 0.8-1.2 s | 179 MB | 0.09 | 0.01 | 0.00 | 0.10 s | 63 MB | 368 |
| 2,605 | 6.7-8.5 s | 901 MB | 0.27 | 0.02 | 0.01 | 0.30 s | 97 MB | 1,061 |
| 5,205 | 40 s | 3.5 GB | 0.66 | 0.10 | 0.03 | 0.79 s | 183 MB | 2,616 |
| 10,405 | 269 s | 13.9 GB | 2.08 | 0.51 | 0.07 | 2.7 s | 463 MB | 7,226 |
| 20,805 | - | - | 6.65 | 2.09 | 0.26 | 9.0 s | 1.3 GB | 22,446 |
| 41,605 | - | - | 27.9 | 10.2 | 1.19 | 39 s | 4.4 GB | 76,886 |

| lines (mixed) | today: ground | today: memory | fast: ground | brave | witnesses | total | fast: memory | pairs |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2,605 | 8.3 s | - | 0.54 | 0.08 | 0.03 | 0.65 s | 138 MB | 1,919 |
| 5,205 | 38-57 s | 3.5 GB | 1.36 | 0.37 | 0.06 | 1.8 s | 283 MB | 4,596 |
| 10,405 | - | - | 3.56 | 1.14 | 0.14 | 4.8 s | 617 MB | 11,186 |
| 20,805 | - | - | 10.4 | 4.15 | 0.42 | 15 s | 1.7 GB | 30,366 |
| 41,605 | - | - | 36.7 | 19.3 | 1.41 | 57 s | 5.1 GB | 92,726 |

Today's witnesses (one focused solve per pair): 1.6 s at 2,605 lines and 11.5 s at 5,205 (own); 5.5 s and 44 s
(mixed). Each run its own single-threaded process, one after another; other studies shared the machine (±20%).
Grounding costs 0.25-0.40 ms per pair at every size.

## The floor: candidate pairs

gen.py renames command strings but keeps each copy's events, so lines triggered by an event (`e_write`, `e_park`, ...)
share a trigger with the same lines in every other copy: candidate pairs by check.lp's own semantics.

| lines (own) | one command trigger | shared-event trigger, across copies | with a universal |
|---:|---:|---:|---:|
| 2,605 | 370 | 225 | 446 |
| 10,405 | 1,480 | 3,900 | 1,766 |

The cross-copy event pairs grow quadratically; a real spec that grows its vocabulary with its lines should have far
fewer. The encoding keeps the cost per pair constant.

## Method

Grounding profiled by timing prefixes of the encoding (`sections.py` at section headers, `prefix_cost.py` at every
statement) at two sizes; `prof.py` for atom growth per predicate. clingo has no per-rule statistics, and `--text` sizes
miss the cost (join work that yields no atoms). For solve calls, `solvestats.py`, `wprobe.py`, `solveoverhead.py`,
`assignprobe.py` split each call into clasp's time and the call's fixed cost.

## Causes and fixes, rule by rule

The grounder orders body literals by estimated domain size; derived pair relations are larger than `resp` or `role`, so
a filter written first is not grounded first (the spike's `pre(A,B)` guard: the grounder still joined `resp(A,..,E)`
with `resp(B,..,E)` on `E=print` first). Fix everywhere: join on a whole key, or copy each side's facts to the pair
first, so every body literal carries `(A,B)`.

| # | check.lp | cause | fix |
|---|---|---|---|
| 1 | `cc`/`can` l.36-41 | every pair sharing an event word compared before any trigger filter (`print` pos x neg, `exit_ok` x `exit_error`, `change_nothing` x every event); 491k `cc` atoms at 2,085 lines | `key(R,K)`, `dem(R,K)` per requirement (`cc(A,B)` iff `dem(A,K)` and `key(B,K)`); trigger pairs joined on trigger and key at once (`tdem`, `tkey`, `tc`); no `cc`/`can` remain |
| 2 | `kin`/`doerk` l.44-49 | guarded by the quadratic `can`; `trig x trig` joined on object/doer | derived from `tp(A,B,X,Y,D1,D2)` |
| 3 | untriggered `cand` l.51 | `role x compat x role` over all triggered requirements: 1.4-5 s alone | `ureq`, `ukey`, `udem`, `ukind`, then `uc` |
| 4 | universal `cand` l.55 | `can` | `unc`, `unames` |
| 5 | L1 `cl` l.185-197 | `resp(A,pos,E) x resp(B,neg,E)` before `ok`: +1.4 s per rule at 10,405 lines | `ra`, `rb`, `sa`, `sb`, `ua`, `ub`, `xa`, `xb` |
| 6 | `fires` l.93 | `trig x trig` before `pair` | `ta`, `tb` |
| 7 | `out` rules with `the` l.95-96 | `tdef x named1` joined on kind; harmless at 10k lines, then **32 s at 20,805** once the grounder's order flipped | `nk`, `thek`, `tda`, `tdb` |
| 8 | named-code and `oattr` constraints l.69-72 | joined on a code or an attribute | `na`, `nb`, `oa`, `ob` |
| 9 | `none`/`cnone`/`rnone`/`ask`/`ucand` | `none(S,..) x pos(..,T,V)`; `kindof x subeq` with the kind bound first | `nonep`, `cnonep`, `kup` |
| 10 | `free`/`holds` l.121 | joined only through `at` | `fr`, `hd` |

Grounding seconds by version (own):

| version | 2,605 | 5,205 | 10,405 | 20,805 |
|---|---:|---:|---:|---:|
| today | 6.7 | 40 | 269 | - |
| v1, the spike's pre-pairs | 1.09 | 3.95 | 16.6 | 112 |
| v2, trigger and key in one join | 1.07 | 4.18 | 17.0 | - |
| v3, fixes 1-4 | 0.54 | 1.73 | 6.55 | - |
| v4, +5 and 6 | - | 0.85 | 2.69 | 32 s in one rule |
| final, +7 to 10 | 0.27 | 0.66 | 2.08 | 6.65 |

From the final version on, the rest of check.lp is linear in pairs (about 200 atoms per pair): unification, the two
states, defined conditions, L3-L5 and the witness part. `self`, L3, L4, L5 are per requirement and never showed in a
profile.

## Solving and witnesses: the externals were the cost

With the fast encoding and today's `spec_solve`: brave solve 2.8 s with 241 models at 10,405 lines (own), 24 s at
20,805, 224 s at 41,605; witnesses 29.6 s for 160 pairs at 10,405 lines, 220 s at 10,405 mixed. A plain solve call at
10,405 lines took 0.149 s, clasp solving 0.008 s; removing the two `#external` atoms per pair (14k-45k of them) cut a
call to 0.030 s, and at 20,805 lines from 1.39 s to 0.15 s.

Fix: the witness rules move into `#program witness.`; after the brave solve `spec_solve` adds the chosen pairs as facts
`focus/focusm` of that part, grounds it once (0.2-0.9 s at 20-40k lines) and solves once for all pairs. No atom or rule
spans two pairs, so the one model holds a witness for each. The per-pair witness is not guaranteed identical in theory,
but was in every run. Without externals the brave solve needs k+1 models under clasp's defaults (41 instead of 241 at
10,405 lines).

## Correctness

- Brave shown atoms identical to `grammar/check.lp` in own and mixed at 265, 1,045, 2,605, 5,205 lines; own at 10,405;
  shared at 265, 1,045, 2,605. Larger sizes: the final version matches the variant with externals, which matched today
  wherever today finishes.
- Witnesses (pre/prec per pair) identical to today's per-pair solves from 265 to 5,205 lines (own, mixed) and at 2,605
  (shared); the joint solve equals per-pair solves on the fast encoding at 10,405 (own, mixed).
- End to end through `spec_solve._findings` (stand-in `Words`): identical in all three modes 265-2,605 lines, and own and
  mixed at 5,205. `run('.')` on the repository: the same 8 findings.
- Fuzz (`fuzz.py`): 40 seeds, about 150 random facts each, exercising rules the real data never reaches (`uses`/`nouse`,
  `free`/`holds`, `oattr`, named codes, extra sets, negated responses, `none`, an untriggered requirement with
  responses), with `pair`, `ok`, `cl`, `out` shown too: all 40 identical.

## What did not work

v1 (the spike's guard) and v2 (trigger and key in one join) stayed quadratic (join order). `act(A,B)` idling unfocused
pairs: no gain. `sign_def=pos`: 1 model and 10x faster while externals existed; not needed without them.
`--heuristic=Domain` with a map heuristic: 50-131 s at 20,805 lines. `--eq=0`: 4x slower. `--no-gamma`, `--keep-facts`:
no change.

## Side finding

The hard named-code constraints (l.69, l.71) can make the whole program unsatisfiable: one pair whose shared code cannot
be unified is enough. The brave solve then returns nothing and reports finished: no findings and no L0. 14 of 40 fuzz
seeds, both encodings. On seed 25, dropping the two constraints gives 22 atoms instead of 0. A soft `out(A,B)` version
would follow the file's own rule that one pair never makes the program unsatisfiable. Not changed here (it changes
findings).

## Recommendation and costs

Adopt `check_fast.lp` and `spec_solve_fast.py` together (the encoding has no externals, so it needs the spec_solve
change). Fallback: `variants/check_fast8_externals.lp` keeps the externals and works with today's spec_solve unchanged:
the whole grounding fix, but solving stays quadratic (24 s brave at 20,805 lines). No new dependency (clingo 5.8).
check.lp grows from 253 to 288 lines, mostly helper rules copying a fact to the pair; spec_solve.py to 204 lines;
`_solve`'s `focus`/`external` parameters become unused. One rule for check.lp's header: *never join two
requirement-level facts on a vocabulary word; copy each to the pair, or join on a whole key, first.* A rule that breaks
it can pass at today's size and blow up later (cause 7); a test that grounds a 4x scaled spec within a time limit would
catch that, and `prefix_cost.py` finds the rule. Remaining growth is in the pair count itself; the next lever is
semantic (e.g. scoping event triggers by what they act on), not the encoding.

## Diff summary

Candidate pairs: `cc`, `can` replaced by `key`, `dem`, `vals`, `posev`, `tdem`, `tkey`, `tc`, `tp`, `ureq`, `ukey`,
`udem`, `uc`, `ukind`, `unames`, `ukeyu`, `udemu`, `unc`. Unification and states: `na`/`nb`/`oa`/`ob`, `ta`/`tb`,
`nk`/`thek`/`tda`/`tdb`, `fr`/`hd`, `kup`/`nonep`/`cnonep`. L1: `cl` reads `ra`, `rb`, `sa`, `sb`, `ua`, `ub`, `xa`, `xb`.
Witness: externals removed; the constraints, `foc`, `pre`, `prec` and their `#show` under `#program witness.`.
`spec_solve_fast.diff`: `_clashes` collects the chosen pairs; the new `_witnesses` adds them as facts of the `witness`
part, grounds it, one normal solve, returns each pair's `pre`/`prec`.
