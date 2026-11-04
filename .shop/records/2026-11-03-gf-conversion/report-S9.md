---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-gf-conversion-report-s9
kind: report
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-04
status: done
---

# S9: the docs and the skill say what the check now is

Written by the layer 3 gate from the task's notes: the harness refused the task's own write of this file.

## What changed (commit 1eb8b308)

- `tests/scripts/test_agents.py::test_no_doc_names_telingo_as_current`: no line of `README.md`,
  `docs/capability-format.md`, `docs/design-model/grammar.md` or `skills/checking-spec-consistency/SKILL.md` names
  telingo or `&tel`.
- `README.md`: the tools are GF, pgf 1.1 and clingo 5.8.2; each grammar fun translates to facts; `model logic` is
  one clingo solve of `grammar/check.lp` over the pairs that share vocabulary (L1-L5); `features generate` reads the
  facts with no solver.
- `docs/capability-format.md`, Verifying: the facts, the one solve, L1-L5 and L0 in S5's wording, exit 1 on an error.
- `docs/design-model/grammar.md` §7: the fact names of design-r3 §3, the two-state reading, candidate pairs,
  unification, L0-L5; `features generate`'s fixed reading rule (§5); the tool list without telingo.
- `docs/design-model/design-model.md`: line 21 and "The logic" rewritten; decision row C38 after C37 names
  design-r3 (C37 kept as history).
- The skill: line 10 describes the new check; line 22 makes every L0-L5 a finding, missing tools "gf, clingo".

## Calls made

- Passages outside the plan's line ranges that still described the old solver were rewritten: capability-format's
  ubiquitous row ("Givens from the witness"), its universal-conditions paragraph, and "A scenario is read off a
  trace" (now design-r3 §5: fixed rule, contrast, no Given for "no K is v", no scenario for an unworded fact, v_s3);
  grammar.md §5's "background theory" sentence (L3).
- L0 is listed wherever codes are, since S5 defines it.

## Test runs

- `test_agents.py` before the edits: 4 subtests failed (one per doc); after: 16 passed, 40 subtests, 1.5 s.
- `tools size --limit 300`: exit 0.

## Left open

- Lines over 120 characters at `docs/capability-format.md` 217-219 and 402 were already there.
