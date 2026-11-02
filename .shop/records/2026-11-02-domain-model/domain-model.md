---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-02-domain-model
kind: design
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-02
status: draft
---

# The domain model, as a typed glossary (draft)

The person, 2026-11-02: "Design the domain model first, as part of the glossary." It is the lexicon of the codified
requirement language (GF grammar, telingo logic, generated Gherkin) of the next major version. Every term has a
**category**, which is the grammar slot it fills; a word in the wrong slot does not parse.

Sources: the four extractions in this directory (`extract-*.md`, from all 19 capabilities, the glossary and
`docs/design-model/`), the spike in `.shop/scratch/spike-cnl/` (`resources.lp`), and the 2026-11-02 conversation.
Cites are `<capability>#r<n>` of today's spec, or `ex-<file>` for an extraction.

## 0. Categories

| category | what it is | in the grammar | in the logic | in Gherkin |
|---|---|---|---|---|
| **actor** | what a requirement's "shall" is about | subject of `shall` | the agent of an event | the subject of When and Then |
| **kind** | a sort of thing with an identity | a noun; quantified ("every initiative", "an initiative") | a unary predicate `initiative(I)` | an instance named in a Given (`i1`) |
| **attribute** | a property of a kind with a closed value set | "whose status is …" | `status(I,S)` | "that is `started`" |
| **value** | one member of an attribute's closed set | only in its own attribute's slot | a constant | a quoted value |
| **relation** | a typed link between two kinds, with a cardinality | a verb or preposition frame ("a work-item of a capability-proposal") | a binary predicate `part_of(W,P)` | a Given linking two instances |
| **event** | something that happens at one step | the trigger of When; the response of shall | an atom true at one step | When (trigger) and Then (response) |
| **resource** | what a session holds while it runs | "holds" | `holds(S,R)`, `exclusive(R)` | not written; checked on the trace |
| **condition** | a named derived predicate | one word for a long clause | a rule | expanded into Givens |
| **universal condition** | a statement true in every state of every trace | a ubiquitous statement (no trigger) | an `always` constraint | checked after every scenario, never restated |

A term entry is written: `- **term** (category): one sentence. Values: … . Not: … .`

## 1. Actors

- **the person** (actor): the human who asks, answers and approves. Not: user, human.
- **`work run`** (actor): the supervisor that takes nodes through transitions by starting sessions.
- **`work`** (actor): the command that writes statuses, transitions and requests; the only writer of a status (ex-queue-build §4).
- **a tool** (actor): one of `features`, `tools`, `measure`, `migrate`, `model`, each with its subcommands (ex-tools §3).
- **a session** (actor): one Claude Code conversation (§2.4), acting within what it holds.

## 2. Kinds

### 2.1 The spec (standing)

- **bounded context** (kind): one repository's spec, with its index, capabilities, decisions and glossary. Identity: `bounded-context/<path>`.
- **capability** (kind): one file under `spec/capabilities/`. Attributes: group (`service`, `guarantees`, `model`, `operations`), narrator (a role).
- **requirement** (kind): one codified statement of a capability, named `<capability>#r<n>`. *New:* one statement, one `shall`, parsed to one tree. Not: capability requirement, behaviour line.
- **requirement group** (kind, *new*): the requirements that together make one scenario, with a title; its statements share a pre-state and a trigger. Identity: `<capability>#g<n>`. Not: compound requirement.
- **term** (kind): one entry of this glossary. Attributes: category. Relations: avoids words.
- **design-decision** (kind): one file under `spec/decisions/`. Attributes: status (§3).
- **feature** (kind): the generated `features/<capability>.feature`; one scenario for each requirement group. *Changed:* generated, not formulated.
- **scenario** (kind): one Gherkin scenario, generated from one requirement group. Not: test case.
- **step** (kind, *new*): one Given, When or Then line, the linearisation of one step function; bound to exactly one step definition.

### 2.2 Work (`.shop/work/`)

- **request** (kind): what brings work into a bounded context: lines its asker proposes to its upstream. Identity: `q<n>`.
- **request line** (kind): one proposed statement of a request, with its line outcome. Not: line (alone).
- **initiative** (kind): the delivery of one request's accepted lines. Identity: `i<n>`. Attributes: status.
- **proposal** (kind, *new supertype*): a part of an initiative proposing changes to the spec, in `adds`, `changes` and `removes`. Sorts: **capability-proposal** (requirements of one capability), **glossary-proposal** (terms). About ten pairs of today's lines differ only in which sort they name (supervision r68/r164, r69/r169, r70/r165, r144/r166, r150/r221, …; ex-supervision §5); each pair becomes one statement about a proposal.
- **work-item** (kind): the unit of delivery under a capability-proposal, accepting requirements or naming a check. Identity: `w<n>`.
- **question** (kind): an open point on a node, with readings and a recommended reading.
- **answer** (kind): the answer to one question, in its answerer's words. Attribute: answerer (`the person`, a delegation).
- **delegation** (kind): the person's words, given with a request, naming the questions a session may answer.
- **node** (kind, *defined now*): anything with a status that `work run` takes through transitions: an initiative, a proposal, a work-item. A request is not a node: it has a status but moves by its sides' turns (ex-supervision §1 asked).

