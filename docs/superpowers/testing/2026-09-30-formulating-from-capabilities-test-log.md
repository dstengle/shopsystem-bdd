# Test log: formulating-features from capability files (0.8.0)

Fixture `promo-3`: the promo fixture with an approved `spec/` (from integrating run intg-2) plus one added Behaviour line with two readings: "If a customer applies a code to a cart of more than 10 items, the shop refuses the code because the cart is too large" (items = units or products?). Implementation carries a bait that reads like behaviour: "a code marketing withdraws may still apply for up to five minutes". The note stays under `docs/`. Prompt (all runs): "The person has approved the Behaviour lines in spec/capabilities/promo-codes.md. Formulate the feature files for it. Stop before slicing or planning."

Fixture flaw, same for baseline and green: the fixture's approval commit message ("lines 1-9 approved") reads as a line count; baseline runs, which read git, questioned whether line 23 was approved.

## Baseline (formb-1..3, 0.7.0 formulating-features with Task 1 present)

- **Formulator read the note, 3/3.** `Read docs/superpowers/specs/2026-09-30-promo-design.md` next to the capability; formb-1: "It isn't in the design note … so I've read 'lines 1-9' as covering it".
- **Header, 3/3.** `So that they get a percentage off the cart total, a customer can apply a promotion code …`; no `Narrator:`. `# formulated from` in 1/3 (the main agent added it).
- **Name, 2/3.** `apply-promotion-code.feature` against `formulated_as: features/promo-codes.feature`; formb-1: "Either the frontmatter or the file name should change so they agree; which do you want?"
- **Not one to one, 3/3.** 11, 10 and 12 scenarios for 9 lines; boundaries the lines do not state ("A cart of exactly 10 items can still take a code", "A cart exactly at a code's minimum can use the code").
- **Scenario-level gate, 3/3.** "Two scenarios need your yes"; "Until you answer, those two stay out of slicing."
- **A reading decided in a scenario.** formb-2: "Applying a second code leaves the cart with one code … The scenario has it replace."
- **The two-reading line dodged, 3/3.** "Both scenarios use one of each product, so it doesn't matter yet whether 'items' means units or different products."
- The Implementation bait was not formulated, 0/3. Not a failure.

## Edit

`skills/formulating-features/SKILL.md`: input is changed capabilities; one file per capability named by it; header `# formulated from` / `Feature:` / `Narrator:`; one scenario per line and no others; Behaviour only; a two-reading line gets no scenario, including one that holds under both; settled/deciding and the scenario-level approval removed. `agents/feature-formulator.md`: path list `spec/` and `features/`, never `docs/`.

## Green (formg-1..3)

3/3: `features/promo-codes.feature` with the new header; 5 scenarios for 5 lines, 4 lines (1–50 range, rounding ties, a second code, "10 items") returned as questions with two readings each and no scenario; formulator read `spec/` and `features/` only; no Implementation scenario; committed alone; nothing held for approval: "The five committed scenarios don't have to wait for that." GREEN.

Deviation: no run invoked integrating-a-proposal for the questions; each showed them to the person and said the answers would go through integration ("Once you answer, I'll feed the changed lines through integrating-a-proposal"). The writer given an unanswered question can only return it, so step 3 now says: show the question, send the answer to integrating-a-proposal's question brief. Re-run formg-4 on the edited step: same result, 5 scenarios, 4 questions, "the lines get changed in the spec and come back here to be formulated." GREEN.
