# Test log: plans carry no code; spec-settled scenarios need no approval (0.6.0)

Two changes, each with a headless baseline on the cart fixture (cwd = fixture, both plugins via --plugin-dir, Opus) before the skill was edited, then the same prompt again after.

## Change 1: the hand-off to writing-plans carries no code

Baseline (plugbase2, fixture: cart with every feature approved, slice 1 green; prompt: place the scenarios, then writing-plans over the first two slices). The run invoked slicing-into-increments then superpowers:writing-plans and wrote `2026-09-27-cart-batch1-implementation.md`: 311 lines, 22 fenced blocks, 9 of them Python, with steps such as "Create `tests/conftest.py` with the shared steps" and "Implement in `cart/__init__.py`, inside `Cart`, after `add`" carrying the code in full. The plan was the implementation, written by the planner on Opus. RED.

Edit: slicing-into-increments step 7 now hands off "The Hand-off to writing-plans" (no code blocks, file contents, diffs or step bodies; what each task carries instead; counts from tags; no scratch build, no replay) with two new rationalization rows; bdd-red-green gains "The Task Is Intent, Not Code".

## Change 2: spec-settled scenarios do not wait for approval

Baseline (plugbase1, fixture: cart with slice 1 green, promo spec approved, no promo feature files, and the approved cart.feature holding a 19.99 total its own slice 1 scenario contradicts; prompt: plan the remaining work, then writing-plans over the first two slices). The run invoked slicing, found no promo features and the contradiction, invoked formulating-features, wrote the promo feature files and a rewrite of the 19.99 scenario, and stopped: "The workflow won't write that plan while any feature file is waiting for your approval." Every scenario waited, the promo scenarios that follow from the approved spec included. RED for the promo scenarios; correct for the 19.99 rewrite, which the spec does not decide.

Edit: formulating-features steps 4 and 5 sort scenarios into settled and deciding, the coverage table carries the word, and only deciding scenarios stop for approval; slicing's step 7 gate reads the same way.

## Green runs

**Run A (no code; same fixture and prompt as plugbase2, edited skills).** Invoked slicing-into-increments then writing-plans and wrote `2026-09-27-cart-batch1-implementation.md`: 108 lines, 0 fenced blocks, 0 `def`/`class`/`import` lines. Each task carries its scenarios and tag, why red today from a run, where the change lands, the decisions left open stated with their source, the steps to reuse, and the expected counts. Header: "This plan carries no code." GREEN.

**Run B (fixture as plugbase1, edited skills).** Slicing found the 19.99 contradiction, sent it to formulating-features, which returned a question rather than a scenario (the spec does not decide it); slice 3 is blocked awaiting approval. Slicing then went on: slice 2, settled, was planned by writing-plans without code, where the baseline had stopped everything for approval. GREEN for the gate. The run did not formulate the missing promo features ("in case you have your own set that just wasn't committed"), a fixture ambiguity the baseline read the other way; run C exercises formulation directly.

**Run C (fixture: cart module, promo spec approved, no feature files; prompt: formulate, then continue as far as the workflow goes).** formulating-features wrote two feature files with a coverage table marking each scenario settled or deciding; slicing placed the settled ones in nine slices and writing-plans wrote a no-code plan (0 fences) for the first two, while the one deciding scenario (half-cent rounding, two readings of rule 3) was left untagged awaiting approval. GREEN for the gate and the plan. Loophole seen: the main agent lowered two of the formulator's `deciding` marks to `settled` on its own reading ("'minimum' normally includes the value itself"). Edit: step 4 now says the mark stands and may only be raised from settled to deciding, never lowered, with a rationalization row. Run D repeats the fixture against that edit.

**Run D (fixture as run C, edited skill).** The formulator's marks stood: two deciding scenarios (rounding the discount vs the total; a code accepted above its minimum, which rule 6 implies but never says) were left untagged and unplanned, with both readings shown; seven settled scenarios went to slicing and a no-code plan. The main agent lowered no mark. GREEN. Released as 0.6.0.
