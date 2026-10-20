---
id: decision-argument/missingmass.io/shopsystem/shopsystem-bdd/2026-10-17-type-first-ids-and-ubiquitous-language-design
kind: decision-argument
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-10-17
---

# Type-first ids and a ubiquitous language: design

Date: 2026-10-17. Agreed with the person in conversation on 2026-10-16/17. Two releases:
0.19.0 (already on branch `0.19.0-requirement-ids`, unmerged) is amended with Part 1; 0.20.0 is Part 2.

## What the person decided

- Every id follows the type-first convention, so prefixes are consistent across the system. The type
  segment is the design model's kind name (bounded-context, capability, design-decision, term, …),
  because those names are scoped and less ambiguous. shop-knol takes these names when it migrates to v3.
- A bounded context's ubiquitous language is part of the model: glossary entries in `spec/index.md`'s
  Glossary section, each a standing node approved at the gate like a Behaviour line.
- A term change rides with the capability-proposal that needs it (`adds: [term/<name>]`).
- A new skill checks a spec's internal consistency. Fix mode settles a term once in the glossary and
  applies it everywhere; findings that are not about a term are asked one at a time. The skill runs on
  demand only in this release; wiring it into rounds is a later change.
- `model check` finds clingo when a project's virtualenv hides it; `features` takes `--file` when a title
  is in several files.
- Two releases: the id convention amends 0.19.0, which is unmerged and unmeasured, so kb migrates once,
  on the final form; the glossary and the skill are 0.20.0.

## Part 1 (0.19.0): type-first ids

### The convention

- A context's path is `<owner domain>/<product>/<context name>`, e.g. `missingmass.io/shopsystem/kb`.
- A node's id is `<kind>/<context path>/<name>`; the context's own id is `bounded-context/<context path>`.
  The IRI is the shared base `https://missingmass.io/shopsystem/` followed by the id.
