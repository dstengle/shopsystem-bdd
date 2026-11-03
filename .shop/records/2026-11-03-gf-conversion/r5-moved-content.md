---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-03-gf-conversion-r5-moved-content
kind: design
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-03
status: draft
---

# R5's hand-off: the content the glossary no longer holds

R5 (revision 2, layer 2) rewrote the glossary of `spec/index.md` and the `## Terms` of every capability to
design-r2 §8: one sentence for each entry, conditions as `Def` sentences or primitive glosses with no `Means:`, and
relations as rows of `## Relations`. What an entry said beyond its one sentence (what a brief, a list or a log
contains, a rule, a cardinality) is no longer in the glossary. The layer 4 rewrite packages turn it into
requirements of the capability named. The second part of this file lists every entry R5 changed or removed, with
its old text verbatim and its new text. It is generated from the two lexicons (the `gf-conversion` base and R5's
branch), so it is complete.

## 1. Content to write as requirements, by the capability it belongs to

| capability | from the entry | the content (old text, verbatim) |
|---|---|---|
| supervision | **worker brief** (kind) | "it names the work-item, the files to read, where its result goes, the plugin's scripts directory, the initiative branch's base, the worker's worktree and its work-item branch; it tells the worker that it starts in its worktree and never changes directory, and to write its result first with the outcome `PARTIAL` and keep it current; it holds each answer of the work-item with the question it answers; a researcher's gives the work-item's file set and accepted scenarios and a limit of 80 turns; an implementer's says how the suite ended in its worktree before it started and, for a work-item an answer to its reviewer's question returned to `ready`, the reviewer's findings and the answer." |
| supervision | **round brief** (kind) | "an `integrate` round's gives the accepted lines of the request its initiative fulfils, every requirement id that the kept drafts of another initiative, not yet applied, add, and, for a proposal that has answers, its questions and answers and the initiative's ledger; a `gate` round's asks only for the questions on what its proposal adds, changes or removes, each a decision with its readings and the recommended reading marked; a `gate` or `apply` round's gives the path of the kept drafts of the `integrate` round that wrote its proposal, and an `apply` round's the answers." |
| supervision | **review brief** (kind) | "each run made at the initiative branch's head before it starts (the suite, each work-item's scenarios, each check a work-item names, `tools check`, `tools size`, `features deprecated` and `features bindings`) with its command, its exit code and its output and the commit they ran at; the commits from the initiative branch's base to its head, each with the work-item it belongs to or none; the change of that range less `.shop/`; and the files to read: the capabilities the work-items are under, the design-decisions those rest on, and each work-item's plan, implementer's report and review findings." |
| supervision | **tool list** (kind) | "this plugin's own directory as its plugin; the tools of its agent less any bare Write or Edit, or the stage's `[allowed_tools]` of `.shop/delivery.toml` less any bare Write or Edit; Bash only for `python3 -m pytest`, the plugin's scripts its stage runs, by path, and the git commands its stage needs; and `Skill` for each skill its agent lists." |
| supervision | **output** (kind) | "a researcher's file set, empty or not; a planner's plan and file set; an implementer's commits on which the work-item's scenarios and the suite pass; a reviewer's findings; an answering session's answer; an `integrate` or `apply` round's change list, or an `apply` round's answers its drafts do not hold; an `intake` round's line outcome or question on each line of its request; a `gate` round's questions." |
| supervision | **change list** (kind) | "the list ... of the requirement ids and the terms it adds, changes and removes, under each capability and the glossary." |
| supervision | **log** (event) | "with the time, the node, the stage, the agent and the session id." |
| supervision | **for** (stage → work-item, initiative, capability-proposal, glossary-proposal, request, question) | which stage is started for which node: "a worker's stage" for a work-item; "an `integrate` round, a branch review or an analysis" for an initiative; "a round" for a capability-proposal or a glossary-proposal; "an `intake` round" for a request; "an `answer` stage" for a question. |
| supervision | **on** (question → work-item, …) | "the work-item a question is written in, under its `## Questions`." |
| supervision | **on** (stage → work-item branch) | "the branch an `implement` stage works on." |
| supervision | **work-item** (kind, spec/index.md) | "complete when the scenarios it accepts or its check pass, or, where every requirement it accepts is of a guarantees capability, when its review passes." |
| supervision | **failed** (condition of work-item, spec/index.md) | "a work-item whose stage was discarded; its committed work is kept, and pushed when the remote takes it, and `work retry` returns it once the fault is remedied." |
| supervision | **green check** (condition of work-item branch, spec/index.md) | "a failing scenario counted after its one rerun alone." |
| supervision | **needs** (relation stage → resource, spec/index.md) | "it starts when every one is free." |
| supervision | **fault** (kind, spec/index.md) | "a push or git command failing, a worker changing a file under `.shop/work/` outside its stage directory, or a session `work run` started ending in an error, at its turn limit or without a result `work run` can read; kept while 0.29 lines name it (U6 replaces it)." |
| supervision, review | **worker** (kind, spec/index.md); **the branch reviewer** (actor, review) | "the branch reviewer, owning no work-item, is not one"; "it owns no work-item." |
| supervision, planning, code-research | **file set** (kind, spec/index.md) | "drafted with it, revised by its researcher and fixed by its planner." |
| supervision, work-queue | **transition** (kind, spec/index.md) | "a work-item's is logged in `log.jsonl`." |
| work-queue | **blocked by** (relation, spec/index.md) | "the relation has no cycle." |
| work-queue | **claim** (resource, spec/index.md) | "no two claims share a file." |
| work-queue | **accepts** (relation work-item → requirement, spec/index.md) | "a requirement a work-item delivers; a group named there means its members." |
| role-boundaries | **`work`** (actor, spec/index.md) | "the only writer of a status." |
| role-boundaries (or U) | **refuse** (event, spec/index.md) | "a refused command changes nothing." |
| requests | **request** (kind, spec/index.md) | "negotiated in turns until each is accepted, refused or withdrawn, and resolved by the requirement ids that hold the accepted ones." |
| requests | **turn** (resource, spec/index.md) | "passed to the other side by `work turn` unless the request becomes accepted, and to the asker when the request is delivered." |
| spec-integration | **glossary-proposal** (kind, spec/index.md) | "listing each `term/<term>` in its `adds`, `changes` or `removes`." |
| formulation | **deprecated scenario** (kind, spec/index.md) | "it formulates no requirement." |
| design-model-check | **requirement group** (kind, spec/index.md) | "its statements share a pre-state and a trigger." |
| migration-tools | **upgrade step** (kind, spec/index.md) | "pending for a repository when its version is above the repository's plugin version and at or below the plugin's." |
| analysis-tools | **reference** (kind) | "a definition is none." |
| feature-file-tools | **feature file** (kind) | "text inside a docstring is never a scenario, keyword or tag." |

