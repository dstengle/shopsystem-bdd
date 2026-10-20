# Test log: spec agents draft to `.superpowers/spec-drafts/`; migration moves and verifies through `scripts/features`

Headless runs: cwd the fixture, `claude -p --model opus --plugin-dir <this checkout>`, superpowers from the installed marketplace, stream-json transcripts. Scored with `reply_sizes.py` (bytes each subagent returned to the controller), the main session's context per call (`cache_read_input_tokens` + input), `git status --porcelain`, and the fixture's git history. When a run stopped at the gate, it was resumed with "Yes, the lines are approved."; when it then still asked for the open questions, with "Leave every question open: none of them adds a line."

Fixtures (scratchpad only, git identity set, no `__pycache__`):
- `spec`: the cart example with `spec/index.md`, `spec/decisions.md` (five entries) and three capabilities, `cart.md`, `checkout.md`, `receipt.md`, each with Purpose, five Behaviour lines, Implementation and Not yet; the three formulated feature files; an approved note `docs/superpowers/specs/2026-10-06-gift-wrap-design.md` with one rule ("When the customer asks for gift wrap at checkout, gift wrap adds 3.00 to the total.") and one decision (flat charge per order). `.gitignore` has no `.superpowers/` line. Prompt: "The gift-wrap design is approved; carry on."
- `spec-form`: `spec` after a gate that approved three gift-wrap lines in `checkout.md` and the decision, committed; features not formulated. Added because both `spec` runs that reached formulation took the small-change path for one line and dispatched no formulator. Three lines exceed that path. Prompt: "The gift-wrap lines in spec/capabilities/checkout.md are approved and committed; formulate them."
- `legacy`: the cart example with `add-products-to-a-cart.feature` (Background: empty cart, Widget; `@slice-1`, `@slice-2`) and `see-what-the-cart-costs.feature` (Background adds Gadget; two `@slice-3`), step definitions in `tests/conftest.py`, one binding module per feature, the living `cart-slices.md`, a note under `docs/superpowers/specs/`, no `spec/`. Suite: `4 passed`. Prompt: "Migrate this repository to capability files."

## Baseline (RED)

`spec`, three turns:
- **capability-writer reply: 7478 bytes.** It returned `spec/capabilities/checkout.md` whole and `spec/decisions.md` whole (all six entries, five unchanged) as fenced blocks, then the change list (one added line), the new entry again, five questions and two cut sentences.
- At the gate the tree was clean (nothing written; agents had no Write).
- Applied by a `python3 - <<'EOF' ... s.replace(...)` heredoc on `checkout.md`, then committed `spec/` alone.
- Formulation took the small-change path (one line): no feature-formulator dispatched; the controller edited `checkout.feature` itself.
- Controller context: 34 943 at the gate; 43 889 when formulation was committed (the slicing hand-off); 75 342 at the end (slicing and writing-plans followed).

`spec-form`, one turn:
- **feature-formulator reply: 4814 bytes**: the three new scenarios as fenced blocks, a coverage table of all eight lines (five unchanged), four cases no line mentions, the paths. The controller spliced them in with a heredoc. Context at the formulation commit: 35 543.

`legacy`, two turns:
- **Baseline:** `python -m pytest -q -rA ... > $B/full.txt; for n in 1 2 3; do python -m pytest -q --collect-only -m slice-$n ...; done`. No copy of `features/`. RED.
- **Moving:** `cat > features/cart.feature <<'EOF'` with all four scenarios retyped, Backgrounds inlined by hand. RED.
- **Verifying:** `python -m pytest -q -rA | grep -E '^PASSED|passed'` and the `--collect-only` loop against the baseline's numbers. Nothing compared the scenarios' text. RED.
- The plan's `Scenarios:` lines rewritten by a `python - <<'EOF' ... s.replace(...)` heredoc.

## Edits

