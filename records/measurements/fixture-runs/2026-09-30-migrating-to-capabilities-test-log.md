# Test log: migrating-to-capabilities (0.8.0)

Harness check (throwaway, scratchpad): `check_invariant.py <before> <after>` compares, as multisets, every scenario's title, description, tags and effective steps (Background then its own, Examples included) over `features/**`, the suite's summary line (warnings aside), the passing tests by name, and the collected count for every `@slice-<n>` tag. Negative control: one changed Then line → `INVARIANT BROKEN`.

## Fixture cart-legacy

Two verb-phrase features (`add-products-to-a-cart`, `see-what-the-cart-costs`) for one note about one cart (five rules, one narrator; rule 5, removing a product, has no scenario), with different Backgrounds; module-local step definitions in both test modules; the title "An empty cart" in both files; `@slice-1..3`; a living slices plan; two ADRs; `docs/capability-format.md`. Suite 5 passed. Prompt: "Migrate this repository to capability files as described in docs/capability-format.md: write spec/, and re-pair the existing features, tests and plans with it. The approved scenarios must not change. Carry on as far as you can without me."

**Baseline (migb-1, migb-2; plugin with Tasks 1–3, no migration skill).** The invariant held in both, because nothing moved: each run made one capability per old feature file, "named after the existing feature files so the tests needed no changes" (migb-1). `So that …` kept under the new `Narrator:` line, 2/2. The unbacked removal rule was written into Behaviour with no gate, 2/2; migb-1 committed `spec/`, features and plan in one commit on the main branch. ADRs into the ledger with `source:`, 2/2 (Task 1's agent).

**Edit.** `skills/migrating-to-capabilities/SKILL.md`: preconditions and a recorded baseline; the writer's migration brief ("as if the feature files had never been split … keeping them to spare renames is not a reason"); the gate on capabilities, unbacked lines and questions; the re-pair rules; verify against the baseline; hand-off.

**Green (migg-1).** One capability, `cart` ("It isn't split into 'contents' and 'total' because the note's removal rule changes both in one sentence"); five scenarios to five lines, the removal rule shown as unbacked; stopped at the gate with nothing written. It also found that pytest-bdd binds only one of two same-titled scenarios in a file ("I tested it … the suite would drop from 5 to 4") and asked for two titles instead of renaming. Resumed with "Yes …; B: use your two suggested titles": `spec/` committed alone, then the re-pair in its own commit, Backgrounds inlined, step definitions moved unedited to `conftest.py`, slices plan rewritten. At the re-pair commit, with the two approved titles applied to the before-tree, `INVARIANT HOLDS` (5 scenarios identical, 5 passed, slice counts 3/1/1). GREEN. Edit: the duplicate-title collapse is now a rule, not luck.

**Precondition (migpre-1).** cart-legacy with `conftest.py` importing a name that does not exist (collection error). "I stopped before changing anything … the migration rules say not to repair a broken suite as part of the migration." GREEN.

## shopsystem-kb (copy at 99708e7, never the checkout)

16 features, 171 scenarios, 265 tests, 89 slice tags, 21 ADRs, most step definitions module-local. kb's suite errors under the system interpreter (another kb installed) and is green in its own venv; both runs found this and built the project's `.venv` with `make dev` (edit: the skill now says the project's own test command, a baseline directory of its own).

**Turn one, two runs.** Both cut capabilities across the old features (20 and 16: judgement, e.g. `names` taking scenarios from five old files), mapped 171 scenarios one to one, listed 17–19 unbacked lines from ADRs 0014–0020, and raised the same real conflicts: ADR 0009's default resolve depth against an approved scenario, and ADR 0020's `kb serve` against the approved "the command line offers only init and validate". Both stopped at the gate with nothing written.

Loophole found: run one stopped on a second blocker: "Eight step texts have two bodies … re-pairing can't happen without editing step definitions." Edit: where one step text has different bodies in different old modules, those modules stay untouched and bind their scenarios from the new file by title (`@scenario(file, title)`); a file bound by title is bound by title everywhere, so each scenario is bound once.

**Resumed run one** with the gate answers and the updated skill: `spec/` committed alone (20 capabilities, a decision superseding 0009); re-pair committed alone (19 feature files; two modules' steps moved to `conftest.py`, 14 modules bind by title); note headed as a proposal; then 13 scenarios formulated for the approved unbacked lines and 6 lines returned as questions. Independent check at the re-pair commit against the untouched clone: `scenarios: before 171, after 171, identical=True`, `suite: before '265 passed', after '265 passed'`, all 89 slice counts equal, `INVARIANT HOLDS`. GREEN.

Seen after migration, outside this skill: one formulator dropped an approved scenario from the file it returned; the main agent appended only the new scenarios and checked the approved ones unchanged. The formulating brief already returns the whole file; this is a case for formulating-features to append to an existing feature, not rewrite it (deferred).

## After the final review

Consistency edits: title collisions are checked in step 2, before the gate, and a gate-approved retitle is the one title change, applied to the baseline; old test modules are deleted only when they bind nothing (the title-binding rule keeps some); verify compares passing scenarios by title through the mapping table, not by test id, since rebinding changes module paths. formulating-features now splices new and changed scenarios into an existing feature and checks every other scenario byte for byte, after the kb run's formulator dropped one. Re-run fixC (cart-legacy): one `cart` capability, baseline recorded, stopped at the gate with nothing written. No regression.
