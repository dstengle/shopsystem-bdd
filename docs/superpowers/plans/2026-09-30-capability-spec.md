# Capability Spec Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `spec/` (capability files, a decision ledger, an index) the single spec the plugin works from, and ship a skill that migrates an existing repository onto it without changing any approved scenario.

**Architecture:** One new agent (`capability-writer`, read-only, blind to code) holds the format rules. Two new skills orchestrate it: `integrating-a-proposal` (every approved note) and `migrating-to-capabilities` (once per repository, adds the re-pairing of features, tests and plans). Existing skills and agents change where they read "the spec" or gate on scenarios.

**Tech Stack:** Claude Code plugin (markdown skills and agents), Gherkin, pytest-bdd for fixtures, headless `claude -p` for baseline and green runs.

**Spec:** `docs/superpowers/specs/2026-09-29-capability-spec-design.md`. Format source: `docs/stage-1-capabilities-and-features.md`.

## Global Constraints

- Every skill is written test-first per superpowers:writing-skills: a headless baseline before the edit, the same prompt after, logged under `docs/superpowers/testing/2026-09-30-*.md`.
- Headless runs: cwd is the fixture, never this repository; `claude -p --model opus --plugin-dir /home/vscode/shopsystem-bdd` plus superpowers from the installed marketplace; fixtures live in the session scratchpad. A run that read any file of this repository is contaminated and discarded.
- Capability and feature names are hyphenated on both sides.
- The ledger is append-only; entry properties are `date`, `revisit_when`, `supersedes`, `source` as in the spec.
- The gate is on Behaviour lines. Nothing in the plugin keeps a scenario-level approval.
- Migration never changes a scenario's effective step sequence, title, description or tags.
- No tooling shipped. A throwaway script in the scratchpad may check a test run; the skill itself never relies on one.
- House style: skills and agents follow the terse, table-and-rule style of the existing ones (compare `skills/formulating-features/SKILL.md`), including a Common Mistakes or Rationalizations table filled from baseline evidence only.
- No commit, push or tag of any consuming repository. `shopsystem-kb` is only ever copied.

## Review Focus

1. A note that contradicts an existing Behaviour line: integration must show the change as `changed` at the gate, never silently overwrite. Pinned in Task 1's second fixture.
2. Migration where scenarios from two source files share a title: must surface as a question, not a rename. Pinned in Task 4's cart fixture.
3. Migration where step definitions are module-local and their scenarios move to a file bound by another module: the suite must stay identical. Pinned in Task 4 (cart fixture has one module-local step; kb has many).
4. Migration started on a repository whose suite does not run cleanly (kb at HEAD errors in collection): the skill must stop at its precondition rather than record a broken baseline. Pinned in Task 4, run against kb HEAD before a green commit.
5. A formulator that reads "Implementation, may change" and writes a scenario from it. Pinned in Task 2's fixture bait.

---

### Task 1: Format reference, capability-writer agent, integrating-a-proposal skill

