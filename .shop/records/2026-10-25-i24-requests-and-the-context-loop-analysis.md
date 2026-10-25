# shopsystem-bdd, i24-requests-and-the-context-loop: analysis

Plugin 0.25.0 (`.claude-plugin/plugin.json:4`). Window 2026-10-24T22:22:07+00:00 to 2026-10-25T03:12:32+00:00. Measurement: `.shop/records/measurements/2026-10-25-i24-requests-and-the-context-loop.md`. Compared with: `.shop/records/measurements/2026-10-23-i22-rulings-round-trips-query-output.md` (the measurement before this one; no i23 measurement exists).

Size: 43 work-items (w121–w163; 40 green, 3 withdrawn), 203 stages, 4 branch reviews. i22 had 10 work-items (w91–w100), 45 stages and 2 branch reviews.

## The delivery

`measure show` prints a 203-row stages table. Its rows are cited by work-item and stage below; the full table is in the measurement record. The work-items table and the totals, as `measure show` printed them:

```
work-items
work-item                         | transitions | awaiting answer | failed | commits
----------------------------------+-------------+-----------------+--------+--------
w121                              | 14          | 3               | 1      | 2
w122                              | 8           | 0               | 1      | 1
w123                              | 8           | 0               | 1      | 3
w124                              | 6           | 0               | 0      | 3
w125                              | 9           | 1               | 0      | 1
w126                              | 8           | 1               | 0      | 1
w128                              | 8           | 1               | 0      | 1
w127                              | 8           | 1               | 0      | 1
w129                              | 6           | 0               | 0      | 1
w130                              | 10          | 2               | 0      | 2
w131                              | 6           | 0               | 0      | 2
w133                              | 10          | 1               | 1      | 1
w132                              | 6           | 0               | 0      | 1
w134                              | 10          | 2               | 0      | 1
w137                              | 10          | 1               | 1      | 2
w138                              | 8           | 1               | 0      | 1
w135                              | 10          | 2               | 0      | 1
w140                              | 6           | 0               | 0      | 1
w139                              | 10          | 1               | 1      | 2
w141                              | 6           | 0               | 0      | 1
w136                              | 4           | 0               | 2      | 0
w142                              | 6           | 0               | 0      | 1
w145                              | 6           | 0               | 0      | 1
w144                              | 8           | 1               | 0      | 1
w143                              | 8           | 0               | 1      | 1
w147                              | 8           | 1               | 0      | 1
w146                              | 10          | 1               | 1      | 2
w148                              | 6           | 0               | 0      | 1
w149                              | 6           | 0               | 0      | 1
w150                              | 6           | 0               | 0      | 1
w151                              | 6           | 0               | 0      | 2
w152                              | 6           | 0               | 0      | 1
w153                              | 6           | 0               | 0      | 1
i24-requests-and-the-context-loop | 1           | 0               | 0      | 0
w155                              | 6           | 0               | 0      | 1
w154                              | 8           | 1               | 0      | 1
w156                              | 3           | 0               | 1      | 0
w160                              | 6           | 0               | 0      | 1
w157                              | 6           | 0               | 0      | 2
w159                              | 6           | 0               | 0      | 3
w158                              | 6           | 0               | 0      | 3
w161                              | 6           | 0               | 0      | 1
w162                              | 9           | 1               | 0      | 1
w163                              | 18          | 3               | 2      | 1

totals
total             | value
------------------+------------------------------
stages            | 203
sessions          | 199
turns             | 6350
round trips       | 4143
output tokens     | 3595825
new input tokens  | 11977419
cache-read tokens | 191142883
cost              | 87.86
time              | 4 hours 50 minutes 25 seconds
```

Stage rows this report relies on, as printed:

