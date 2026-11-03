---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-03-gf-conversion-e2e
kind: report
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-03
---

# The GF conversion: the live run (P16)

This record is evidence, not a gate (design §18 point 28). One real request went through the converted system with
the real `claude` (Claude Code 2.1.317), from `work request` to a `done` initiative. **Request q47** became
**initiative i67**, and i67 reached `done` with its one work-item, w247, `green`.

## Where it ran

- Scratch branch `gfc/P16-live`, cut from `gf-conversion` at 11158f12 (the layer 5 gate). The scratch branch is in a
  clone in the session's scratchpad (`.../scratchpad/p16/live`). Its `origin` is a local bare repository
  (`.../scratchpad/p16/remote.git`), so `work run`'s pushes (supervision r38) never reached GitHub. The branch was
  not merged or pushed upstream. It ends at be95e5b5, 37 commits past 11158f12.
- `SHOPSYSTEM_GF` was unset, so P1's installer set up the grammar.
- **Scratch-only setup commit** (f27bc347): `work run` with no initiative takes every open initiative. To make the run
  take q47 alone, this commit sets the twelve open initiatives (i39, i45, i47, i49, i52, i53, i55, i56, i58, i59, i60,
  i61) to `abandoned` and the open request q46 to `withdrawn`. A second scratch commit (e29c5c10) does the same for
  i66 (see "What happened", step 3).

## The request

The `raising-a-request` skill was followed:
1. `model lexicon` found the words. `line count` (kind) is a term of code-research.
2. One line was written.
3. `model parse --file` gave one tree on the first try:

```
When the person runs `tools size --limit 3`, `tools` shall print the Python file and the line count.
When (Runs (ActorSubj a_the_person) (CmdCode (CodeLit "`tools size --limit 3`"))) (Shall (ActorSubj a_tools)
  (Print (MoreNP (k_python_file_toNP ...) (OneNP (k_line_count_toNP ...)))))
```

It was raised with `work request "tools size prints each file's line count" --from internal --lines … --delegation
"…answer every question with its recommended reading; questions of a glossary-proposal are the person's."`. The
command printed `q47` and committed d6398f39. The first attempt failed with "git commit failed: Author identity
unknown", because the fresh clone had no `user.name`. It wrote nothing, and it succeeded once the identity was set.

## What happened