**Files:**
- Create: `docs/capability-format.md` (the stage-1 doc, with hyphenated names and the ledger entry shape from the spec's File conventions; the untracked `docs/stage-1-capabilities-and-features.md` is moved here with `git mv` after being added)
- Create: `agents/capability-writer.md`
- Create: `skills/integrating-a-proposal/SKILL.md`
- Create: `docs/superpowers/testing/2026-09-30-integrating-a-proposal-test-log.md`
- Scratchpad: `fixtures/promo/` (cart example copy plus `docs/superpowers/specs/2026-09-30-promo-design.md`), `fixtures/promo-2/`, `run_headless.sh`

**Interfaces:**
- Produces: agent type `shopsystem-bdd:capability-writer`; its return shape (files, change list with `added|changed|removed`, ledger entries, questions, cut sentences; mapping table in migration mode); skill `integrating-a-proposal` whose last step invokes `formulating-features` with changed capability paths plus the change list.

- [ ] **Step 1: Build the fixture and harness.** Copy `skills/bdd-red-green/example/` to `$SCRATCH/fixtures/promo/`, `git init` it and commit. Write a promo-code note as a brainstorming note would (purpose, business rules with one inclusive boundary, a data-model section with column names, a UI section with message copy, an "Implementation" style paragraph on caching, a rationale paragraph comparing a rejected design, a decisions section, a "not in this version" list, and one rule with an unstated condition: what happens when a second code is applied). `run_headless.sh <fixture> <name> <prompt>` runs `claude -p` in the fixture with the Global Constraints flags and saves the transcript to `$SCRATCH/runs/<name>.jsonl`.
- [ ] **Step 2: Baseline (RED).** Three runs with no agent and no skill: prompt gives the note path and the stage-1 doc copied into the fixture as prose, asks for `spec/`. Score each: "shall" count; Behaviour lines whose response the narrator cannot observe; rationale kept; unstated conditions not raised; decisions missing from `decisions.md`; data-model or UI words in Behaviour. Record verbatim evidence in the test log.
- [ ] **Step 3: Write `agents/capability-writer.md`** (Read, Glob, Grep; `model: opus`): its read list, the format rules from `docs/capability-format.md` condensed into the definition, the return shape above, migration mode's mapping table rules from the spec's Migration step 1.
- [ ] **Step 4: Write `skills/integrating-a-proposal/SKILL.md`** with the spec's trigger and five steps, the dispatch brief verbatim (as `formulating-features` has one), and a Common Mistakes table from the Step 2 evidence. Description starts "Use when a brainstorming note or design spec has been approved…".
- [ ] **Step 5: Green run.** Same prompt, plugin loaded. Pass: 0 "shall"; every Behaviour response observable; rationale cut or in the ledger; the second-code condition raised as a question; the skill stops at the gate. Iterate the agent/skill wording until it passes; log each iteration.
- [ ] **Step 6: Second fixture.** `promo-2` = `promo` with the green `spec/` committed plus a second note that adds one rule, changes the boundary of an existing one, and drops one. Pass: no second spec; change list shows one `added`, one `changed`, one `removed`; earlier ledger entries byte-identical; removed line shown at the gate.
- [ ] **Step 7: Verify inventory.** `claude --plugin-dir /home/vscode/shopsystem-bdd plugin details shopsystem-bdd` lists 6 agents and 4 skills, all parsed.
- [ ] **Step 8: Commit** the format doc, agent, skill and test log.

### Task 2: formulating-features and feature-formulator read capabilities

**Files:**
- Modify: `skills/formulating-features/SKILL.md` (Process, The Brief, The Hand-back Brief, Common Mistakes; description)
- Modify: `agents/feature-formulator.md` (read list)
- Create: `docs/superpowers/testing/2026-09-30-formulating-from-capabilities-test-log.md`

**Interfaces:**
- Consumes: capability files and the change list from Task 1.
- Produces: feature files with the header `# formulated from spec/capabilities/<name>.md` / `Feature: <title>` / `  Narrator: <narrator>`; a coverage table one row per line; a question returned for a two-reading line, on which the skill invokes `integrating-a-proposal`.

- [ ] **Step 1: Fixture.** `promo-3` = the approved `spec/` from Task 1 with an Implementation sentence that reads like behaviour ("codes are cached for five minutes, so a revoked code may still apply") and one Behaviour line with two readings ("When the cart total reaches the minimum, the code applies": reaches = at or above?). No `features/` for promo.
- [ ] **Step 2: Baseline (RED).** Current 0.7.0 skill, prompt: "the capability files under spec/ are approved; formulate". Score: file named by verb phrase instead of capability; `So that` header instead of `Narrator:`; scenarios not 1:1 with lines; a scenario from the caching sentence; the two-reading line decided in a scenario; settled/deciding sort still applied.
- [ ] **Step 3: Edit** the skill and agent as the spec's "Changes: formulating-features and feature-formulator" states: input, read list (`spec/` and `features/` only), header, one scenario per line, outline rules, descriptions kept, changed/removed lines, 1:1 coverage both ways, settled/deciding removed (steps 4 and 5 and their two Common Mistakes rows replaced), two-reading line returned as a question and routed to `integrating-a-proposal`, hand-back brief rewritten, description triggers on changed capability files.
- [ ] **Step 4: Green run.** Pass: header shape; name matches the capability; 1:1; nothing from Implementation; the two-reading line comes back as a question with both readings and no scenario; the skill invokes `integrating-a-proposal` for it.
- [ ] **Step 5: Commit** skill, agent, test log.

### Task 3: slicing-into-increments and agent wording

**Files:**
- Modify: `skills/slicing-into-increments/SKILL.md` (step 2 stack source, step 3 order of building, step 7 gate wording, re-plan section, Semantics section, one rationalization row from the baseline)
- Modify: `agents/bdd-branch-reviewer.md` (the vision-document rule), `agents/architecture-reviewer.md` (ledger, Implementation sections, fired `revisit_when`), `agents/bdd-implementer.md`, `agents/bdd-task-reviewer.md`, `skills/bdd-red-green/SKILL.md` (wording: "the capability's Behaviour" where the contract is meant)
- Create: `docs/superpowers/testing/2026-09-30-slicing-with-capabilities-test-log.md`

**Interfaces:**
- Consumes: `integrating-a-proposal` (Task 1) as the destination of `QUESTION FOR THE SPEC:`; formulating's question route (Task 2).

- [ ] **Step 1: Fixture.** `promo-4` = promo with `spec/`, formulated features, slice plan with slice 1 green, `index.md` stating one bound ("apply returns within 200 ms for a cart of 100 lines") and an order of building, and a HAND-BACK entry whose scenario no Behaviour line decides.
- [ ] **Step 2: Baseline (RED).** 0.7.0 slicing plus Task 1–2 skills. Score: stack slice source; order of building ignored; the hand-back resolved by editing a scenario or a line; question left in the plan log only.
- [ ] **Step 3: Edit** the skill and agents as the spec's "Changes: slicing-into-increments" and "Changes: agents".
- [ ] **Step 4: Green run.** Pass: a stack slice from the `index.md` bound; order of building respected; hand-back goes to formulating, then `integrating-a-proposal`; no Behaviour line or scenario edited by slicing.
- [ ] **Step 5: Verify wording.** `grep -n "vision document" agents/` returns nothing; `grep -n "decisions.md\|Implementation" agents/architecture-reviewer.md` returns the new rules.
- [ ] **Step 6: Commit** skill, agents, test log.

### Task 4: migrating-to-capabilities

**Files:**
- Create: `skills/migrating-to-capabilities/SKILL.md`
- Create: `docs/superpowers/testing/2026-09-30-migrating-to-capabilities-test-log.md`
- Scratchpad: `fixtures/cart-legacy/`, `fixtures/kb/`, `check_invariant.py`

**Interfaces:**
- Consumes: `capability-writer` migration mode (Task 1), `integrating-a-proposal` step 4 gate (Task 1), `formulating-features` (Task 2).

- [ ] **Step 1: Cart fixture.** `cart-legacy`: two verb-phrase features (`add-products-to-a-cart.feature`, `see-what-the-cart-costs.feature`) that the note clusters into one capability, with different Backgrounds; one module-local step definition in each test module; one scenario title present in both files; `@slice-<n>` tags; a living `docs/superpowers/plans/…-slices.md`; a note; an `adrs/` with two ADRs. Suite green.
- [ ] **Step 2: Invariant script.** `check_invariant.py <before> <after>`: parses both trees' feature files, compares each scenario's effective step sequence, title, description and tags keyed by title, and compares `pytest -q` summary, passing node set by scenario name, and `pytest --collect-only -q -m slice-<n>` counts. For the harness only.
- [ ] **Step 3: Baseline (RED).** Plugin with Tasks 1–3, no migration skill; prompt: "migrate this repository to capability files per docs/capability-format.md". Score with the script plus: scenarios merged or reworded; tests broken; collision renamed silently; ADRs ignored; no gate.
- [ ] **Step 4: Write the skill** with the spec's trigger, preconditions, five steps, the writer's migration brief verbatim, and rationalizations from the baseline.
- [ ] **Step 5: Green run on cart-legacy.** Pass: invariant script clean; one feature per capability with the new header; collision raised as a question; ADRs in the ledger with `source:`; stop at the gate, then (second prompt approving) re-pair and verify; notes carry the proposal header.
- [ ] **Step 6: kb, precondition.** Copy `/home/vscode/shopsystem-kb` to `$SCRATCH/fixtures/kb` (`git clone --local`), install it editable in a fresh venv, run the skill at HEAD. Pass: if the suite errors, the skill stops at the precondition and records nothing.
- [ ] **Step 7: kb, full run.** Check out the latest kb commit whose suite runs green in that venv (bisect back from HEAD by running the suite), run the skill through the gate with a scripted approval. Pass: invariant script clean across all 16 source features; module-local steps moved unedited; slices plan updated; batch plans untouched. Record counts in the log.
- [ ] **Step 8: Commit** skill and test log.

### Task 5: Trigger test, docs, release

**Files:**
- Modify: `README.md` (pipeline, skills and agents lists, agents table row for `capability-writer`, the `CLAUDE.md` line for consuming repos, a 0.8.0 section)
- Modify: `docs/superpowers/specs/2026-09-22-bdd-workflow-design.md` (pointer where its pipeline and formulating sections are superseded)
- Modify: `.claude-plugin/plugin.json` (version `0.8.0`, description mentions capability specs)
- Modify: `docs/superpowers/testing/2026-09-30-integrating-a-proposal-test-log.md` (trigger section)

- [ ] **Step 1: Trigger test.** Fixture `promo` with the note freshly committed; prompt as a person finishing brainstorming: "the design is approved, carry on". Pass: `integrating-a-proposal` is invoked before `formulating-features` or `writing-plans` in 3 of 3 runs. If not, tighten the description and rerun; record each.
- [ ] **Step 2: Docs.** README and design-doc edits as listed; README states the kb migration counts from Task 4.
- [ ] **Step 3: Version.** Bump to 0.8.0; `claude --plugin-dir /home/vscode/shopsystem-bdd plugin details shopsystem-bdd` parses with 6 agents, 5 skills.
- [ ] **Step 4: Commit** as `0.8.0: …` in the style of earlier release commits.
