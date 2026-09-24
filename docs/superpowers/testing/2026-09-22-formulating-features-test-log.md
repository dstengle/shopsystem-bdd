# Baseline: formulating-features (no skill)

Fixture C: cart project with existing cart.feature (house style visible) + approved promo-codes
spec containing data-model, API and UI sections as bait.
Fixture D: same spec, empty features/ (first feature in the project).

## Subagent reps (Agent tool, general-purpose)
CONTAMINATION: subagents start with cwd = this repo. formb-2 ran `find .` there and read both
docs/superpowers/specs/2026-09-22-bdd-workflow-design.md and skills/bdd-red-green/SKILL.md before
writing. Its output is NOT a baseline. Every subagent rep must be checked for reads of those files.
Fix: headless `claude -p` with cwd = fixture (run_headless.sh). No plugin, no repo in reach.

- formb-1 (clean, no outside reads): 1 file, so-that present, 12 scenarios all @assumes-tagged,
  0 impl / 0 UI / 0 first-person steps. Read tests/test_cart.py and reused step vocabulary.
  One inferred scenario flagged for review. Shape already correct WITH an example file present.
- formb-2: CONTAMINATED (read the recipe). Discarded.
- formb-3: CONTAMINATED (cites "the formulating-features recipe in the workflow spec"). Discarded.
- formd-2: CONTAMINATED (cites the house recipe from the knowledge repo). Discarded.

## Fixture D (no existing feature file) -- the condition that matters
- formd-1 (subagent, CLEAN, 0 contamination hits): 1 file named promo_codes.feature (the TABLE
  name); Feature description is a paragraph with NO "so that" value line; 0 @assumes tags; a
  Background data table with columns percent_off / expires_at / min_total copied from the schema;
  "the customer is told to add £7.50 more" (UI copy); "£" amounts "to match the UI section";
  invented 100%-code scenario ("checks the upper bound behaves"); read cart/__init__.py and tests/.
  Verbatim: "the Background's code table mirrors the promo_codes columns".
- formd-3: CONTAMINATED (cites the recipe). Discarded, but NOTE: even with the recipe it wrote
  `Then the customer is told "That code has expired"` (UI copy verbatim) and named the file
  promo_codes. The spec's recipe wording does not stop UI copy or table naming on its own.

## Headless clean baselines (cwd = fixture, no plugin) formdh-1..3, all 0 contamination
- formdh-1: 1 file promo_codes.feature; description restates spec, no "so that"; 0 tags;
  20 scenarios; Background table with percent_off/expires_at/min_total; read cart/__init__.py.
- formdh-2: 2 files: promo_codes.feature + promo_codes_api.feature (HORIZONTAL slice: "POST
  /carts/c1/promo", "response status is 422", JSON body assertions, 23 impl steps); no "so
  that"; 0 tags; schema tables; read cart/ and tests/.
- formdh-3: 1 file promo_codes.feature; no "so that"; 0 tags; 16 scenarios; read cart/.

## Patterns across the 4 clean no-example runs (formd-1, formdh-1..3)
F1. No value statement: 4/4. Feature description is a paraphrase of the spec's Background.
F2. No assumption tags: 4/4. The spec's two stated assumptions are never referenced.
F3. File named after the table (promo_codes): 4/4.
F4. Data tables with schema column names: 3/4. "the Background's code table mirrors the
    promo_codes columns".
F5. Horizontal slice (separate API feature with status codes): 1/4.
F6. Over-generation: 14-23 scenarios for 8 rules. Invented in >=3/4: 100%-off code, removing a
    code when none is applied, discount recalculated on add, dropped code not restored.
    Rationalisations: "checks the upper bound behaves", "pins boundaries so the implementer
    doesn't have to guess", "the complement of rule 6".
F7. UI copy in Then steps: 1/4 clean (+1 contaminated). "£" amounts "to match the UI section".
F8. Read the source tree: 4/4 (cart/__init__.py), 2/4 also tests/.
Shape WITH an example file present (formb-1) was already correct on F1-F5, F7. F6 mild.
=> Guidance is needed for the first feature in a project. Form: positive contract + coverage
   table (scenario -> spec sentence) so extras have nowhere to hide. Source-tree restriction
   must be structural (agent definition with read-only tools + path list).

# GREEN v1 (headless, --plugin-dir, skill not named) formg-1..3
- 3/3 invoked shopsystem-bdd:formulating-features; 3/3 dispatched
  shopsystem-bdd:feature-formulator with the path-restricted brief; formulator subagent
  transcript shows Read(spec), Glob(features/**), Glob(docs/**) only. 0 source reads.
- 3/3 "so that" line; 3/3 every scenario tagged; 0 impl/UI/schema; verb-phrase file names;
  3/3 stopped for approval. Scenario count 12/15/14 (baseline 14-23).
- LOOPHOLES: formg-2 wrote first-person steps ("When I apply the code", "my cart"): 20 steps.
  3/3 invented "Applying the same code again does not discount twice", citing rule 4 loosely.
  2/3 added a 1%/100% outline (rule 2 does say "1 to 100": a stated boundary, acceptable).
-> REFACTOR: third-person rule; a report slot for unmentioned cases so they stop becoming scenarios.

# GREEN v2 (after refactor) formg2-1..3, headless, skill not named
- 3/3 skill fired; 3/3 formulator agent dispatched; 3/3 formulator read only spec/docs/features.
- 3/3: so-that line, every scenario tagged, 0 impl/UI/schema/first-person, verb-phrase names.
- "Same code again" scenario: 0/3 (was 3/3). Scenario counts 12/13/13, each traceable to a spec
  sentence (1..100 range, optional minimum, inclusive expiry, "at least" minimum).
- Low variance: all three produced the same two files (redeem-promotion-code, remove-promotion-code)
  with near-identical scenario sets. The brief wording is binding.

# VERDICT formulating-features v2: passes. Baseline F1-F8 all closed; GREEN-v1 loopholes closed.

# Addendum (during slicing tests)
- Hand-back mode was missing from the brief: on a RE-FORMULATE with no spec in the repo, 3/3
  runs improvised the right outcome (stopped, asked the human). Added the hand-back brief.
- With a spec present (fixture F2), 4/4 runs rewrote only the contested line, cited the deciding
  spec sentence, committed alone, and stopped for approval. 0/4 continued.
- Trigger re-test with superpowers loaded (brainstorming/writing-plans competing): fired 1/1.

# v0.2.0 (2026-09-23): tag requirement removed; operator is a role where the spec gives one
Verification: v2form-1, v2form-2 (headless, both plugins): 2/2 fired, formulator read only the
spec, 0 tags, shape unchanged (so-that, no impl/UI/first-person).

# v0.3.1 (2026-09-24): model pins
- agents/feature-formulator.md `model: opus`: in a `--model sonnet` session (v5form-1, v5sle-1)
  every formulator subagent turn ran on Opus while every main-session turn stayed on Sonnet.
- SKILL.md `model: opus` on formulating-features and slicing-into-increments: no effect on the
  main session's turns when the skill was invoked through the Skill tool. Removed; the README
  says the session model is chosen at launch.
- Both skills fired and produced correct output on Sonnet sessions (formulation: 2 files, clean
  shape; slicing: 12 capability slices).

# v0.4.0 (2026-09-24): one-line description on every scenario
Change: the brief requires a description line between the Scenario title and the first step,
saying what the scenario pins and why. Reason: the user asked for the explanations given in
review to live on the scenarios. Verification (v6form-1, Opus, fixture D): 11/11 scenarios
described, shape otherwise unchanged (2 files, no impl/UI/first-person).
