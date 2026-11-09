# Study: the check's architecture around the solver (index outside clingo, partitioning, incremental)

(Saved by the session from the study agent's reply; its own write of this file was refused.)

Moving the candidate-pair index into Python and then checking the pairs in separate groups gives exactly today's
findings and makes `model logic` cost proportional to the number of candidate pairs. At 5,205 lines a full check takes
1-2 s instead of 38-58 s, and a re-check after a few edited lines takes about 0.5 s.

Code and raw logs: `scratchpad/b112/scale/architecture/` (`arch.py`, `incr.py`, `msh.py`, `check_noidx.lp`, `t1.py`;
results `final.log`, `results.jsonl`, `par.log`).

**Correctness:** every variant gives the same findings as today's `grammar/check.lp` at k = 1, 4, 10 and 20 in all
three modes. At k=20, today's check took 38 / 40 / 58 s and 3.5-3.8 GB of memory (own / mixed / shared). At k=40 to
120, where today's check is impractical, the variants agree with each other. On edited specs, the incremental check
equals a fresh check every time, and at k=4 and k=10 the fresh check also equals today's check.lp (36 of 36 cases,
some changing up to 145 findings).

## 1. Index outside clingo

- **What moves:** check.lp lines 36-56 (cc, can, kin, doerk, names, cand) become about 150 lines of Python (`arch.py`).
  The joins are dictionaries keyed by (verb, event) trigger, untriggered kind, a universal's events and attributes, and
  uses/nouse. `can` is tested only on those candidates.
- **The cut encoding:** `check_noidx.lp` is check.lp without those lines. Python gives clingo `cand(A,B)` facts, plus
  `kseed` facts with one added rule, `subeq(K,K) :- kseed(K).`
- **Index cost:** 0.03 s at 2,605 lines and 0.4 s at 10,405 (own and mixed), 2.4 s at 10,405 in shared.

| mode, lines | today: ground / solve | with the index: ground / solve |
|---|---|---|
| own, 2,605 | 6.8 / 0.08 s | 0.44 / 0.05 s |
| own, 5,205 | 38.0 / 0.43 s | 1.33 / 0.26 s |
| mixed, 5,205 | 39.6 / 1.02 s | 1.78 / 0.73 s |
| own, 10,405 | - | 6.0 / 1.7 s |
| shared, 10,405 | - | 18 / 280 s |

As one program it still grows faster than the line count: grounding rises about 4.5x when lines double, and the solve
explodes when many pairs share a program.

## 2. Partitioning

- **Why splitting is exact:** every atom, the one choice rule and every constraint in check.lp's pair section belong to
  a single pair (A,B). Pairs are therefore independent, and a group can be any set of pairs.
- **The one global input** is how kinds are seeded (`subeq(K,K) :- role(_,_,K)` looks at every requirement). Every
  group gets the whole spec's kinds as `kseed` facts, so nothing is lost.
- **Self-clash, L3 and L4** depend on one requirement plus the domain. They come from one program with no pairs
  (0.23 s at k=20).
- **L5 is the only finding that crosses groups:** an untriggered obligation is joined with every trigger of its event
  anywhere in the spec. It is computed over the whole spec, in Python, in about 20 lines, and matches today's output
  exactly.

**Grouping by connected components does not work.** Universals and shared kinds chain the copies together:

| mode | largest component | cost |
|---|---|---|
| own | grows linearly: 111 / 426 / 1,056 / 2,106 pairs at k = 1/4/10/20 | many one-pair components each pay the fixed cost of a group |
| mixed, k=20 | 5,166 pairs | 0.93 s |
| shared, k=20 | 21,486 of about 45,000 pairs | 11.7 s, mostly solving |

**Bins of 200 pairs keep every group at 50-150 ms**, whatever the component structure. With 16 workers, the clingo part
of a 10,405-line check takes 0.7 s (own and mixed) and 3.5 s (shared).