### 2.3 Execution

- **delivery** (kind): one invocation of `work run`, from start to exit. Attribute: scope (one initiative, every open initiative).
- **stage** (kind): one session `work run` starts for one node. *Changed:* one name for each stage, used everywhere; the role, agent and starting status are attributes, not other names (ex-supervision §6 found four names for each).

  | stage kind | node | starts from status | role | agent |
  |---|---|---|---|---|
  | research | work-item | `drafted` | researcher | code-scout |
  | plan | work-item | `researched` | planner | bdd-planner |
  | implement | work-item | `ready` (claimed) | implementer | bdd-implementer |
  | review | work-item | `done` | reviewer | bdd-task-reviewer |
  | integrate, gate, apply, formulate | proposal | (§3) | — | initiative-round |
  | intake | request | in this context's turn | — | initiative-round |
  | answer | a question | unanswered, under a delegation | — | delegation-answerer |
  | branch review | initiative | its work-items green or withdrawn | branch reviewer | bdd-branch-reviewer |
  | analysis | initiative | measured | analyst | batch-analyst |

- **round** (kind): a stage of the kinds integrate, gate, apply, formulate or intake. Not: iteration.
- **worker** (kind): a stage of the kinds research, plan, implement or review (the four that hold a worker slot, §6).
- **session** (kind): one Claude Code conversation with an id and a transcript; every stage is one.
- **result** (kind): the `result.json` a stage writes. Attribute: outcome (§3).
- **brief** (kind): the input data of one stage.
- **fault** (kind): a failure outside a session's work that stops it (§7, U6).

### 2.4 Files and git

- **checkout** (kind): the repository's main working tree.
- **worktree** (kind): a working tree `work run` makes for one stage.
- **initiative branch**, **work-item branch** (kinds): as today.
- **commit** (kind). **remote** (kind).
- **file set** (kind): the paths a work-item says its work changes.
- **claim** (kind): the files a claimed work-item holds; a resource (§6).
- **stage directory** (kind): `runs/<node>/<k>-<stage>/`.

### 2.5 Records

- **record** (kind), with the sorts **measurement**, **observation**, **analysis**, **design**, **review finding**.

## 3. Values and lifecycles

Each attribute's values are a closed set. A value is accepted only in its own attribute's slot: "an initiative that
is `drafted`" does not parse. Transitions are the only events that change a status; each is one row, and a
requirement names the row rather than restating it.

| kind | status values | transitions (from → to: event) |
|---|---|---|
| initiative | `proposed`, `started`, `done`, `abandoned` | proposed → started: `work start`; started → done: the initiative is complete (§8); started → abandoned: `work abandon` |
| capability-proposal | `drafted`, `awaiting-answer`, `approved`, `formulated`, `withdrawn` | drafted → awaiting-answer: gate with questions; awaiting-answer → drafted: answers change lines; → approved: the person approves; approved → formulated: formulate round; any open → withdrawn |
| glossary-proposal | `drafted`, `awaiting-answer`, `approved`, `withdrawn` | as capability-proposal, with no formulated |
| work-item | `drafted`, `researched`, `planned`, `ready`, `claimed`, `done`, `green`, `awaiting-answer`, `failed`, `withdrawn` | drafted → researched → planned → ready → claimed → done → green: each stage's result; any stage → awaiting-answer: a question; awaiting-answer → the stage's starting status: `work answer`; any → failed: a fault; failed → its status before: `work retry`; any open → withdrawn |
| request | `open`, `awaiting-asker`, `awaiting-upstream`, `accepted`, `delivered`, `refused`, `withdrawn` | (requests capability; the turn is §6) |
| design-decision | `proposed`, `accepted`, `rejected`, `superseded` | |

Other closed sets:

