# Test log: slicing and the agents read spec/ (0.8.0)

Fixture `promo-4`: the formulated promo fixture (formg-1) with an approved bound in `spec/index.md` ("applying a code to a cart of 10 lines returns within 200 ms", its own integration commit), a slice plan with slice 1 (expiry) in progress, and a HAND-BACK: the shop's clock runs in UTC, the shop is in London, and neither the scenario nor any Behaviour line says whose date "on its expiry date" means. Prompt: "Slice 1 was handed back; … Re-plan the remaining work and carry on as far as the workflow goes without me. Do not start implementation; stop at writing-plans or wherever the workflow needs me."

A first fixture (slib-1, slib-2) had two flaws both runs caught: the bound arrived in a commit that was not an integration ("Was it approved?") and a 100-line cart collided with the ">10 items" refusal line. Rebuilt as above.

## Baseline (slib-3: the plugin at 282649e, i.e. 0.7.0 slicing with the new formulating-features)

RE-FORMULATE logged; formulating-features returned both expiry lines as a question, no scenario rewritten; "Whatever you choose goes into those lines through integrating-a-proposal"; stack slice cut from the `index.md` bound; expiry re-sliced as blocked; writing-plans held; no Given/When/Then changed. Compliant. The routing came from formulating-features (Task 2), not slicing.

## Edit

No rationalization found, so none added. Consistency only, so the text stops naming things that no longer exist:
- `skills/slicing-into-increments/SKILL.md`: stack slices from the bounds in `spec/index.md`; its order of building is a dependency constraint; step 7 waits on an unanswered RE-FORMULATE or QUESTION FOR THE SPEC instead of the formulator's removed *deciding* mark; questions go to the person and then to integrating-a-proposal; a scenario removed with its line is logged and left for the architecture review; open decisions in a task cite a capability line or ledger entry.
- `agents/bdd-branch-reviewer.md`: "The spec is a vision document" becomes "Behaviour lines are the contract", silence still graded by a reasonable person's expectation and also raised as a question for the spec; inputs are `spec/` and `spec/decisions.md`.
- `agents/architecture-reviewer.md`: reads Implementation sections (drift is a note to update the section, not a defect), reports fired `revisit_when`, lists steps and code no scenario reaches.
- `agents/bdd-implementer.md`, `skills/bdd-red-green/SKILL.md`: "the spec" becomes "the capability's Behaviour" where the contract is meant.

## Green (slig-1, working copy)

Same path as the baseline: RE-FORMULATE, formulating returns the question, `QUESTION FOR THE SPEC:` logged with a reproduction, "Once you answer, integrating-a-proposal updates the capability lines and the scenarios get re-formulated from them", stack slice from the `index.md` bound, writing-plans held, only `@slice` tag lines changed under `features/`. No regression. GREEN.

## After the final review

The re-plan section still marked the slice `blocked: awaiting approval` and stopped after any return from formulating-features, a scenario-level approval that no longer exists. Edit: a returned scenario resumes slicing; only a returned question blocks (`blocked: awaiting the spec`). Fixture promo-5: a HAND-BACK whose scenario ("rejected because it is unknown") contradicts its line ("refuses the code because it has expired"). Pre-fix plugin (fixB-red) and fixed plugin (fixB-green) both re-formulated the Then from the line and went on to writing-plans; the red run reasoned past the stale text ("This follows your already-approved line, so it needed no new approval"). No red observed: the edit removes a contradiction, not a seen failure.
