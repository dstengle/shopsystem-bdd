---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-26-a-fourth-new-user-trial-of-the-product-layer
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-26
---

# A fourth new-user trial of the product layer

A fresh agent played a new user of the plugin's product layer with a clean clone of main at f130dbb55 as `$CLAUDE_PLUGIN_ROOT`, on a fresh repository (identity "Trial User", no GitHub), reading only README.md, docs/, the skills and `--help` output; it opened no scripts or tests, every failure being explained by its message or the docs. The scenario: a repair café (visitors book a repair slot, volunteers take on and record repairs), with a second area for a parts shelf. It is the fourth trial of the day, the last of the iterations the person asked for (quote-104), and it checks the third's findings and records whether each problem could be worked around from the docs.

## Summary

The walkthrough runs from start to finish: `migrate init`, the product declarations, an item with two capabilities in two areas (`desk`, `parts`) sharing the actor "the volunteer", `spec check --item`, `spec trace --item`, `work ready`, `work batch start`; the batch laid both capabilities, their model, vocabulary and the Composition table and wrote both features. Of nine prior findings, six are fixed and three partly. Still open: a gloss after `Frame:` read into the frame; a `Frame:` naming a slot that does not exist accepted; `(proper noun) → object x` accepted; `--reword-model` with identical text a raw git error; `spec --help`'s contract describing the old layout. New and most misleading: `--serves <job>` written before the line text swallows the line and the error blames the job. Every command answered in 0.1-0.7 s (caches probably warm).

## Steps

