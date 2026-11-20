---
id: measurement/missingmass.io/shopsystem/shopsystem-bdd/2026-11-20-the-readiness-bar-on-b418-timed
kind: measurement
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-20
---

# The readiness bar on b418, timed

# Readiness bar time on b418: 15 s warm, 730 s with an empty cache

## What was run

`readiness_bar.check(root, backlog_items.load(root, "b418"))` called directly in Python (b418 is `ready`, the bar's
entry point is `check`, which runs `well_formed` then `decision_reasons`), wrapped in cProfile and timing wrappers
(script and profiles in the session scratchpad, outside the repository). No tracked file changed. The result of every
run was `([], [])` (passing). b418 holds 11 requirement lines and 6 retirements; `spec/capabilities` has 51 files.

## Setup and load

nproc 32. uptime at start 15:10:48: load average 2.13, 1.63, 1.91 (no other `work`, pytest, clingo or gf process
was running when the runs began; `ps` matched none). Load stayed about 2.0-2.4 during the runs (the runs themselves
are single-threaded: python at about 100% of one core). Python 3.11.15, GF 3.12.

## Wall times

| Run | Cache | Wall |
|---|---|---|
| 1 | default `~/.cache/shopsystem-bdd` (358 MB parse, 1.1 GB pgf, about 300 sha folders; this lay's grammar already in it) | 14.9 s |
| 2 | same, immediately after run 1 | 15.0 s |
| 3 | empty `XDG_CACHE_HOME` (cold: no compiled PGF, no parse cache) | 730.1 s (12 min 10 s) |
| 4 | the cache run 3 filled, immediately after | 14.4 s |

Warm (runs 1, 2, 4) 14.4-15.0 s; cold 730 s. Run 1 was already warm because an earlier bar run on b418's lay had
filled the default cache.

## Stages (seconds; spec_language.parse and spec_lexicon.read are called from inside other stages, so rows overlap)

| Stage | warm (run 2) | cold (run 3) |
|---|---|---|
| `well_formed` total | 14.95 | 730.09 |
| copytree of `spec/` and `lay_onto` | 0.01 | 0.01 |
| `spec_lexicon.read` (20 calls) and `problems` (2) | 0.88 / 0.02 | 0.87 / 0.02 |
| `_violations` (`spec check` facts + model.lp), 2 calls (before the lay, after the lay) | 9.16 | 354.17 |
| `adapter_annotate.annotate` (after the lay) | 2.22 | 350.71 |
| `_parses` (the item's lines, 11 + universal) | 0.05 | 0.05 |
| `_logic` (`spec_solve.run`, clingo + spec_entail) | 2.32 | 3.75 |
| `_broken` (a third read of the model facts, after the lay) | 4.39 | 4.24 |
| `_scenarios` (`features_generate.generate`, 3 calls) | 1.06 | 21.27 |
| `decision_reasons` | 0.01 | 0.01 |
| `spec_language.parse`: 2042 calls, 815 distinct lines | 8.66 | 702.18 |
| `spec_gf.compile` (3 PGF compiles, gf subprocess) | 0 | 58.59 |

## Top functions, cold run (cumulative / self)

- `spec_language.parse` 702.2 s cum (2042 calls); `spec_grammar4.parse` 701.1 s (2452 calls); `_trees` 656.0 s;
  `_gf_trees` 654.6 s (815 calls).
- `pgf.Concr.parse` 604.4 s self, 817 calls (0.74 s per call).
- `spec_grammar4.py:155` genexpr (list of GF parses): 50.2 s self, 1630 calls.
- `spec_gf._run_gf` / `subprocess.run` 58.6 s, 3 calls (gf -make).
- `spec_rgl_steps._load` 20.1 s, 97 calls (the step grammar's PGF load for `features generate`).
- `model_facts.read_capabilities` 332.1 s; `model_spec.read_codified` 332.1 s (102 calls); `model_spec.parsed` 348.6 s (815).

## Top functions, warm run (cumulative / self)

- `spec_language.parse` 8.6 s cum (2042 calls); `spec_grammar4.parse` 6.6 s (2452); `_named` 5.8 s (5305);
  `spec_grammar4._context` 5.1 s (5403 calls); `_state` 4.3 s (5403 calls).
- `posix.stat` 1.31 s self, 1,029,685 calls; `posixpath.join` 0.61 s self, 1,012,949 calls (the `_state` genexprs at
  spec_grammar4.py:75 and :81 stat every file of the grammar's inputs on each call: 961,734 and 1,004,958 calls).
- `builtins.sorted` 0.52 s self, 39,907 calls; `pgf.readPGF` 0.59 s, 3 calls; clingo ground 0.30 s, 5 calls.
- `domain_model`/`model_domain.domain_line` 4.7 s cum, 809 calls.

## Where the time goes

1. A parse-cache miss on every line of the context. `spec_parse_cache.key` includes the sha of grammar 4's sources
   (core files plus the files generated from the lexicon). The cache miss run parsed 815 distinct lines in GF
   (817 `Concr.parse` calls, 604 s, 0.74 s each) against 8.6 s of parse time on a hit. The lines parsed are all of the
   context's lines (815 distinct), not the item's 11 lines: the whole of `spec/` is read by `spec check`'s facts and
   `spec logic` after the lay. Any lay that changes the grammar's sources (a lexicon term, a vocabulary or model entry
   on the item) gives a new sha, so every line misses. In the cold run this one stage is 83% of the wall time. The
   cache folders hold about 300 sha folders (358 MB parse, 1.1 GB pgf).
2. The same parse work is reached through three readers, each of which reparses nothing in the warm case but is
   charged in the cold case to whichever stage first needs a line: `_violations` after the lay (354 s over its two
   calls; the call before the lay, with the unlaid sha, is the cheap one), `adapter_annotate.annotate` (350.7 s of
   that, via `governing` -> `model_spec.parsed`), then `spec_solve.run`, `_broken` and `features_generate` reuse them
   (3.75 s, 4.2 s, 21 s).
3. The model facts of the copy are read three times per run: `_violations` before the lay, `_violations` after the
   lay (inside `_broken`), and `annotate`'s `governing`; each reads every capability file and calls
   `model_spec.read_codified` / `parsed` / `domain_line` (815 parsed lines, 809 `domain_line` calls) with only the
   in-process caches in between. In the warm case `_violations` is 9.16 s of 14.95 s, `annotate` 2.22 s, `_broken` 4.39 s.
4. Per-call fixed cost in `spec_grammar4._context`/`_state`: 5403 calls, 5.1 s cum of the warm 14.95 s, each call
   statting the grammar's input files (1.03 million `stat` calls, 1.3 s self, 2.1 s in the genexpr at line 75).
5. The grammar compile is cached by sha (`~/.cache/shopsystem-bdd/pgf/<sha>/`): in the cold run `spec_gf.compile`
   ran 3 times (58.6 s total, about 19.5 s each: the copy before the lay, the copy after the lay, and one more); in
   the warm runs it ran 0 times, and `pgf.readPGF` loads it (3 calls, 0.59 s). It is not per run when the sha is
   unchanged. The step grammar load for `features generate` (`spec_rgl_steps._load`, 97 calls) is 20.1 s cold and
   about 1 s warm.

What would remove the time: the parse cache hitting across the lay (a key that does not change for lines whose
words did not change), or the three reads of the model facts sharing one read; the per-call `_state` stat walk
would remove about 2-5 s of the warm 15 s.

## Not reproduced

A 22 minute run was not reached: the cold run on this machine (empty cache) took 12 min 10 s. The 4-run, ~88 minute
session was not observed; the figure above is for one b418 lay with an empty cache, not for a lay that changes
the lexicon of several capabilities.
