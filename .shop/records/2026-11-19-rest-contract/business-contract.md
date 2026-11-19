# The business contract: contracts (b348) and term proposals (b42)

The domain model elements, vocabulary entries and requirement lines of this artifact, as they stand on the items
(`scripts/work show b348`, `scripts/work show b42`), copied here on 2026-11-19. The items are the source: a later
`work line` on them changes them there, not here. No word of HTTP, of a command line, of GitHub or of a file is in
any of them; those are the interface contracts' (cli-adapter.toml, http-adapter.openapi.yaml) and the decisions'.

Each line was parsed in grammar 4 (`spec parse`) on a copy of `spec/` with the model lines and vocabulary entries
laid in; the readiness bar's result on each item is in README.md.

## b348: the contracts service (a new capability `contracts`, its model in the specification area)

### contracts

narrator: the person
group: service
purpose: A bounded context's contract at one version: published from its specification, fetched by the bounded contexts downstream of it without a context request, and obtained from an upstream and kept.

#### [g1] A contract published keeps the specification at a version
- [r1] When the person publishes a contract with the `1.2.0` version, the contracts service shall keep a contract that has the `1.2.0` version.

#### [g2] A later contract supersedes the published one
- [r4] While a contract is `published`, when the person publishes a contract with the `1.3.0` version, the contracts service shall set the status of the contract to `superseded`.

#### [g4] A downstream context fetches a contract without a context request
- [r7] When a downstream context fetches a contract, the contracts service shall return the contract whose status is `published` and change nothing.

#### [g5] A contract fetched at a version never published is refused
- [r9] While no contract has the `2.0.0` version, if a downstream context fetches a contract with the `2.0.0` version, then the contracts service shall refuse the request and name the version.

#### [g6] A contract obtained from an upstream is kept
- [r10] When the person obtains a contract from a bounded context, the contracts service shall keep the contract and keep no context request.

#### [g7] A contract is not obtained from a bounded context with no channel
- [r11] If the person obtains a contract from a bounded context that has no channel, then the contracts service shall refuse the request and name the bounded context.

#### [g10] A contract at a version already published is refused
- [r14] While a contract has the `1.2.0` version, if the person publishes a contract with the `1.2.0` version, then the contracts service shall refuse the request and name the version.

#### [g11] A contract is refused while a requirement is out of the requirement grammar
- [r15] While a requirement does not conform to the requirement grammar of this bounded context, if the person publishes a contract, then the contracts service shall refuse the request and name the requirement.

#### [g12] A downstream context fetches a contract at a version
- [r16] When a downstream context fetches a contract with the `1.2.0` version, the contracts service shall return the contract that has the `1.2.0` version.

#### [g13] A contract published holds the requirements and the terms and is published
- [r17] When the person publishes a contract, the contracts service shall keep a contract whose status is `published` and keep every requirement and every term in the contract.

### specification model

```model
object contract kind of artifact
  attributes: status: published | superseded
  lifecycle status: published → superseded
  relations: describes → bounded context (one); has → version (one); holds → domain model | term | requirement | design-decision | data schema | interface contract (many)

object domain model kind of artifact
  relations: of → bounded context (one)

object data schema kind of artifact

object interface contract kind of artifact

object downstream context kind of agent

service contracts
  operation publish(contract, version) by the person
    outcomes: done → the contract | refused: version already published, requirement not in the requirement grammar
  operation fetch(contract, version) by downstream context
    outcomes: returned → the contract | refused: version not published
  operation obtain(contract, bounded context, version) by the person
    outcomes: done → the contract | refused: bounded context with no channel

event contract published: raised by contracts.publish
```

- **contract** (noun) → object contract. What a bounded context offers the bounded contexts that build on it, at one version: its domain model, its terms, its requirements, its design-decisions, its data schemas and its interface contracts.
- **domain model** (noun) → object domain model. The objects, attributes, relations, lifecycles, services and operations of a bounded context, without its rules.
- **data schema** (noun) → object data schema. The shape of a request, a response or a thing that a contract's operations pass, made from the domain model.
- **interface contract** (noun) → object interface contract. How one port asks a contract's operations and gives their outcomes: a command line's commands and exits, or HTTP's methods, paths and statuses.
- **published** (adjective) → value contract.status published.
- **superseded** (adjective) → value contract.status superseded.
- **describe** (verb, state) → relation contract.describes. A contract is the contract of one bounded context. Forms: describes, described. Frame: <contract> describes <bounded context>.
- **publish** (verb, action) → operation contracts.publish. Forms: publishes, published. Frame: <actor> publishes <contract>.
- **fetch** (verb, action) → operation contracts.fetch. Forms: fetches, fetched. Frame: <actor> fetches <contract>.
- **obtain** (verb, action) → operation contracts.obtain. Forms: obtains, obtained. Frame: <actor> obtains <contract> from <bounded context>.
- **the contracts service** (proper noun) → service contracts.
- **downstream context** (noun) → object downstream context. A bounded context that builds on the contract of this bounded context. Plural: downstream contexts.
- **status** (attribute) → attribute contract.status. Where a contract stands: `published` while it is the latest, `superseded` once a later one is published.

## b42: term proposals on a context request (capability `context-requests`, its model in the tracking area)

A term proposal is a kind of request line, so the lines the context requests service already has for a request line
(settled with a line outcome, countered by a rewritten one, refused with a line reason, every line settled before the
request is accepted: context-requests#r1-r3, r8, r23-r28) hold for it unchanged; the new lines say only what is new.


### context-requests

#### [g51] A term proposal suggested is kept on its context request
- [r51] When the person suggests a term proposal for a context request, the context requests service shall keep a context request that holds the term proposal and keep an entry on the context request.

#### [g53] An accepted term proposal brings its term into the item
- [r54] While a context request holds a term proposal whose line outcome is `accepted`, when the person accepts the context request, the context requests service shall keep an item that holds every term that the term proposal concerns.

#### [g54] A term proposal out of the asker's turn is refused
- [r55] While a context request is `awaiting-upstream`, if the person suggests a term proposal for the context request, then the context requests service shall refuse the request and name the context request.

#### [g55] A term proposal out of the vocabulary-entry form is refused
- [r56] If the person suggests a term proposal that does not conform to the vocabulary-entry form, then the context requests service shall refuse the request and name the term proposal.

### tracking model

```model
object term proposal kind of request line
  relations: concerns → term (many)

object vocabulary-entry form kind of artifact

service context requests
  operation suggest(context request, term proposal) by the person
    outcomes: done → the term proposal | refused: term proposal not in the vocabulary-entry form, context request not this side's turn
```

- **term proposal** (noun) → object term proposal. A request line that proposes a term, with the model elements the term names, for the upstream to take into its own vocabulary in its own words.
- **suggest** (verb, action) → operation context requests.suggest. Forms: suggests, suggested. Frame: <actor> suggests <term proposal>. Frame: <actor> suggests <term proposal> for <context request>.
- **the vocabulary-entry form** (proper noun) → object vocabulary-entry form. A bullet `- **<word>** (<part of speech>) → <model element>. <definition>`, with the model lines that declare the element when the upstream has none.
- **concern** (verb, state) → relation term proposal.concerns. A term proposal is about a term: the term it adds, or the term whose entry it changes. Forms: concerns, concerned. Frame: <term proposal> concerns <term>.
