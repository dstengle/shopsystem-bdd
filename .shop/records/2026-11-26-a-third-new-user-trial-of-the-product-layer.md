---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-26-a-third-new-user-trial-of-the-product-layer
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-26
---

# A third new-user trial of the product layer

A fresh agent played a new user of the plugin on a fresh repository ("Trial User", no GitHub), with a clean clone of main at 5593743b4 as `$CLAUDE_PLUGIN_ROOT`, reading only the README, docs, skills, `--help` and command output (never scripts/ or tests/). The product: a community garden, one bounded context `bounded-context/example.org/garden/plots` with capabilities `plots` (request, allocate, log a harvest) and `watering` (a watering rota); from `migrate init` through the product declarations, one item with model lines, vocabulary, four job-serving groups, `spec check --item`, `spec trace --item`, `work ready`, `work batch start` (batch-1 building), then the take-back commands and likely mistakes. It is the third trial of the day and checks the second's findings.

## Summary

Every command answered in under 0.7 s (grammar already installed). `migrate init`, the product, actor, job, subdomain, context and assign commands and the unassign and drop commands mostly refuse mistakes clearly and in the user's terms. Of 10 prior findings, 6 fixed, 3 partly (3, 9, 13), 1 not as a sibling (1). New majors: `spec plays` accepts a bounded context the product never declared, adding it to the product file and mapping there without checking its model; and wrong parts of speech pass `work line --term` and every later check. Minor: a product actor before any product; no form check on the product id; a gloss after `Frame:` read as part of the frame; a second area cannot read the first area's actor through an item; how a line states a refusal reason undocumented; rewording a term with identical text gives a raw git error; v_t7's message repeats itself.

## Steps

`C` is `bounded-context/example.org/garden/plots`.

