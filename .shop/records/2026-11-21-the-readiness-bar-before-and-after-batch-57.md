---
id: measurement/missingmass.io/shopsystem/shopsystem-bdd/2026-11-21-the-readiness-bar-before-and-after-batch-57
kind: measurement
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-21
---

# The readiness bar before and after batch-57

Batch-57 (b437, the relative clauses factored) measured on one fresh item of 5 lines, each with a relative clause, before (1c1a0c4f2) and after (a2be349ff), `readiness_bar.check` called directly, one run at a time, each commit with its own empty XDG_CACHE_HOME for the cold run. Script and raw output: the session's scratchpad `ready-timing/`.

| Run | before | after |
|---|---|---|
| cold, empty cache | 433.6 s | 43.7 s |
| warm 1 | 14.5 s | 14.1 s |
| warm 2 | 14.4 s | 14.0 s |

| Stage (cumulative s) | before cold | after cold | before warm | after warm |
|---|---|---|---|---|
| `_violations` (2 calls) | 406.66 | 32.95 | 9.16 | 8.99 |
| `adapter_annotate.annotate` | 3.81 | 2.05 | 2.08 | 1.98 |
| `_logic` | 2.34 | 2.32 | 2.31 | 2.32 |
| `_broken` | 4.37 | 4.41 | 4.38 | 4.37 |
| `_scenarios` | 20.64 | 6.23 | 0.72 | 0.60 |
| `spec_grammar4.parse` (2494 calls) | 405.28 | 30.07 | 6.64 | 6.35 |
| `spec_gf.compile` (2 calls) | 39.08 | 11.09 | - | - |
| `spec_rgl_steps._load` | 20.14 | 5.73 | 0.22 | 0.10 |
| `spec_grammar4._state` (5410 calls) | 4.78 | 4.58 | 4.37 | 4.35 |

- Cold: 10x faster (parse 405 -> 30 s, compile 39 -> 11 s).
- Warm: unchanged at 14 s; 1,030,757 stat calls at both commits; the warm cost is b430's (stats, repeated parses, annotate).
- Load rose to 4-10 during the warm runs (another session's processes); warm times agree within 0.5 s.
- The 730 s cold figure of the earlier record was on b418's lines and is not compared.