| attribute | values |
|---|---|
| outcome (of a result) | `DONE`, `DONE_WITH_CONCERNS`, `PARTIAL`, `BLOCKED`, `HAND-BACK`, `QUESTION`, `NEEDS_CONTEXT`; each role allows a subset (ex-queue-build §8: researcher {DONE, NEEDS_CONTEXT}, …) |
| line outcome (of a request line) | `accepted`, `rewritten`, `refused`, `question`, `withdrawn` |
| side (of a request) | asker, upstream |
| stage kind | research, plan, implement, review, integrate, gate, apply, formulate, intake, answer, branch review, analysis |
| grade (of a finding) | Critical, Important, Minor |
| capability group | service, guarantees, model, operations |
| scope (of a delivery) | one initiative, every open initiative |

`merged` (capability-proposal) is not used by any line; this draft drops it (ex-supervision §10, ex-spec-side §4).

## 4. Relations

| relation | from → to | cardinality |
|---|---|---|
| fulfils | initiative → request | exactly 1 / 0..1 |
| part of | proposal → initiative | n..1 |
| argues | capability-proposal → capability | n..1 (one capability) |
| adds, changes, removes | capability-proposal → requirement; glossary-proposal → term | 0..n |
| under | work-item → capability-proposal | n..1 |
| accepts | work-item → requirement | 0..n (at least one, or a check) |
| blocked by | work-item → work-item | 0..n, acyclic |
| retires | work-item → deprecated scenario | 0..n |
| generates | requirement group → scenario | 1..1 (*new*) |
| member of | requirement → requirement group | n..1 (*new*) |
| restates | requirement → today's requirement | 0..n (*new*, the migration's trace; a source only) |
| in | requirement group → capability; capability → bounded context | n..1 |
| rests on | capability → design-decision | 0..n |
| supersedes | design-decision → design-decision | 0..1 |
| asker, upstream | request → bounded context | 1 each |
| raised for | request → request | 0..1 |
| has delegation | request → delegation | 0..1 |
| on | question → node or request line | n..1 |
| answers | answer → question | 1..1 |
| for | stage → node | n..1 |
| in | stage → worktree | 0..1 (a worker: 1) |
| writes | stage → result | 0..1 |
| belongs to | commit → work-item | 0..1 |
| merges into | work-item branch → initiative branch | 1 |
| holds | session → resource | 0..n (§6) |

## 5. Events

| event | actor | object | before | after |
|---|---|---|---|---|
| transition | `work` | node | the from status (§3) | the to status, committed (U4) |
| start | `work run` | stage | every resource it holds is free (U2) | the stage runs; it holds its resources |
| end | a session | stage | it runs | it writes a result, or a fault (U6) |
| commit | `work`, `work run`, a worker | change | — | a commit on its branch; pushed (U4) |
| merge | `work run` | work-item branch | the suite passes on it (§8 green check) | it is in the initiative branch |
| rerun | `work run` | failing scenario | it failed in the suite | it is run once more, alone (supervision r219, r222) |
| refuse | an actor | a command | the command cannot be done | nothing changed; the reason named (U3) |
| exit | `work run`, a tool | delivery, command | — | an exit code and what it prints |
| ask | a stage | question | — | the node is `awaiting-answer` |
| answer | the person, a delegation | question | it is open | the node returns (§3) |
| raise | an initiative | request | — | a request into an upstream |
| pass the turn | a side | request | it is that side's turn | the other side's turn |

## 6. Resources

A session holds resources while it runs; a resource that is **exclusive** is held by one session at a time, and a
**counted** resource by at most its number. Exclusivity is never stated as "one at a time, except …": it follows from
what each session holds (the spike's `resources.lp` checks supervision r20, r59, r66 and r95 this way, with no
exception left).

| resource | kind | held by | replaces today's |
|---|---|---|---|
| **spec lock** | exclusive, one per bounded context | every integrate, apply and formulate round | r95, r66 ("the rounds r95 names") |
| **initiative lock** | exclusive, one per initiative | every stage of an initiative that is not a worker: rounds, answers, branch review, analysis | r66 ("one session of an initiative at a time") |
| **node** | exclusive, one per node | every stage for that node | (implicit) |
| **claim** | exclusive per file | an implement stage, for its work-item's file set | r20, glossary claim |
| **worker slot** | counted, `workers` in `.shop/delivery.toml` (default 4) | every worker | r60, r59, r20 ("within the number of workers r60 gives") |
| **merge lock** | exclusive, one per initiative branch | a merge | r61 |
| **initiative directory** | exclusive, `.shop/work/<initiative>/` | the delivery running that initiative | r214–r218 |
| **turn** | exclusive, one per request | the side whose turn it is | requests turn, r67, r101 |
| **checkout** | exclusive, one per repository | one delivery of `work run` | r21 (no nested `work run`) |

## 7. Universal conditions

True in every state of every trace. Written once, never restated in a requirement, and checked on the trace of every
scenario rather than by a scenario of their own (with one scenario each to show a boundary, where one is useful).