| # | command | time | outcome |
|---|---|---|---|
| 1 | `git init -b main`, venv, pytest 9.1.1, pytest-bdd 8.1.0 | 3.2 s | ok |
| 2 | `shop --help`, `shop tools probe` | 34 ms, 133 ms | clean, no internal ids; grammar block |
| 3-4 | `migrate init --id community-garden` / `bounded-context/communitygarden/plots` | <0.1 s | refused clearly |
| 5 | `migrate init --id C --purpose ...` | <0.2 s | founded, one commit |
| 6 | `spec actor "the gardener"` before any product | 89 ms | **accepted**; file has `actors`, no id |
| 7-8 | `spec product garden`; then `spec product example.org/garden` | ~95 ms | **accepted** with no dot; second silently replaces the id |
| 9 | `spec actor gardener` (no "the") | 93 ms | accepted |
| 10-13 | `spec job` with no `--actor`, a malformed statement, an unknown actor, a mismatched actor | ~78 ms | each refused |
| 14-16 | four jobs declared; an unknown need and a cycle | ~80-90 ms | declared; refused |
| 17-19 | `spec subdomain` with `--type main`, an unknown `--serves`; three declared (any id form, `Watering_Rota`) | ~85 ms | refused; declared |
| 20-23 | `spec context plots`, `example.com/...`, `--addresses nowhere`; C and `.../rota` | ~110 ms | refused; declared |
| 24 | `spec assign water-plants --to C` | 117 ms | refused: no job of the product (fixed) |
| 25-26 | assign to `.../nowhere`, `plots`; four jobs to C; repeats | ~110 ms | refused; assigned; repeats refused |
| 27 | `spec plays "the farmer" --in C --as "nobody at all"` | 80 ms | refused on the product actor first (fixed) |
| 28 | `spec plays "the gardener" --in .../nowhere --as "the gardener"` | 98 ms | **accepted and committed**: undeclared context created |
| 29 | `spec plays "the gardener" --in C --as "the gardener"` | 80 ms | refused: C's model holds no actor (only on the item) |
| 30-31 | `work idea`, `work shape`, `work line --capability plots` / `watering` | ~125 ms | ok |
| 32 | `work line --model` with `lifecycle status: free → requested → allocated` | 158 ms | accepted; v_m8 later (the docs say `;`) |
| 33-35 | `--term` `(verb) → object plot`; `(noun) → operation garden.request`; verb with no `Frame:` | ~160 ms | **accepted** |
| 36 | `--term` with a two-sentence gloss | 138 ms | refused v_t7 (message repeats itself) |
| 37 | `--term` `bed → object bed`, `attribute plot.size` | ~135 ms | refused v_t19 |
| 38 | `--term` with `Frame: actor requests plot.` | 135 ms | accepted |
| 39 | `--term` with no arrow; `(thing)` | ~115 ms | refused |
| 40 | `--term "- **log** (verb) → ..."` (no aspect) | 147 ms | **accepted** |
| 41-42 | `--remove-term plot` (two entries), by `word → element`; `nothing-here` | ~120 ms | asks which, removes; refused |
| 43-44 | `--reword-term plot` two sentences; `(verb) → object plot` | ~150 ms | refused v_t7; **accepted** |
| 45 | `--reword-term take` with identical text | 119 ms | **raw `git commit failed ... On branch main`** |
| 46 | `spec parse --item b1 "When the gardener requests a plot, ..."` | 409 ms | refused at "requests", no hint of the bad frame |
| 47 | `spec check --item b1` | 166 ms | v_t13 per frame; bracketless explained; gloss after `Frame:` read as frame |
| 48 | `--reword-model`, `--reword-term` | ~150 ms | ok |
| 49-50 | lines with `--serves` x4; `--serves allocat-plots` | ~120 ms | echoed with text (fixed); typo refused |
| 51 | `spec check --item b1` | 489 ms | v_m1: watering#r1's "the gardener" is a word of plots |
| 52 | `work line b1 --remove watering`; `--capability watering --area plots`; again | ~130 ms | ok |
| 53 | `spec parse --item b1` of `a plot that is not \`requested\`` | 144 ms | refused at "is"; `whose status is not` parses |
| 54 | `work line b1 --reword plots#r3 ...` | 117 ms | `plots#r3 reworded` (no text) |
| 55-56 | `spec check --item b1` | 214 ms | v_m4 for reason `not requested`; after renaming to `status`, 0 violations, no v_s3 (fixed) |
| 57 | `spec trace request-plot` (no `--item`) | 152 ms | refused with "trace it with --item b1" (fixed) |
| 58-59 | `spec trace <job> --item b1`; `no-such-job`, `--item b9` | ~110-165 ms | full traces; "served by no requirement group" / "no item b9" |
| 60-61 | `work ready b1` (unrated); `work rate --value 3` then right values | ~110-490 ms | ready; refused listing values, then rated |
| 62 | `work batch start` | 689 ms | batch-1 building |
| 63 | `spec plays ... --in C` after start; `work batch next batch-1` | 110, 166 ms | refused (model on batch-1 only); "prepare task" |
| 64-68 | `spec unassign`, `spec drop job/actor/subdomain/context` held, needed, twice, unknown, short id | ~75-95 ms | refused naming the referrer; dropped; refused (no no-op "dropped"); **dropped `nowhere` from step 28** |
| 69 | scratch b2: `(verb) → object`, `(adjective) → service`, `(verb)` no frame or aspect; `spec check --item b2` | 142 ms | only v_t14; wrong parts of speech never caught |

## Prior findings