The cardinalities the old relation glosses gave ("exactly one") are now the `one` of the rows' fourth cell. The
glosses of the other relation entries named only the relation ("a term the glossary-proposal adds") and carry
nothing a row does not.

The condition `complete` (an initiative) is now a `Def`. Its last conjunct, "its branch review lists no finding to
fix now", is the primitive condition **unfixed** (new), since the words of a branch review's findings are not in
the lexicon.

## 2. Every entry changed or removed, by file

### spec/index.md (glossary)

- **`work`** (actor) - gloss shortened to one sentence; the cut text is requirement content (layer 4)
  - old: the command that writes statuses, transitions and requests; the only writer of a status.
  - new: the command that writes statuses, transitions and requests.
- **worker** (kind) - gloss shortened to one sentence; the cut text is requirement content (layer 4)
  - old: a session `work run` starts with `claude -p` for one stage of one work-item, as that stage's agent; the branch reviewer, owning no work-item, is not one.
  - new: a session `work run` starts with `claude -p` for one stage of one work-item, as that stage's agent.
- **requirement group** (kind) - gloss shortened to one sentence; the cut text is requirement content (layer 4)
  - old: the requirements of a capability that together make one scenario, named `<capability>#g<n>`, with a title; its statements share a pre-state and a trigger.
  - new: the requirements of a capability that together make one scenario, named `<capability>#g<n>`, with a title.
- **deprecated scenario** (kind) - gloss shortened to one sentence; the cut text is requirement content (layer 4)
  - old: a scenario kept in its feature file, tagged `@deprecated`, after its line is changed or removed, until its replacement passes; it formulates no requirement. Not: held, holding, superseded.
  - new: a scenario kept in its feature file, tagged `@deprecated`, after its line is changed or removed, until its replacement passes. Not: held, holding, superseded.
- **request** (kind) - gloss shortened to one sentence; the cut text is requirement content (layer 4)
  - old: the one way work enters a bounded context: lines that its asker (another context, the product level, or the context itself) proposes to its upstream (the context asked), negotiated in turns until each is accepted, refused or withdrawn, and resolved by the requirement ids that hold the accepted ones.
  - new: the one way work enters a bounded context: lines that its asker (another context, the product level, or the context itself) proposes to its upstream (the context asked).
- **initiative** (kind) - `Kind of: node` added
  - old: the delivery of one request's accepted lines, named `i<n>`.
  - new: the delivery of one request's accepted lines, named `i<n>`. Kind of: node.
- **proposal** (kind) - `Kind of: node` added
  - old: a part of an initiative that proposes changes to the spec in its `adds`, `changes` and `removes`: a capability-proposal or a glossary-proposal.
  - new: a part of an initiative that proposes changes to the spec in its `adds`, `changes` and `removes`: a capability-proposal or a glossary-proposal. Kind of: node.
- **capability-proposal** (kind) - `Kind of: proposal` added
  - old: the proposal of an initiative that adds, changes and removes the requirements of one capability.
  - new: the proposal of an initiative that adds, changes and removes the requirements of one capability. Kind of: proposal.
- **glossary-proposal** (kind) - gloss shortened to one sentence; the cut text is requirement content (layer 4)
  - old: the part of an initiative, beside its capability-proposals, that proposes the terms the glossary of `spec/index.md` adds, changes and removes, listing each `term/<term>` in its `adds`, `changes` or `removes`.
  - new: the part of an initiative, beside its capability-proposals, that proposes the terms the glossary of `spec/index.md` adds, changes and removes. Kind of: proposal.
- **work-item** (kind) - gloss shortened to one sentence; the cut text is requirement content (layer 4)
  - old: the unit of delivery under a capability-proposal, named by its id `w<n>`, complete when the scenarios it accepts or its check pass, or, where every requirement it accepts is of a guarantees capability, when its review passes, run through its stages by `work run`.
  - new: the unit of delivery under a capability-proposal, named by its id `w<n>`, that `work run` runs through its stages. Kind of: node.
- **transition** (kind) - gloss shortened to one sentence; the cut text is requirement content (layer 4)
  - old: one change of a node's status, written by `work`; a work-item's is logged in `log.jsonl`. Not: move.
  - new: one change of a node's status, written by `work`. Not: move.
- **fault** (kind) - gloss shortened to one sentence; the cut text is requirement content (layer 4)
  - old: a failure outside a session's work that stops it: a push or git command failing, a worker changing a file under `.shop/work/` outside its stage directory, or a session `work run` started ending in an error, at its turn limit or without a result `work run` can read; kept while 0.29 lines name it (U6 replaces it).
  - new: a failure outside a session's work that stops it, such as a push or git command failing.
- **initiative branch** (kind) - gloss shortened to one sentence; the cut text is requirement content (layer 4)
  - old: the branch `work run` commits each transition on and merges each work-item branch into; its base is the commit it started from. Plural: initiative branches. Not: integration branch.
  - new: the branch `work run` commits each transition on and merges each work-item branch into, whose base is the commit it started from. Plural: initiative branches. Not: integration branch.
