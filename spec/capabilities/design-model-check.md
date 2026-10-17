---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/design-model-check
title: Design model check
narrator: a person or agent checking a repository against the design model
group: service
rests_on: [design-decision/plugin-adopts-the-design-model, design-decision/model-check-solves-with-clingo, design-decision/scenario-names-requirement-by-tag, design-decision/retired-ids-in-capability-frontmatter, design-decision/work-file-forms, design-decision/capability-ids-are-context-scoped]
formulated_as: features/design-model-check.feature
retired: []
---

# Design model check

## Purpose
`scripts/model` reads a bounded context's files — spec, feature files, decisions, work and records — as the
facts of `docs/design-model/grammar.md`, and reports what the grammar refuses. It also writes the generated
decisions index and traces a requirement to why it exists. It does not edit the spec, the work or the
records, and it checks one bounded context: product-level artifacts are read only where the files hold them.

## Behaviour
- [r1] **When** `model check` finds no violation, unresolved reference or file problem, it says so with the counts and exits 0.
- [r2] **When** `model check` finds violations, it prints each violated relation by its grammar.md name, with its rows, and exits 1.
- [r3] **If** a requirement bullet in a capability's Behaviour has no `[r<n>]`, `model check` reports it under v15a.
- [r4] **If** two requirements of one capability carry the same id, `model check` reports them under v15b.
- [r5] **If** a capability uses an id it lists as retired, `model check` reports it under v15c.
- [r6] **If** a capability-proposal changes a requirement no capability has, `model check` reports it under v15e.
- [r7] **If** a capability-proposal is `formulated` while a requirement it adds or changes has no scenario, and the capability is not guarantees, `model check` reports it under v15f.
- [r8] **If** a requirement of a capability that is not guarantees has no scenario naming it, `model check` reports it under v_s3.
- [r9] **If** a scenario names a requirement its capability does not have, or a capability rests on a decision that does not exist, `model check` reports the unresolved reference and exits 1.
- [r10] **If** a part has no `part_of`, or its `part_of` chain does not reach an initiative, `model check` reports it under v9a or v9c.
- [r11] **When** `model check` finds warnings, it prints each warning relation with its count and they alone do not change the exit status.
- [r12] **If** the clingo package is missing, `model check` says so with the command that installs it and exits 2.
- [r13] **When** `model facts` is run, it prints the facts read, one a line in clingo's syntax, using only the standard library.
- [r14] **When** `model decisions` is run, `spec/decisions.md` lists every decision under `decisions/` with its summary, status, what it supersedes and when to revisit it.
- [r15] **When** `model decisions --check` is run and `spec/decisions.md` is not what `model decisions` would write, it says so, exits 1 and writes nothing.
- [r16] **When** `model why <capability>#r<n>` is run, it prints the requirement, each capability-proposal that adds or changes it, the `part_of` chain to its initiative and the initiative's sources.
- [r17] **If** no capability-proposal adds or changes the requirement, `model why` says so and exits 1.
- [r18] **Where** a proposal's or work-item's list names `<capability>#r<a>-r<b>`, `model` reads it as every id from a to b.
- [r19] `model` reads, under `--root` (default the current directory), `spec/index.md`, `spec/capabilities/*.md`, every `*.feature` under `features/`, `decisions/*.md`, `work/<initiative>/*.md`, `records/observations.md` and any other Markdown under `records/` whose frontmatter has an `id`.
- [r20] A scenario names a requirement by a tag `@r<n>`, its own or its feature's, in the feature file its capability is `formulated_as`, or `features/<capability name>.feature` when it gives none.
- [r21] A reference written `<name>#r<n>` or `capability/<name>#r<n>` is read as a requirement of the capability `capability/<context path>/<name>` in the bounded context, the field fixing the kind where it is written `<name>`.
- [r22] **If** a list names a reference that is not `<capability>#r<n>` or `<capability>#behaviour/r<n>`, with the capability written `capability/<context path>/<name>`, `capability/<name>` or `<name>`, or a range `#r<a>-r<b>` with a greater than b, `model check` reports it as unresolved.
- [r23] **If** a capability-proposal adds or removes a requirement no capability has, `model check` reports it as unresolved, except that adding an id the capability lists as retired is reported under v15c. Removing an id the capability lists as retired is reported as unresolved like any other.
- [r24] **If** a `supersedes`, `source`, `part_of`, `argues`, `under`, `for`, `blocked_by` or `depends_on` names nothing in the repository, or names a node of the wrong kind (`supersedes` needs a design-decision, `under` and `depends_on` a capability, `for` and `blocked_by` a work-item), `model check` reports it as unresolved.
- [r25] **If** `spec/index.md` is missing or has no `id`, a capability's `id` is not `capability/<context path>/<file name>`, a capability has no `## Behaviour` section, or its `retired` lists an entry that is neither `r<n>` nor a number, `model check` reports a file problem naming the file.
- [r26] **If** a feature file is not the `formulated_as` of any capability, where a capability that gives none has `features/<its name>.feature`, or two of its scenarios share a title, `model check` reports a file problem naming the file. A scenario tagged `@holding` is not counted in the title check.
- [r27] **If** a work directory has no `initiative.md`, an initiative or part has no `id`, a part's kind is not a part kind, a status is missing or not in its kind's lifecycle, an initiative's priority is not a number or its date is not `YYYY-MM-DD`, `model check` reports a file problem naming the file; for a work directory with no `initiative.md` it names the directory, not the missing file.
- [r28] **If** a work-item accepts a requirement no scenario names yet, `model check` reports a file problem naming the work-item's file.
- [r29] **If** a decision has no `id`, a record with an `id` has a kind that is not a record kind, a frontmatter value is written as a folded or literal block, or one id names nodes of two kinds, `model check` reports a file problem.
- [r30] **If** `model check` finds a file problem, it prints each and exits 1.
- [r31] **When** `model check` ends without `--json`, it prints the counts of violations, warnings, unresolved references and file problems.
- [r32] **Where** `--limit <n>` is given, default 10, `model check` prints at most n rows of each violated relation and how many more there are.
- [r33] **Where** `--json` is given, `model check` prints the violations, warnings, unresolved references and file problems as one JSON object, with the same exit status.
- [r34] **If** an initiative that is not a capability-change has more than one part directly under it, `model check` reports it under v_k5, while a capability-change initiative may hold several capability-proposals.
- [r35] **If** a capability-proposal argues more than one capability, `model check` reports it under v_k6.
- [r36] A capability-proposal at `formulated` counts as closed when `model check` decides whether an initiative may be done.
- [r37] **When** `model decisions --check` finds `spec/decisions.md` is what `model decisions` would write, it says the file is current and exits 0.
- [r38] **When** `model decisions` is run, it prints the file it wrote, and a decision file with no `id` is left out of the index.
- [r39] **If** `model why` is given an argument that is not a requirement reference, it says why and exits 2.
- [r40] **If** no capability has the requirement `model why` names, it says so in place of the requirement's text and still lists the proposals that name it.
- [r41] **When** `model why` is run, it lists each capability-proposal that adds, changes or removes the requirement, in date order with its status and date. **If** no capability-proposal adds or changes it, including when every one that names it only removes it, `model why` exits 1; one proposal that adds or changes it is enough for exit 0.
- [r42] A reference written `capability/<context path>/<name>#behaviour/r<n>`, the requirement as a part in shopsystem-knowledge's IRI form, names the same requirement as `capability/<context path>/<name>#r<n>`.
- [r43] A node is written `<kind>/<context path>/<name>`, or in short `<kind>/<name>`, and a field that fixes the kind (`rests_on`, `supersedes`, `argues`, `under`, `depends_on`) and the capability part of a `#r<n>` reference may write the bare `<name>`; `part_of`, `for` and `blocked_by` need `<kind>/<name>`; the context path is `<owner>/<product>/<context name>` and the bounded context is `bounded-context/<context path>`.
- [r44] A scenario tagged `@holding` is not read as an acceptance-scenario, whatever `@r<n>` tag it carries.
- [r45] **Where** a repository has no `decisions/` directory, `model` reads each `## design-decision/<slug>` heading of `spec/decisions.md` as a design-decision, and the entry's text up to a blank line, a heading or a property line (`date:`, `revisit_when:`, `supersedes:` or `source:`) as its summary.
- [r46] **If** a node's `id` is not `<kind>/<context path>/<name>` with its own kind, or spec/index.md's `id` is not `bounded-context/<context path>`, `model check` reports a file problem naming the file.
- [r47] **If** a reference is written `<context name>/<name>`, `decision/<name>` or `obs/<name>`, `model check` reports it as unresolved.
- [r48] A glossary entry is a bullet of `spec/index.md`'s `## Glossary` written `- **<term>**: <one-sentence definition>. Not: <word>, <word>.`, the `Not:` part optional, and `model` reads it as a term of the bounded context, with the id `term/<context path>/<term>`, the term lowercased with spaces as hyphens.
- [r49] **If** a bullet in `spec/index.md`'s `## Glossary` is not of that form, `model check` reports a file problem naming the file.
- [r50] **When** `model facts` is run, it prints for each glossary entry a `node` fact of kind `term`, a `term_of` fact naming the bounded context, and an `avoid` fact for each word after its `Not:`.
- [r51] **When** `model facts` is run, it prints a `mentions` fact for each requirement and each scenario and each term or avoided word it holds, matching a whole word, whatever its case, with a plural "s" allowed, so that "restore" is no mention of "store".
- [r52] **If** a requirement or a scenario mentions a word that its context's glossary lists after `Not:`, `model check` reports it under v_t1, naming the requirement or scenario, the word and the term.
- [r53] **If** two glossary entries have one term, `model check` reports it under v_t2.
- [r54] **If** a word one term lists after `Not:` is another term of the context, or the term itself, `model check` reports it under v_t3.
- [r55] **If** `import clingo` fails, `model check` looks for an interpreter that has clingo in this order: `$SHOPSYSTEM_MODEL_PYTHON`, each `python3` on `PATH` outside the active virtualenv's `bin/`, `/usr/local/bin/python3`, `/usr/bin/python3`, and runs again under the first that has it.
- [r56] **When** `model check` has run again under another interpreter, it does so once, and a second failure to import clingo does not run it again.
- [r57] **If** no interpreter has clingo, `model check` exits 2 with its message naming each interpreter it tried.

## Implementation, may change
- `scripts/model.lp` is grammar.md v3 sections 1, 3 and 4 in clingo, with FIX notes where grammar.md does not
  compile as written; facts use grammar.md's relation names.
- Node ids: the bounded-context is spec/index.md's `id`; a requirement without an id is `<capability>#line<k>`;
  a scenario is `<feature path>:<title>`.
- The frontmatter reader is a YAML subset: scalars, `[a, b]` lists and `- x` block lists.

## Not yet
- Product-level artifacts (jobs, the context-map, seams, pins) read from a product repository — trigger: a second bounded context is checked together with this one.
- A work-queue view (ready items, claims) — trigger: initiative i5 is approved.
