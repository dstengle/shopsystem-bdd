# How we got here

Date: 2026-10-14. A condensed account of the conversation that produced
`design-model.md`, in the order the ideas arrived, with what each turn
decided and what it later overturned. Two sessions: 23–29 September on
specifying, 13 October on building.

## September: why the specs worked

**The question.** Two design notes (kb, shop-knowledge) had produced good
Gherkin features and slice plans. Why did they work, how to separate
their levels, and could the method be generalised without becoming the
overweight product-ops system that preceded it?

**The answer.** Nearly every sentence in the notes was one of five kinds
— decision, belief, observable behaviour, implementation that may change,
scope — each with its own home and its own way of being falsified. Three
mechanisms held them together: a declared narrator, a demand chain
(downstream scenarios drive upstream features), and a walking skeleton as
the plan. The product thinking was compressed into the narrator and the
beliefs; that was why the notes stayed short.

**Over time.** A spec is the authority above features, so it must be
rewritten in place and versioned with the contract; proposals are dated
notes that merge and retire. Delta notes and consolidation-by-squash were
proposed and withdrawn as contradictory to spec-as-authority.

**Decomposition.** A document has one order and its edits describe its
history. The unit of change became the capability: a cluster of
observable behaviour with one narrator, one file, paired one-to-one with
a feature file. Cross-cutting things — decisions, beliefs — became their
own entries. A worked decomposition of kb into eleven capabilities found
two the note hadn't named (boundary, identity) and one gap (what a
contract-version mismatch does).

**Capability groups.** Ports, day-1/day-2 operations and quality
characteristics combined into four groups by narrator and kind of
promise: model, service, operations, guarantees. The admin CLI belonged
to operations; nearly all of kb's deferrals landed there.

**EARS.** Behaviour lines adopted EARS with two adaptations: no "shall",
and the response must be observable by the narrator — the rule that sorts
behaviour from mechanism. Rewriting `contract` found one implied
requirement (transport equivalence) and one real gap.