- **file set** (kind) - gloss shortened to one sentence; the cut text is requirement content (layer 4)
  - old: the paths, globs or directories a work-item says its work changes: drafted with it, revised by its researcher and fixed by its planner. Not: fileset, scope.
  - new: the paths, globs or directories a work-item says its work changes. Not: fileset, scope.
- **upgrade step** (kind) - gloss shortened to one sentence; the cut text is requirement content (layer 4)
  - old: one change to a repository's files that the plugin holds with the version that introduced it and a one-line description, pending for a repository when its version is above the repository's plugin version and at or below the plugin's.
  - new: one change to a repository's files that the plugin holds with the version that introduced it and a one-line description.
- **status** (attribute initiative) - gloss shortened to one sentence; the cut text is requirement content (layer 4)
  - old: a node's, request's or design-decision's place in its kind's lifecycle, written in its frontmatter by `work`; this entry gives an initiative's, and the entries below give the other kinds'. Values: `proposed`, `started`, `done`, `abandoned`. Transitions: `proposed` → `started`: `work start`; `started` → `done`: complete; `started` → `abandoned`: `work abandon`. Not: state.
  - new: a node's, request's or design-decision's place in its kind's lifecycle, written in its frontmatter by `work`. Values: `proposed`, `started`, `done`, `abandoned`. Transitions: `proposed` → `started`: `work start`; `started` → `done`: complete; `started` → `abandoned`: `work abandon`. Not: state.
- **open** (condition initiative) - `Means:` -> a `Def` sentence
  - old: Means: its status is not `done` and not `abandoned`.
  - new: An initiative is open when the initiative is not `done` and the initiative is not `abandoned`.
- **open** (condition work-item) - `Means:` -> a `Def` sentence
  - old: Means: its status is not `green` and not `withdrawn`.
  - new: A work-item is open when the work-item is not `green` and the work-item is not `withdrawn`.
- **complete** (condition initiative) - `Means:` -> a `Def` sentence
  - old: Means: a work-item of it is `green`, every work-item of it is `green` or `withdrawn`, every capability-proposal of it is `formulated` or `withdrawn`, and its branch review lists no finding to fix now.
  - new: An initiative is complete when a work-item of the initiative is `green` and every work-item of the initiative is closed and every capability-proposal part of the initiative is closed and the initiative is not unfixed.
- **settled** (condition request line) - `Means:` -> a `Def` sentence
  - old: Means: its line outcome is `accepted`, `refused` or `withdrawn`.
  - new: A request line is settled when the request line is `accepted` or the request line is `refused` or the request line is `withdrawn`.
- **closed** (condition capability-proposal) - `Means:` -> a `Def` sentence
  - old: Means: its status is `formulated` or `withdrawn`.
  - new: A capability-proposal is closed when the capability-proposal is `formulated` or the capability-proposal is `withdrawn`.
- **closed** (condition glossary-proposal) - `Means:` -> a `Def` sentence
  - old: Means: its status is `approved` or `withdrawn`.
  - new: A glossary-proposal is closed when the glossary-proposal is `approved` or the glossary-proposal is `withdrawn`.
- **closed** (condition work-item) - `Means:` -> a `Def` sentence
  - old: Means: its status is `green` or `withdrawn`.
  - new: A work-item is closed when the work-item is `green` or the work-item is `withdrawn`.
- **failed** (condition work-item) - `Means:` -> a `Def` sentence
  - old: a work-item whose stage was discarded; its committed work is kept, and pushed when the remote takes it, and `work retry` returns it once the fault is remedied. Means: its status is `failed`. Not: aborted.
  - new: A work-item is failed when the work-item is `failed`. Not: aborted.
- **free** (condition resource) - `Means:` -> a primitive gloss
  - old: Means: no session holds it, or for a counted resource, fewer than its number.
  - new: a resource that no session holds, or a counted resource that fewer sessions hold than its number.
- **green check** (condition work-item branch) - `Means:` -> a primitive gloss
  - old: Means: the scenarios of its work-item and the suite pass on it, a failing scenario counted after its one rerun alone.
  - new: a work-item branch on which the scenarios of its work-item and the suite pass.
- **part of** (relation proposal → initiative) - relation entry -> row of `## Relations` in spec/index.md
  - old: each proposal is part of exactly one initiative.
- **argues** (relation capability-proposal → capability) - relation entry -> row of `## Relations` in spec/index.md
  - old: each capability-proposal argues exactly one capability.
- **removes** (relation capability-proposal → requirement) - relation entry -> row of `## Relations` in spec/index.md
  - old: a requirement the proposal retires.
- **changes** (relation capability-proposal → requirement group) - relation entry -> row of `## Relations` in spec/index.md
  - old: a group whose title or membership the proposal changes.
- **adds** (relation glossary-proposal → term) - relation entry -> row of `## Relations` in spec/index.md
  - old: a term the glossary-proposal adds.
- **changes** (relation glossary-proposal → term) - relation entry -> row of `## Relations` in spec/index.md
  - old: a term the glossary-proposal changes.
- **removes** (relation glossary-proposal → term) - relation entry -> row of `## Relations` in spec/index.md
  - old: a term the glossary-proposal removes.
- **under** (relation work-item → capability-proposal) - relation entry -> row of `## Relations` in spec/index.md
  - old: a work-item delivers part of exactly one capability-proposal.
- **accepts** (relation work-item → requirement) - relation entry -> row of `## Relations` in spec/index.md
  - old: a requirement a work-item delivers; a group named there means its members.
