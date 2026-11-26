---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-26-a-new-user-s-trial-of-the-product-layer-on-an-empty-project
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-26
---

# A new user's trial of the product layer on an empty project

A fresh agent played a new user of the plugin as the next release would ship it (a clean clone of main at 719e1935c, used as `$CLAUDE_PLUGIN_ROOT`) on an empty git repository, reading only the plugin's README, docs, skills, `--help` and command output, with no GitHub. The scenario: a household-chores product declared through the product layer, then an item whose groups serve its jobs.

## Summary

Without GitHub, a user gets as far as starting a batch locally (`batch-1 building`). Everything before that works: setup, founding the context, declaring the product (product, actors, jobs with statements and needs, subdomains, the bounded context, job assignment, actor mapping), shaping an item with a capability, model lines, vocabulary and two groups that each serve a job, readying it, and `shop work batch start`.

Two limits: `spec check` and `spec trace` only see an item's groups once a batch has laid them (on main the trace is refused; it prints correctly only in the batch worktree); and building needs the app written and `work batch review` needs a remote and gh. Until the batch merges, the new capability belongs to its item: a second item cannot add lines to it.

Every command took 60-700 ms (the grammar tools were already installed, so a first install was not timed).

Top problems: (1) the product layer has no walkthrough; (2) bounded-context ids come in two forms and the product commands accept both as separate contexts; (3) `spec assign` creates an undeclared context and nothing in the product can be undone but by hand; (4) a `Frame:` shaped like recipes.md's is refused with an unhelpful message; (5) an item's `serves` cannot be checked or traced before a batch.

## Steps

All commands as `python3 $CLAUDE_PLUGIN_ROOT/scripts/shop ...` from the project.

| # | command | time | outcome |
|---|---|---|---|
| 1 | venv + `pip install pytest==9.1.1 pytest-bdd==8.1.0` (shaping-items step 1) | 3.4 s | ok |
| 2 | `shop tools install` | 0.13 s | each tool already installed; prints "no Python file: the analysis tools are not probed or installed" |
| 3 | `shop tools probe` | 0.13 s | grammar block, exit 0 |
| 4 | `git init` gave `master`; renamed to `main` by hand | - | - |
| 5 | `shop migrate init --id bounded-context/example.org/chores/chores-app --purpose "..."` | 0.10 s | refused first for no git identity (clear); then written and committed, `imports: [base, request]` |
| 6-8 | `spec product example.org/chores --purpose ...`; `spec actor` x2; `spec job keep-up` / `share-out`, then `keep-up --needs share-out` | ~0.09 s each | declared, one commit each; a needs cycle refused clearly |
| 9 | bad inputs to `spec job` | ~0.07 s | malformed statement and unknown `--actor` refused; a statement naming a different actor accepted |
| 10 | `spec subdomain chore-keeping --type core --serves ...`; `notifications --type generic`; `--type main` | ~0.09 s | declared; `main` refused clearly |
| 11 | `spec context` with the id with and without `bounded-context/` | ~0.09 s | both accepted, as two contexts |
| 12 | `spec assign` x3, one to `example.org/chores/nowhere` | ~0.09 s | all accepted; `nowhere` created undeclared |
| 13 | `spec plays` | ~0.09 s | mapped; unknown actor refused as `product_actor 'the cat'` |
| 14 | `spec check` before any capability | 0.16 s | 7 expected warnings |
| 15 | hand edit of `.shop/product/product.toml` | - | no command removes a job or context; the next `spec assign` commit took the hand edit with it |
| 16-19 | `work context list`, `work idea`, `work quote`, `work shape b1 --note` | ~0.1 s | ok but `work quote`: `no session is known` (no hook in the trial) |
| 20-22 | `work line b1 --capability chores ...`, `--into chores --model ...`, 11 x `--term` | ~0.12 s | ok |
| 23-24 | `spec parse --item b1 "...keep the chore assigned to the member."` | 0.44 s | refused at "assigned"; relation reworded to `for -> member`, parsed |
| 25 | `work line b1 --into chores --group ... "<line>" --serves share-out` (and keep-up) | 0.12 s | prints only `chores#g1 serves share-out` |
| 26 | `work ready b1` | 0.42 s | v_t13 Frame `<actor> lists the chores of <member>`; v_t6 actor `the member` reads as kind `member` |
| 27-29 | `--reword-term` attempts | ~0.1 s | leading `-` taken for an option; `--into` refused; works with `--` and no `--into` |
| 30-31 | Frame changed to `<actor> lists <member>`, lines reworded, `work ready b1` | 0.69 s | ready |
| 32 | `spec trace keep-up` on main | 0.13 s | `job keep-up is served by no requirement group` |
| 33-34 | `spec plays ... --as "the housemate"`; `work batch start` | 0.67 s | `batch-1 building: t1 b1`; feature generated |
| 35-36 | in the batch worktree: `spec check`; `spec trace keep-up` / `share-out` | ~0.15 s | 2 warnings (w_m5; notifications subdomain no context addresses); trace correct, with why per line and the needed job |
| 37 | `work batch next batch-1`, `work batch status` | ~0.15 s | `prepare task`; stopped |
| 38-39 | b2: lines into `chores`; new capability `rota` with `--serves no-such-job` | ~0.1 s | `chores` refused clearly (new on b1 in batch-1); unknown job accepted |

