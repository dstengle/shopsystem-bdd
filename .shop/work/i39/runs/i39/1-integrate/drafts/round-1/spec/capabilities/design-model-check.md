## Behaviour

### `model check`
- [r1] **When** `model check` finds no violation, unresolved reference or file problem, `model check` shall say so and exit successfully.
- [r2] **If** `model check` finds a violation, an unresolved reference or a file problem, then `model check` shall print each, a violated relation by its grammar.md code and plain label with its rows, and exit with an error.
- [r11] **When** `model check` finds warnings, `model check` shall print each warning relation with its plain label and its count, with no effect on whether it exits successfully.
- [r111] **While** the bounded context has no job, `model check` shall print no `w_unserved_cap` warning.
- [r120] **When** `model check` reads a request whose `part_of` names a job-thread kept in another repository, `model check` shall print no `v17` for the request.
- [r121] **When** `model check` reads a request raised for a request of another context, `model check` shall print neither `v17` nor `v18` for the request.
- [r33] **Where** `--json` is given, `model check` shall print its violations, warnings, unresolved references and file problems as one JSON object, each code mapped to its plain label, exiting as it would without `--json`.
- [r36] **When** `model check` decides whether an initiative may be `done`, `model check` shall count a `formulated` capability-proposal, and any `withdrawn` part, as closed.
- [r55] **If** `import clingo` fails, then `model check` shall try again, once, under the first interpreter that has clingo of `$SHOPSYSTEM_MODEL_PYTHON`, each `python3` on `PATH` outside the active virtualenv's `bin/`, `/usr/local/bin/python3` and `/usr/bin/python3`, in that order.
- [r12] **If** no interpreter has clingo, then `model check` shall exit with an error, naming each interpreter it tried and the command that installs clingo.

**If** `model check` finds a case of a row below, then `model check` shall print it under the row's code; a file
problem names the file.

| id | code | what is printed |
|---|---|---|
| [r3] | v15a | a requirement bullet in a capability's Behaviour has no `[r<n>]` |
| [r4] | v15b | two requirements of one capability have the same id |
| [r5] | v15c | a capability uses an id it lists as retired, or a capability-proposal that is not `merged`, `formulated` or `withdrawn` adds one |
| [r6] | v15e | a `drafted` or `approved` capability-proposal changes a requirement no capability has |
| [r7] | v15f | a `formulated` capability-proposal adds or changes a requirement with no scenario, of a capability that is not guarantees |
| [r8] | v_s3 | a requirement of a capability that is not guarantees has no scenario naming it |
| [r107] | v_s2 | a scenario not tagged `@deprecated` has more than one `@r<n>` tag, its own and its feature's together |
| [r10] | v9a, v9c | a part has no `part_of` (v9a), or its `part_of` chain reaches no initiative (v9c) |
| [r34] | v_k5 | an initiative that is not a capability-change has more than one part directly under it (a capability-change may have several capability-proposals) |
| [r35] | v_k6 | a capability-proposal argues more than one capability |
| [r59] | v_d2 | an initiative is `abandoned` while a part of it, at any depth, is neither closed nor `withdrawn` |
| [r113] | v16a | an initiative dated after 2026-10-23 fulfils no request |
| [r114] | v_d1 | an initiative is `done` while a request kept in this context, whose asker is this context and whose `part_of` or `source` names the initiative, is not `delivered` |
| [r119] | v_d3 | a request is `delivered` while the initiative that fulfils it is not `done` |
| [r115] | v17 | a request neither is part of a job-thread nor cites an origin |
| [r116] | v3 | a `delivered` request's resolution names a requirement the spec does not have |
| [r117] | v18 | an id in this context's files has another context's path on a kind kept in `.shop/work/`, judged from the id alone |
| [r52] | v_t1 | a requirement or a scenario mentions a word its context's glossary lists after `Not:`, named with the word and the term |
| [r53] | v_t2 | two glossary entries have one term |
| [r54] | v_t3 | a word one term lists after `Not:` is another term of the context, or the term itself |
| [r103] | v_e1 | a Behaviour line is in none of EARS's patterns, combines their clauses in an order other than Where, While, then When or If, or has an If clause with no then |
| [r104] | v_e2 | a Behaviour line has more than one "shall" or more than one sentence |
| [r106] | v_w4 | a work-item that is not `withdrawn` has no `accepts` and no `check` |
| [r110] | file problem | a work-item's file name is not `w<n>.md`, or two work-items have one id |
| [r112] | file problem | a request is not of the form `work request` writes (capability/requests) |
| [r118] | file problem | an initiative's kind is `job` or `job-path` |
| [r9] | unresolved | a scenario names a requirement its capability does not have, or a capability rests on a decision that does not exist |
| [r22] | unresolved | a list names a reference that is not `<capability>#r<n>` (`#behaviour/r<n>` included), with the capability written `capability/<context path>/<name>`, `capability/<name>` or `<name>`, or a range `#r<a>-r<b>` with a greater than b |
| [r23] | unresolved | a capability-proposal adds or removes an id its capability neither has nor lists as retired, or removes a retired id while not `merged`, `formulated` or `withdrawn`; a proposal that is may name a retired id in `adds`, `changes` or `removes`, one it removes read as that requirement |
| [r24] | unresolved | a `supersedes`, `source`, `part_of`, `argues`, `under`, `for`, `blocked_by`, `depends_on`, `fixes` or `findings` names nothing in the repository, a node of the wrong kind (`supersedes` needs a design-decision, `under` and `depends_on` a capability, `for`, `blocked_by` and `fixes` a work-item, `findings` a review-finding); or any reference is written `<context name>/<name>`, `decision/<name>` or `obs/<name>` |
| [r66] | unresolved | a capability-proposal's `adds`, `changes` or `removes` names `term/<term>` the glossary does not have, except one a `merged` or `formulated` proposal removes |
| [r25] | file problem | `spec/index.md` is missing or has no `id`; a capability's `id` is not `capability/<context path>/<file name>`, it has no `## Behaviour` section, its `retired` lists an entry that is neither `r<n>` nor a number, or its frontmatter has `formulated_as` |
| [r46] | file problem | a node's `id` is not `<kind>/<context path>/<name>` with its own kind, or `spec/index.md`'s is not `bounded-context/<context path>` |
| [r26] | file problem | a feature file is not `features/<name>.feature` for a capability `<name>`, two of its scenarios not tagged `@deprecated` share a title, or a scenario is tagged `@holding` |
| [r27] | file problem | a work directory has no `initiative.md` (the directory named, not the file), an initiative or part has no `id`, a part's kind is not a part kind, a status is missing or not in its kind's lifecycle, an initiative's priority is not a number or its date not `YYYY-MM-DD`, or a work-item that is not `withdrawn` accepts a requirement of a capability that is not guarantees and no scenario names it yet, other than a retired id the work-item accepts while `green` |
| [r29] | file problem | a decision has no `id` or no `## Decision` section, a record with an `id` has a kind that is not a record kind, a frontmatter value is written as a folded or literal block, or one id names nodes of two kinds |
| [r49] | file problem | a bullet in `spec/index.md`'s `## Glossary` is not of the form r48 gives |
| [r61] | file problem | the repository has `spec/decisions.md`, or a `decisions/`, `work/` or `records/` directory at its root, each named with `scripts/migrate` |