| # | command | time | outcome |
|---|---|---|---|
| 1 | `git init`, venv, pytest 9.1.1, pytest-bdd 8.1.0 | 4 s | ok |
| 2 | `shop tools probe` | 0.14 s | gf 3.12.0, pgf 1.1, clingo 5.8.2, gf-rgl 20250812 |
| 3 | `migrate init --id bounded-context/repaircafe/cafe` | 0.13 s | refused, domain needs a dot |
| 4 | `migrate init --id bounded-context/example.org/repaircafe/cafe-desk --purpose ...` | 0.09 s | scaffold, one commit |
| 5 | `spec actor "the visitor"` before any product | 0.09 s | refused: "declare it first with spec product <id>" |
| 6 | `spec job ...` before any product | 0.08 s | refused on `--actor` |
| 7 | `spec subdomain repairs --type core` before any product | 0.10 s | **accepted** (finding 3) |
| 8 | `spec context bounded-context/...` before any product | 0.11 s | refused: outside the product's id (none declared) |
| 9 | `spec product repaircafe`, `example.org`, `Example.org/Repair_Cafe` | 0.08 s | each refused naming the product id form |
| 10-12 | `spec product example.org/repaircafe`; `example.org/othercafe`; same id, new purpose | 0.08-0.10 s | declared; refused ("a product keeps the id it was declared with"); purpose replaced |
| 13 | `spec actor visitor`; `the visitor`, `the volunteer`, `the organiser` | 0.08 s | form refused; declared |
| 14-15 | `spec job book-repair`; `spec job Take_Repair` | 0.09 s | declared; **accepted with no job id form** (finding 4) |
| 16 | `spec job` bad form, another actor, unknown `--needs`, cycle, unknown actor | 0.07-0.08 s | each refused naming the option |
| 17-18 | three more jobs; `drop job Take_Repair`, `drop job nosuch` | 0.08-0.10 s | declared; dropped; refused |
| 19-20 | `spec subdomain` bad id, bad type, unknown `--serves`; two declared, one dropped | 0.07-0.10 s | refused; ok |
| 21-22 | `spec context` no prefix, outside, unknown subdomain; then declared | 0.11-0.13 s | refused; declared |
| 23-24 | `spec assign` unknown job, bad id, undeclared context; `spec plays` undeclared context, unknown actor, bad id | 0.11 s | each refused |
| 25 | `spec plays "the visitor" --in <ctx> --as "the visitor"` | 0.12 s | refused: "it holds no actor" |
| 26 | `spec assign` x4; book-repair twice | 0.10-0.12 s | assigned; second refused |
| 27-28 | `work idea`, `shape`, `--capability bookings --area desk`, `shelf --area parts`; `--area Parts` | 0.10-0.12 s | ok; area name form refused |
| 29 | `--model` into each area | 0.15 s | kept per area |
| 30-35 | `--term` wrong parts of speech; no aspect; bracketless frame; `(thing)`; two sentences; missing element | 0.11-0.14 s | refused v_t22, v_t14, v_t13, v_t4, v_t7 (once), v_t19 |
| 36 | `--term` verb with no `Frame:` | 0.17 s | accepted (docs give a default frame) |
| 37-39 | `--term` gloss after `Frame:`; slot `<gadget>`; `(proper noun) → object slot` | 0.15-0.17 s | **accepted** (findings 5-7) |
| 40-42 | `--remove-term book` (two entries); `--reword-term` new then same; unknown term | 0.08-0.12 s | asks for `<word> → <element>`; "reworded"/"unchanged"; refused |
| 43 | `--term` x12 desk, x4 parts | 0.13-0.16 s | one commit each, every entry printed |
| 44 | `work line ... --serves book-repair '<line>'` | 0.10 s | **refused, misleading** (finding 1) |
| 45-46 | `work line ... '<line>' --serves book-repair` (5 lines); `--serves nojob` | 0.10-0.12 s | written; refused "the product holds no job nojob" |
| 47-48 | `spec check --item b1` before and with the lines | 0.15 / 0.52 s | expected v_m4, v_m7, w_unserved_job; then 0 violations, 0 warnings |
| 49-52 | `spec trace` without `--item`; with `--item` and `--json`; `nojob`; no job | 0.06-0.17 s | refused pointing at `--item b1`; traces right, needs followed; "served by no requirement group"; usage error |
| 53 | `spec parse --item b1 --form ...` | 0.14 s | right forms; short "may follow" (finding 12) |
| 54-55 | `work rate`, `work ready b1`; `work batch start` | 0.13-0.73 s | ready; batch-1 building |
| 56 | `spec --root <worktree> check`, `coupling`, `trace keep-parts` | 0.14-0.21 s | 0 violations; "desk by parts: 1 requirement" |
| 57-61 | drops while referred to; drops/unassigns of nothing; unassign twice; plays after start | 0.07-0.13 s | each refused naming one blocker at a time; refused; done then refused; still refused (no model on main) |
| 62-64 | `--reword` same text; `--reword`/`--remove` of r9 and other absent pieces; `--into ... --reinstate-model` | 0.08-0.11 s | "bookings#r1 unchanged: <line>"; refused naming the piece; "... each alone" (finding 13) |
| 65 | `--reword-model "service parts"` with identical lines | 0.10-0.12 s | **raw git error** (finding 2) |
| 66-68 | `work batch status`, `next`, `reopen b1`; probe item b2; `work withdraw b2` | 0.10-0.34 s | right; confirms 5-7; withdrawn |

## Prior findings

1. **`spec plays` into an undeclared context: fixed** (`--in bounded-context/example.org/repaircafe/undeclared is no bounded context of the product`).
2. **Wrong parts of speech: partly fixed.** v_t22 refuses noun→operation, adjective→object, attribute→object, noun→actor, `(verb, state)`→operation; `(proper noun) → object slot` still accepted (finding 7).
3. **`--term` accepting bad verbs: partly fixed.** No aspect (v_t14) and bracketless frame (v_t13) refused; a slot naming nothing (`<gadget>`) accepted by `--term`, `spec check --item` and `work ready` (finding 6).
4. **Gloss after `Frame:`: partly fixed.** v_t7 said once; text after `Frame:` still read as part of the frame (finding 5).
5. **Two areas of one item sharing an actor: fixed.** The lay writes `imports: [parts]` in desk and `imports: [desk]` in parts; `spec coupling` reports `desk by parts: 0 words, 0 elements, 1 requirement, 0 imports`.
6. **How a line states a refusal reason: fixed** (domain-model.md "An outcome"; `refused: slot already booked` stated by "... name the slot").
7. **Reword to identical text: partly fixed.** `--reword` and `--reword-term` say "unchanged: <text>"; `--reword-model` still a raw git error (finding 2).
8. **Product declarations: fixed** for actor before product, product id form and replacement; `spec subdomain` before a product still accepted (finding 3).
9. **`spec job` usage and `spec --help`: partly fixed.** `spec job --help` reads `[--actor <actor>] --statement <text> [--needs <job>]`, "design model v5" gone; `spec --help`'s contract still `## Glossary` bullets, `codified-1`, `.shop/work/`, `<owner>/<product>/<context name>`, nothing of `spec/model/`, `spec/vocabulary/` or the product file (finding 8).

