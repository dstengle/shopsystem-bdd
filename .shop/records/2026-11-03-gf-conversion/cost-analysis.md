---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-03-gf-conversion-cost
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-03
---

# The GF conversion: length and cost, against `work run`

The overnight GF conversion ran on 2026-11-03 from 02:36 to 08:57 UTC, on branch `gf-conversion`. This record gives
what it measurably took and cost. It then estimates what the same work would have cost through the regular request →
initiative → work-item system (`work run`).

**Measured** figures come from the `usage` fields of the Claude Code transcripts. **Estimates** are labelled as
estimates and give their basis.

## Method and prices

- **Transcripts read.**
  - The main session `248cf039-…jsonl`, from 02:36 to 13:10. 13:10 is the person's first message after the run;
    everything after it is out of scope.
  - The 7 agent transcripts of design workflow `wf_336e55f8-527`.
  - The 22 agent transcripts of build workflow `wf_bbfe2b24-5b0`.
  - The 13 `claude -p` sessions of the live run (P16), under `~/.claude/projects/-tmp-work-run-*`, all between 07:16
    and 08:35.
- **Counting.** Each assistant message is counted once, by `message.id`, and `<synthetic>` messages are skipped. The
  counts are input (uncached), output, cache creation split by TTL (`ephemeral_5m`, `ephemeral_1h`), and cache read.
- **Cross-checks.** The workflow counts match the journals exactly: 190 tool uses (design) and 2,097 (build). Wall
  times also match: 28.8 min against 1,730,579 ms, and 335 min against 20,116,409 ms.
- **The workflows' "subagent tokens" figures** (851,451 and 4,793,786) are not a sum of billed token kinds. The billed
  input + output + cache-write tokens are 970,409 and 8,074,712, and those figures leave out cache reads. This record
  does not use them.
- **Prices** (claude-api skill, models table cached 2026-10-06, and `shared/prompt-caching.md`; $/MTok):

| model | input | output | cache write 5 m (1.25×) | cache write 1 h (2×) | cache read |
|---|---|---|---|---|---|
| claude-opus-5-5 | 4.00 | 20.00 | 5.00 | 8.00 | 0.20 |
| claude-sonnet-5-5 (live run rounds) | 2.00 | 10.00 | 2.50 | 4.00 | 0.20 |
| claude-haiku-5-5 (live run research) | 0.10 | 0.50 | 0.125 | 0.20 | 0.01 (assumed 0.1×; the skill does not state it; affects $0.03 at most) |

- **Models used.** All workflow agents and the main session ran on Opus 5.5. The workflow agents wrote 5-minute cache
  entries, and the main session wrote 1-hour entries.
- **The live run's own USD figures.** These were in `e2e.md`, from `total_cost_usd`. They agree with this pricing to
  within $0.08 per session: intake 0.12 vs 0.11, branch review 0.76 vs 0.76, plan 0.38 vs 0.38, review 0.38 vs 0.38.
  The integrate session is 0.71 vs 0.63; the transcript also counts the background capability-writer.

## The overnight run, measured

### Totals

