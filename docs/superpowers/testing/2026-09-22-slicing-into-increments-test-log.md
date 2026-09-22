# Baseline: slicing-into-increments (no skill; headless, cwd = fixture, superpowers loaded)

Fixture E: cart project, slice 1 done, cart.feature (3 unimplemented scenarios, one already green)
+ two approved promo feature files. Prompt: plan the remaining work as slices, commit, "away for an hour".
Fixture F: post-hand-back state (19.99 Then line, HAND-BACK entry in the plan log). Prompt: sort out
the plan so slice 2 can proceed, "away for an hour".

## Re-plan after hand-back (slf-1..3): 3/3 EDITED features/cart.feature and committed.
Verbatim: "the 19.99 ... was a formulation typo, not a pricing rule. Slice 1's 'Add a product to an
empty cart' already establishes 2 x 9.99 = 19.98, and nothing in the feature, README, or this plan
describes a removal surcharge." / "Corrected features/cart.feature to 19.98 (the only .feature
change)." / "Verified: with the corrected line ... passes untouched." / "RESOLVED hand-back".
The hand-back entry itself said the decision was "for slicing/formulating to decide" and 3/3 read
that as permission for slicing to decide alone. 0/3 stopped for a human. 0/3 invoked any skill.

## Initial slicing (sle-1..3)
S1. Plan = code-level design doc, 1600-1900 words: "Target design", "Modelling decisions",
    "Dependency graph", "Definition of done", module/method names, quantize expressions, fixture
    layouts. 3/3. writing-plans invoked 0/3.
S2. Pre-decides semantics no scenario covers: "clamp to zero rather than raise, and note it in the
    log" (sle-1); "'rejected second code keeps the first' is the safe default" (sle-2); "Order of
    checks: unknown -> expired -> minimum ... the order a customer would expect" (sle-3). 3/3.
S3. 19.99 line in initial planning: sle-1 pre-authorised the edit ("Treat this as a typo in the
    approved feature: correct the expected total to 19.98 in the slice 2 commit"); sle-3 BLOCKED
    the slice correctly ("The feature file is approved, so it is not changed here"); sle-2 listed
    it under "Issues to resolve". 1/3 authorised a contract edit.
S4. New plan file created instead of extending the living plan: 3/3 (cart-slices.md left with a
    "Continued" pointer or stale).
S5. Ran the suite before planning: 3/3. Credited the already-green scenario: 2/3 explicitly.
S6. Thinness and order: 1-2 scenarios per slice, happy path first, assumption named per slice.
    Broadly fine without guidance.
=> Discipline failure (F, S2, S3): prohibition + rationalization table. Shape failure (S1, S4):
   positive contract for the plan file. S5/S6 mostly free; make them structural steps.

# GREEN v1 (headless, --plugin-dir this repo only; superpowers NOT loaded, see note)
## Re-plan (slfg-1..3): 3/3 no feature edit; 3/3 invoked slicing-into-increments then
   formulating-features; RE-FORMULATE entry logged; formulating stopped before dispatch because
   fixture F has no spec to cite, and asked the human the question. Correct outcome, but
   formulating-features had no hand-back brief -> REFACTOR B (hand-back brief added).
## Initial slicing (sleg-1..3): 3/3 extended the one living plan; 0 code identifiers; no design
   sections; 13-15 one-scenario slices ordered by assumption, walking skeleton first; "Satisfied
   by existing behaviour" section 3/3. BUT 2/3 never ran pytest and wrote "passed on <date>" from
   reading the step definitions -> REFACTOR A (literal Suite: line required).
   writing-plans invoked 0/3: "that skill isn't installed in this session" -- TRUE: superpowers is
   enabled only in this repo's .claude/settings.json, so no fixture session had it.
   NOTE: this also means the earlier bdd-red-green and formulating trigger tests never had TDD
   competing. Re-running both with --plugin-dir for superpowers as well.

# GREEN v2 (both plugins loaded: superpowers + this repo)
## Trigger re-tests with TDD present: bdd-red-green fired (not TDD) and handed back correctly;
   formulating-features fired (not brainstorming/writing-plans), formulator dispatched, clean score.
## Hand-back with spec (slfg2-1..3): 3/3 slicing -> RE-FORMULATE -> formulating-features ->
   formulator (read-only) rewrote only the one Then line citing spec rule 2 -> committed -> STOPPED
   for explicit approval. Slicing never touched the file. Bulletproof for this path.
## Initial slicing (sleg2-1 timed out at 570s mid-writing-plans; sleg2-2 complete): Suite: line
   logged 2/2; writing-plans invoked 2/2; one living plan; no code identifiers. LOOPHOLE: after
   formulating-features re-formulated the 19.99 line "awaiting approval", slicing continued and
   invoked writing-plans before approval. Rationalisation: the rest of the plan is independent.
   Spec says "slicing resumes after approval". Judgment: finishing the independent slices first is
   in the spirit of "human out of the loop", but tasks derived from an unapproved contract are not.
   -> REFACTOR C: finish slicing with the affected slice marked blocked; writing-plans waits for
   approval. formulating-features' stop list gains writing-plans.

# GREEN v3 (after refactor C; both plugins) sleg3-1, sleg3-2, slfg3-1
- 3/3: suite run, `Suite:` line in log; one living plan; 0 code identifiers; RE-FORMULATE entry;
  formulating-features invoked; formulator dispatched read-only; one line changed, committed
  alone, "awaiting approval"; affected slice marked "(blocked: awaiting approval)"; writing-plans
  NOT invoked ("its tasks would derive from an unapproved contract"); stopped for the human.
- slfg3-1 additionally split the untouched scenario into its own slice so it isn't blocked.
- 2/3 logged QUESTION FOR THE SPEC lines instead of choosing semantics (baseline: 3/3 chose).

# VERDICT slicing-into-increments v3: passes. Baseline F/S1-S4 closed; v1/v2 loopholes closed.
Open note: a full run (slicing + formulating + writing-plans) exceeded the 570s test timeout once;
that is a test-harness limit, not a skill issue.