| # | command / round | result | took | cost (USD) |
|---|---|---|---|---|
| 1 | `work run` (no initiative): intake of q47 | `initiative-round` intake, 7 turns: line 1 `accepted` ("r40 prints the file only; the line count is a consistent addition") | 11 s session | 0.11 |
| 2 | same run | also started **i66 for q45**, an accepted request that no initiative fulfilled (r103), and began its integrate round | — | not recorded (killed after ~10 s; 9 Sonnet calls, 1846 output tokens) |
| 3 | I stopped the run (exit 143) | removed i66's round worktree and branch; scratch commit e29c5c10 set i66 aside; `work start q47` → **i67** | | |
| 4 | `work run i67`: integrate | r47 replaces r40 in analysis-tools g32. It also drafted a new local term `term/line-count` and a glossary-proposal for it | 19 min 28 s | 0.63 |
| 5 | gate (analysis-tools, glossary) | 2 questions, both left for the person: one is a glossary-proposal's, the other names a term (r162). `work run` exited 3 | 18 s + 14 s | 0.10 + 0.07 |
| 6 | `work answer` ×2 (judgement delegated) | analysis-tools: reading (b), r47 without the new term, since `line count` already exists. glossary: not added | | |
| 7 | `work run i67`: apply | spec commit 70b6e194, analysis-tools `approved` | 44 s | 0.14 |
| 8 | formulate (script, no session) | `features generate analysis-tools`, commit 7cb1f277, `formulated` | ~34 s | 0 |
| 9 | glossary gate again | asked the already-answered question again (see "Defects seen") | 9 s | 0.06 |
| 10 | w247 research (code-scout) | g32 red at the Then step. Production `tools_size` already prints `<path> <count>`, so only the handler changes | 8 min 1 s | 0.03 |
| 11 | w247 plan (bdd-planner) | planned → ready → claimed | 53 s | 0.38 |
| 12 | suite before implement | 769 passed, 1 failed (g32) | 392 s | |
| 13 | w247 implement (bdd-implementer) | 4c19f31d: `analysis_tools_handlers.py` +13/−1 (the Then step checks the file's own count on its line) | 7 min 12 s | 0.28 |
| 14 | merge suite | 770 passed, 0 failed; merged; w247 `done` | 391 s (+384 s to merge) | |
| 15 | w247 review (bdd-task-reviewer) | `green` | 1 min 14 s | 0.38 |
| 16 | branch review (bdd-branch-reviewer) | DONE: no Critical or Important findings, 3 Minor. Suite 770/0, tools check clean, size clean | 2 min 31 s (after ~13 min of runs) | 0.76 |
| 17 | measure + analysis session | `.shop/records/measurements/2026-11-03-i67.md` and `2026-11-03-i67-analysis.md` on the scratch branch; i67 → `done` | ~2 min | not recorded (Opus, 45 calls, 33264 output and 2.1 M cache-read tokens) |

The second `work run i67` exited 0 after 56 min 12 s of wall time. In all, the run took from 07:16 to 08:35 UTC.

**Costs:**
- The measurement records **2.08 USD** for i67's nine sessions, over a window of 1 hour.
- With the intake (0.11) and the branch review (0.76), whose costs the measurement leaves out, the recorded total is
  **2.95 USD**.
- Not recorded in USD: the analysis session and the killed i66 integrate session (token counts are in the table).
- The `measure` analysis compares i67 with i64, an earlier initiative of the same size measured under 0.29: i67 cost
  0.53 times as much (3.91 → 2.08) and took 0.80 times as long.

## What the conversion showed working

- The request line parsed on the first try, in the context's own grammar, through `model parse` and `work request`.
- The integrate round wrote a codified requirement (r47 retiring r40, with `retired: [r40]`). `work run` accepted it
  with no send-back.
- Formulate is a script: `features generate` regenerated g32 from r47 with no session, and the branch reviewer
  confirmed it was identical to the gate's preview.
- The implementer wrote only a handler (§14) and never edited the feature. Production code was unchanged because it
  already printed the count.
- Suite at the end: 770 passed, 0 failed. `tools check`, `tools size`, `features bindings` and `features deprecated`
  were clean.

## Defects seen (not fixed here; for the queue)

1. **Integrate round drafts a term that exists.** It drafted `term/line-count` although code-research's `## Terms`
   has `line count`. That cost two gate stops and three gate sessions. The analysis record proposes making the round
   look in every capability's `## Terms` first.
2. **An answered glossary-proposal is asked again, and is left `awaiting-answer` when the initiative is `done`.**
   `work answer i67/glossary` returned it to `drafted`. The next run's gate asked the same question again, and i67
   went `done` with the glossary-proposal still `awaiting-answer`. The branch review lists this as Minor finding 3.
3. **The integrate session outlived its result by 9 minutes.** `initiative-round` started `capability-writer` in the
   background. That writer's writes were refused, so the round wrote the drafts itself. Its result was written at
   07:27, but `claude -p` did not exit until 07:36, when the background wait timed out. As a result, session.json
   holds the last result only (1 turn, 3 s), and the measurement's integrate row undercounts turns and tokens.
4. **`work run` with no initiative starts every unfulfilled accepted request** (here q45 → i66) and runs it in the
   same pass. That is r103 as written, but nothing scopes a run to one request's intake. A live run has to set the
   others aside.
5. **`work answer analysis-tools` is ambiguous** ("more than one work-item analysis-tools"), because every initiative
   names its proposal after the capability. The `i67/analysis-tools` form works (r30).
6. **The suite runs four times** (about 390 s each: before implement, at merge, and twice in the branch review),
   filling 26 of the 60 minutes. The research stage also ran the whole suite where it meant to run one scenario. The
   analysis record has both as candidates.
7. q47's `## Resolution` was not written when i67 went `done`, and q47 stays `accepted`.

## Where it stopped

It did not stop early: i67 is `done`. The only things left open are the glossary-proposal (defect 2) and q47's
resolution (defect 7).