```
work-item | stage         | agent               | session                              | took                  | turns | round trips | output tokens | new input tokens | cache read tokens | cost
w133      | research      | code-scout          | 57bbdf20-4d59-41a1-91fd-1d17d80c0ebe | 3 minutes 56 seconds  | 41    | 40          | 42383         | 115825           | 2812254           | 0.17
w137      | research      | code-scout          | eff88d3c-22af-411e-a7fd-f20e4a61e676 | 3 minutes 59 seconds  | 41    | 40          | 44280         | 133744           | 3104554           | 0.23
w139      | research      | code-scout          | a44dd250-3a73-402b-8465-338517c3fb56 | 5 minutes 3 seconds   | 41    | 40          | 57862         | 130692           | 3237477           | 0.25
w136      | research      | code-scout          | a2db0fc1-9119-4289-82ca-58f902a0f7cf | 4 minutes 11 seconds  | 41    | 40          | 43189         | 140866           | 3369838           | 0.26
w136      | research      | code-scout          | 66b6095e-07ce-4b55-a40e-b648f2fe186b | 4 minutes 5 seconds   | 41    | 40          | 38626         | 121217           | 3200741           | 0.21
w143      | research      | code-scout          | 0f040d9f-5c6b-45d7-aa9e-945c12511f92 | 3 minutes 29 seconds  | 41    | 40          | 34359         | 103654           | 2854476           | 0.11
w146      | research      | code-scout          | f46ec820-e974-4c00-9672-2962a31d8208 | 4 minutes             | 41    | 40          | 39632         | 124408           | 3039575           | 0.22
w163      | research      | code-scout          | e52ecfa4-164d-418f-b8db-2cb3cc239de6 | 3 minutes 43 seconds  | 41    | 40          | 41234         | 125070           | 3030841           | 0.19
w134      | implement     | bdd-implementer     | 1b0a6cc5-2864-4d0f-99fe-de21d14e1753 | 12 minutes 35 seconds | 104   | 53          | 34069         | 129542           | 5502281           | 1.41
w138      | implement     | bdd-implementer     | 34488282-d5c8-40f4-8be5-617724a4030d | 7 minutes 46 seconds  | 1     | 35          | 95            | 1170             | 100250            | 0.87
          | branch-review | bdd-branch-reviewer | 6abdc3db-66e7-4860-94c9-8a531073170c | 15 minutes 30 seconds |       | 105         |               |                  |                   |
          | branch-review | bdd-branch-reviewer | a531de94-b0a0-4024-a357-1d2e25a2b639 | 9 minutes 35 seconds  |       | 63          |               |                  |                   |
          | branch-review | bdd-branch-reviewer | 7ec942f2-4220-4257-9223-9a5d060ad08c | 8 minutes 39 seconds  |       | 49          |               |                  |                   |
          | branch-review | bdd-branch-reviewer | 40a5cb56-f76f-43c4-9a58-68a44c547081 | 8 minutes 16 seconds  |       | 54          |               |                  |                   |
```

## Against 2026-10-23-i22-rulings-round-trips-query-output

```
total             | a                              | b                             | ratio
------------------+--------------------------------+-------------------------------+------
stages            | 45                             | 203                           | 4.51
sessions          | 44                             | 199                           | 4.52
turns             | 1530                           | 6350                          | 4.15
round trips       | 892                            | 4143                          | 4.64
output tokens     | 859642                         | 3595825                       | 4.18
new input tokens  | 2674947                        | 11977419                      | 4.48
cache-read tokens | 42721389                       | 191142883                     | 4.47
cost              | 23.51                          | 87.86                         | 3.74
time              | 12 hours 53 minutes 18 seconds | 4 hours 50 minutes 25 seconds | 0.38

total       | a | b | ratio
------------+---+---+------
round trips | 0 | 0 | -
tool uses   | 0 | 0 | -
compactions | 0 | 0 | -
```

The two initiatives are different sizes: i22 had 10 work-items and 45 stages, i24 had 43 work-items and 203 stages (4.3 times the work-items, 4.51 times the stages). Per stage the token figures are about the same: the token ratios are 4.18–4.48 against 4.51 for stages. The cost ratio of 3.74 is below the stage ratio, partly because i24's four branch reviews have no token or cost figures (see Not counted). i22's branch reviews cost 3.69 and 1.84. i22's time includes a w97 review stage of 10 hours 51 minutes 3 seconds, so the time ratio says little.

## Work-items that stopped

