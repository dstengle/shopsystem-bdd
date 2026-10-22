---
id: measurement/missingmass.io/shopsystem/shopsystem-bdd/2026-10-06-agent-efficiency-sdd-task-5
kind: measurement
about: [capability/missingmass.io/shopsystem/shopsystem-bdd/spec-integration, capability/missingmass.io/shopsystem/shopsystem-bdd/formulation, capability/missingmass.io/shopsystem/shopsystem-bdd/spec-migration]
date: 2026-10-07
---

# Agent efficiency task 5: spec agents draft to files, migration through features, implementer report

Implementer report for task 5 of the 2026-10-06 agent-efficiency plan (0.10.0): capability-writer and feature-formulator reply sizes (7478 B and 4814 B at baseline, under 4 KB after), controller context figures, and the legacy migration runs through scripts/features, with fix round 1 (one round-<n>/ drafts directory per dispatch). The brief is Task 5 of .shop/records/archive/plans/2026-10-06-agent-efficiency.md. Commits 34010f5..28bb4d2.

Archived from `.superpowers/sdd/2026-10-06-agent-efficiency/task-5-report.md` (git-ignored scratch), text as it was.

---

# Task 5 report: spec agents draft to files; migration through `features`

Status: DONE_WITH_CONCERNS (all Step 5 criteria pass; concerns below are outside the criteria)
Commit: e6ec51f "Spec agents draft to .superpowers/spec-drafts and reply with the change list; migration moves and verifies through scripts/features"
Test log: docs/superpowers/testing/2026-10-06-spec-agent-drafts-test-log.md (full evidence)

## Fixtures ($SCRATCH/pristine, copied to $SCRATCH/fixtures; builders in $SCRATCH/t5/)

- `spec`: as the brief. Three capabilities with five lines each, five ledger entries, three formulated features, the gift-wrap note, and no `.superpowers/` in `.gitignore`.
- `legacy`: as the brief. Two features for one capability with different Backgrounds, `@slice-1..3`, the living plan, one note, no `spec/`; `4 passed`.
- `spec-form` (added): `spec` with three approved gift-wrap lines committed. Both `spec` runs that reached formulation took formulating-features' small-change path for a single line and dispatched no formulator, so this fixture was needed to measure the feature-formulator.

## Baseline (RED), before any edit

- `spec`, capability-writer reply **7478 B**: `checkout.md` whole plus `decisions.md` whole (six entries) as fenced blocks, plus the change list, the entry again, five questions and the cut sentences. Controller context: 34 943 at the gate, 43 889 at the slicing hand-off, 75 342 at the end (that run also did slicing and writing-plans). Formulation used the small-change path, so there was no formulator reply.
- `spec-form`, feature-formulator reply **4814 B**: three scenarios as fenced blocks, a coverage table of all eight lines, the cases. Context at the formulation commit: 35 543.
- `legacy`:
  - baseline from `--collect-only -q -m slice-$n` in a loop, with no copy of `features/`;
  - `cat > features/cart.feature <<'EOF'` retyped all four scenarios with the Backgrounds inlined by hand;
  - verified by grepping `pytest -rA` and re-running the collect-only loop;
  - plan edited by a Python heredoc.

## Edits

Each was made as the brief says, with the brief's wording.
- capability-writer: tools gain Write; the write-path sentence; item 1 becomes drafts; the reply sentence.
- feature-formulator: tools gain Write; the drafts sentence.
- integrating-a-proposal: step 1 drafts path and `.gitignore` line; step 2 porcelain check first, "each drafted Behaviour section"; step 4 "Apply the drafts …"; both briefs carry the `<DRAFTS PATH>` line and "Write the drafts and reply with"; one Common Mistakes row (7.5 KB).
- formulating-features: steps 1, 2 and 4; the Brief's write/reply paragraph; the Hand-back Brief; one Common Mistakes row (4.8 KB).
- migrating-to-capabilities: the Preconditions baseline; step 4 `features move` / `--inline-background`; step 5 `verify-moved` and `count --by-tag`; two Rationalizations rows and one Red Flag from the baseline.

Consistency edits beyond the brief's list:
- capability-writer: "you return" becomes "you reply with" in two places.
- The "read-only tools" wording in both skills became "a path list, no edit or shell tools, drafts only".
- The text after the Hand-back Brief now checks porcelain and writes the drafted scenario.
- The Migration Brief names `<DRAFTS PATH>`. It had to: the writer now writes only where a brief says. Migration steps 1–3 choose the path, check porcelain and copy the drafts in.

Iteration edits:
- it2, capability-writer: the reply's parts, in order and nothing else.
- it2, migration step 3: `decisions.append.md` becomes `spec/decisions.md` under `# Decisions`.
- it3, migration steps 1 and 2: the drafts path written out in full ("inside the repository"), the `.gitignore` line and the porcelain check.