## Findings

1. **major: `--serves <job>` before the line text swallows the line, and the error blames the job.** `shop work line b1 --into bookings --group "A slot booked is booked" --serves book-repair 'When the visitor books a slot, ...'` -> `work line: --serves: 'book-repair' is not a requirement group <capability>#g<n>`, exit 1. `--serves` takes one or more arguments; the docs show no example. Worked around by putting `--serves <job>` after the line, found by knowing argparse, not from the docs or the message.
2. **minor: `--reword-model` with identical lines** -> `work: git commit failed in the repository .../app: On branch main`, exit 1 (`--json`: refused with that git text). No harm; no workaround needed.
3. **minor: `spec subdomain` accepted before any product** (`declared the subdomain repairs`, committed into a product file with no id), while `spec actor` and `spec context` are refused. Workaround: drop it.
4. **minor: job ids have no form** (`spec job Take_Repair ...` -> `declared the job Take_Repair`), while subdomain ids must be lower-case words joined by hyphens. Workaround: `spec drop job`.
5. **major: a gloss after `Frame:` is accepted and read into the frame.** `--term "- **make** (verb, action) → operation probe.make. Forms: makes, made. Frame: <actor> makes <widget>. Then it is kept by the tester."` accepted; `spec parse --item b2 'When the tester makes a widget, ...'` -> `does not parse at a ... may follow: widget`. Nothing names the entry; found only by comparing with an entry without the gloss.
6. **major: a `Frame:` slot naming no kind, actor or parameter is accepted everywhere.** `Frame: <actor> makes <gadget>.` accepted by `--term`; `spec check --item` gives only v_p1; `work ready` gives `does not parse at a ...; nearest words: none`. v_t13's own wording says a slot must be "a kind, an actor or a parameter of its operation".
7. **minor: `(proper noun) → object x` accepted by `--term`**; the docs say a proper noun names a service or an actor (it may name an object, as b825's build documented in language.md, so docs and check disagree). Caught later only on a collision (v_t20).
8. **minor: `spec --help`'s contract is stale** (codified-1, glossary, `<owner>/<product>/<context name>`); commands.md says `--help` is right where the two differ.
9. **minor: drop refusals name one blocker at a time** (`spec drop job keep-parts`: first the bounded context that holds it, after unassigning the subdomain that serves it).
10. **minor: an unknown job is described as unserved or unassigned** (`spec trace nojob --item b1` -> `job nojob is served by no requirement group`; `spec unassign nojob --from <ctx>` -> "... is not assigned to ..."), where assign and plays say "no job of the product".
11. **minor: the removal refusal for two entries of one word suggests a form that cannot tell them apart** (`--remove-term "book → operation desk.book"` -> `2 terms of the item are book → operation desk.book; name one by <word> → <element> or its whole bullet`); the whole bullet works.
12. **info: a parse refusal's `may follow:` is short** (after "When the volunteer" only `record`, though take, list and book fit).
13. **info: `--into bookings --reinstate-model "object gadget"`** -> `work line: --reinstate-model, --reinstate-term and --remove-import each alone`, meaning "without `--into`", while `--retire-model` needs `--into`.
14. **info: the lay makes the two areas import each other, both `kind: core`**, though only parts uses a desk word and parts' subdomain is `supporting`; no item option gives a non-port area its kind.
15. **info: `spec plays` cannot run in the docs' order on a new context until the first batch merges** (`--as 'the volunteer' is no actor of the domain model of ...; it holds no actor`); `plays` has no `--item`.
16. **info: non-ASCII text is written escaped in product.toml** ("café" as `café`).
