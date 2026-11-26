---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-26-a-second-new-user-trial-of-the-product-layer
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-26
---

# A second new-user trial of the product layer

A fresh agent played a new user of the plugin as the next release would ship it: a clean clone of main at 39c060967 (plugin 0.44.0), used as `$CLAUDE_PLUGIN_ROOT`, on an empty git repository (`trial2/app`, branch `main`, no remote, no GitHub), reading only the README, docs, skills, `--help` and command output. The scenario: a "book club" product (members propose books, the club picks the next one, members rate what they read), declared through the product layer, then an item whose groups serve its jobs, checked and traced before a batch, readied, a batch started, then the take-back commands and likely mistakes. It is the second trial of the day; it checks each finding of the first.

## Summary

A new user gets all the way through: context founded, product declared, item shaped, checked and traced with `--item`, readied, batch started (`batch-1 building: t1 b1 ...`). Every product command took 0.07-0.12 s, `spec check --item` 0.15-0.4 s, `work ready` about 0.5 s, `work batch start` 0.66 s (GF's caches were warm).

Most findings of the first trial are fixed. Top problems now: (1) `spec assign` accepts a job the product does not hold; (2) `spec check --item` fails a correct item with one `v_s3` per group, exit 1; (3) vocabulary mistakes still pass `work line --term`; (4) a Frame without angle brackets is refused unhelpfully; (5) several refusals and acknowledgements mislead.

## Steps

| # | command | time | outcome |
|---|---|---|---|
| 1 | `git init -b main`; venv with pytest 9.1.1, pytest-bdd 8.1.0 | 3.2 s | ok |
| 2 | `shop tools probe` | <0.1 s | gf 3.12.0, pgf 1.1, clingo 5.8.2, gf-rgl 20250812 |
| 3 | `shop migrate init --id bounded-context/example.org/bookclub/club --purpose "..."` | 0.13 s | scaffold committed, `imports: [base, request]` |
| 4 | `spec product example.org/bookclub --purpose "..."` | 0.09 s | declared |
| 5 | `spec actor "the member"`, `"the organiser"` | 0.09 s each | declared |
| 6 | `spec job` with 3 malformed statements, an actor mismatch, an unknown actor, an unknown need | 0.06-0.08 s | all refused |
| 7 | `spec job propose-books / pick-next-book (--needs) / rate-books (--needs)` | 0.08-0.09 s | declared |
| 8 | `spec job propose-books ... --needs rate-books` | 0.07 s | refused: closes a cycle |
| 9 | `spec subdomain reading-circle --type core --serves` x3 | 0.09 s | declared; `--type Core` and an unknown `--serves` refused |
| 10 | `spec context` short form, trailing `/`, uppercase domain, outside the product | 0.10-0.11 s | each refused |
| 11 | `spec context bounded-context/example.org/bookclub/club --addresses reading-circle --shop ...` | 0.12 s | declared |
| 12 | `spec assign` to an undeclared context / with the short form | 0.08-0.09 s | refused |
| 13 | `spec assign find-books --to ...` (job never declared) | 0.09 s | **accepted** |
| 14 | `spec assign` x3, then the same job again | 0.09-0.11 s | assigned; the repeat refused |
| 15 | `spec unassign find-books`, then again | 0.09 / 0.07 s | done / refused |
| 16 | `spec plays "the member" --in ... --as "the member"` | 0.11 s | refused: the model holds no actor until the batch merges |
| 17 | `work idea`, `work shape`, `work line --capability club` | 0.11-0.12 s | ok |
| 18 | `work line --model` (book, rating, service club, actor) | 0.15 s | ok |
| 19 | 5 bad `--term`s (missing element, `(thing)`, no Frame, no aspect, two sentences) | 0.14 s each | **all accepted** |
| 20 | `spec check --item b1` | 0.15 s | catches `v_t19` and `v_t14` only |
| 21 | `--reword-term` / `--remove-term` with `--into`, no `--` | 0.11-0.13 s | works; an ambiguous name gets a helpful refusal |
| 22 | 15 `--term`s in one call (including `Frame: <actor> lists the books.`) | 0.15 s | ok |
| 23 | `spec parse --item b1 "<line>"` | 0.43 s | one tree |
| 24 | `work line ... --serves propose-book` (typo) | 0.10 s | refused |
| 25 | 4 lines with `--serves`, 1 without | 0.11-0.12 s | ok; the line and the pair confirmed |
| 26 | `spec check --item b1` | 0.22 s | **5 violations (`v_s3`), exit 1** |
| 27 | `spec trace propose-books` / `--item b1` / `rate-books --item b1 [--json]` | 0.13-0.16 s | refused without `--item`; correct trace with it, needs followed, `coordination: null` |
| 28 | `work rate b1`; `work ready b1` | 0.11 s; 0.46 s | ready |
| 29 | `work batch start` | 0.66 s | `batch-1 building`; worktree, feature with 5 scenarios, brief written |
| 30 | `spec trace propose-books --item b1` (item in batch) | 0.16 s | works |
| 31 | `spec drop job / actor / subdomain / context` on things still referred to | 0.07 s | refused, naming the referrer |
| 32 | `spec drop job nothing-here`; `spec drop context example.org/bookclub/club` | 0.07 s | **"dropped ..." exit 0** (no commit) |
| 33 | Full take-back cycle: second context, unassign, assign elsewhere, re-assign, drop context, subdomain, actor | 0.07-0.12 s | all work, one commit each |
| 34 | `migrate init` on a `master` repository | 0.13 s | warns about `master` |
| 35 | Malformed frames in a fresh context, `spec check --item`, `work ready` | 0.39 s | unhelpful parse refusal (finding 4) |

## Prior findings

- **1 No product walkthrough: fixed.** getting-started §8 walks through product, actor, job, subdomain, context, assign, plays, unassign/drop, `--serves`, and `trace`/`check --item`; concepts and commands cover them.
- **2 Ids in two forms: fixed** (`spec context example.org/bookclub/club` -> `id ... is not of the context id form bounded-context/<domain>/<path>`; trailing `/` and uppercase refused). Partly: `spec drop context` of the short form still answers `dropped ...` (finding 5).
- **3 assign creating a context, nothing undoable: fixed** (`--to ... is no bounded context of the product`; unassign and four drops work and refuse while referred to). New hole of the same kind: assign accepts an undeclared job (finding 1).
- **4 recipes-shaped Frame: fixed for that shape** (`Frame: <actor> picks <book>.`, `Frame: <actor> lists the books.` read). A Frame without `<>` is still refused unhelpfully (finding 4).
- **5 serves not checkable before a batch: fixed** (`spec check --item` drops `w_unserved_job`; `spec trace --item` prints the trace with needed jobs), marred by finding 2.
- **6 job statement refusal hides its cause: mostly fixed** (`the job statement mentions 'the reader', no actor of the product: declare it with spec actor, then give it as --actor`). A pure form error only restates the form without saying which part is wrong.
- **7 statement's actor vs --actor: partly fixed.** Mismatch refused; with no `--actor` the job is declared with `actors = []`; with `--actor "the reader"` (not a product actor) the message blames the statement.
- **8 `product_actor` leak: not fixed in argparse** (`usage: shop spec drop actor [-h] [--json] product_actor`; the same in `spec plays`). Domain refusals are clean.
- **9 --serves unknown job: fixed** (`work line: --serves: the product holds no job propose-book`).
- **10 rewording a term: fixed.**
- **11 --serves confirming the line: fixed.** A plain `work line` still prints only the id (finding 9).
- **12 vocabulary mistakes only at work ready: partly fixed.** `work line --term` accepts every mistake tried; `spec check --item` catches `v_t19` and `v_t14` only.
- **13 docs drift: mostly fixed.** Imports, usage lines (`usage: shop <command> ...`) and the coordination line match. Left: docs/index.md lists packs "`request`, `spec`, `time`; `cli` retired" without `base`; `shop --help` shows "(decision 0132)", "(adapter_cli_respond's notice, b631)".
- **14 no warning on master: fixed** (`warning: this bounded context is founded on the branch master, not the base branch main; ...`).
- **16 coordination line: consistent** (`"coordination": null` with no port); saga and other kinds not exercised.

## Findings

1. **major: `spec assign` accepts an undeclared job.** `shop spec assign find-books --to bounded-context/example.org/bookclub/club` -> `assigned the job find-books to the bounded context bounded-context/example.org/bookclub/club`, exit 0; `spec check` then warned only `w_unserved_job job/example.org/bookclub/club/find-books` as if it were real.
2. **major: `spec check --item` fails a correct item.** On b1, which `work ready` passed right after: `v_s3  a group has no scenario  (5)  ... club#g1 ... #g5`, `5 violations, 1 warnings`, exit 1. getting-started §8 suggests nothing else changes. (Idea b808 already.)
3. **major: vocabulary mistakes go through `work line --term`.** Each printed `a vocabulary entry of club`, exit 0: `- **book** (thing) → object book. ...`; `- **propose** (verb, action) → operation club.propose. Forms: proposes, proposed.` (no Frame); `- **book** (noun) → object book. A book. A member proposes it.`; `- **novel** (noun) → object novel. ...` (no such element). `spec check --item` reported only `v_t14` and `v_t19`; `spec lexicon` has no `--item`.
4. **minor: a Frame without angle brackets is refused unhelpfully.** `Frame: the member removes a book.` gave no `v_t13`; `work ready`: `shelf#r1: does not parse at book (token 6 of 20); parsed up to: When the member removes a; nearest words: book, books`; `spec parse --item` added `may follow: book`. `Frame: <member> lists the books.` was accepted silently.
5. **minor: no-op drops claim success.** `spec drop job nothing-here` -> `dropped the job nothing-here`, exit 0; `spec drop context example.org/bookclub/club` -> `dropped the bounded context ...`, skipping the id-form check.
6. **minor: a drop refusal has a garbled tail.** `spec drop job propose-books` -> `spec: the job pick-next-book needs propose-books: drop it first, or declare it again without the need; pick-next-book`.
7. **minor: `spec plays` checks `--as` before the product actor** (`--as 'the member' is no actor of the domain model ...; it holds no actor`, never that `the reader` is no product actor), and does not say the actor is on a batch not yet merged.
8. **minor: `spec trace <job>` without `--item` gives no hint** (`spec: job propose-books is served by no requirement group`, with b1 in batch-1 serving it).
9. **info: `work line` confirms inconsistently** (with `--serves` the line's text; without, only `club#r5`).
10. **info: a new item cannot add to a capability only in a batch** (`there is no codified capability club in spec/capabilities/; it is new on b1 ... in batch-1, and its lines go into that item`): clear, but blocks a second item until the merge.
11. **info: removing a served job from a subdomain means declaring the subdomain again** with its type and every other job.