## Green iterations

| Criterion | it1 | it2 | it3 |
|---|---|---|---|
| spec: writer reply < 4 KB | FAIL 5164 B (8 questions, a drafts description, the ledger entry restated; no file content) | PASS 3653 B | n/a |
| spec: drafts only under spec-drafts, only checkout.md changed sections + decisions.append.md | PASS | PASS | n/a |
| spec: `.gitignore` has `.superpowers/` | PASS (own commit) | PASS | n/a |
| spec: porcelain clean at gate | PASS | PASS | n/a |
| spec: spec/ matches approved lines; other two capabilities and five entries byte-identical | PASS | PASS | n/a |
| spec: formulator reply < 4 KB | not dispatched (small-change path); spec-form: PASS 2688 B | PASS 2970 B | n/a |
| spec: other scenarios byte-identical | PASS (diff only adds) | PASS | n/a |
| legacy: baseline = features/ copy + count --by-tag | discarded x2 (contaminated) | PASS | PASS |
| legacy: moved by `features move` with `--inline-background` | (discarded) | PASS | PASS |
| legacy: verify-moved prints `4 scenarios match` | (discarded) | PASS | PASS |
| legacy: suite summary unchanged | (discarded) | PASS `4 passed` | PASS `4 passed, 8 warnings` |

Controller context, spec fixture:

| Point | Baseline | it1 | it2 |
|---|---|---|---|
| At the gate | 34 943 | 33 937 | 32 765 |
| At the slicing hand-off | 43 889 (no formulator dispatched) | 44 174 | 46 171 (formulator dispatched) |
| At the end | 75 342 | 68 106 | 72 127 |

The end figures are not comparable: the runs did different amounts of slicing and planning.

Discarded legacy runs:
- it1a ran `ls /home/vscode/shopsystem-bdd/docs/`.
- it1b ran `grep … /home/vscode/shopsystem-bdd/docs/capability-format.md`, the format file the skill names, while working out how to apply `decisions.append.md` with no `spec/decisions.md`. The it2 wording fixed that, and later runs did not touch docs/.

## Files changed

agents/capability-writer.md, agents/feature-formulator.md, skills/integrating-a-proposal/SKILL.md, skills/formulating-features/SKILL.md, skills/migrating-to-capabilities/SKILL.md, docs/superpowers/testing/2026-10-06-spec-agent-drafts-test-log.md

## Concerns

1. The controller's context barely falls on this fixture: about 2K lower at the gate, and no lower at the hand-off. The controller `cat`s the drafts it checks, and the change here is one line. The saving should grow with the size of the spec. This fixture does not show it.
2. In migration mode the capability-writer's reply is still 5.5–5.8 KB, because the mapping table is part of it. There is no criterion for it. The writer's "nothing else" reply order sits beside "Reply, in addition to the above, with the mapping table"; the runs read it as intended.
3. README.md:77 still calls the capability-writer "read-only". It is outside Step 6's file list, so I left it.
4. Untested: the Question Brief, the Hand-back Brief, and an agent that actually writes outside the drafts path (Review Focus 5). In every green run porcelain was clean and the controller checked it before the gate, but no run made the check send an agent back.
5. Twice, in legacy resumes (one discarded, one it2), `git rm -q` of the old features and tests hung in the headless harness. The controller redid the step with `-f`. This is not caused by the skill wording.

## Fix round 1

Finding (Important): merging a question round's drafts was undefined; a second round on the same path would have overwritten the first.

Commit 28bb4d2 "Spec drafts: one round-<n>/ directory per dispatch, applied in order"
- integrating-a-proposal:
  - Step 1: each dispatch is a round in `<drafts path>/round-<n>/`, named in its brief.
  - Step 3: answers go back as the next round.
  - Step 4: the rounds are applied in order. A later round's section replaces an earlier round's; each round's `decisions.append.md` is appended in order.
  - The Brief writes to `round-1/`. The Question Brief writes to `round-<N>/`, may read the earlier rounds, and drafts a section it changes whole, with the earlier rounds' drafts of that section applied. Without that, "a later section replaces" would drop lines approved in round one.
- capability-writer: its read list adds "in a question round the earlier rounds' drafts".
- formulating-features: in step 1, the hand-back and a changed line coming back are later rounds. Step 4 writes round by round, and a later round's scenario replaces an earlier one. The Brief and the Hand-back Brief write to `round-<N>/`.
- migrating-to-capabilities: steps 1 and 3 and the Migration Brief (`round-1/`) take the same rule.
- Test log: a "Fix round 1" section. There was no headless re-run, by ruling.

Concern: the round rule is untested by any run, as the question round was before the fix.