### Reading
- [r19] `model` shall read, under `--root` (default the current directory), only `spec/index.md`, `spec/capabilities/*.md`, every `*.feature` under `features/`, every `spec/decisions/*.md` but `index.md` and `README.md`, `.shop/work/<initiative>/*.md`, `.shop/work/requests/*.md`, `.shop/records/observations.md` and any other Markdown under `.shop/records/` whose frontmatter has an `id`.
- [r20] `model` shall read the `@r<n>` tag of a scenario not tagged `@deprecated` in `features/<capability name>.feature`, its own or its feature's, as the one requirement of that capability the scenario names.
- [r21] `model` shall read a reference written `<name>#r<n>` or `capability/<name>#r<n>` as a requirement of the capability `capability/<context path>/<name>` in the bounded context, the field fixing the kind where it is written `<name>`.
- [r18] `model` shall read `<capability>#r<a>-r<b>` in a proposal's or work-item's list as every id from a to b.
- [r43] `model` shall read a node written `<kind>/<context path>/<name>`, or `<kind>/<name>`, as that node, and a bare `<name>` as one only in a field that fixes the kind (`rests_on`, `supersedes`, `argues`, `under`, `depends_on`) or the capability part of a `#r<n>` reference, the context path being `<owner>/<product>/<context name>` and the bounded context `bounded-context/<context path>`.
- [r64] `model` shall read a decision's `source`, and not its `by`, as a list of ids, each resolved as r24 says for `source` and naming a node of any kind.
- [r48] `model` shall read each bullet of `spec/index.md`'s `## Glossary` written `- **<term>**: <one-sentence definition>. Not: <word>, <word>.`, the `Not:` part optional, as a term of the bounded context with the id `term/<context path>/<term>`, the term lowercased with spaces as hyphens, and each word after `Not:` as a word the term avoids.
- [r51] `model` shall read a requirement or a scenario as mentioning a term or avoided word when it contains it as a whole word, whatever its case, with a plural "s" allowed, outside code spans, double-quoted strings and `@` tags, so that "restore" is no mention of "store" and a line naming the tag `@holding` is no mention of "holding".

### Other commands
- [r13] **When** `model facts` is run, `model facts` shall print the facts read, one a line in clingo's syntax, using only the standard library.
- [r14] **When** `model decisions` is run, `model decisions` shall write `spec/decisions/index.md` listing every decision in `spec/decisions/` that has an `id`, with its summary, status, what it supersedes and when to revisit it, each linked to its file.
- [r15] **If** `model decisions --check` finds `spec/decisions/index.md` is not what `model decisions` would write, then `model decisions` shall say so and exit with an error, writing nothing.
- [r37] **When** `model decisions --check` finds `spec/decisions/index.md` is what `model decisions` would write, `model decisions` shall say the file is current and exit successfully.
- [r16] **When** `model why <capability>#r<n>` is run, `model why` shall print the requirement's text (or that no capability has it), each capability-proposal that adds, changes or removes it in date order with its status and date, the `part_of` chain to its initiative and the initiative's sources.
- [r17] **When** no capability-proposal adds or changes the requirement given to `model why`, `model why` shall say so and exit successfully.
- [r108] **Where** `--json` is given, `model why` shall print its result, the requirement's text and the capability-proposals that trace it, as one JSON object.
- [r65] **When** `model rules` is run, `model rules` shall print each rule's code and plain label, one a line, the violations first and then the warnings, and exit successfully.
- [r109] **Where** `--json` is given, `model rules` shall print its result, each rule's code, plain label and kind, as one JSON object.
- [r105] **If** `model` cannot do what it was asked, then `model` shall exit with an error, say why, and change nothing.