## 3. Incremental checking

- **The cache:** a pair's findings are stored under a hash of its two requirements' facts plus the domain and kinds;
  each requirement's own findings likewise. Only pairs or requirements with a new hash are solved again.

| change at k=20 | own: pairs re-solved / clingo time | mixed: pairs re-solved / clingo time |
|---|---|---|
| full check (16 workers) | 4,336 / 0.37 s | 10,756 / 0.43 s |
| 1 line | 1 / 0.018 s | 4 / 0.018 s |
| 5 lines | 19 / 0.020 s | 79 / 0.028 s |
| 20 lines | 100 / 0.044 s | 292 / 0.080 s |

- **What is left:** the whole re-check is 0.5-0.6 s, almost all of it Python rebuilding the indexes from the fact
  strings. That part is linear and could also be made incremental.
- **clingo's multi-shot API also works and is exact.** check.lp cut into per-requirement and per-pair parts, each
  requirement's facts guarded by an external, a changed line given a new versioned id. It is 10-40x slower per change:
  0.3-1.4 s of grounding plus a solve of the whole program each time; its memory keeps growing, and the encoding has to
  be split by hand. The hash cache is simpler and faster.

## 4. Combined check, cold

Python index, bins of 200, process pool and cache together:

| mode | lines | 1 thread | 16 workers | 1 line changed | memory (16 workers) |
|---|---|---|---|---|---|
| own | 2,605 | 0.76 s | 0.43 s | 0.24 s | 60 MB |
| own | 5,205 | 1.9 s | 0.96 s | 0.57 s | 92 MB |
| own | 10,405 | 5.6 s | 2.4 s | 1.1 s | 148 MB |
| own | 20,805 | 16.5 s | 5.9 s | 2.8 s | 302 MB |
| own | 31,205 | 36 s | 10.7 s | 4.6 s | 478 MB |
| mixed | 10,405 | 7.0 s | 2.7 s | 1.3 s | 176 MB |
| mixed | 31,205 | 54 s | 14.8 s | 4.7 s | 550 MB |
| shared | 10,405 | 64 s | 9.2 s | 4.0 s | 584 MB |

Cost per candidate pair is roughly constant: 0.3-0.5 ms single-threaded, about 90% of it grounding. The curve is not
linear in lines only because `gen.py`'s copies produce ever more pairs per line. In own mode this rises from 1.3 to 2.6
between k=10 and k=80, because copies share their triggers that have no backtick command string (for example
`does e_refuse`). Shared mode is quadratic by design. A real spec that grows by new triggers should stay near today's
1.1-1.3 pairs per line.

## Caveats

- **One pair could make today's whole program fail.** If check.lp's line-71 constraint fails for a single pair, today
  the whole program has no answer and every finding is hidden. Partitioned, only that group fails. It never happened in
  these tests, but a production version should report such a group as an error on that pair, not drop it silently.
- **The Python index duplicates check.lp lines 36-56.** A change to those rules has to be made in Python too, so it
  needs a test comparing the two sets of candidate pairs (`t1.py` does this).
- **Not done:** making the Python rebuild incremental (the next 5-10x for re-checks), and saving the cache to disk.

## Recommendation

1. Adopt the Python candidate index and the cut check.lp: about 150 lines in a new module, no new dependency, 15-30x
   faster at 2,600-5,200 lines.
2. Adopt pair bins of about 200, with self/L3/L4 in one program without pairs and L5 in Python, plus a process pool
   when there are many bins: about 80 more lines, standard library only. Witness solves run in the pair's own small
   group; the 20 s limit applies per group, so one slow pair no longer hides the others.
3. Adopt the per-pair and per-requirement hash cache, saved next to `spec_parse_cache`: about 60 lines.
4. Skip multi-shot and keep clingo. No Datalog engine is needed.

The ongoing cost is keeping the Python index and check.lp's candidate rules in step, guarded by that comparison test.