25 moves to awaiting-answer and 13 to failed (the measurement's work-items table; the log agrees: `log.jsonl` lines 1–3, 53–1019).

| work-item | what stopped | cause | cited |
|---|---|---|---|
| w121, w122, w123 | failed before research (×1 each) | other: `work run` could not verify a push to origin (no GitHub credential); `work retry` 22 s later | w121.md:17, w122.md:17, w123.md:14; log.jsonl:1-6 |
| w121 | claimed → awaiting-answer | other: the scenario's fixture `work run` loaded the main checkout's `work_items.py` through the inherited PYTHONPATH, not the branch's | w121.md:20-189, :194 |
| w121 | done → awaiting-answer (×2) | other: task review Important (r65's exit under xdist). The answer's fix was never committed before the item was moved to done again; withdrawn and redrafted as w125 | w121.md:190-191, :195; log.jsonl:94-99 |
| w125 | claimed → awaiting-answer | other: whole-suite failures from phase B/C scenarios formulated before any work-item accepted them, so r43 did not count them as expected | w125.md:16, :161 |
| w126 | done → awaiting-answer | decision missing: a `--lines` file that does not exist ends on a traceback, and no scenario pins it; accepted, fixed by w148 | w126.md:14, :17 |
| w127 | researched → awaiting-answer | scenario wrong: the r17 outline needed an Examples table (5d4cc75) | w127.md:17 |
| w128 | done → awaiting-answer | decision missing: requests r8/r9 did not say they hold only for an undelivered request; lines changed, fixed by w149 | w128.md:14, :17 |
| w130 | researched → awaiting-answer | decision missing: whether `work run` is a `work` command under r23 (Reading A/B) | w130.md:14, :18 |
| w130 | done → awaiting-answer | decision missing: `work retry` back to green skips the r23 check; accepted, later branch review F5, fixed by w160 | w130.md:15, :19 |
| w133 | failed | other: researcher reached its turn limit (41 turns) | w133.md:14 |
| w133 | done → awaiting-answer | decision missing: `measure` refusals no line asks for; accepted, later branch review F4, fixed by w161 | w133.md:17, :20 |
| w134 | researched → awaiting-answer | decision missing: which work-item builds the gate rounds r66's scenario needs; w134 got blocked_by w146, w136 | w134.md:15, :19 |
| w134 | done → awaiting-answer | decision missing: a non-Refused exception in an initiative's thread; accepted as an observation | w134.md:16, :20 |
| w135 | researched → awaiting-answer (×2) | decision missing: dependency on w134 and which `work run` starts intake rounds; then how a non-DONE intake round exits | w135.md:15-16, :19-20 |
| w136 | failed (×2) | other: researcher reached its turn limit twice; withdrawn and split into w151, w152 | w136.md:14-15; log.jsonl:425, 462 |
| w137 | failed | other: researcher reached its turn limit | w137.md:14 |
| w137 | researched → awaiting-answer | decision missing: three readings (merge order, a gate with no question, a faulted round) | w137.md:20 |
| w138 | done → awaiting-answer | other: plan decision 4 said ranges are included, and the implementation matched by equality; fixed by w150 | w138.md:14, :17 |
| w139 | failed | other: researcher reached its turn limit | w139.md:14 |
| w139 | done → awaiting-answer | decision missing: the analysis session's result and a non-DONE branch review were unpinned; fixed by w153 | w139.md:17, :20 |
| w143 | failed | other: researcher reached its turn limit | w143.md:17 |
| w144 | done → awaiting-answer | other: the review's finding was on a skill section that w143 removes; accepted as moot | w144.md:17, :20 |
| w146 | failed | other: researcher reached its turn limit | w146.md:14 |
| w146 | done → awaiting-answer | decision missing: no line for a round's non-DONE outcome; fixed by w154 | w146.md:19, :22 |
| w147 | done → awaiting-answer | decision missing: a faulted delegated-answer session; fixed by w155 | w147.md:15, :18 |
| w154 | researched → awaiting-answer | decision missing: what "ends" means in r85 | w154.md:14, :17 |
| w156 | failed after research | other: the research probe repository inside the stage directory changed the main checkout while the planner worked; withdrawn and replaced by w157–w161 | w156.md:14; log.jsonl:841 |
| w162 | claimed → awaiting-answer | scenario wrong: R2-F1's case needed a new @r79 scenario (e3fbf0b) | w162.md:18 |
| w163 | failed (×2) | other: researcher reached its turn limit; then probe repositories in the stage directory changed the checkout during planning | w163.md:15, :18 |
| w163 | claimed → awaiting-answer (×2) | scenario wrong: the @r84 scenario was missing and the implementer may not write it (c552fa6c); then a rebase onto it | w163.md:21-22, :26-27 |
| w163 | done → awaiting-answer | scenario wrong: the Then reads "one commit" and the step accepts two; accepted as it stands | w163.md:23, :28 |

By stage: 13 of the 25 awaiting-answer moves came from task reviews (done → awaiting-answer), 7 from planners (researched → awaiting-answer) and 5 from implementers (claimed → awaiting-answer). By cause, the 13 failures were: researcher turn limit 8, push credential 3, probe files in a stage directory 2.

## Findings

Branch reviews 1–4 gave no Critical finding. Every Important one is listed, including those triaged as observations.

| finding | grade | found by | earliest it could have been found | cited |
|---|---|---|---|---|
| BR1 F1: delegated answers fail on a node with two or more questions (w147) | Important, fix now | branch review 1 | formulation of r77: its scenario had one question per node. Two-question gates were already in r68/r85 | runs/branch-review/1/findings.md:114-134 |
| BR1 F2: a `proposed` initiative that fulfils no request is left invalid (w151) | Important, fix now | branch review 1 | w151's task review. i24 had already met the same failure itself (observation 2026-10-25-integrate-round-without-request) | runs/branch-review/1/findings.md:136-159 |
| BR1 F3: `model check` rejects `awaiting-answer` and `withdrawn` (w131, w146) | Important, fix now | branch review 1 | w146's plan: the branch added the statuses to term/status and the plan did not name `model_work.STATUSES` | runs/branch-review/1/findings.md:161-172 |
| BR1 F4: `measure` refusals no line asks for (w133) | Important, fix now | w133's task review, then branch review 1 | w133's task review, which found it. It was accepted under the delegation | w133.md:17, :20; runs/branch-review/1/findings.md:174-188 |
| BR1 F5: `work retry` to green skips r23's check (w130) | Important, fix now | w130's task review, then branch review 1 | w130's task review, which found it. It was accepted under the delegation | w130.md:15, :19; runs/branch-review/1/findings.md:190-198 |
| BR1 F-obs-1: a thread crash exits 0 (w134) | Important, observation | w134's task review | w134's task review (found there) | w134.md:16; runs/branch-review/1/findings.md:232 |
| BR1 F-obs-2: the answer pass runs once a run (w147) | Important, observation | w147's task review | w147's task review (found there) | w147.md:18; runs/branch-review/1/findings.md:233 |
| BR1 F-obs-3: hooks act in worker sessions (w124) | Important, observation | branch review 1 | w124's plan: hooks load in every session `work run` starts | runs/branch-review/1/findings.md:234-238 |
| R2-F1: a `fulfils` naming a missing request is left invalid (w158) | Important, fix now | branch review 2 | w158's plan, which named it as open case B and left it | runs/branch-review/2/findings.md:131-160 |
| R3-F1: a DONE integrate round leaves its stage directory uncommitted (w151) | Important, fix now | branch review 3 | w151's task review. w162's researcher found it (notes D3) and w162's plan listed it as an open case | runs/branch-review/3/findings.md:133-157 |
| R3-F2: r79's line does not state the two held-back cases (w158, w162) | Important, observation | branch review 3 | the delegate's ruling on w158 (331acaf), which made the scenario say more than the line | runs/branch-review/3/findings.md:175-200 |

## Work-items added

The first work-items drafted were w121–w124 (phase A, 22:21). Phase B (w126–w133, 23:12) and phase C (w134–w147, 23:21) were drafted in the order initiative.md:18 sets, so they are not counted as added. Seventeen work-items were added beyond those:

| work-item | caused by | cited |
|---|---|---|
| w125 | hand-back: w121 withdrawn, because the fix the answer asked for was never committed; redraft | w125.md title; w121.md:191 |
| w148 | task-review finding on w126, accepted | w126.md:17 |
| w149 | task-review finding on w128 (spec lines r8/r9 changed) | w128.md:17 |
| w150 | task-review finding on w138 | w138.md:17 |
| w151, w152 | re-count: w136 split after its researcher reached the turn limit twice | w136.md:14-15; w151/w152 titles "(split of w136)" |
| w153 | task-review finding on w139 | w139.md:20 |
| w154 | task-review finding on w146 | w146.md:22 |
| w155 | task-review finding on w147 | w147.md:18 |
| w156 | branch review 1, drafted by `work run` as one work-item for all its findings; withdrawn after a planner fault | w156.md:14; runs/branch-review/1/findings.md:241 |
| w157–w161 | branch review 1 F1–F5, drafted by hand, one a finding (F-obs-6) | w157–w161 titles; runs/branch-review/2/findings.md:221 |
| w162 | branch review 2, R2-F1 | w162.md findings |
| w163 | branch review 3, R3-F1 | w163.md findings |

## Observations

- 8 of the 13 failures were researcher sessions that ended at the turn limit (41 turns, 40 round trips). Those 8 rows add up to 341565 output tokens, 995476 new input tokens, 24649756 cache-read tokens and a cost of 1.64. The sums are 42383+44280+57862+43189+38626+34359+41234+39632 output tokens, and 0.17+0.23+0.25+0.26+0.21+0.11+0.22+0.19 for cost. Each of those stages was then run again. (stages rows w133, w137, w139, w136 ×2, w143, w146, w163 research)
- 13 of the 25 awaiting-answer moves were task reviews moving a done work-item back. 8 of those findings became added work-items (w148, w149, w150, w153, w154, w155, then w160 and w161 by way of branch review 1). (work-items table; Work-items added above)
- The branch review ran 4 times. Reviews 2 and 3 each found one new fix-now finding, in a fix work-item (w158) or an earlier one (w151). In both cases a planner had listed the finding as an open case first: w158's plan open case B, and w162's plan with w162's research D3. (runs/branch-review/2/findings.md:141; runs/branch-review/3/findings.md:153)
- All 7 planner stops put a Reading A / Reading B choice on a spec line. All 24 `work answer` transitions were made by the coordinator under the person's delegation. (log.jsonl `"by": "work answer"` ×24; w127.md:17, w130.md:18, w134.md:19, w135.md:19-20, w137.md:20, w154.md:17)
- Probe files a researcher left in its stage directory faulted two planner stages (w156, w163). Branch review 4 found 224 probe files tracked under runs/w163/2-research/probe_repos/, the third time this has happened. (w156.md:14, w163.md:18; runs/branch-review/4/findings.md:205-210)
- Against i22, the stage count was 4.51 times larger and the time 0.38 times as long (4 hours 50 minutes 25 seconds for 203 stages). (compare table)

## Candidates

- Try: keep researcher sessions from ending at the turn limit, either with a narrower brief or by having the session stop and hand over its notes before the limit. Rests on: 8 of 13 failures were turn-limit research sessions, each run again. It worked if: the failed column's total (13 here) falls, and the stages table has fewer code-scout rows at 41 turns.
- Try: settle the open cases a plan lists, which today it leaves unchosen, before the implement stage, so they do not come back as review findings. Rests on: 13 awaiting-answer moves from task reviews, 8 added fix work-items, and branch reviews 2 and 3 each finding a case a plan had listed. It worked if: the done → awaiting-answer moves, the work-items added after the first drafting (17 here) and the branch-review stages (4 here) fall.
- Try: count the branch-review sessions' tokens and a session's whole usage when its session.json ends on a follow-up result. Rests on: four branch-review rows with no token figures, and the w138 implement row (1 turn, 95 output tokens in 7 minutes 46 seconds). It worked if: the branch-review rows show output, new input and cache-read tokens and a cost, and no implement row shows 1 turn for a stage that made a commit.

## Not counted

- **Branch-review tokens and cost.** The four branch-review rows give only time and round trips. Their session.json files do hold usage: runs/branch-review/1/session.json gives 62890 output tokens, 13703088 cache-read tokens and total_cost_usd 5.91. These are not in the measurement's totals, so the totals and the cost ratio against i22 are low by the four reviews.
- **w138's implement stage.** The measurement took the usage of the session's last result, a one-turn reply to a task notification (95 output tokens, 100250 cache-read tokens). The same session.json's modelUsage gives 21384 output tokens and 2750562 cache-read tokens (runs/w138/3-implement/session.json). Other stages with a follow-up result may be under-counted the same way; I did not check them.
- **The sessions around the delivery.** The measurement was made without `--sessions`, so `compare`'s second table is all 0. That includes the coordinator's session, which made the integrate and formulate rounds (`spec:`/`features:` commits) and all 24 delegated answers.
- **Per-agent sums.** This session was not allowed to run a script over the measurement's JSON, so the report gives no total per agent or per stage kind. The one sum it gives is the 8 turn-limit rows, worked by hand above.
- **w147's task-review question and w135's third question** are long lines that I read only in part. Their causes are taken from the questions' opening and from the answers (w147.md:18, w135.md:20).