**Up a level.** Capabilities come from jobs (not processes, which encode
today's solution); the relationship between contexts is a DDD context-map
pattern written as fields a downstream author can act on. The derivation
chain was redrawn as a graph with typed edges rather than a ladder.

**Citation direction.** An upstream naming the downstream scenarios that
need it inverts the dependency and breaks at the second client. Demand
is recorded by the downstream (`@uses`), carried by a request, and the
upstream's spec names no client.

**The product level.** Owns the map, not the work: jobs, the map,
threads. One check — does every crossing land on a seam the map has —
decides whether the centre is involved. Four escalations are its whole
queue. Thread and request were modelled as types and walked end to end.

**Beliefs.** Sorted into five kinds, then found to have no place inside a
context: a context controls everything within its boundary, so there is
nothing to be wrong about except its decisions, which carry
`revisit_when`. Then removed everywhere a signal nobody reads would make
them misleading. Rule: a watch condition exists only where someone
already reads its signal.

**Consolidation.** `spec-method.md`: five parts, a learning path, twelve
use-case traces, a FAQ. Then stage-1 (capability files paired with
features), ADRs vs `decisions.md`, where vision lives, and when jobs are
introduced (on a trigger, not a schedule).

## October: the "how"

**The question.** The plugin (shopsystem-bdd, 0.18.0) and its example
(shopsystem-kb, 0.9.0) had grown. Three asks: see current and intended
state; see what work is going on and how it relates to the spec; run
work efficiently.

**The assessment.** The spec layer worked — 21 capabilities, 361
scenarios, 154 decisions with sources. The gaps were around it: nothing
said the spec was the present; the future lived in a request file, 97
delegation rulings and a 160-line backlog; a slice reached its capability
only by scenario title; reports were git-ignored. On cost: closing was
38–44% of agent time with half of task reviews clean, the controller
session read up to 55% of a batch's cache tokens, `Lands:` was wrong in
15 of 23 slices, and six plugin versions had never been measured on a
real batch. The plugin had become the product-ops system in the "how"
layer: 1,348 lines of instruction, 86 rationalization rows, 51 red flags,
none ever removed, and no spec of its own.

**Re-imagining the flow.** Vocabulary mapped to tickets: slice ≈ story,
enabling slice ≈ subtask, task ≈ the story's notes, batch ≈ sprint. Slices
had become dispatch-sizing units, not learning units. The controller was
an LLM running a scheduler loop; a pull model — items with file sets and
`blocked_by`, workers claiming from a queue, a script as supervisor —
collapsed slice, task, step and lane into one work item and dissolved
batch into scope-for-measurement and cadence-for-review. The plugin's own
spec needs no BDD suite: its rules are quality requirements verified by
`measure`.

**The item.** The brief is today's task made self-contained; the file set
is what the scout already produces, kept as names rather than counts and
used as the claim. One record filled in stages — drafted, researched,
planned, ready — each stage a pull. No slice plan; slicing drafts items.

**Rolling up.** Work rolls up to a job through threads and requests.
NFRs are guarantee capabilities; enabling work is `for:` an item. "Scope"
was introduced, then replaced by "change to a capability", then removed
when it proved to be what a merged proposal already is. Capabilities are
demanded, not scenarios; a request originates from a capability, with
the red scenario as evidence.

**Standing vs transactions.** The decisive split: standing artifacts are
the design, rewritten in place and read to learn the system; transactions
— thread, proposal, request, item — carry `needs`, leave something
standing, and are archived. The design diagram shows only what stands,
including the map. `needs` is the one intent word; `depends_on` and
`serves` are what intent becomes.

**The path of a job.** A flat `serves` loses which dependencies a job
exercises. `serves … using: [...]` keeps it per job; `depends_on` is
derived as the union; the path is the walk along `using`. `uses` and
`via` were dropped as duplicate names. `depends_on` is derived from
`serves`, not from items, because items are ephemeral.

**The language test.** A maker's shop was written in the design and read
back as sentences, one pattern per edge; eight ill-formed statements were
refused with the rule and the corrected form. Four findings: upstream
capabilities need `serves` too; external capabilities must be nameable;
a job inside one context still has a path; a thread's status is read
from its items.

**Result.** `design-model.md`, version 1.

## 14 October: the second pass

**Records.** Observations and potential future work needed a home that
was neither design nor work: records, dated and never edited. Then split
into origins (observation, measurement, review-finding), which may be
cited as a source, and history (decision-argument, initiative-archive),
which may not.

**Decisions as files.** A decision can't always be one line — it may be a
schema. The ADR's Decision section is standing; its Context, Alternatives
and Consequences are record; the summary is a required frontmatter field;
`decisions.md` is generated, never authored.

**Scoped terms.** Generic words (context, proposal, request, item, line,
transaction) were replaced by scoped ones: bounded-context,
capability-proposal / job-proposal, cross-context-request, work-item,
capability-requirement, initiative.

**Intake vs work-tracking.** Choosing what to begin is different from
following through on what was begun. The initiative became its own
artifact — the only thing in intake, the only thing with a priority and
sources — and everything done to realise it is a part with exactly one
`part_of`. A cross-context-request's fulfilment upstream is part of the
requesting initiative, not a new root; the upstream's inbound requests
are parts awaiting acceptance, not a backlog. Job-threads own no
work-items. A new job and its first thread are one initiative. The
priority-XOR-`part_of` test was replaced by the two types.

**Result.** `design-model.md`, version 2; `grammar.md` and
`ecommerce-example.md` rewritten to match.

## 15 October: requirements as first-class

The grammar had requirements as nodes while the files had them as bullets
referenced by text; the plugin's `rebind` tool existed because titles
drift. Each capability-requirement now carries a stable id, unique within
its capability and never reused; scenarios, resolutions and proposals
reference by id. A capability-proposal lists `adds`, `changes`, `removes`
by id — which is what the gate approves — and gains a `formulated` stage.
Feature files are named as containers, not artifacts; step definitions
are code and outside the model.

**Result.** version 3.

## Decisions that were made and unmade

| introduced | replaced by | why |
|---|---|---|
| delta notes, consolidation by squash | spec rewritten in place | spec is the authority; it can't be historical |
| beliefs as a statement kind | `revisit_when` on decisions; rationale on jobs | nothing to be wrong about inside a context; unread signals mislead |
| upstream cites downstream scenarios | downstream records demand; request carries it | dependency direction; second client |
| request `demanded_by` a scenario | request from a capability; scenario as evidence | capabilities are demanded |
| scope → change → (removed) | a merged proposal; items under the capability | it was already an artifact |
| release as an artifact | the contract version | already existed |
| `uses`, `via` | `depends_on`, `using` | one name per fact |
| `depends_on` from items | `depends_on` derived from `serves` | items are ephemeral; `serves` is current |
| `@uses` scenario tag | the step definition | code is the real link at that grain |
| slice, task, step, lane, batch | item; queue | execution constraints masquerading as work units |
| LLM controller | script supervisor; pull | a scheduler needs no judgment |
| transaction | initiative | clearer to outside readers; and the root is now its own artifact |
| `needed_by` | `part_of` | one execution edge, required on every part |
| priority XOR `part_of` | initiative type vs part types | a presence test is not a schema |
| request as a new root upstream | request's fulfilment as parts of the requesting initiative | all work traces to one intake item |
| job-thread → work-items | job-thread → capability-proposals → work-items | the product role never touches a work-item |
| ADR as a pure record | Decision section standing, the rest record | a decision may be a schema |
| `decisions.md` authored | generated from decision files | two authored places drift |
| generic names | scoped names | cognitive load |
| requirements referenced by text; `rebind` | stable requirement ids | links that don't drift; the gate approves ids |

## Documents

| file | what |
|---|---|
| `spec-method.md` | the September method: five parts, learning path, traces, FAQ |
| `stage-1-capabilities-and-features.md` | the first adoption step |
| `kb-and-bdd-assessment.md` | the October assessment of the plugin and kb |
| `design-model.md` | the model, version 2: standing artifacts, initiatives and parts, records, grammar |
| `grammar.md` | the grammar formally: schema, Datalog constraints, lifecycles, sentence forms |
| `ecommerce-example.md` | the model read as sentences |
| `terms-and-flow.md` | an earlier draft; retired with version 2 |
