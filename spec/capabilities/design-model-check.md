---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/design-model-check
title: Design model check
narrator: a person or agent checking a repository against the design model
group: service
rests_on: [design-decision/final-layout, design-decision/references-are-ids, design-decision/light-decisions, design-decision/model-check-solves-with-clingo, design-decision/a-scenario-may-name-several-requirements, design-decision/retired-ids-in-capability-frontmatter, design-decision/work-file-forms, design-decision/capability-ids-are-context-scoped, design-decision/one-requirement-form, design-decision/review-of-work-items]
retired: [r28, r30, r31, r32, r38, r39, r40, r41, r42, r44, r45, r47, r50, r56, r57, r58, r60, r62, r63, r67]
---

# Design model check

## Purpose
`scripts/model` reads a bounded context's files — spec, feature files, decisions, work and records, in the
final layout and no other — as the facts of `docs/design-model/grammar.md`, and reports what the grammar
refuses, each rule by its code and its plain label. It also writes the generated decisions index, lists the
rules, and traces a requirement to why it exists. It does not edit the spec, the work or the records, and it
checks one bounded context: product-level artifacts are read only where the files contain them.

## Behaviour

### Checking
- [r1] **When** `model check` finds no violation, unresolved reference or file problem, `model check` shall say so and exit 0.
- [r2] **If** `model check` finds a violation, an unresolved reference or a file problem, then `model check` shall print each, a violated relation by its grammar.md code and plain label with its rows, and exit 1.
- [r11] **When** `model check` finds warnings, `model check` shall print each warning relation with its plain label and its count, leaving the exit status as the other findings set it.
- [r33] **Where** `--json` is given, `model check` shall print its violations, warnings, unresolved references and file problems as one JSON object, each code mapped to its plain label, with the same exit status.
- [r36] **When** `model check` decides whether an initiative may be done, `model check` shall count a `formulated` capability-proposal, and any `withdrawn` part, as closed.
- [r55] **If** `import clingo` fails, then `model check` shall run again, once, under the first interpreter that has clingo of `$SHOPSYSTEM_MODEL_PYTHON`, each `python3` on `PATH` outside the active virtualenv's `bin/`, `/usr/local/bin/python3` and `/usr/bin/python3`, in that order.
- [r12] **If** no interpreter has clingo, then `model check` shall exit 2, naming each interpreter it tried and the command that installs clingo.

**If** `model check` finds a case of a row below, then `model check` shall report it under the row's code; a file
problem names the file.