- `<name>` is one plain name: lowercase letters and digits in hyphen-separated runs (kb's IRI grammar).
  Names that held a `/` (`first-spec/slicing`, `design-model-check/1`) become hyphenated
  (`first-spec-slicing`, `design-model-check-1`).
- A requirement is a part of its capability: `capability/<path>/<name>#r<n>`, short for
  `#behaviour/r<n>`. A term id is `term/<path>/<term>`, the term lowercased with spaces as hyphens.
- Inside one context, `<kind>/<name>` stands for `<kind>/<context path>/<name>`. Where a field fixes the
  kind (`argues`, `rests_on`, `under`, `depends_on`, a `#r<n>` reference), a bare `<name>` is accepted too.
- Kind names used as type segments: bounded-context, capability, design-decision, acceptance-scenario
  (internal only), term, initiative, capability-proposal, job-proposal, cross-context-request,
  work-item, observation, measurement, review-finding, decision-argument, initiative-archive.
- Not type-first and refused: `<context name>/<name>` (0.19.0's short form), `decision/<name>`,
  `obs/<name>`, `capability/<name>` as a frontmatter `id` (an `id` is always written in full).

### Changes

- decision 0027 rewritten (it is proposed, never accepted) to this convention.
- `scripts/model`: reads full and short forms; a node `id` not in full type-first form is a file problem;
  a reference not in any accepted form is unresolved. The 0.19.0 `<context name>/<name>` form is
  removed. Its tests change with it.
- `docs/capability-format.md`, `agents/capability-writer.md`, `agents/feature-formulator.md` (if it names
  ids), and `skills/migrating-to-capabilities` teach the convention. Adding Ids also rewrites a
  repository's `decision/<name>` references and ledger headings to `design-decision/<name>`, and its
  `capability/<name>` references are left as they are (they are valid short forms).
- This repository is renamed: spec/index.md, capability ids, decisions' ids and `supersedes`,
  observations' headings and `about:`, records' ids, work initiatives and parts, every reference.
  A mechanical rename that changes no content is a migration, not an edit of a decision or observation.
- Evidence: unit tests for every accepted and refused form; the integrate and migrate fixture cases rerun
  three times each with the new forms; the kb-clone trial rerun (Adding Ids, report the result).

## Part 2 (0.20.0): a ubiquitous language

### Glossary entries

- Form, in `spec/index.md`'s `## Glossary`:
  `- **<term>**: <one-sentence definition>. Not: <word>, <word>.` The `Not:` part is optional. A bullet in
  that section not of this form is a file problem.
- A term is standing (`node(T, "term")`), id `term/<path>/<term>`, approved at the gate. Renaming a term is
  removing one and adding another.
- Facts from `model facts` (stdlib): `node(T,"term")`, `term_of(T, Ctx)`, `avoid(T, Word)`, and
  `mentions(X, Word)` for each requirement and scenario, for each term and avoided word, matched as a whole
  word, case-insensitively, a plural "s" allowed.
- Constraints in model.lp, proposed against grammar.md as FIX/extension notes:
  `v_t1(X, W, T)` a requirement or scenario mentions a word its context's glossary avoids;
  `v_t2(T)` two entries with one term; `v_t3(W)` a word one term avoids is another term of the context.
- How a glossary change reaches the gate: in a consuming repository, through integrating-a-proposal's gate
  like a line, the spec commit naming terms added, changed, removed; in a repository with `work/`, a term
  rides with the capability-proposal that needs it (`adds: [term/<name>]`).

### The skill: `checking-spec-consistency`, and the agent `spec-checker`

- `spec-checker` reads only `spec/` and `features/` (Read, Glob, Grep, Write; writes only under the drafts
  path), never the source, and replies with a short summary; its findings go to a file.
- Dispatches: one per capability (its lines against its scenarios: scenario wording that drifts from its
  line, lines with two readings); one for the whole context (every Behaviour line and the glossary, no
  scenarios: one term for two things, two words for one thing, likely terms the glossary lacks).
  `model check` runs first for `v_t1`–`v_t3`. The skill states the dispatch count before it starts.
- Report mode (default): one findings file, grouped by term cluster, then lines with two readings, then
  other drift; each finding names its ids. Changes nothing.
- Fix mode walks the person through the findings:
  1. Terms first: per cluster, a proposed glossary entry with its `Not:` words; on the person's yes, the
     entry and the line changes that apply it (ids kept) go through one gate pass per term.
  2. Scenarios follow: scenarios using an avoided word are reworded to their line through formulation's
     small-change path, with no further approval.
  3. Then one at a time: a line with two readings is a question with its readings, answered through
     integrating-a-proposal's question path; other drift asks which side is right.
  4. `model check` after each step. Done when `v_t*` is clean and every finding is applied, rejected or
     deferred to the backlog.
- The skill is on demand; it is not wired into integration or formulation rounds.

### Fixes

- `scripts/model`: when `import clingo` fails, it tries `$SHOPSYSTEM_MODEL_PYTHON`, each `python3` on `PATH`
  outside the active virtualenv's `bin/`, `/usr/local/bin/python3`, `/usr/bin/python3`, with
  `-c "import clingo"`, and re-runs itself under the first that has it (once, by an environment flag). With
  none, exit 2 as today, naming each interpreter tried.
- `scripts/features`: `tag`, `hold`, `retire` and `move` take `--file <path>`: work in that file only;
  refuse if the title is not in it or is in it twice. Without `--file`, a title in several files is refused
  as now. Adding Ids step 5 and formulating-features step 4 say to use `--file` when `features` names
  several files.

### Spec and evidence

- A new initiative with one capability-proposal per capability: a new capability `spec-consistency`
  (workflow; its scenarios come as fixture sessions with i4); design-model-check (terms, `v_t1`–`v_t3`, the
  clingo search); feature-file-tools (`--file`); spec-integration (a term rides with a change; the gate and
  commit name terms); formulation (scenarios follow a term).
- Unit tests for every new script line.
- A fixture case `consistency` with planted drift (two words for one thing across two capabilities, a
  scenario off its line, a line with two readings): report mode finds all three, three runs; fix mode with
  the person's answers in the prompt ends with `v_t*` clean, `model check` otherwise unchanged and the suite
  green, three runs.
- The kb clone, report mode: finds version/revision, journal/history and query-the-store r6; its cost.

## Not in these releases

- Seam translations between contexts' terms; stemming beyond a plural "s"; checking step text against
  definitions; generating model.lp from grammar.md (with the move to shopsystem-knowledge); wiring the
  consistency check into rounds; decisions as files in consuming repositories.
