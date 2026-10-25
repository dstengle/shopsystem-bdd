# Plan of w145: formulating-features without a small-change path (formulation#r14)

## 1. What goes green

- **formulation#r14**: "When a scenario uses a word its context's glossary avoids, `formulating-features` shall reword the scenario to its line in a round of the kind `formulate`, without a further gate."
  - Scenarios: none. This is a guarantees work-item (formulation is `group: guarantees`, design-decision/workflow-capabilities-are-guarantees). There is no `features/formulation.feature`, and the `@r14` tags in `features/` belong to other capabilities (notes §1). The review judges the work, and `--work-item w145` exits successfully for a guarantees-only item once w125 is in (w125 is green).
  - Why it fails today (notes §3): `skills/formulating-features/SKILL.md` has the session reword such a scenario itself through "The Small-Change Path", with no round. It also keeps an "If the person is talking to you" section and a step-4 sentence that hands `v_t1` rows to "the session the person talks to". Under design-decision/the-context-runs-without-a-coordinator no such session exists, and nothing picks up those rows (notes §2: `work run` starts formulate rounds only for approved capability-proposals).
- Deprecated scenarios retired: none. The work-item has no Retires section.

## 2. Where the change lands

- `skills/formulating-features/SKILL.md`:
  - The "If the person is talking to you" section goes.
  - The sentence "The small-change path below has no round" goes.
  - "The Small-Change Path" section goes as a section. Its glossary-reword rules (change only the words the term replaces, keep the `@r<n>` tag and the title unless the title has the word, a title-only reword is a rebind with no work-item, a step reword is a changed scenario that is deprecated and rebound when it passes) move into the formulate round's process, as Decision 1 says.
  - Step 4's last sentences say the round itself rewords the `v_t1` scenarios, not a session.
  - "Who Does What" says `work run` starts the `initiative-round` of the kind `formulate`, not that a session hands it over.
- `agents/initiative-round.md`: in the `formulate` bullet, the reply clause that lists `v_t1` rows "of a capability this round did not formulate" changes. It now reports the rewording this round did for those rows: the commit, and the scenarios reworded or deprecated. Only this clause changes. w143 (also blocked by w125, not yet started) rewrites this file's "job" to "kind" and the `gate` kind, so leave the rest of the file alone to keep the merge small. The description line (l.3) stays: it may still be true (notes §3).

No file is added. Not changed, by the work-item's scope (Decision 3):
- `skills/integrating-a-proposal/SKILL.md` (w143's);
- `skills/checking-spec-consistency/SKILL.md`;
- `spec/capabilities/spec-consistency.md` r6;
- `README.md` and `docs/` (no small-change mention, notes §3).

No Python file changes, and no test file changes (§4).

## 3. Decisions

1. **The round that finds a `v_t1` row naming another capability's scenario rewords it itself.** After its own commit, the same `formulate` round dispatches one `feature-formulator` for each such capability, in a later round directory. The formulator gets the skill's template, and the change list is the named scenario reworded to its line for the avoided word. The round then verifies the porcelain and the coverage, splices it in, deprecates and rebinds an old scenario that passes (step 4), runs `features bindings` and `model check`, and commits with no gate.
   - Rests on formulation#r14, which says the reword happens "in a round of the kind `formulate`, without a further gate".
   - Rests on design-decision/the-context-runs-without-a-coordinator: no session writes feature files, and its rule stands that a new scenario a fix needs is written by the `feature-formulator` in a `formulate` round.
   - Rests on design-decision/formulation-needs-no-second-approval.
   - The notes' reading A(ii) (leave the row in the reply for a person) is not taken. It would not reword the scenario, so r14 rules it out. Reading A(i) (`work run` starts a new formulate round for it) would need code that r14 does not ask for (notes §7). Either way the narrator sees the same thing: the scenario reworded and committed without a gate. So this choice is not the narrator's to make.
2. **Rows of other capabilities found in the reword's own `model check` are not followed again in that round.** The reword commit is checked like any other, and only failures in scenarios it wrote block it (step 4's existing rule). This keeps a round from chasing rows without end. It rests on formulation#r14 and design-decision/controller-per-spec-round (one round, ending with it).
3. **Leave the small-change references outside w145's file set as they are** (notes' reading B(ii)):
   - integrating-a-proposal's are w143's;
   - spec-consistency r6 changes only through integrating-a-proposal's gate (design-decision/the-context-runs-without-a-coordinator: no session writes spec);
   - `skills/checking-spec-consistency/SKILL.md` l.62-64 belongs to no work-item of i24. The implementer names it in the report as a dangling reference for the branch review, and does not edit it.

   This rests on the work-item's text, which names only formulating-features' Small-Change Path and its "talking to you" section.

## 4. Tests the decisions break

None. I checked the notes (§4): no test reads any `skills/*.md` or agent body text. `tests/scripts/test_agents.py` reads agent frontmatter only, and the frontmatter of `agents/initiative-round.md` does not change (tools and skills stay). `tests/scenarios/supervision_rounds_steps.py` covers only proposal formulate rounds, and no code changes. `tools size --limit 300` printed nothing, and no Python file is touched.

## 5. Open cases (for the implementer to name, not to choose)

- **A reword in a capability whose feature file this round also wrote.** The `v_t1` row then names this round's own scenario, which blocks the commit by step 4's rule. Name whether the skill's text needs to say anything more.
- **A formulator returns a question for a reword** (the reword changes a step's meaning). It goes in the round's reply like any question (r3). Name it if the text leaves this unclear.
- **The Hand-back Template's closing paragraph** ("The session verifies `git status --porcelain` ..., writes the drafted scenario over the old one and commits") still has a session writing a feature file. It is outside the work-item's named sections. Name it in the report for the review; do not change it.
- **Step 3** ("Show the person the question") loses its owner when the "talking to you" section goes. Under `work run` the round returns the question in its reply. Name whether "Who Does What" needs a clause on who shows the question.