| id | code | what is reported |
|---|---|---|
| [r3] | v15a | a requirement bullet in a capability's Behaviour has no `[r<n>]` |
| [r4] | v15b | two requirements of one capability have the same id |
| [r5] | v15c | a capability uses an id it lists as retired, or a capability-proposal that is not `merged`, `formulated` or `withdrawn` adds one |
| [r6] | v15e | a `drafted` or `approved` capability-proposal changes a requirement no capability has |
| [r7] | v15f | a `formulated` capability-proposal adds or changes a requirement with no scenario, of a capability that is not guarantees |
| [r8] | v_s3 | a requirement of a capability that is not guarantees has no scenario naming it |
| [r10] | v9a, v9c | a part has no `part_of` (v9a), or its `part_of` chain reaches no initiative (v9c) |
| [r34] | v_k5 | an initiative that is not a capability-change has more than one part directly under it (a capability-change may have several capability-proposals) |
| [r35] | v_k6 | a capability-proposal argues more than one capability |
| [r59] | v_d2 | an initiative is `abandoned` while a part of it, at any depth, is neither closed nor `withdrawn` |
| [r52] | v_t1 | a requirement or a scenario mentions a word its context's glossary lists after `Not:`, named with the word and the term |
| [r53] | v_t2 | two glossary entries have one term |
| [r54] | v_t3 | a word one term lists after `Not:` is another term of the context, or the term itself |
| [r103] | v_e1 | a Behaviour line is in none of EARS's patterns, combines their clauses in an order other than Where, While, then When or If, or has an If clause with no then |
| [r104] | v_e2 | a Behaviour line has more than one "shall" or more than one sentence |
| [r106] | v_w4 | a work-item that is not `withdrawn` has no `accepts` and no `check` |
| [r9] | unresolved | a scenario names a requirement its capability does not have, or a capability rests on a decision that does not exist |
| [r22] | unresolved | a list names a reference that is not `<capability>#r<n>` (`#behaviour/r<n>` included), with the capability written `capability/<context path>/<name>`, `capability/<name>` or `<name>`, or a range `#r<a>-r<b>` with a greater than b |
| [r23] | unresolved | a capability-proposal adds or removes an id its capability neither has nor lists as retired, or removes a retired id while not `merged`, `formulated` or `withdrawn`; a proposal that is may name a retired id in `adds`, `changes` or `removes`, one it removes read as that requirement |
| [r24] | unresolved | a `supersedes`, `source`, `part_of`, `argues`, `under`, `for`, `blocked_by`, `depends_on`, `fixes` or `findings` names nothing in the repository, a node of the wrong kind (`supersedes` needs a design-decision, `under` and `depends_on` a capability, `for`, `blocked_by` and `fixes` a work-item, `findings` a review-finding); or any reference is written `<context name>/<name>`, `decision/<name>` or `obs/<name>` |
| [r66] | unresolved | a capability-proposal's `adds`, `changes` or `removes` names `term/<term>` the glossary does not have, except one a `merged` or `formulated` proposal removes |
| [r25] | file problem | `spec/index.md` is missing or has no `id`; a capability's `id` is not `capability/<context path>/<file name>`, it has no `## Behaviour` section, its `retired` lists an entry that is neither `r<n>` nor a number, or its frontmatter has `formulated_as` |
| [r46] | file problem | a node's `id` is not `<kind>/<context path>/<name>` with its own kind, or `spec/index.md`'s is not `bounded-context/<context path>` |
| [r26] | file problem | a feature file is not `features/<name>.feature` for a capability `<name>`, two of its scenarios not tagged `@deprecated` share a title, or a scenario is tagged `@holding` |
| [r27] | file problem | a work directory has no `initiative.md` (the directory named, not the file), an initiative or part has no `id`, a part's kind is not a part kind, a status is missing or not in its kind's lifecycle, an initiative's priority is not a number or its date not `YYYY-MM-DD`, or a work-item that is not `withdrawn` accepts a requirement no scenario names yet |
| [r29] | file problem | a decision has no `id` or no `## Decision` section, a record with an `id` has a kind that is not a record kind, a frontmatter value is written as a folded or literal block, or one id names nodes of two kinds |
| [r49] | file problem | a bullet in `spec/index.md`'s `## Glossary` is not of the form r48 gives |
| [r61] | file problem | the repository has `spec/decisions.md`, or a `decisions/`, `work/` or `records/` directory at its root, each named with `scripts/migrate` |

### Reading
- [r19] `model` shall read, under `--root` (default the current directory), only `spec/index.md`, `spec/capabilities/*.md`, every `*.feature` under `features/`, every `spec/decisions/*.md` but `index.md` and `README.md`, `.shop/work/<initiative>/*.md`, `.shop/records/observations.md` and any other Markdown under `.shop/records/` whose frontmatter has an `id`.
- [r20] `model` shall read each `@r<n>` tag of a scenario not tagged `@deprecated` in `features/<capability name>.feature`, its own or its feature's, as a requirement of that capability the scenario names.
- [r21] `model` shall read a reference written `<name>#r<n>` or `capability/<name>#r<n>` as a requirement of the capability `capability/<context path>/<name>` in the bounded context, the field fixing the kind where it is written `<name>`.
- [r18] `model` shall read `<capability>#r<a>-r<b>` in a proposal's or work-item's list as every id from a to b.
- [r43] `model` shall read a node written `<kind>/<context path>/<name>`, or `<kind>/<name>`, as that node, and a bare `<name>` as one only in a field that fixes the kind (`rests_on`, `supersedes`, `argues`, `under`, `depends_on`) or the capability part of a `#r<n>` reference, the context path being `<owner>/<product>/<context name>` and the bounded context `bounded-context/<context path>`.
- [r64] `model` shall read a decision's `source`, and not its `by`, as a list of ids, each resolved as r24 says for `source` and naming a node of any kind.
- [r48] `model` shall read each bullet of `spec/index.md`'s `## Glossary` written `- **<term>**: <one-sentence definition>. Not: <word>, <word>.`, the `Not:` part optional, as a term of the bounded context with the id `term/<context path>/<term>`, the term lowercased with spaces as hyphens, and each word after `Not:` as a word the term avoids.
- [r51] `model` shall read a requirement or a scenario as mentioning a term or avoided word when it contains it as a whole word, whatever its case, with a plural "s" allowed, outside code spans, double-quoted strings and `@` tags, so that "restore" is no mention of "store" and a line naming the tag `@holding` is no mention of "holding".