- **blocked by** (relation work-item → work-item) - relation entry kept (a checked-in feature's Given needs it)
  - old: a work-item waits for another; the relation has no cycle.
  - new: a work-item waits for another.
- **member of** (relation requirement → requirement group) - relation entry -> row of `## Relations` in spec/index.md
  - old: each requirement is a member of exactly one group.
- **generates** (relation requirement group → scenario) - relation entry -> row of `## Relations` in spec/index.md
  - old: each group that is not logic-only generates exactly one scenario.
- **in** (relation requirement group → capability) - relation entry -> row of `## Relations` in spec/index.md
  - old: each group is in exactly one capability.
- **in** (relation capability → bounded context) - relation entry -> row of `## Relations` in spec/index.md
  - old: each capability is in exactly one bounded context.
- **rests on** (relation capability → design-decision) - relation entry -> row of `## Relations` in spec/index.md
  - old: a decision a capability rests on.
- **supersedes** (relation design-decision → design-decision) - relation entry -> row of `## Relations` in spec/index.md
  - old: a decision that replaces another.
- **asker** (relation request → bounded context) - relation entry -> row of `## Relations` in spec/index.md
  - old: the context that proposes a request's lines.
- **upstream** (relation request → bounded context) - relation entry -> row of `## Relations` in spec/index.md
  - old: the context a request asks.
- **raised for** (relation request → request) - relation entry -> row of `## Relations` in spec/index.md
  - old: the request an integrate round raised this one for.
- **belongs to** (relation commit → work-item) - relation entry -> row of `## Relations` in spec/index.md
  - old: the work-item a commit is made for.
- **merges into** (relation work-item branch → initiative branch) - relation entry -> row of `## Relations` in spec/index.md
  - old: the branch a work-item branch is merged into.
- **needs** (relation stage → resource) - relation entry -> row of `## Relations` in spec/index.md
  - old: a resource a stage must hold to start; it starts when every one is free.
- **in** (relation file → worktree) - relation entry -> row of `## Relations` in spec/index.md
  - old: a file of a worktree.
- **of** (relation file → initiative) - relation entry -> row of `## Relations` in spec/index.md
  - old: a file under the initiative directory of an initiative.
- **outside** (relation initiative → delivery) - relation entry -> row of `## Relations` in spec/index.md
  - old: an initiative the delivery does not run.
- **refuse** (event) - gloss shortened to one sentence; the cut text is requirement content (layer 4)
  - old: a tool declines a command; a refused command changes nothing.
  - new: a tool declines a command.
- **claim** (resource) - gloss shortened to one sentence; the cut text is requirement content (layer 4)
  - old: the tracked files a `claimed` work-item holds: those its file set covers and any added with `work claim`; no two claims share a file. Not: lock, reservation.
  - new: the tracked files a `claimed` work-item holds: those its file set covers and any added with `work claim`. Not: lock, reservation.
- **turn** (resource) - gloss shortened to one sentence; the cut text is requirement content (layer 4)
  - old: one for each request, held by the side whose part of the request is to be written next, passed to the other side by `work turn` unless the request becomes accepted, and to the asker when the request is delivered.
  - new: one for each request, held by the side whose part of the request is to be written next.

### analysis-tools

- **reference** (kind) - gloss shortened to one sentence; the cut text is requirement content (layer 4)
  - old: a use of a name the project defines, through an import or an alias included, written `path:line`; a definition is none.
  - new: a use of a name the project defines, through an import or an alias included, written `path:line`.

### code-research

- **of** (relation scenario → work-item) - relation entry -> row of `## Relations` in spec/capabilities/code-research.md
  - old: a scenario of a requirement the work-item accepts.
- **of** (relation line count → module) - relation entry -> row of `## Relations` in spec/capabilities/code-research.md
  - old: the line count of a module.
- **broken by** (relation test → work-item) - relation entry -> row of `## Relations` in spec/capabilities/code-research.md
  - old: an existing test the work-item's accepted requirements make impossible to keep.
- **changed by** (relation file → work-item) - relation entry -> row of `## Relations` in spec/capabilities/code-research.md
  - old: a production or test file the work-item must change for its scenarios to pass and for everything that passes today to keep passing.
- **in** (relation probe → worktree) - relation entry -> row of `## Relations` in spec/capabilities/code-research.md
  - old: a probe run on a worktree's files.

### design-model-check

- **clingoless** (condition interpreter) - `Means:` -> a primitive gloss
  - old: Means: it cannot import clingo, and a `python3` on `PATH` can.
  - new: an interpreter that cannot import clingo, where a `python3` on `PATH` can.
- **unfound** (condition interpreter) - `Means:` -> a primitive gloss
  - old: Means: it cannot import clingo, and no interpreter `model` tries can.
  - new: an interpreter that cannot import clingo, where no interpreter `model` tries can.
- **stale** (condition decisions index) - `Means:` -> a primitive gloss
  - old: Means: it is not what `model decisions` would write.
  - new: a decisions index that is not what `model decisions` would write.
- **sound** (condition bounded context) - `Means:` -> a primitive gloss
  - old: Means: `model check` finds no violation, unresolved reference or file problem in it.
  - new: a bounded context in which `model check` finds no violation, unresolved reference or file problem.
- **unmigrated** (condition bounded context) - `Means:` -> a primitive gloss
  - old: Means: it has `spec/decisions.md`, or a `decisions/`, `work/` or `records/` directory at its root.
  - new: a bounded context with `spec/decisions.md`, or with a `decisions/`, `work/` or `records/` directory at its root.
- **unnumbered** (condition capability) - `Means:` -> a primitive gloss
  - old: Means: a requirement bullet of its Behaviour has no `[r<n>]`.
  - new: a capability with a requirement bullet in its Behaviour that has no `[r<n>]`.
- **renumbered** (condition capability) - `Means:` -> a primitive gloss
  - old: Means: two of its requirements have the same id.
  - new: a capability two of whose requirements have the same id.
- **reusing** (condition capability) - `Means:` -> a primitive gloss
  - old: Means: it uses an id it lists as retired.
  - new: a capability that uses an id it lists as retired.
- **misnamed** (condition capability) - `Means:` -> a primitive gloss
  - old: Means: its `id` is not `capability/<context path>/<file name>`, or it has no `## Behaviour`.
  - new: a capability whose `id` is not `capability/<context path>/<file name>`, or that has no `## Behaviour`.
- **untested** (condition requirement) - `Means:` -> a primitive gloss
  - old: Means: no scenario names it, and its capability is not of the group `guarantees`.
  - new: a requirement that no scenario names, of a capability that is not of the group `guarantees`.
- **avoiding** (condition requirement) - `Means:` -> a primitive gloss
  - old: Means: it mentions a word its context's glossary lists after `Not:`.
  - new: a requirement that mentions a word its context's glossary lists after `Not:`.
- **unparsed** (condition requirement) - `Means:` -> a primitive gloss
  - old: Means: it does not parse in the requirement grammar of its context.
  - new: a requirement that does not parse in the requirement grammar of its context.
- **overtagged** (condition scenario) - `Means:` -> a primitive gloss
  - old: Means: it is not tagged `@deprecated` and has more than one `@r<n>` tag.
  - new: a scenario not tagged `@deprecated` that has more than one `@r<n>` tag.
- **misreferring** (condition scenario) - `Means:` -> a primitive gloss
  - old: Means: it names a requirement its capability does not have.
  - new: a scenario that names a requirement its capability does not have.
- **misfiled** (condition feature) - `Means:` -> a primitive gloss
  - old: Means: it is not `features/<name>.feature` for a capability `<name>`.
  - new: a feature that is not `features/<name>.feature` for a capability `<name>`.
- **duplicated** (condition term) - `Means:` -> a primitive gloss
  - old: Means: two glossary entries have it as their term.
  - new: a term that two glossary entries have as their term.
- **selfavoiding** (condition term) - `Means:` -> a primitive gloss
  - old: Means: a word it lists after `Not:` is a term of the context, or the term itself.
  - new: a term with a word after `Not:` that is a term of the context, or the term itself.
- **malformed** (condition term) - `Means:` -> a primitive gloss
  - old: Means: its bullet in the `## Glossary` of `spec/index.md` is in no form of a term entry.
  - new: a term whose bullet in the `## Glossary` of `spec/index.md` is in no form of a term entry.
- **reaching** (condition capability-proposal) - `Means:` -> a primitive gloss
  - old: Means: it is `drafted` or `approved` and changes a requirement no capability has.
  - new: a `drafted` or `approved` capability-proposal that changes a requirement no capability has.
- **unformulated** (condition capability-proposal) - `Means:` -> a primitive gloss
  - old: Means: it is `formulated` and adds a requirement with no scenario, of a capability that is not of the group `guarantees`.
  - new: a `formulated` capability-proposal that adds a requirement with no scenario, of a capability that is not of the group `guarantees`.
- **plural** (condition capability-proposal) - `Means:` -> a primitive gloss
  - old: Means: it argues more than one capability.
  - new: a capability-proposal that argues more than one capability.
- **dangling** (condition capability-proposal) - `Means:` -> a primitive gloss
  - old: Means: it adds or removes an id its capability neither has nor lists as retired.
  - new: a capability-proposal that adds or removes an id its capability neither has nor lists as retired.
- **termless** (condition capability-proposal) - `Means:` -> a primitive gloss
  - old: Means: its `adds`, `changes` or `removes` names `term/<term>` the glossary does not have.
  - new: a capability-proposal whose `adds`, `changes` or `removes` names a `term/<term>` the glossary does not have.
- **termless** (condition glossary-proposal) - `Means:` -> a primitive gloss
  - old: Means: its `adds`, `changes` or `removes` names `term/<term>` the glossary does not have.
  - new: a glossary-proposal whose `adds`, `changes` or `removes` names a `term/<term>` the glossary does not have.
- **parentless** (condition work-item) - `Means:` -> a primitive gloss
  - old: Means: it has no `part_of`.
  - new: a work-item with no `part_of`.
- **uncommitted** (condition work-item) - `Means:` -> a primitive gloss
  - old: Means: it is not `withdrawn` and has no `accepts` and no `check`.
  - new: a work-item that is not `withdrawn` and has no `accepts` and no `check`.
- **misnumbered** (condition work-item) - `Means:` -> a primitive gloss
  - old: Means: its file name is not `w<n>.md`.
  - new: a work-item whose file name is not `w<n>.md`.
- **alien** (condition work-item) - `Means:` -> a primitive gloss
  - old: Means: its `part_of` has another context's path, on a kind kept in `.shop/work/`.
  - new: a work-item whose `part_of` has another context's path, on a kind kept in `.shop/work/`.
- **misreferenced** (condition work-item) - `Means:` -> a primitive gloss
  - old: Means: its `accepts` names a reference that is not `<capability>#r<n>`.
  - new: a work-item whose `accepts` names a reference that is not `<capability>#r<n>`.
- **unresolving** (condition work-item) - `Means:` -> a primitive gloss
  - old: Means: its `under` names nothing in the repository.
  - new: a work-item whose `under` names nothing in the repository.
- **misidentified** (condition work-item) - `Means:` -> a primitive gloss
  - old: Means: its `id` is not `<kind>/<context path>/<name>` with its own kind.
  - new: a work-item whose `id` is not `<kind>/<context path>/<name>` with its own kind.
- **homeless** (condition work-item) - `Means:` -> a primitive gloss
  - old: Means: its directory has no `initiative.md`.
  - new: a work-item whose directory has no `initiative.md`.
- **crowded** (condition initiative) - `Means:` -> a primitive gloss
  - old: Means: it is not a capability-change and has more than one part directly under it.
  - new: an initiative that is not a capability-change and has more than one part directly under it.
- **unrequested** (condition initiative) - `Means:` -> a primitive gloss
  - old: Means: it is dated after 2026-10-23 and fulfils no request.
  - new: an initiative dated after 2026-10-23 that fulfils no request.
- **unwaiting** (condition initiative) - `Means:` -> a primitive gloss
  - old: Means: it is `done` while a request whose asker is its context and that names it is not `delivered`.
  - new: a `done` initiative while a request whose asker is its context and that names it is not `delivered`.
- **jobbed** (condition initiative) - `Means:` -> a primitive gloss
  - old: Means: its kind is `job` or `job-path`.
  - new: an initiative whose kind is `job` or `job-path`.
- **unanchored** (condition request) - `Means:` -> a primitive gloss
  - old: Means: it is part of no job-thread, cites no origin and is raised for no request.
  - new: a request that is part of no job-thread, cites no origin and is raised for no request.
- **misresolved** (condition request) - `Means:` -> a primitive gloss
  - old: Means: it is `delivered` and its resolution names a requirement the spec does not have.
  - new: a `delivered` request whose resolution names a requirement the spec does not have.
- **misformed** (condition request) - `Means:` -> a primitive gloss
  - old: Means: it is not of the form `work request` writes.
  - new: a request that is not of the form `work request` writes.
- **headless** (condition design-decision) - `Means:` -> a primitive gloss
  - old: Means: it has no `id` or no `## Decision` section.
  - new: a design-decision with no `id` or no `## Decision` section.

### feature-file-tools

- **feature file** (kind) - gloss shortened to one sentence; the cut text is requirement content (layer 4)
  - old: a `*.feature` file under the directory `--dir` names (default `features`), read line by line; text inside a docstring is never a scenario, keyword or tag.
  - new: a `*.feature` file under the directory `--dir` names (default `features`), read line by line.

### planning

- **broken by** (relation test → plan decision) - relation entry -> row of `## Relations` in spec/capabilities/planning.md
  - old: a test a decision of the plan makes impossible to keep, with what becomes of it.
- **settled by** (relation plan decision → requirement) - relation entry -> row of `## Relations` in spec/capabilities/planning.md
  - old: the requirement or design-decision that settles a decision.

### red-green

- **passing** (condition scenario) - `Means:` -> a primitive gloss
  - old: Means: it passes when it is run alone with `python3 -m pytest`.
  - new: a scenario that passes when it is run alone with `python3 -m pytest`.
- **large** (condition work-item) - `Means:` -> a primitive gloss
  - old: Means: its work needs more than 15 files touched.
  - new: a work-item whose work needs more than 15 files touched.
- **outside** (relation file → file set) - relation entry -> row of `## Relations` in spec/capabilities/red-green.md
  - old: a file the work needs that the work-item's file set does not cover.

### requests

- **closed** (condition request) - `Means:` -> a `Def` sentence
  - old: Means: its status is `delivered`, `refused` or `withdrawn`.
  - new: A request is closed when the request is `delivered` or the request is `refused` or the request is `withdrawn`.
- **unparsed** (condition request line) - `Means:` -> a primitive gloss
  - old: Means: it does not parse in the requirement grammar of the upstream.
  - new: a request line that does not parse in the requirement grammar of the upstream.
- **uncited** (condition observation) - `Means:` -> a primitive gloss
  - old: Means: the `source` of no initiative and of no request names it.
  - new: an observation that the `source` of no initiative and of no request names.
- **originless** (condition command) - `Means:` -> a primitive gloss
  - old: Means: it gives none of `--source`, `--thread` and `--raised-for`.
  - new: a command that gives none of `--source`, `--thread` and `--raised-for`.
- **sourced** (condition command) - `Means:` -> a primitive gloss
  - old: Means: it gives `--source` with `--thread` or `--raised-for`.
  - new: a command that gives `--source` with `--thread` or `--raised-for`.
- **foreign** (condition command) - `Means:` -> a primitive gloss
  - old: Means: it gives `--from` an asker other than the bounded context it is run in.
  - new: a command that gives `--from` an asker other than the bounded context it is run in.
- **downstream** (condition bounded context) - `Means:` -> a primitive gloss
  - old: Means: its `spec/index.md` lists an upstream under `## Upstreams`.
  - new: a bounded context whose `spec/index.md` lists an upstream under `## Upstreams`.

### review

- **the branch reviewer** (actor) - gloss shortened to one sentence; the cut text is requirement content (layer 4)
  - old: the session of a `branch review` stage, started as the agent `bdd-branch-reviewer`; it owns no work-item.
  - new: the session of a `branch review` stage, started as the agent `bdd-branch-reviewer`.
- **changes** (relation commit → feature) - relation entry -> row of `## Relations` in spec/capabilities/review.md
  - old: a commit that changes a feature file.
- **weakens** (relation commit → test) - relation entry -> row of `## Relations` in spec/capabilities/review.md
  - old: a commit that removes, loosens, skips or rewrites a test.
- **contradicts** (relation commit → requirement) - relation entry -> row of `## Relations` in spec/capabilities/review.md
  - old: a commit whose behaviour contradicts a requirement.
- **deletes** (relation commit → scenario) - relation entry -> row of `## Relations` in spec/capabilities/review.md
  - old: a commit that removes a scenario.
- **of** (relation work-item → initiative) - relation entry -> row of `## Relations` in spec/capabilities/review.md
  - old: a work-item under a capability-proposal of the initiative.
- **of** (relation commit → work-item) - relation entry -> row of `## Relations` in spec/capabilities/review.md
  - old: a commit made on the work-item's branch for the work-item.

### spec-integration

- **quotes** (relation requirement → design note) - relation entry -> row of `## Relations` in spec/capabilities/spec-integration.md
  - old: a drafted statement that quotes a sentence of the note.
- **added by** (relation requirement → capability-proposal) - relation entry -> row of `## Relations` in spec/capabilities/spec-integration.md
  - old: a statement a capability-proposal adds.
- **on** (relation question → term) - relation entry -> row of `## Relations` in spec/capabilities/spec-integration.md
  - old: a question about a term a glossary-proposal adds, changes or removes.

### supervision

- **for** (relation stage → work-item) - relation entry deleted: covered by a `Kind of:` expansion of a row in spec/index.md
  - old: the work-item a worker's stage is started for.
- **for** (relation stage → initiative) - relation entry deleted: covered by a `Kind of:` expansion of a row in spec/index.md
  - old: the initiative an `integrate` round, a branch review or an analysis is started for.
- **for** (relation stage → capability-proposal) - relation entry deleted: covered by a `Kind of:` expansion of a row in spec/index.md
  - old: the capability-proposal a round is started for.
- **for** (relation stage → glossary-proposal) - relation entry deleted: covered by a `Kind of:` expansion of a row in spec/index.md
  - old: the glossary-proposal a round is started for.
- **for** (relation stage → request) - relation entry -> row of `## Relations` in spec/capabilities/supervision.md
  - old: the request an `intake` round is started for.
- **for** (relation stage → question) - relation entry -> row of `## Relations` in spec/capabilities/supervision.md
  - old: the question an `answer` stage is started for.
- **on** (relation question → work-item) - relation entry kept (a checked-in feature's Given needs it)
  - old: the work-item a question is written in, under its `## Questions`.
  - new: the work-item a question is written in.
- **on** (relation question → request) - relation entry -> row of `## Relations` in spec/capabilities/supervision.md
  - old: the request a question is written in.
- **on** (relation stage → work-item branch) - relation entry -> row of `## Relations` in spec/capabilities/supervision.md
  - old: the branch an `implement` stage works on.
- **log** (event) - gloss shortened to one sentence; the cut text is requirement content (layer 4)
  - old: `work run` appends a line to `.shop/work/<initiative>/log.jsonl` with the time, the node, the stage, the agent and the session id. Forms: logs, logged.
  - new: `work run` appends a line to `.shop/work/<initiative>/log.jsonl`. Forms: logs, logged.
- **output** (kind) - gloss shortened to one sentence; the cut text is requirement content (layer 4)
  - old: what a stage's result gives as its stage's work: a researcher's file set, empty or not; a planner's plan and file set; an implementer's commits on which the work-item's scenarios and the suite pass; a reviewer's findings; an answering session's answer; an `integrate` or `apply` round's change list, or an `apply` round's answers its drafts do not hold; an `intake` round's line outcome or question on each line of its request; a `gate` round's questions.
  - new: what a stage's result gives as its stage's work.
- **change list** (kind) - gloss shortened to one sentence; the cut text is requirement content (layer 4)
  - old: the list an `integrate` or `apply` round's result gives of the requirement ids and the terms it adds, changes and removes, under each capability and the glossary.
  - new: the list an `integrate` or `apply` round's result gives of what it adds, changes and removes.
- **tool list** (kind) - gloss shortened to one sentence; the cut text is requirement content (layer 4)
  - old: what `work run` gives a worker to work with: this plugin's own directory as its plugin; the tools of its agent less any bare Write or Edit, or the stage's `[allowed_tools]` of `.shop/delivery.toml` less any bare Write or Edit; Bash only for `python3 -m pytest`, the plugin's scripts its stage runs, by path, and the git commands its stage needs; and `Skill` for each skill its agent lists.
  - new: what `work run` gives a worker to work with.
- **worker brief** (kind) - gloss shortened to one sentence; the cut text is requirement content (layer 4)
  - old: the brief of a worker: it names the work-item, the files to read, where its result goes, the plugin's scripts directory, the initiative branch's base, the worker's worktree and its work-item branch; it tells the worker that it starts in its worktree and never changes directory, and to write its result first with the outcome `PARTIAL` and keep it current; it holds each answer of the work-item with the question it answers; a researcher's gives the work-item's file set and accepted scenarios and a limit of 80 turns; an implementer's says how the suite ended in its worktree before it started and, for a work-item an answer to its reviewer's question returned to `ready`, the reviewer's findings and the answer.
  - new: the brief `work run` gives a worker.
- **round brief** (kind) - gloss shortened to one sentence; the cut text is requirement content (layer 4)
  - old: the brief of a round: an `integrate` round's gives the accepted lines of the request its initiative fulfils, every requirement id that the kept drafts of another initiative, not yet applied, add, and, for a proposal that has answers, its questions and answers and the initiative's ledger; a `gate` round's asks only for the questions on what its proposal adds, changes or removes, each a decision with its readings and the recommended reading marked; a `gate` or `apply` round's gives the path of the kept drafts of the `integrate` round that wrote its proposal, and an `apply` round's the answers.
  - new: the brief `work run` gives a round.
- **review brief** (kind) - gloss shortened to one sentence; the cut text is requirement content (layer 4)
  - old: the brief of a branch review: each run made at the initiative branch's head before it starts (the suite, each work-item's scenarios, each check a work-item names, `tools check`, `tools size`, `features deprecated` and `features bindings`) with its command, its exit code and its output and the commit they ran at; the commits from the initiative branch's base to its head, each with the work-item it belongs to or none; the change of that range less `.shop/`; and the files to read: the capabilities the work-items are under, the design-decisions those rest on, and each work-item's plan, implementer's report and review findings.
  - new: the brief `work run` gives a branch review.
- **faulty** (condition session) - `Means:` -> a primitive gloss
  - old: Means: it ends in an error or at its turn limit, or leaves output that holds no JSON result.
  - new: a session that ends in an error or at its turn limit, or leaves output that holds no JSON result.
- **meddling** (condition session) - `Means:` -> a primitive gloss
  - old: Means: it changes a file under `.shop/work/` outside its stage directory.
  - new: a session that changes a file under `.shop/work/` outside its stage directory.
- **littering** (condition session) - `Means:` -> a primitive gloss
  - old: Means: while it works, a file under `.shop/work/` of the checkout changes and is left uncommitted.
  - new: a session during whose work a file under `.shop/work/` of the checkout changes and is left uncommitted.
- **crossing** (condition session) - `Means:` -> a primitive gloss
  - old: Means: while it works, a session of another initiative that `work run` runs side by side commits a file of that other initiative and a change to a file of its own.
  - new: a session during whose work a session of another initiative that `work run` runs side by side commits a file of that other initiative and a change to a file of its own.
- **outputless** (condition result) - `Means:` -> a `Def` sentence
  - old: Means: it gives neither a question nor its stage's output.
  - new: A result is outputless when the result gives no question and the result gives no output.
- **setless** (condition result) - `Means:` -> a primitive gloss
  - old: Means: it gives an empty file set.
  - new: a result that gives an empty file set.
- **listless** (condition result) - `Means:` -> a `Def` sentence
  - old: Means: it gives no change list.
  - new: A result is listless when the result gives no change list.
- **glossarial** (condition result) - `Means:` -> a primitive gloss
  - old: Means: its change list names the glossary.
  - new: a result whose change list names the glossary.
- **raising** (condition result) - `Means:` -> a primitive gloss
  - old: Means: it gives the lines of a request into an upstream.
  - new: a result that gives the lines of a request into an upstream.
- **awaited** (condition result) - `Means:` -> a primitive gloss
  - old: Means: it gave the lines of a request into an upstream, and that request is not `delivered`.
  - new: a result that gave the lines of a request into an upstream, where that request is not `delivered`.
- **strange** (condition result) - `Means:` -> a primitive gloss
  - old: Means: its change list names a capability that neither `spec/capabilities/` nor its drafts have.
  - new: a result whose change list names a capability that neither `spec/capabilities/` nor its drafts have.
- **unheld** (condition result) - `Means:` -> a primitive gloss
  - old: Means: it gives an answer that the drafts its stage applied do not hold.
  - new: a result that gives an answer the drafts its stage applied do not hold.
- **fixing** (condition result) - `Means:` -> a primitive gloss
  - old: Means: it gives a question listing review findings to fix now.
  - new: a result that gives a question listing review findings to fix now.
- **unparsing** (condition result) - `Means:` -> a primitive gloss
  - old: Means: a requirement its drafts hold does not parse, or the logic check on the spec with its drafts finds an L1 or an L3.
  - new: a result whose drafts hold a requirement that does not parse, or with whose drafts the logic check on the spec finds an L1 or an L3.
- **naming** (condition result) - `Means:` -> a primitive gloss
  - old: Means: it names a report the session wrote in its worktree.
  - new: a result that names a report its session wrote in its worktree.
- **unpushable** (condition remote) - `Means:` -> a primitive gloss
  - old: Means: it refuses every push.
  - new: a remote that refuses every push.
- **ahead** (condition initiative branch) - `Means:` -> a primitive gloss
  - old: Means: it has commits its remote does not have.
  - new: an initiative branch with commits its remote does not have.
- **reviewed** (condition initiative branch) - `Means:` -> a primitive gloss
  - old: Means: a kept branch review has read every commit on it but the kept branch reviews' own.
  - new: an initiative branch whose every commit but the kept branch reviews' own a kept branch review has read.
- **gitless** (condition initiative branch) - `Means:` -> a primitive gloss
  - old: Means: the repository it would be in is not a git repository.
  - new: an initiative branch whose repository would not be a git repository.
- **lost** (condition work-item branch) - `Means:` -> a primitive gloss
  - old: Means: its implementer deleted it before `work run` merged it.
  - new: a work-item branch its implementer deleted before `work run` merged it.
- **kept** (condition work-item branch) - `Means:` -> a primitive gloss
  - old: Means: `work run` kept it when its work-item became `awaiting-answer`.
  - new: a work-item branch `work run` kept when its work-item became `awaiting-answer`.
- **flaky** (condition work-item branch) - `Means:` -> a primitive gloss
  - old: Means: a scenario fails on it once and passes on its second run alone.
  - new: a work-item branch on which a scenario fails once and passes on its second run alone.
- **dirty** (condition file) - `Means:` -> a primitive gloss
  - old: Means: it is under `.shop/work/` and differs from its last commit.
  - new: a file under `.shop/work/` that differs from its last commit.
- **answered** (condition question) - `Means:` -> a primitive gloss
  - old: Means: an answer to it is written under its node's `## Answers`.
  - new: a question with an answer written under its node's `## Answers`.
- **bare** (condition initiative) - `Means:` -> a primitive gloss
  - old: Means: it fulfils a request and has no capability-proposal, no glossary-proposal and no work-item.
  - new: an initiative that fulfils a request and has no capability-proposal, no glossary-proposal and no work-item.
- **itemless** (condition initiative) - `Means:` -> a primitive gloss
  - old: Means: no work-item is kept in it.
  - new: an initiative in which no work-item is kept.
- **codified** (condition change list) - `Means:` -> a primitive gloss
  - old: Means: every capability it names has `language: codified-1` in its file.
  - new: a change list whose every capability has `language: codified-1` in its file.
- **uncodified** (condition change list) - `Means:` -> a primitive gloss
  - old: Means: a service capability it names has no `language: codified-1` in its file.
  - new: a change list that names a service capability with no `language: codified-1` in its file.

### work-queue

- **of** (relation ledger → initiative) - relation entry -> row of `## Relations` in spec/capabilities/work-queue.md
  - old: the ledger of an initiative is `.shop/work/<initiative>/ledger.md`.
- **out of step** (condition work-item) - `Means:` -> a primitive gloss
  - old: Means: the last status `log.jsonl` gives it differs from the status in its file.
  - new: a work-item whose last status in `log.jsonl` differs from the status in its file.

### Entries added

- **unfixed** (condition) in spec/index.md (glossary): an initiative whose kept branch review lists a review finding to fix now.

