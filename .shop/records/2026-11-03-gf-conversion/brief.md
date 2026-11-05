---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-03-gf-conversion-brief
kind: design
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-03
status: draft
---

# The GF conversion: the brief every session of it reads

## What the person asked (2026-11-03, verbatim where quoted)

"I want as much of v4 to stay as possible as long as it is compatible with the new grammar tools."

"I'd like you to continue work on a branch. Conserve context and use subagents. I delegate all judgement to you on
this branch. Please make a full conversion of the plugin to using a grammatical framework. I'd like to come back
tomorrow and see the full plugin converted along with the tools. At that point, I want to be able to create new
requests and have them go through the new requirements system. This is an experimental branch, so make whatever
alterations you need, judging whatever code to keep or rewrite."

Yes to: installing GF and telingo/clingo as real dependencies (network allowed), pushing the branch, multi-agent runs.

## Why

Today's Behaviour lines are free English. They admit two readings, so formulation raises spec questions, rounds
loop, and the suite keeps growing (see memory note "requirements are the linchpin" and the domain-model record).
The next major version writes requirements in a controlled language: the glossary is the GF lexicon, GF parses
every requirement (a line that does not parse is refused before any session reads it), telingo/clingo checks the
logic (resources, exclusivity, universal conditions), and Gherkin scenarios are generated mechanically from the
parsed requirements, not written by a formulator session.

## Where things are

- Branch: `gf-conversion` (pushed to origin). Never touch `main`. No PR.
- The domain model (the typed glossary, the lexicon's source): `.shop/records/2026-11-02-domain-model/domain-model.md`
  and its four extractions beside it.
- Design model v4: `docs/design-model/` (`design-model.md`, `grammar.md`). `spec/index.md` still says v3.
- The spike (throwaway, gitignored, readable on disk): `.shop/scratch/spike-cnl/` - `lexicon.py` (lexicon from the
  glossary), `gf/` (Ears and Steps grammars), `run.py`, `resources.lp`, `cluster.ears`, `out/generated.feature`,
  `venv/` (its Python env), `dl/gf-3.12-ubuntu-24.04.deb` (the GF build), `gf-src/`.
- Today's spec: `spec/` (19 capability files with `[r<n>]` Behaviour lines, glossary, decisions, index) and
  `features/*.feature`, step definitions in `tests/scenarios/`.
- The plugin: `skills/`, `agents/`, `hooks/`, `scripts/` (module map in CLAUDE.md).

## Decisions taken under the delegation (the domain model's §10)

1. Design model: v4 stays wherever it fits the grammar tools; the next design model (v5) is v4 fitted to the
   domain model, not a rewrite. Where v4 and the live files disagree (rule codes, `accepts`, `argues`), the
   grammar tools decide; each change from v4 is listed in v5 with its reason.
2. Kind names: **requirement** and **scenario** (the glossary forbids "capability requirement"); v5 says so once.
3. Initiative transitions: `work start` (to `started`) and `work abandon` (to `abandoned`), from the scripts.
4. Ids: a fresh spec with fresh ids; today's ids are kept only as `restates` on the requirement group that
   replaces them. The retire-and-renumber rule applies from the converted spec onward.
5. Universal conditions get their own ids `U<n>`, in one file of their own under `spec/`, checked on every trace.

## Constraints

- Every tracked Python file stays at 300 lines or fewer (`python3 scripts/tools size --limit 300`).
- A new concern gets a new module and a row in CLAUDE.md's module map.
- Keep reports as records: analysis and subagent reports go under `.shop/records/2026-11-03-gf-conversion/`.
- Push with gh's credentials (GH_TOKEN in the env is invalid):
  `env -u GH_TOKEN GIT_CONFIG_COUNT=2 GIT_CONFIG_KEY_0=credential.helper GIT_CONFIG_VALUE_0= GIT_CONFIG_KEY_1=credential.helper 'GIT_CONFIG_VALUE_1=!gh auth git-credential' git push`
- Never use agent-vault.

## Done means

Tomorrow the person can, on this branch: raise a new request (`work request ...`), and see it go through the new
requirements system - its lines written or checked as codified requirements that parse, logic-checked, scenarios
generated - and on into delivery with `work run`. The tools (`features`, `model`, `tools`, `measure`, `migrate`)
work on the converted spec. The test suite is green.