### Other commands
- [r13] **When** `model facts` is run, `model facts` shall print the facts read, one a line in clingo's syntax, using only the standard library.
- [r14] **When** `model decisions` is run, `model decisions` shall write `spec/decisions/index.md` listing every decision in `spec/decisions/` that has an `id`, with its summary, status, what it supersedes and when to revisit it, each linked to its file.
- [r15] **If** `model decisions --check` finds `spec/decisions/index.md` is not what `model decisions` would write, then `model decisions` shall say so and exit 1, writing nothing.
- [r37] **When** `model decisions --check` finds `spec/decisions/index.md` is what `model decisions` would write, `model decisions` shall say the file is current and exit 0.
- [r16] **When** `model why <capability>#r<n>` is run, `model why` shall print the requirement's text (or that no capability has it), each capability-proposal that adds, changes or removes it in date order with its status and date, the `part_of` chain to its initiative and the initiative's sources.
- [r17] **If** no capability-proposal adds or changes the requirement, then `model why` shall say so and exit 1.
- [r65] **When** `model rules` is run, `model rules` shall print each rule's code and plain label, one a line, the violations first and then the warnings, and exit 0.
- [r105] **If** `model` cannot do what it was asked, then `model` shall exit non-zero, say why, and change nothing.

## Implementation, may change
- `scripts/model.lp` is grammar.md v3 sections 1, 3 and 4 in clingo, with FIX notes where grammar.md does not
  compile as written; facts use grammar.md's relation names.
- Each rule's plain label is a fact `label("<code>", "<label>")` beside the rule in `model.lp`, the one place it
  is written; `check` and `rules` read the labels from the solve. A unit test fails when a relation `model.lp`
  shows has no label or two.
- Output: `<code>  <label>  (<count>)` above a violated relation's rows; `warning <code>  <label>  (<count>)`;
  `rules` prints `<code>  <label>`. `--json` adds `"labels": {code: label}` for the codes it prints.
- Without `--json`, `model check` ends with the counts of violations, warnings, unresolved references and file
  problems. `--limit <n>` (default 10) prints at most n rows of each violated relation and how many more there are.
- A file problem for `@holding` names the scenario's title too. `model decisions` prints the file it wrote.
  `model why` given an argument that is not a requirement reference exits 2.
- `model facts` prints, for each glossary entry, a `node` fact of kind `term`, a `term_of` fact naming the
  bounded context and an `avoid` fact for each word after its `Not:`, and a `mentions` fact for each mention r51
  reads.
- `withdrawn` is in the lifecycle of a capability-proposal and of a work-item.
- Node ids: the bounded-context is spec/index.md's `id`; a requirement without an id is `<capability>#line<k>`;
  a scenario is `<feature path>:<title>`.
- The frontmatter reader is a YAML subset: scalars, `[a, b]` lists and `- x` block lists.
- A decision's `source` gives no `source` fact (grammar.md's `source` is an initiative's); its ids are only
  resolved.
- `model decisions` links each row to `<file name>`, relative to `spec/decisions/index.md`.

## Not yet
- Product-level artifacts (jobs, the context-map, seams, pins) read from a product repository — trigger: a second bounded context is checked together with this one.