## Findings

1. **major: the product layer has no user walkthrough.** Getting started, the tour, concepts, talking-with-claude and every skill never mention product, job, subdomain, `serves` or `spec trace`; they appear only in `docs/reference/commands.md` and the product check table of `docs/reference/design-model.md`. `work line --serves` is in `--help` only; the capability-file reference lacks the `serves:` line. Expected: a "declare your product" step and guidance on dedicating a group to a job.
2. **major: bounded-context ids in two forms.** `migrate init`, `work context list` and `keep` use `bounded-context/example.org/...`; the reference examples of `spec context`, `assign`, `plays` use unprefixed ids. Both accepted and kept apart: product.toml held `[contexts."example.org/chores/chores-app"]` and `[contexts."bounded-context/example.org/chores/chores-app"]`, one job each, and `spec check` treated both as this context.
3. **major: `spec assign` declares an unknown context, and nothing can be taken back.** `spec assign bad5 --to example.org/chores/nowhere` -> `assigned the job bad5 to the bounded context example.org/chores/nowhere`; reassigning refused `job bad5 is assigned to the bounded context example.org/chores/nowhere already`. No command unassigns or drops a job, context or actor; a hand edit of product.toml was taken silently into the next `spec assign` commit.
4. **major: a `Frame:` shaped like recipes.md's is refused unhelpfully.** recipes.md shows `Frame: <actor> lists the characters of <note>.`; the same shape gives `v_t13 ... the Frame: does not read at "the chores of member": the verb's object is a kind or an actor of the glossary (nearest: the chores service, the member)` (angle brackets dropped, unrelated suggestions). Diagnosed from spec_frames.py after the failure: fixed words after the verb are allowed only when none is a kind unless the whole phrase reads as a noun; the docs do not say what does.
5. **major: an item's `serves` cannot be checked or traced before a batch.** On main after b1 was ready, `spec trace keep-up` -> `job keep-up is served by no requirement group`, and `spec check` still warns `w_unserved_job`, `w_untriggered_actor`. `spec parse` has `--item`; `spec check` and `spec trace` do not, and the docs do not say the trace waits for a batch.
6. **minor: the job-statement refusal hides its cause.** `--statement "When x, the cat wants y, so they can z."` refused as not of the job statement form; the cause appears to be the unknown actor.
7. **minor: the statement's actor is not checked against `--actor`.**
8. **minor: a refusal leaks a parameter name.** `spec plays "the cat"` -> `product_actor 'the cat' is no actor of the product`; siblings say `--actor`.
9. **minor: `--serves` accepts a job the product does not have.** `rota#g1 serves no-such-job`, exit 0.
10. **minor: rewording a term has traps.** An entry starting `- ` is taken for an option (`--help` does not say to put `--` first); `--reword-term` refuses `--into` while `--reword-model` needs it and `--term` takes it.
11. **minor: `work line ... --serves` does not confirm the line**, printing only `chores#g1 serves share-out`.
12. **minor: vocabulary mistakes surface only at `work ready`** (actor `the member` beside object `member`, v_t6); `spec plays --as` accepts any actor name without checking the model.
13. **minor: docs drift.** shaping-items says `migrate init` writes `imports: [request]`; it writes `[base, request]`. `--help` usage lines say `migrate init`, `spec job`, not `shop ...`.
14. **minor: git default branch.** A repository on `master` gets `migrate init`'s commit without a warning.
15. **minor (trial setup): `work quote` needs the hook's session**; expected without a plugin install, but shaping-items relies on it.
16. **minor: `spec trace` prints no `coordination:` line when there is none**, while the reference says it is printed after the first line.
17. **info: everything is fast**, no step over 0.7 s with the toolchain installed.