| id | statement | today restated in |
|---|---|---|
| U1 | `work run` shall hold at most `workers` worker slots at a time. | r59, r20 (and implied by r60) |
| U2 | `work run` shall start a stage only when every exclusive resource it holds is free and its counted resources are not exhausted. | r20, r59, r61, r66, r95, r21 |
| U3 | Where an actor refuses a command, it shall exit with an error naming the reason and change nothing. | ~20 queue lines, ~16 tool lines, 12 supervision lines (seven wordings of "change nothing", four of the reason; ex-queue-build §5, ex-tools §2–3) |
| U4 | Every transition shall be committed; every commit on the initiative branch shall be pushed to its remote. | ~14 queue lines, ~20 supervision lines, r38, r54 |
| U5 | Only `work` shall write a status. | work-queue, role-boundaries |
| U6 | When a stage ends in an error, at its turn limit or without a result `work run` can read, `work run` shall take it as a fault: a round's node keeps its status, a work-item becomes `failed`. | r128, r86–r90, r115, r42, r45 (seven restatements) |
| U7 | A worker shall change files only in its worktree and its stage directory. | r6, r17, r34, r218 |
| U8 | Where `--json` is given, a tool shall print one JSON object. | 7 tool lines |
| U9 | A delivery shall change no initiative directory but those of the initiatives it runs. | r214–r218 |
| U10 | A stage `work run` started shall be given a brief, and no other input. | ~31 lines carrying "that `work run` started" (ex-supervision §5) |

## 8. Conditions (named)

A clause spelled out in many lines becomes one term.

| term | definition | replaces |
|---|---|---|
| **open** (of an initiative) | its status is neither `done` nor `abandoned` | 4 spellings (ex-tools §7), r66 |
| **open** (of a node) | its status is not `withdrawn` and not final | |
| **complete** (of an initiative) | at least one work-item is `green`, every work-item is `green` or `withdrawn`, every proposal is `formulated` or `withdrawn`, and its kept branch review lists nothing to fix now | 7 lines (r75, r93, r123, r124, r27, r212, r213), work-queue r62 |
| **settled** (of a request line) | its line outcome is `accepted`, `refused` or `withdrawn` | requests |
| **closed** (of a part) | a capability-proposal that is `formulated`, a glossary-proposal that is `approved`, a work-item that is `green`, or any part that is `withdrawn` | dmc#r36, dmc#r123, grammar.md §3 |
| **green check** (of a work-item branch) | its work-item's scenarios and the whole suite pass on it, a failing scenario counted after its one rerun alone | supervision r4, r219, r222 |

## 9. Words with one sense

Each word below has several senses today. Each sense gets its own term, and the word alone is avoided (`Not:`).

| word today | senses → terms |
|---|---|
| done | the status `done` (work-item, initiative); the outcome `DONE` |
| accepted | the request status `accepted`; the line outcome `accepted`; "the requirements it accepts" (relation accepts) |
| turn | the turn of a request (resource); the turn limit (of a session); a round trip |
| outcome | the outcome of a result; the line outcome |
| line | a request line; a requirement |
| kept | kept drafts; a kept branch review; a node keeps its status; … (six senses, ex-supervision §7): each written as its own verb |
| take | "take through transitions" → **run** a node; "take back" a failed run → **rerun** |
| ledger | the initiative's ledger; the old `spec/decisions.md` (migration only: **old ledger**) |
| target | a code target (analysis-tools); a trial's target repository |
| stage / role / agent / status | one stage kind each (§2.3); role and agent are its attributes |

## 10. Left open

These are the person's to decide:

1. **The design model.** `spec/index.md` says the plugin keeps design model v3, while `docs/design-model/` is v4. The
   two reuse rule codes for different rules, and their edges differ: `accepts` points at a scenario in grammar.md and
   at a requirement here; `argues` is 1..n in grammar.md and one capability here (ex-spec-side §2). This model follows
   the live files. Should the next design model be rewritten from this one, or this one fitted to it?
2. **The kind names.** grammar.md says `capability-requirement` and `acceptance-scenario`; the glossary forbids
   "capability requirement". This draft keeps **requirement** and **scenario**.
3. **The initiative's transitions.** No line today moves an initiative to `started` or `abandoned`
   (ex-queue-build §1). The table in §3 gives `work start` and `work abandon`, from the scripts' commands.
4. **Ids in the new version.** A fresh spec with fresh ids, with today's ids kept only as `restates` (§4), was the
   conversation's working assumption; it ends the retire-and-renumber rule's cost for the migration.
5. **Universal conditions as requirements.** Are U1–U10 requirements of a capability (with ids), or a section of
   their own in the index? This draft gives them their own ids, `U<n>`.
