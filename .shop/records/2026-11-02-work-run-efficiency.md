# shopsystem-bdd, work run efficiency over i42–i64: analysis

Plugin 0.28.3. 2026-10-28 to 2026-11-02. Measurements: `measurements/2026-10-28-i42.md`, `-i43`, `-i44`, `-i46`, `-i50`, `2026-10-29-i51`, `2026-10-30-i54`, `2026-10-29-i63`, `2026-11-02-i64`, `2026-11-02-i48` (10 finished initiatives; i54's later measurement used). The per-initiative analyses are `<date>-<initiative>-analysis.md`. Figures below are sums or ratios of the measurements' stage rows (spec rounds = integrate, gate, apply, formulate, answer; reviews = review, branch-review).

## The delivery

| initiative | stages | spec rounds $ | research/plan/implement $ | reviews $ | total $ | work-items | implement sessions | active min | window h | $ / work-item |
|---|---|---|---|---|---|---|---|---|---|---|
| i42 | 20 | 3.45 | 2.53 | 1.18 | 7.16 | 2 | 2 | 35 | 0.7 | 3.58 |
| i43 | 25 | 3.56 | 4.39 | 2.42 | 10.37 | 3 | 4 | 50 | 0.8 | 3.46 |
| i44 | 9 | 0.51 | 0.48 | 0.48 | 1.47 | 1 | 1 | 11 | 0.1 | 1.47 |
| i46 | 51 | 4.72 | 10.16 | 6.23 | 21.11 | 9 | 12 | 108 | 3.1 | 2.35 |
| i50 | 9 | 1.35 | 0.58 | 0.35 | 2.28 | 1 | 1 | 11 | 2.2 | 2.28 |
| i51 | 24 | 4.52 | 0.95 | 1.31 | 6.78 | 1 | 2 | 28 | 18.0 | 6.78 |
| i54 | 26 | 3.24 | 1.70 | 1.37 | 6.31 | 3 | 3 | 37 | 47.0 | 2.10 |
| i63 | 33 | 4.06 | 3.00 | 1.25 | 8.31 | 2 | 5 | 39 | 0.7 | 4.15 |
| i64 | 11 | 1.27 | 1.80 | 0.84 | 3.91 | 1 | 3 | 20 | 1.2 | 3.91 |
| i48 | 23 | 2.77 | 2.01 | 0.80 | 5.58 | 1 | 7 | 36 | 119.1 | 5.58 |
| **all** | 231 | 29.45 | 27.60 | 16.23 | 73.28 | 24 | 40 | 375 | | 3.05 |

By agent, over the same ten:

| agent | sessions | cost | output tokens | cache read tokens |
|---|---|---|---|---|
| initiative-round | 86 | 28.75 | 325958 | 28786198 |
| bdd-task-reviewer | 27 | 16.24 | 234370 | 11872470 |
| bdd-implementer | 40 | 14.08 | 242711 | 25105718 |
| bdd-planner | 23 | 12.39 | 204936 | 7052831 |
| code-scout | 24 | 1.11 | 604239 | 19752710 |
| delegation-answerer | 16 | 0.70 | 9892 | 376700 |
| bdd-branch-reviewer | 15 | not counted | not counted | not counted |

## Against the earlier measurement

Not compared pairwise: the ten differ in size (1 to 9 work-items). The table above gives the sizes beside each total.

## Work-items that stopped

Stop causes as the ten analyses give them, grouped:

| cause | stops | cited |
|---|---|---|
| decision missing (a spec line or plan left a case open) | 8 | i46, i48, i63, i64 analyses, "Work-items that stopped" |
| other: a proposal's ids dropped on a redraft or apply, so other scenarios had no accepting work-item | 5 | i46 (w221 ×2, w222), i63 (r214–r216), i64 (r219/r220) analyses |
| other: a flaky or foreign scenario failed the whole-suite check | 3 | i64, i48 analyses; `tests/scenarios/supervision_given.py:72` |
| other: a stage's output field missing or an empty file set read as missing | 3 | i46 (w220), i51 (w230), i63 (w237) analyses |
| other: a session start or credential failure | 2 | i48 analysis (0-token sessions), i54 analysis |
| other: the work-item's branch not rebased before a resumed stage | 2 | i48 analysis |
| listing omission | 2 | i63 analysis (w236) |
| scenario wrong | 1 | i46 analysis (r161 Given) |

## Findings

none new: each initiative's branch-review findings are judged in its own analysis.

## Work-items added

none judged here; see each initiative's analysis.

## Observations

- Spec rounds cost 29.45 of 73.28 (40%), more than research, plan and implement together (27.60). (table above, "all")
- In the five one-work-item initiatives (i44, i50, i51, i64, i48), the spec rounds cost 0.51 to 4.52. In i51 they were 4.52 of 6.78 (67%), and in i48 2.77 of 5.58 (50%). (table above)
- initiative-round is the costliest agent, at 28.75 over 86 sessions. (by-agent table)
- The task reviewer (16.24) costs more than the implementer (14.08). (by-agent table)
- Implement sessions per work-item rose from 1.0–1.3 (i42, i44, i46, i50) to 2.5 (i63), 3 (i64) and 7 (i48). (table above)
- 12 of the 26 stops came from outside the work-item: dropped ids, flaky or foreign scenarios, start failures and an unrebased branch. None of these needed a spec or code decision. (stops table)
- Active session time is 11 to 108 minutes per initiative, but the window runs to 18 h (i51), 47 h (i54) and 119 h (i48). (table above)
- code-scout writes the most output (604239 tokens) at the lowest cost (1.11). (by-agent table)

## Candidates

- Try: keep every id a proposal already holds through a redraft or apply round, and renumber a taken id rather than redraft. i48 delivered the first half; q46 asks for the second. Rests on: the 5 dropped-id stops and the hand repairs in i55, i60 and i62. It worked if: no stop has a cause of "no work-item accepts" in the next five analyses, and implement sessions per work-item fall back toward 1.
- Try: when the whole-suite check fails only on scenarios outside the work-item's change, rerun them once and then hold the merge, without starting another implement session. i62 (w245) is building the rerun. Rests on: the 3 flaky or foreign stops and i64's two implement stages with no edit (0.49). It worked if: implement rows with no commit fall to 0.
- Try: let the gate settle each changed line's questions in one round, so a one-work-item initiative needs one integrate, gate and apply. Rests on: i51's 5 integrate, 6 gate and 4 apply rounds and spec rounds at 40% of all cost. It worked if: spec-round cost per initiative falls below delivery cost in the next one-work-item initiatives.

## Not counted

- bdd-branch-reviewer sessions: the measurements give no tokens or cost for them (15 sessions), so the review figures above leave them out.
- Resumed implement sessions are counted by their last turn only (i64 analysis, third candidate), so implementer figures are low.
- The time spent waiting on the person, and the hand repairs made outside `work run` (in i55, i60 and i62), are not counted by any measurement. The window column shows them only as elapsed time.
- Unfinished initiatives (i39, i45, i47, i49, i52, i53, i55, i56, i58, i59, i60, i61, i62) have no measurement. Their spec-round costs, including the stale drafts, are not counted here.