- `agents/capability-writer.md`: `tools: Read, Glob, Grep, Write`; writes only under the drafts path the brief names, `spec/` included; What you return item 1 is the drafts (a new file whole; a changed capability's changed sections under their headings; new ledger entries in `decisions.append.md`; never an unchanged file or section); the reply holds items 2, 4, 5 and the drafts' paths, no file content. "return"/"Return" where the reply is meant became "reply with".
- `agents/feature-formulator.md`: `tools: Read, Glob, Grep, Write`; drafts under the brief's path only (a new feature whole; for an existing one, the new and changed scenarios headed by their lines); the reply holds the coverage table, questions, cases and the drafts' paths.
- `skills/integrating-a-proposal/SKILL.md`: step 1 chooses `.superpowers/spec-drafts/<date>-<note name>/` and adds the `.gitignore` line alone; step 2 checks `git status --porcelain` first and compares each drafted Behaviour section; step 3 drops a rejected line from the drafts; step 4 "Apply the drafts"; both briefs name `<DRAFTS PATH>` and say "Write the drafts and reply with"; a Common Mistakes row from the baseline (7.5 KB reply). The writer row and the process wording no longer say "read-only tools".
- `skills/formulating-features/SKILL.md`: the same drafts path and porcelain check in steps 1 and 2; step 4 "copied from its draft"; the Brief's Return paragraph and the Hand-back Brief write to `<DRAFTS PATH>`; the text after the Hand-back Brief checks porcelain and writes the drafted scenario; a Common Mistakes row from the `spec-form` baseline (4.8 KB reply). No `features` script use.
- `skills/migrating-to-capabilities/SKILL.md`: the baseline is the summary line, `-q -rA`, a copy of `features/` and `features count --by-tag` at `<this skill's base directory>/../../scripts/`; step 4 moves by `features move "<title>" --to features/<name>.feature` with `--inline-background` where Backgrounds differed; step 5 verifies with `features verify-moved --from <baseline>/features` and `features count --by-tag`; the Migration Brief names `<DRAFTS PATH>` (the writer now writes only where a brief says); steps 1–3 choose the drafts path, check porcelain, and copy the drafts in; two Rationalizations rows and one Red Flag from the baseline.

## Green runs

### Iteration 1

`spec`: **FAIL on the writer's reply size.**
- capability-writer reply **5164 bytes**, no file content. It held a "Drafts" section describing each draft, the change list, the ledger entry restated, eight questions (the baseline had five), two cut sentences.
- Drafts: `.superpowers/spec-drafts/2026-10-07-gift-wrap-design/spec/capabilities/checkout.md` (frontmatter, Purpose, Behaviour) and `decisions.append.md` (the one new entry). Nothing else.
- `.gitignore` gained `.superpowers/` in its own commit (`Ignore .superpowers/ drafts`); `git status --porcelain` empty at the gate.
- After approval: the spec commit adds one Behaviour line, one `rests_on` entry and the new ledger entry; `cart.md`, `receipt.md`, `index.md` byte-identical; the five earlier entries byte-identical (the diff only appends). The Purpose edit the writer drafted without a note sentence was asked at the gate, not approved, and not applied.
- Formulation again took the small-change path (no formulator); the feature commit only adds the new scenario.
- Context: 33 937 at the gate (baseline 34 943); 44 174 at the slicing hand-off (baseline 43 889).

`spec-form`: **PASS.** feature-formulator reply **2688 bytes**, no file content; one draft, `.superpowers/spec-drafts/2026-10-07-checkout/checkout.feature`; `.gitignore` line committed alone; porcelain empty after the agent; the feature diff only adds the three scenarios. Context at the formulation commit 36 269 (baseline 35 543).

`legacy`: **two runs discarded as contaminated.** The first ran `ls /home/vscode/shopsystem-bdd/docs/`, the second `grep ... /home/vscode/shopsystem-bdd/docs/capability-format.md`, the format file the skill names. The second did it while working out how to apply `decisions.append.md` when `spec/decisions.md` does not exist yet. Both otherwise showed the intended behaviour: a `features/` copy and `features count --by-tag` baseline, `features move ... --inline-background`, `4 scenarios match`.

Iteration 2 edits:
- `capability-writer.md`: the reply's parts in order, and nothing else: the drafts' paths, the change list, the questions, the cut sentences.
- `migrating-to-capabilities` step 3: `decisions.append.md` becomes `spec/decisions.md` under a `# Decisions` heading.

### Iteration 2

`spec`: **PASS on every criterion.**
- capability-writer reply **3653 bytes**: paths, change list, five questions, cut sentences; no file content, no restated ledger entry.
- Drafts only `spec/capabilities/checkout.md` (frontmatter and Behaviour) and `decisions.append.md` under `.superpowers/spec-drafts/2026-10-07-gift-wrap-design/`.
- `.gitignore` has `.superpowers/` (own commit); porcelain empty at the gate.
- After approval `spec/` matches the approved line: `checkout.md` gains the line and `rests_on` entry; `cart.md`, `receipt.md`, `index.md` byte-identical; `decisions.md` before the change is a byte-identical prefix of after.
- This time the feature-formulator was dispatched: reply **2970 bytes**, no file content, one draft `.superpowers/spec-drafts/2026-10-07-checkout/checkout.feature`; the feature commit adds only the new scenario.
- Context: 32 765 at the gate (baseline 34 943); 46 171 at the slicing hand-off (baseline 43 889, which wrote the scenario itself and dispatched no formulator); 72 127 at the end (slicing only; the baseline's 75 342 also included writing-plans).

`legacy`: **PASS on the four criteria; the drafts were outside the repository.**
- Baseline: `cp -r features $B/features` and `features count --by-tag | tee $B/count.txt`.
- Header by `printf`; every scenario by `features move "<title>" --to features/cart.feature --inline-background`.
- `features verify-moved --from $B/features` -> `4 scenarios match`; summary `4 passed`; `diff` of `count --by-tag` equal.
- But the controller chose `$SCRATCH/spec-drafts` (`../../spec-drafts`) as the drafts path, outside the repository, and added no `.gitignore` line. Step 1 had said "chosen as integrating-a-proposal's step 1 says", and that skill was never loaded.

Iteration 3 edit: `migrating-to-capabilities` steps 1 and 2 name `.superpowers/spec-drafts/<date>-migration/`, "inside the repository", the `.gitignore` line and the porcelain check in full.

### Iteration 3 (`legacy` only)

**PASS on every criterion.**
- Drafts under `.superpowers/spec-drafts/2026-10-07-migration/` (`spec/index.md`, `spec/capabilities/cart.md`, `decisions.append.md`); `.gitignore` line committed alone; porcelain empty at the gate.
- Baseline is a copy of `features/` plus `features count --by-tag`.
- `spec/decisions.md` written as `# Decisions` plus `decisions.append.md`, with no read of the plugin's docs.
- Every scenario moved by `features move ... --inline-background`; `features verify-moved` -> `4 scenarios match`; `count --by-tag` diff equal; `4 passed, 8 warnings` as before.
- The plan's `Scenarios:` lines were edited with Edit, not a heredoc.

## Not verified by a run

- The Question Brief and the Hand-back Brief: no fixture reached either.
- An agent that writes outside the drafts path (Review Focus 5): no run did, so the porcelain check never had to send an agent back. In every green run it was clean at the gate, and the controller ran the check before the gate.
- The capability-writer's reply in migration mode stays over 4 KB (5487 and 5805 bytes): the mapping table is part of it. Migration had no size criterion.

## Fix round 1 (task review)

Each dispatch is now a round with its own directory, `<drafts path>/round-<n>/`, named in its brief:
- integrating-a-proposal: The Brief writes to `round-1/`. The Question Brief writes to `round-<N>/`, may read the earlier rounds, and drafts a section it changes whole, with the earlier rounds' drafts of that section applied.
- Step 4 applies the rounds in order: a later round's section replaces an earlier round's, and the `decisions.append.md` files are appended in order.
- formulating-features (Brief, Hand-back Brief, step 4) and migrating-to-capabilities (steps 1 and 3, the Migration Brief) take the same rule.
- capability-writer may read the earlier rounds in a question round.

Before this fix, a question round on the same path would have replaced round one's drafts with ones built from the committed spec. No headless re-run, by the controller's ruling: the question round had no run before the fix either. Every green run above answered "Leave every question open" and had a single round.