| part | wall clock (UTC) | API calls | output | input (uncached) | cache write | cache read | USD |
|---|---|---|---|---|---|---|---|
| design workflow (7 agents) | 02:45–03:14, 29 min | 157 | 222,660 | 314 | 747,435 | 12,878,593 | 10.77 |
| build workflow (22 agents) | 03:15–08:51, 5 h 36 min | 1,798 | 1,761,802 | 3,610 | 6,309,300 | 331,271,688 | 133.05 |
| live run (P16's 13 `claude -p` sessions) | 07:16–08:35, 1 h 19 min | 144 | 86,823 | 292 | 482,041 | 4,423,602 | 4.37 |
| main session (orchestrator) | 02:36–08:57 | 26 | 18,749 | 64 | 141,885 | 1,945,185 | 1.90 |
| **overnight total** | **02:36–08:57, 6 h 21 min** | 2,125 | 2,090,034 | 4,280 | 7,680,661 | 350,519,068 | **150.09** |

- **Unattended time.** The person's last message before the run was at 02:44 ("yes to all three"). The next was at
  13:10. The run asked the person no questions, because all judgement on the branch was delegated.
- **The live run is outside the workflow's token count.** P16's own agent ($7.77, 89 min) is inside the build
  workflow. It drove `work run`, whose sessions are separate `claude -p` processes with their own transcripts. Those
  sessions are the $4.37 row.
- **Where the build's $133.05 went:**

| token kind | tokens | at | cost | share |
|---|---|---|---|---|
| cache read | 331.3 M | $0.20 | $66.25 | 50% |
| output | 1.76 M | $20 | $35.24 | 26% |
| cache write | 6.31 M | $5 | $31.55 | 24% |

- **The main session stayed small.** It made 26 calls in 6 h 21 min, and waited while the workflows ran.

### By phase and layer

| phase | agents | window | wall min | agent min | calls | tool uses | output | cache write | cache read | USD |
|---|---|---|---|---|---|---|---|---|---|---|
| design: 4 surveys | 4 | 02:45–02:49 | 4 | 14 | 84 | 90 | 70,077 | 377,676 | 6,105,661 | 4.51 |
| design: design | 1 | 02:49–03:00 | 11 | 11 | 21 | 23 | 63,215 | 138,736 | 2,138,420 | 2.39 |
| design: builder check + revise | 2 | 03:00–03:14 | 14 | 14 | 52 | 77 | 89,368 | 231,023 | 4,634,512 | 3.87 |
| L1 P1–P4 | 4 | 03:15–03:39 | 24 | 63 | 241 | 283 | 345,274 | 794,468 | 32,521,107 | 17.38 |
| L1 gate | 1 | 03:39–03:46 | 7 | 7 | 48 | 49 | 31,465 | 125,182 | 4,354,629 | 2.13 |
| L2 P5–P7 | 3 | 03:46–04:18 | 32 | 67 | 250 | 333 | 371,415 | 834,579 | 46,241,038 | 20.85 |
| L2 gate | 1 | 04:18–04:23 | 5 | 5 | 23 | 26 | 15,218 | 81,850 | 1,422,355 | 1.00 |
| L3 P8–P11 | 4 | 04:23–05:04 | 41 | 109 | 533 | 618 | 511,496 | 1,343,926 | 124,802,505 | 41.91 |
| L3 gate | 1 | 05:04–05:16 | 12 | 12 | 48 | 51 | 26,355 | 108,255 | 3,579,180 | 1.78 |
| L4 P12–P13 | 2 | 05:16–06:04 | 48 | 67 | 255 | 304 | 265,409 | 699,712 | 66,259,058 | 22.06 |
| L4 gate | 1 | 06:04–06:27 | 22 | 22 | 27 | 30 | 9,860 | 243,502 | 1,265,932 | 1.67 |
| L5 P14 | 1 | 06:27–07:05 | 39 | 39 | 177 | 186 | 97,810 | 536,072 | 34,054,313 | 11.45 |
| L5 gate | 1 | 07:05–07:14 | 9 | 9 | 19 | 21 | 7,849 | 121,629 | 895,771 | 0.94 |
| L6 P15–P16 | 2 | 07:14–08:43 | 89 | 103 | 158 | 176 | 71,474 | 1,289,618 | 14,962,745 | 10.87 |
| L6 gate | 1 | 08:43–08:51 | 8 | 8 | 19 | 20 | 8,177 | 130,507 | 913,055 | 1.00 |
| **all 16 packages** | 16 | | 327 | 447 | 1,614 | 1,900 | 1,662,878 | 5,498,375 | 318,840,766 | 124.53 |
| **all 6 gates** | 6 | | 63 | 63 | 184 | 197 | 98,924 | 810,925 | 12,430,922 | 8.52 |

Uncached input is 2 tokens a call throughout and is left out of this table.

### By package

| package | layer | took (min) | calls | tool uses | output | cache write | cache read | USD |
|---|---|---|---|---|---|---|---|---|
| P1 toolchain | 1 | 7 | 34 | 34 | 31,305 | 102,797 | 2,480,850 | 1.64 |
| P2 grammar, parser | 1 | 24 | 62 | 81 | 142,056 | 242,431 | 9,613,839 | 5.98 |
| P3 format, glossary, v5 docs | 1 | 21 | 89 | 110 | 111,338 | 247,865 | 12,819,699 | 6.03 |
| P4 graph rules v5 | 1 | 11 | 56 | 58 | 60,575 | 201,375 | 7,606,719 | 3.74 |
| P5 model reads codified | 2 | 15 | 80 | 88 | 78,581 | 245,672 | 12,878,095 | 5.38 |
| P6 logic check | 2 | 20 | 70 | 90 | 108,855 | 236,812 | 11,214,166 | 5.60 |
| P7 generation, vocabulary | 2 | 32 | 100 | 155 | 183,979 | 352,095 | 22,148,777 | 9.87 |
| P8 flow | 3 | 22 | 128 | 146 | 110,636 | 312,700 | 26,715,528 | 9.12 |
| P9 11 guarantees capabilities | 3 | 18 | 75 | 87 | 80,667 | 212,809 | 10,418,431 | 4.76 |
| P10 4 small service capabilities | 3 | 41 | 206 | 248 | 183,969 | 482,376 | 61,071,491 | 18.31 |
| P11 3 core service capabilities | 3 | 28 | 124 | 137 | 136,224 | 336,041 | 26,597,055 | 9.73 |
| P12 supervision (164 lines) | 4 | 48 | 161 | 184 | 197,298 | 502,716 | 53,714,215 | 17.20 |
| P13 1.0.0 upgrade step | 4 | 18 | 94 | 120 | 68,111 | 196,996 | 12,544,843 | 4.86 |
| P14 release | 5 | 39 | 177 | 186 | 97,810 | 536,072 | 34,054,313 | 11.45 |
| P15 end-to-end test | 6 | 14 | 67 | 80 | 39,184 | 160,910 | 7,580,229 | 3.10 |
| P16 live run (driver only) | 6 | 89 | 91 | 96 | 32,290 | 1,128,708 | 7,382,516 | 7.77 |

- **Agent count.** The journal confirms 22 build agents: 16 packages and one merge-and-gate agent per layer. No fix
  round was launched, and every gate passed on its first run.
- **Packages that returned `done: false`.** Four did: P9, P10, P11 and P12. In each case one accept check needed a
  change to a file the package did not own. Examples are `model parse --file` on codified statements, and the
  `LiveRestatesTest` assertion. The layer 3 and layer 4 gate agents made those changes test-first at the merge
  (`gate-L3.md`, `gate-L4.md`).

### What it produced

- **Commits.** 67 commits on `gf-conversion` past 96818f71.
- **Change outside `.shop/`.** 297 files, +22,915 / −22,251 lines:

| area | files | insertions | deletions |
|---|---|---|---|
| scripts | 40 | +4,220 | −908 |
| tests | 176 | +7,726 | −12,997 |
| spec | 22 | +6,538 | −856 |
| features (generated) | 10 | +2,807 | −6,313 |
| grammar | 28 | +447 | 0 |

- **Spec.** All 19 capabilities are codified. `model restates` gives 581 ids of 0.29, of which 516 are restated and 65
  dropped (`gate-L5.md`). The spec now holds 636 requirement ids.
- **Scenarios.** 575 before the conversion, 319 after.
- **Live run.** One request (q47) went to `done` (i67) through the converted system. The measured cost was $4.37 by
  transcript ($2.95 recorded in `e2e.md`, with two sessions unrecorded there).

### Context, not counted in the total

- **Before the run.** The previous session (`98c29820`) ran the design conversation that led to the run, from the
  21:06 "very large request" message to 02:36. That covered the CNL spike and the domain model, with 4 extraction
  subagents. It cost $8.84: main $5.36 and subagents $3.48.
- **After the run.** The person's session after 13:10, up to this analysis, cost $1.21. This analysis is not counted.

## The counterfactual: the same work through `work run` (estimate)

### Per-unit figures used (measured)

From the ten measured initiatives i42–i64 (plugin 0.28.3; `2026-11-02-work-run-efficiency.md` and the measurement
JSON of each). Their costs are Claude Code's `total_cost_usd` for each stage session.

| unit | value | basis |
|---|---|---|
| spec rounds per request line | $1.02 | $29.45 over the 29 lines of q20, q22–q24, q30, q34, q36, q37, q42 and q44 |
| spec rounds, fitted | $0.65 per proposal + $0.56 per gate stop | least squares over the 10 initiatives' (proposals, proposal stops, spec $). Residuals $0.00–1.17; the largest are i63 (2.89 fitted against 4.06) and i48 (1.77 against 2.77) |
| gate stops (proposal `awaiting-answer`) per line | 1.10 | 32 stops / 29 lines, 16 proposals |
| work-items per request line | 0.79 | 23 work-items / 29 lines |
| work-item stops (awaiting-answer and failed) per work-item | 1.13 | 24 + 2 over 23 (the efficiency record: 26 stops / 24) |
| work-item stops from outside the work-item | 12 of 26 | the efficiency record's stops table. Without those the rate is about 0.58 |
| research + plan + review + extra implement sessions per work-item | $1.55 | $0.046 + $0.539 + $0.601 × 27/23 reviews + $0.352 × 17/23 extra implement sessions (stage means) |
| delivery + reviews per changed line | $0.028 | ($27.60 + $16.23) / 1,566 changed lines (outside `.shop/`) of the 21 work-items with commits |
| work-item size | median 40, mean 75 changed lines | the same 21 work-items |
| intake per request | $0.12 | i67 transcript |
| branch review per initiative | $0.76 for 1 work-item | i67 transcript (the efficiency record could not count branch reviews). i46's took 3.1× i67's time |
| analysis per initiative | $1.07 | i67 transcript |
| stage session time | integrate 134 s, gate 19 s, apply 37 s, formulate 101 s, research 135 s, plan 94 s, implement 114 s, review 99 s, branch review 238 s | means of the stage rows |
| suite and merge per work-item | 391 s suite + 384 s merge, one merge at a time | `e2e.md` steps 12–14; `supervise_merge.py:104` (r20) |
| initiative window | median 1.7 h, mean 19.3 h (0.1 h to 119 h) | the efficiency record's window column. Waiting on the person dominates it |

### Sizing (estimate)

| unit | low | likely | high | basis |
|---|---|---|---|---|
| requests / initiatives | 6 | 10 | 19 | one a layer / about one a package / one a capability |
| capability-proposals | 21 | 21 | 21 | 19 capabilities, the typed glossary and `universal.md` |
| request lines to integrate | 581 | 581 | 581 | measured: the 581 0.29 ids each need an outcome. New lines for the tools (P1–P8, P13) are not counted |
| gate questions | 65 | 175 | 640 | low: one per dropped line, all measured. Likely: 0.3 per line, a judgement (restating existing behaviour should raise fewer readings than new lines do). High: the measured 1.10 per line |
| work-items | 60 | 160 | 480 | 36,046 changed lines (outside `.shop/`, generated features excluded) divided by about 600, 225 and 75 (the measured mean) lines a work-item |
| work-item stops | 35 | 173 | 542 | the work-item counts × 0.58 / 1.08 / 1.13 |

### Cost (estimate)

The structure is the same in all three columns.

- **Design.** The design workflow is kept as it ran ($10.77), since the requests would be written from it.
- **Content work.** The writing the 16 packages did is kept as it ran ($124.53), done by implementers and
  integrate rounds instead.
- **Overhead per unit.** On top of those, the regular system adds the measured overhead for each unit.

The high column instead prices everything at the measured per-unit rates of recent deliveries.

| component | low | likely | high |
|---|---|---|---|
| design (as run) | 10.77 | 10.77 | 10.77 |
| intake | 0.72 | 1.20 | 2.28 |
| spec rounds | 50.05 (21 × 0.65 + 65 × 0.56) | 111.65 (21 × 0.65 + 175 × 0.56) | 590.06 (581 × 1.02) |
| delivery | 217.57 (124.53 + 60 × 1.55) | 372.64 (124.53 + 160 × 1.55) | 1,008.87 (36,046 × 0.028) |
| branch reviews | 4.56 (6 × 0.76) | 15.00 (10 × 1.50) | 47.50 (19 × 2.50) |
| analyses | 6.42 | 10.70 | 20.33 |
| person's session (as run) | 1.90 | 1.90 | 1.90 |
| **total** | **≈ $292** | **≈ $524** | **≈ $1,682** |
| against the overnight $150.09 | 1.9× | 3.5× | 11.2× |

- **Stops and person rulings** (gate questions + work-item stops): **about 100 / 350 / 1,180**. Overnight, the person
  answered none.
- **Elapsed time** (estimate):

| | low | likely | high |
|---|---|---|---|
| merges alone, one at a time (r20) | 6.5 h (60 × 6.5 min) | 34 h (160 × 12.9 min) | 103 h (480 × 12.9 min) |
| other machine time | about 5 h of spec rounds | about 10 h of spec rounds | |
| total machine time | about 12 h | about 45 h | weeks |
| elapsed, with the person's latency on 100–1,180 rulings | 1.5–2 days | 5–7 days, answering in daily batches | 2–3 weeks or more |

  Further assumptions behind these times:
  - Integrate, gate and apply rounds run one at a time across initiatives (r95).
  - Implementers whose claims share a file wait for each other (r20). Most capability conversions touch `world_*.py`,
    `vocab.py` or `conftest.py`.
- **Sensitivity.** These are 0.29 per-unit costs, and the conversion would have had to run on 0.29.
  - After the conversion, i67 cost 0.53× i64 (`e2e.md`, `measure compare`).
  - Formulate is now a script with no session.
  - Running the same work on the converted system would put the likely column lower. That cannot apply to the
    conversion itself.

### Why the difference

1. **Fixed overhead per unit, and many units.** The regular system pays for each work-item a research ($0.05), a plan
   ($0.54), a review ($0.60 × 1.17) and 0.74 extra implement sessions. It pays for each proposal and each gate stop a
   round of its own. The overnight packages averaged $7.78 each and did a capability's whole conversion in one
   context.
2. **Questions with the person.** The measured rate is 1.10 gate stops per line and 1.13 stops per work-item. At this
   size that is hundreds of rulings. Each ruling costs a round, and waiting for it costs hours or days. The overnight
   run delegated every judgement and made the calls itself: the 65 dropped lines, and the wording moved to prose.
3. **Serial bottlenecks.** The regular system merges one work-item at a time, with about 13 min of suite and merge
   each. Spec rounds run one at a time across initiatives, and claims that share a file wait. The overnight run
   merged once a layer (6 merges in all) and ran up to 4 packages side by side on disjoint files.
4. **Bootstrapping.** P8 changes the integrate and formulate flow that `work run` itself runs, and P14 removes the
   legacy reader. The regular system would have to deliver those changes with the flow being changed.
   - It would also sweep in the 13 open initiatives (`e2e.md` defect 4).
   - The overnight run's layers and per-file codified marker (design §13.4) avoided that.

### What each bought that the other did not

**The regular system would have given:**
- **An independent reviewer for each work-item.** The task reviewer reads the commits against the plan and the spec,
  and grades its findings. Overnight, the gate agents ran each package's accept commands, the suite and
  `model check`, but nobody read each package's code against the spec apart from the agent that wrote it.
- **A branch review for each initiative,** with Critical and Important triage. Overnight, only i67's branch review
  ran.
- **Spec gates with the person.** Overnight, the 65 dropped lines and the wording moved under "Implementation, may
  change" were decided by agents under delegation. The person has not yet ruled them.
- **Traceability.** Each commit is tied to a work-item, and each work-item to the requirement ids it accepts.
- **A measurement and analysis for each initiative.**

**The overnight run gave:**
- One coherent design across all 19 capabilities and the tools: surveys, design, builder check and revise, for $10.77.
- A full-suite and model-check gate after each layer.
- A system that changes its own flow without a bootstrap problem.
- About 6 h of unattended wall clock with no person rulings.
- Roughly 2× to 11× lower cost.

**Left open by the overnight run** (`gate-L5.md`, `gate-L6.md`):
- 25 open capability-proposals still in 0.29 lines, to re-integrate.
- The live run's defects, raised as q47.
- The optional generator and vocabulary fixes.

## Observations

- Cache reads are half the build's cost: $66.25 of $133.05, from 331.3 M tokens.
- Layer 3 (P8–P11) is the costliest layer at $41.91 for its packages. P10 alone is $18.31, with 61.1 M cache-read
  tokens in 206 calls.
- P12 (supervision, 164 lines) cost $17.20. P9 (11 capabilities, 156 lines, spec only) cost $4.76.
- The gates cost $8.52 for 6 merges, 6% of the build.
- P16 waited 89 min for a live run whose sessions cost $4.37. P16's own agent cost $7.77, of which 1.13 M tokens were
  cache writes.

## Not counted

- **The person's time** on the regular system's questions. The elapsed-time column shows it only as days.
- **New requirement lines** for the tools themselves (grammar, `model parse`, `model logic`, `features generate`, the
  upgrade step). The counterfactual counts only the 581 lines that exist, so every column is low by that much.
- **Local machine time.** The suite runs, the grammar compile and the merges are not priced.
- **Claude Code calls outside the transcripts,** if any, such as title generation.
- **The suite's length before the conversion.** It had 575 scenarios against 319 after. The counterfactual uses the
  390 s suite i67 measured after the conversion.
- **Branch review cost for an initiative larger than one work-item** is unmeasured. $1.50 and $2.50 scale i67's $0.76
  by review time (i46's took 3.1× as long).
