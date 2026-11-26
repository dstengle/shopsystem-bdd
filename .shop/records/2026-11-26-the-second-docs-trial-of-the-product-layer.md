---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-26-the-second-docs-trial-of-the-product-layer
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-26
---

# The second docs trial of the product layer

A fresh agent played a new user testing whether the documentation works, on a clean clone of main at e81fa1ca6, after b846 fixed the first docs trial's findings. It read only README.md, docs/, the skills, `--help` and command output, replayed every product-layer command the docs show from the start states they describe, and built a fresh "seed swap" app (the person's own verbs, "return" among them) from an empty folder to a started batch and, after a simulated merge, `spec plays`. No GitHub. It is the second docs iteration the person asked for (quote-106).

## Summary

- The product walk works: every command of talking-with-claude's "Your product and its jobs" matched the page exactly (11 declarations, the 10-warning check, the item, `--serves`, the typo refusal, the trace with and without `--item`, `work ready`, `work batch start` with its `batch brief:` line, the laid `serves:` lines); the product file built was identical to the example's.
- The fresh seed-swap project went through every step without getting stuck; `spec plays` was refused before the merge as documented and worked after it.
- Of the first docs trial's findings: five fixed, two partly, two fixed with a caveat. No major findings; no broken link or anchor (README, docs/ outside history, the skills).
- Left: a pack verb's frame trap documented only in recipes; getting-started §8 inconsistent with the example and with its place after the merge; no reminder of the after-merge `spec plays` in the batch flow; minor reference gaps.

## Example reproduced

From talking-with-claude's start state (the example less `.shop/product/`, the `serves:` lines and g5, annotated and generated): `spec product`/`actor`/3 `job`/`subdomain`/`context`/3 `assign`/`plays` match every line (`mapped the product actor the writer to the person in the bounded context bounded-context/example.org/notes/notes-cli`); `spec check` (10 warnings), `work idea`, `work shape --note`, 4 `--serves notes#gN`, the r5/g5 line with `--serves clear-notes`, `--serves ... write-notes` (`the product holds no job write-notes`), `spec trace keep-notes` (`... the item b1 holds one that serves it: trace it with --item b1`), `spec check --item b1` (0/0), `spec trace clear-notes --item b1`, `work ready b1`, `work batch start` (with `batch brief: ...`), the batch branch's g4/g5 with `serves: clear-notes` and `unbuilt: [r5]`, and `spec --root docs/examples/notes-cli trace` of the three jobs: all match. getting-started §5 and §8's declarations after a first merge match; the side note's refused `plays` and 3-warning check match in a freshly founded context; a check after the merge and before `plays` differs (4 warnings: w_unplayed_actor, w_unreached_sub, w_unserved_cap, w_unserved_job), which §8 does not show.

## Fresh project

Seed swap (`bounded-context/example.org/seeds/seed-swap`, product `example.org/seeds`): setup and `migrate init` as step 3 says (`imports: [base, request]`); item, capability `swap` with narrator, model (seed, report, service swap with offer/request/return, actor the member), a relation, 12 terms. The verb "return" written as the skill says (`Redefines: request`, `Frame: <actor> returns <report>`) gave v_t15 at `spec check --item b1`, and the attribute `text` v_t16 (base defines it); fixed by `Frame: the member returns <report>.` and `Redefines: base.`. Four lines parse ("The member requests a seed" reads as `swap.request`); product declared; `spec plays` refused as documented, `spec check` warned w_unplayed_actor, w_unreached_sub, w_unserved_job; `--serves` on the item's groups worked; trace without `--item` pointed at `--item b1`, with it right; `work ready`, `work batch start` worked. After a simulated merge, `spec plays` mapped the actor and `spec check` was 0/0. A pack verb with no `Redefines` (`keep`) warns `v_t6: ... the grammar spells keep itself`, as design-model.md's row now says.

## Prior findings

- talking-with-claude skipped `work shape --note`: fixed.
- "return" blocked by v_t6, v_t6 described wrongly: fixed (the following v_t15 trap is only in recipes: finding 2).
- `spec check --item` missed the item's lexicon problems: fixed (reports v_t15, v_t16).
- actor mapping silently forgotten: partly (getting-started, talking-with-claude and the skill say `plays` waits for the merge, and `spec check` warns w_unplayed_actor, but the after-merge flow never brings it up: finding 3).
- the example being the end state: fixed in talking-with-claude; partly in getting-started §8 (finding 1).
- missing `batch brief:` line: fixed. Broken R11 anchor: fixed. "first row": gone. commands.md's `work line` synopsis: fixed but for `--json`.

## Findings

1. **minor** getting-started §8: declares one job `keep-notes`, says the example "keeps the result" (it holds three jobs and g5), and shows a 3-warning check with w_unplayed_actor that only occurs before a context's first batch, while the step comes after the step-7 merge. Fix: label the refused-`plays` block "in a new context, before its first batch", and declare the three jobs or point at talking-with-claude's replay.
2. **minor** shaping-items step 2 and getting-started §4: `Frame: <actor> adds <note>` and "`Redefines: <pack>` when a pack has the word"; a request-pack verb so written fails v_t15, whose fix (the actor named in the frame) is only in recipes.md and design-model.md. Fix: one sentence in the skill and a link to the recipe.
3. **minor** building-a-batch step 7 and getting-started step 7: after the merge, `work batch merged`, `measure batch`, the next batch; a pending `spec plays` is never brought up again. Fix: "run `shop spec check`, and any pending `spec plays`" in the after-merge step.
4. **minor** concepts.md "Vocabulary and packs" and getting-started §3: packs listed as `request`, `spec`, `time`; `migrate init` imports `[base, request]`, and base's `text` collides with a natural attribute name (v_t16). Fix: list `base` (and `cli`), and say a new context imports base.
5. **minor** commands.md `shop spec job`: synopsis `[--actor <actor> ...]` reads as optional; a job with no `--actor` is refused. Fix: unbracket it.
6. **info** commands.md product commands: "in one commit", but they also push (`not pushed: origin: ...`).
7. **info** getting-started §3: nothing about the context purpose; `## Purpose` stays empty. Fix: the session asks for it and passes `migrate init --purpose`.
8. **info** the capability file laid by `work batch start` has no blank line after its headings and no `## Dropped`, unlike the example's form.
9. **info** commands.md `work line` synopsis lacks `--json`.
