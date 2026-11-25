---
id: model/missingmass.io/shopsystem/shopsystem-bdd/specification
area: specification
kind: core
imports: []
---

# The specification

## Purpose

The bounded context's specification: its domain model, vocabulary, requirements and decisions, how a line is read and checked, the scenarios generated from its requirements, and the records kept beside it.

```model
object bounded context
  relations: has → job | fact | index file | requirement grammar | channel (many); holds → upstream entry | term (many)
  relations: has → contract (many)

object capability kind of file
  attributes: group: service | guarantees | model | operations; language: codified-1 | codified-2
  relations: has → section | requirement | feature | requirement group | Behaviour line (many); holds → requirement id | count | order | given block (many)

object requirement kind of text
  relations: has → precondition | trigger | logical form | consequence | parse | compiled grammar | translation | response | act | restriction | upper bound | requirement id (many); omits → requirement (many); allows → act (many); oblige → requirement (many); overrides → requirement (many); adds → consequence (many); permits → act (many); retires → requirement id (many); uses → construct | rule (many)
  relations: governs → operation (many)
  relations: has → ambiguous text | plural object (many)
  relations: supports → requirement id (many)
  relations: has → requester (many)

object requirement group
  relations: has → requirement | scenario (many)
  relations: has → group title (one)

object universal condition kind of text
  relations: has → universal condition id | translation (many); entails → step (many)

object term
  attributes: part of speech: noun | verb | adjective | attribute | proper noun | artifact; aspect: state | action
  relations: has → subject | object | recipient | frame | sense | noun phrase | value order (many); redefines → pack (many); agrees with → subject (many)
  relations: means → element (one)

object design-decision kind of file
  attributes: status: proposed | accepted | rejected | superseded; tier: check | requirement | judgement
  relations: supersedes → design-decision (many); has → route | index entry | section | id (many); holds → qualifier (many); supersedes (supersede) → design-decision (many); verifies → universal condition (many)
  relations: has → enforcer | foundation (many)

object feature kind of file
  relations: has → scenario | step (many); holds → scenario (many)

object scenario kind of text
  relations: has → capability | tag | requirement tag | scenario title | replacement | counter-example | boundary | order counter-example | step (many); refers to → requirement id (many); satisfies → precondition (many); succeeds in → workspace (many); breaks in → workspace (many)

object step kind of text
  relations: has → handler (many); asserts → act (many)

object fact

object file kind of text
  relations: holds → finding (many)

object version kind of text

object text
  relations: forbids → act (many); contains → text (many); precedes → act (many); follows → act (many); introduces → instance (many); mentions → text (many); identifies → bounded context (many)
  relations: denotes → node | item | batch (many)

object test
  attributes: verdict: passed | failed
  relations: executes → function (many); enforces → design-decision (many)

object violation

object record kind of file
  relations: concerns → node | item | batch (one)

object route kind of text
  attributes: kind: scenario | check | judgement | monitor

object rule
  relations: has → catalogue entry (many)
  attributes: severity: error | warning

object decisions index kind of file
  relations: holds → index entry (many); lacks → index entry (many)

object rule catalogue kind of file
  relations: holds → catalogue entry (many)

object interpreter
  relations: imports → interpreter (many)

object file form
  attributes: writer: command | item | hand

object pack kind of file
  relations: has → term (many)

object logical form kind of text
  relations: holds → value in use (many)

object verb kind of term

object frame kind of text
  relations: has → preposition (many); takes → noun phrase (many)

object subject

object object

object recipient

object preposition

object job

object index entry kind of text

object catalogue entry kind of text
  relations: has → purpose (many)

object section kind of text
  attributes: heading: Purpose | Terms | Relations | Behaviour | Context | Decision | Consequences

object id kind of text

object precondition kind of text
  relations: has → comparison (many); holds → count (many)

object trigger kind of text

object noun phrase

object passive form
  relations: has → by-phrase (many)

object by-phrase

object sense kind of text
  relations: has → value order (many)

object definite noun phrase kind of noun phrase
  relations: has → antecedent (many)

object antecedent

object negated indefinite

object fragment kind of text

object code
  relations: unifies → code (many)

object act
  relations: holds → order (many); brings in → referent (many)

object consequence

object perfect

object count
  relations: has → boundary (many); contradicts → count (many)

object clock trigger

object number
  relations: has → unit (many)

object unit

object refusal

object corpus kind of file
  relations: holds → requirement | logical form (many)

object parse cache kind of file
  relations: holds → parse (many)

object compiled grammar kind of file

object parse kind of text

object translation

object comparison

object value order

object order
  relations: on → term (many)

object response kind of text

object closing comma

object construct catalogue kind of file
  relations: holds → catalogue entry (many)

object referent
  relations: has → description (many)
  relations: has → instance (one)

object description kind of text

object restriction kind of text

object upper bound

object counter-example kind of text

object given step kind of step

object instance

object boundary

object order counter-example kind of text

object repository
  attributes: release: 0.23.1 < 0.24.0 < 0.25.0 < 0.29.0 < 0.30.0 < 0.31.0 < 0.32.0 < 0.32.1 < 0.33.0 < 0.34.0 < 0.34.1 < 0.99.0; store: taking | rejecting
  relations: holds → old-layout directory | uncommitted change (many); has → decision ledger | plugin version file | shop directory | capability | decisions index | frozen notice | initiative (many); rejects → kept change (many)
  relations: has → context scaffold (one)
  relations: has → scenario conftest (one)
  relations: has → ignore file (one)

object construct
  relations: has → catalogue entry (many)

object language reference kind of artifact

object clingo

object final layout kind of artifact

object request form kind of artifact

object entry form kind of artifact

object capability id form kind of artifact

object feature form kind of artifact

object node id form kind of artifact

object L1

object L7

object L8

object no findings kind of text

object specification
service language
  operation parse(text, logical form (flag))
    outcomes: returned → the reading | refused: requirement not in the language, requirement of more than one logical form, reading rule broken, construct with no catalogue entry, fragment
  operation explain(text)  outcomes: returned | refused: requirement id of no requirement
  operation look up(pack)  outcomes: returned → every term of the pack
  operation preview(text, item, logical form (flag))
    outcomes: returned → the reading | refused: requirement not in the language

service specification
  operation check(specification, capability)  outcomes: passed → findings | failed → findings, an interpreter without clingo | refused: capability not in the language
  operation examine(specification, capability)  outcomes: passed → logic findings | failed → logic findings
  operation consult(rule catalogue)  outcomes: returned → every rule
  operation renew(rule catalogue, audit (flag))  outcomes: done | failed → the stale rule catalogue
  operation inventory(specification, audit (flag))  outcomes: returned → every file form | failed → each form written by hand
  operation translate(specification)  outcomes: returned → every fact
  operation annotate(adapter contract, audit (flag))  outcomes: done → the adapter contract | failed → each stale adapter contract
  operation describe(catalogue entry, purpose, item)
    outcomes: done → the catalogue entry | refused: catalogue entry of no rule or construct
  operation prepare(contract)  outcomes: returned → the contract
  operation publish(contract, version) by the person
    outcomes: done → the contract | refused: version already published, requirement not in the language
  operation fetch(contract, version) by downstream context
    outcomes: returned → the contract | refused: version not published
  operation obtain(contract, bounded context, version) by the person
    outcomes: done → the contract | refused: bounded context with no contract

service decisions
  operation enter(design-decision, title, summary, tier, wording, route, supersedes)
    outcomes: done → the design-decision | refused: no tier, no summary, no wording, design-decision not in force
  operation rebuild(decisions index, audit (flag))  outcomes: done | failed → each failing design-decision
  operation amend(design-decision, enforcer, foundation)
    outcomes: done → the design-decision | refused: design-decision not in force

service records
  operation file(record, title, summary, text)  outcomes: done → the record | refused: text not a node id
  operation file design(design, title, summary)  outcomes: done → the design
  operation file plan(plan, design, title)  outcomes: done → the plan | refused: design that does not exist
  operation file observation(observation, summary)  outcomes: done → the observation

service scenarios
  operation generate(feature, capability, audit (flag))  outcomes: done → the feature | failed → each stale feature
  operation audit(feature)  outcomes: passed | failed → each step with no handler

object adapter contract kind of file
  relations: holds → operation (many)
  relations: holds → operation table (many)

object operation
  relations: holds → requirement (many)
  relations: makes → referent (many)
  relations: has → operation table (one)
  relations: has → property (many)

object reading rule kind of rule

object collection
  relations: has → member (many)

object member
  relations: has → order (many)

object purpose kind of text

object release kind of text

object ambiguous text kind of text

object plural object kind of noun phrase

object when step kind of step

object value in use kind of text

object enforcer kind of text

object foundation kind of text

object operation table kind of text
  relations: names → operation (one)

object node

object design kind of file
  relations: holds → plan (many)

object plan kind of file

object element

object contract kind of artifact
  relations: holds → operation | property | requirement (many)
  attributes: status: published | superseded
  lifecycle status: published → superseded
  relations: has → version (one); holds → term | design-decision (many)

object contract form kind of artifact

object property kind of text
  relations: refers to → operation (many)

object area
  attributes: kind: core | supporting | generic | port
  relations: holds → operation | capability (many)

object group title kind of text

object requester

object downstream context kind of agent

event contract published: raised by specification.publish
```
