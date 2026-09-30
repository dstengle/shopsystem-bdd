# Test log: integrating-a-proposal and capability-writer (0.8.0)

Fixture `promo`: the cart example (`skills/bdd-red-green/example`) with an approved promotion-codes note carrying bait: a data model with column names, an API with status codes, UI message copy, implementation notes (a five-minute cache, `ROUND_HALF_UP`), a rationale paragraph comparing a rejected design, decisions, a "not in this version" list, and unstated conditions (a second code; a refused code; a code with no minimum). The stage-1 doc is copied into the fixture as prose. Headless `claude -p`, Opus, cwd = fixture.

Prompt (all runs): "The promotion codes note at docs/superpowers/specs/2026-09-30-promo-design.md is approved. Write this project's spec from it following docs/stage-1-capabilities-and-features.md: spec/index.md, spec/decisions.md and spec/capabilities/. Stop once spec/ is written; do not write feature files."

## Baseline (intb-1..3, installed 0.7.0 plugin, no agent, no skill)

The format doc alone does most of the work: 0 "shall" in 3/3, responses observable, rationale cut or moved into decisions, and 7–10 open questions each, the second code among them in 3/3. What it does not do:

- **Reads the code, 3/3.** Every run ran `cat cart/__init__.py tests/test_cart.py`. intb-2 wrote `capability/cart` from it: "Amounts are `Decimal`; the total of an empty cart is `0.00`."
- **Message copy as the contract, 3/3.** "the code is refused and the customer is told \"We don't recognise that code\"", "\"Add £X more to use this code\"". The house rule since 0.1 is a reason, never the wording.
- **Lines the note never states, 3/3.** "If a code is refused, the cart total is unchanged" (3/3), "Where a code has no minimum cart total … the code is applied" from the nullable column (3/3). intb-1: "'A refused code leaves the total unchanged' is not in the note; I added it as the obvious reading", said only in the closing message. No line cites a sentence, so a gate cannot tell inference from the note.
- **Implementation promoted to Behaviour, 2/3.** "A discount that falls exactly on half a penny rounds up." intb-1: "I made it a rule because a customer can see the difference."
- **Underscore names, 3/3.** `formulated_as: features/promo_discount.feature`, following the doc's own `write_path.feature`.
- **Ledger without dates, 3/3.**
- **No gate.** Each run stopped because the prompt said so; none asked for approval of lines.

## Edit

- `docs/capability-format.md`: the stage-1 doc, moved into the plugin; hyphenated on both sides; a refusal names its reason and message wording is implementation; the ledger entry shape (`date`, `revisit_when`, `supersedes`, `source`); a later note integrates into the same `spec/`.
- `agents/capability-writer.md`: Read/Glob/Grep, Opus, a path list; the format rules; every line cites its note sentence in the returned change list, and an unstated line is a question with the line each answer would give; the return shape.
- `skills/integrating-a-proposal/SKILL.md`: dispatch, two-way check of the change list, commit `spec/` alone, the gate on added/changed/removed lines, hand-off to formulating-features.

## Green (intg-1..3, working copy by --plugin-dir)

`integrating-a-proposal` invoked first in 3/3; `capability-writer` dispatched in 3/3; the writer's reads were the note, the format doc, `features/cart.feature` and a glob of `{spec,features,docs}`: no source in 3/3. 0 "shall"; refusals read "the shop refuses the code because it has expired" with the wording under Implementation, 3/3; "total unchanged", "no minimum" and "half up" came back as questions each with its line, 3/3; `formulated_as: features/promo-codes.feature` 3/3; ledger entries dated with `source:` 3/3; `spec/` committed alone and the run stopped asking for "an explicit yes on lines 1–8 and an answer to each question", 3/3. GREEN.

Loophole: intg-1 wrote the citations into the capability file ("*(rule 1; API …)*"). Edit: the citation goes in the change list; the file carries the line alone. Checked in the second fixture: 0 citations in 2/2.

## Second note into an existing spec (promo-2)

Fixture: `promo` with intg-2's `spec/` committed as approved and a second note that adds case-insensitive matching, moves expiry from inclusive to exclusive, withdraws minimum totals, and records a decision. Prompt: "The second promotion codes note … is approved. Take it through to the spec, following docs/stage-1-capabilities-and-features.md. Stop before any feature files."

- **Baseline int2b-1 (0.7.0):** edited `spec/` in place, no second spec, ledger appended with earlier entries byte-identical. Nothing committed, no change list with sources, the removed minimum-total line reported in prose, no approval asked: "When you're ready, the next step is to write features/promo-codes.feature." RED for the gate.
- **Green int2g-1, int2g-2:** skill and agent in both. Change list with 3 added, 1 changed (old and new shown), 1 removed, each quoting its note sentence; "Removing this line deletes that part of the contract"; earlier ledger entries byte-identical; one new dated entry; `spec/` committed alone; stopped at the gate with four questions each carrying its lines. int2g-2 also noticed the first round's lines had no feature file and asked whether they had been approved. GREEN.

`supersedes:` was not written in either run: the inclusive reading was a Behaviour line, never a ledger entry, and both runs said so. Correct.

## Inventory

`claude --plugin-dir <checkout> plugin details shopsystem-bdd`: `Skills (4)` with integrating-a-proposal, `Agents (6)` with capability-writer.

## Trigger

Fixture `promo` without the format doc, the note freshly committed, working copy loaded with superpowers. Prompt: "Thanks, the promotion codes design in docs/superpowers/specs/2026-09-30-promo-design.md is approved. Carry on with the next step." trig-1..3: the first skill invoked is `shopsystem-bdd:integrating-a-proposal` in 3/3; neither formulating-features nor writing-plans is invoked. Each then invoked migrating-to-capabilities, because the fixture holds an approved `features/cart.feature` and no `spec/` ("the promo note has to go in as part of setting up the first spec/, not as a normal integration"), recorded a baseline, and stopped at the gate with nothing written. GREEN.