| # | prior finding | status | evidence |
|---|---|---|---|
| 1 | `spec assign` accepted an undeclared job | fixed for assign, not for a sibling | `job water-plants is no job of the product`; `spec plays` accepts an undeclared bounded context (finding 1) |
| 2 | `spec check --item` failed a correct item with v_s3 | fixed | `0 violations, 1 warnings` |
| 3 | `work line --term` accepted vocabulary mistakes | partly | v_t4 (unknown part of speech), v_t7, v_t19 refused; a verb with no frame, no aspect (v_t14), a Frame that doesn't read (v_t13) and wrong parts of speech (`(verb) → object`, `(adjective) → service`, `(noun) → operation`) accepted; `--reword-term` the same |
| 4 | Frame without angle brackets refused unhelpfully | fixed at `spec check` | v_t13 `takes no noun phrase: a frame names its slots in angle brackets, each a kind, an actor or a parameter of its operation`; `spec parse --item` still only `does not parse at requests` |
| 5 | no-op drops said "dropped" | fixed | `product actor gardener is no product actor of the product` |
| 6 | drop refusal garbled tail | fixed | `the job allocate-plots needs request-plot: drop it first, or declare it again without the need` |
| 7 | plays checked `--as` first; job with no `--actor` accepted | fixed | `product actor 'the farmer' is no actor of the product`; `spec job` without `--actor` refused |
| 8 | trace without `--item` no hint | fixed | `...; the item b1 holds one that serves it: trace it with --item b1` |
| 9 | `work line` confirmed inconsistently | partly | lines echo text; `--reword` says `plots#r3 reworded`, `--term` `10 vocabulary entries of plots`, `--reword-term` `term log reworded` |
| 13 | docs pack list, `shop --help` ids, product_actor in usage | partly | index and `shop --help` clean; `spec job` usage `[--actor PRODUCT_ACTOR] --statement JOB_STATEMENT`; `spec --help` says "design model v5" and "`--check` gives v_t4-v_t10" |

## Findings

1. **major: `spec plays` creates an undeclared bounded context.** `shop spec plays "the gardener" --in bounded-context/example.org/garden/nowhere --as "the gardener"` -> `mapped the product actor the gardener to the gardener in the bounded context bounded-context/example.org/garden/nowhere`, exit 0, committing `[contexts."bounded-context/example.org/garden/nowhere".actors] "the gardener" = "the gardener"`. `--as` unchecked there, while for C the same `--as` is refused; `spec assign` refuses the same id.
2. **major: wrong parts of speech pass every check.** Accepted by `work line --term`/`--reword-term`: `- **plot** (verb) → object plot.`, `- **plot** (noun) → operation garden.request.`, `- **tool** (verb) → object tool.`, `- **the shed service** (adjective) → service shed.`; `spec check --item b2` reported only `v_t14 ... borrow` and `v_m7`.
3. **minor: `--term` refuses some lexicon rules, not others:** a verb with no aspect accepted (`spec check` v_t14); a verb with no `Frame:` accepted and v_t11 never reported for `borrow`; a bracketless `Frame:` accepted (`spec check` v_t13).
4. **minor: a gloss after `Frame:` is read as part of the frame:** `v_t13 ... the Frame: "<actor> allocates <plot>. What the coordinator does ..." does not read at "plot. What the coordinator does ..."`; nothing says a frame must be last.
5. **minor: two new areas on one item cannot share an actor:** `v_m1 ... watering#r1, the gardener, the gardener is a word of plots, which the area watering does not read`; no `work line` option adds an area import.
6. **minor: how a line states a refusal reason is undocumented:** `refused: not requested` with `... shall refuse the request and name the status of the plot.` left `v_m4 garden.allocate, not requested`; renaming the reason `status` cleared it.
7. **minor: rewording a term with identical text:** `work: git commit failed in the repository /…/app: On branch main`, exit 1.
8. **minor: the product file accepts unformed declarations:** an actor before any product; `spec product garden` (no dot); a second `spec product` silently replacing the id; `spec actor gardener`, `spec subdomain Watering_Rota`.
9. **minor: v_t7's message repeats itself:** `(spec/vocabulary/plots.md: the entry's gloss is more than one sentence; the entry's gloss is more than one sentence)`.
10. **info: `spec plays` cannot be done before the first batch merges**, and its refusal (`it holds no actor`) doesn't say the actor is on b1.
11. **info: `spec trace no-such-job --item b1`** says `served by no requirement group`, not that the job is no job of the product.
12. **info: quoting inconsistent:** `product actor 'the gardener'` vs `product actor the nobody is no product actor of the product`.
13. **info: grammar refusals with nothing to act on:** `a plot that is not \`requested\`` refused at "is" with `may follow: conform`; `work ready` readies an unrated item.
14. **info: the laid capability says `specifies: service plots`, but its service is `garden`.**
