---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-24-contracts-between-bounded-contexts-and-adapter-specs
kind: design
about: item/missingmass.io/shopsystem/shopsystem-bdd/b540
date: 2026-11-24
---

# Contracts between bounded contexts and adapter specs

A design for contracts between bounded contexts and for port adapters as adapter specs (b540), drawn from three worked examples:
- `2026-11-23-a-worked-example-of-contracts-between-bounded-contexts-ordering-over-inventory-and-payments.md` (record 1)
- `2026-11-23-a-reworked-example-of-contracts-between-bounded-contexts-port-contracts-and-swapped-providers.md` (record 2)
- `2026-11-24-a-worked-example-of-port-adapters-as-adapter-specs-realisation-lines-and-entailment.md` (record 3)

It supersedes the plan of `2026-11-21-a-plan-to-publish-contracts-between-bounded-contexts.md`. Status: a draft for the person's review; no decision or item is filed from it yet.

## Summary

- **Shape.** Each driven port is an area of the downstream's own model, and its port contract is a capability. Each adapter is a nested context under `adapters/<port>-<provider>/`, with its own spec where three vocabularies meet: the port's (read from the parent), the provider's (a pinned published contract, or an assumed description) and technical words. Mechanisms go in the adapter's `adr/`. The trace, the realises result and drafted requests are derived, never written by hand.
- **Ten design-decisions** (D1-D10).
- **Two tracks.** The language track (L-1 to L-9) is changes for every context; state invariants is L-4, b542. The contract and adapter track (C-1 to C-13) is plugin and layout work.
- **First slice:** an adapter spec over an internal upstream whose realises check names a gap and drafts the request. It needs L-1, L-2, C-1, C-3, C-5, C-6, L-3, C-7 and C-8. It does not need b348's publish/obtain, since a hand-placed pinned contract is enough, nor L-4.
- **Out of scope:** choreographed sagas between peers, architecture description languages (b541), and consumer-driven contract checking.

## 1. Standing decisions this design builds on

- A downstream keeps its own terms and never imports an upstream's vocabulary into its core (quote-71).
- The core orchestrates, sagas included.
- The port contract is the downstream's and is bounded by the core.
- An adapter is code, bound by conformance tests generated from the port contract.
- The core is tested against a stub generated from the port contract.
- The upstream owns its contract's detail.
- Adapter specs: one nested context per adapter (quote-75).
- State invariants are a language change for every context (quote-74, b542).

## 2. Concepts, names and layout

| concept | what it is | where it lives |
|---|---|---|
| core | the context's business areas and capabilities | `spec/model/<area>.md` (`kind: core`), `spec/capabilities/` |
| driven port | an area of kind `port` in the downstream's model: operations, outcomes and things in the downstream's words | `spec/model/<port>.md`, `spec/vocabulary/<port>.md` |
| port contract | a capability in the port's area, narrated by the core's service; each line is a guarantee a core line stands on and carries `Relied on by: <ids>` | `spec/capabilities/<port>-port.md` |
| published contract | what an upstream publishes at a version, in its own words: operations, parameters, outcomes and reasons, governing requirements, events and the properties below | the upstream, where b348 keeps it; proposed `.shop/contracts/<version>/contract.toml` |
| adapter spec | a nested context of kind `adapter` realising one port over one or more providers | `adapters/<port>-<provider>/` |
| provider | a pinned published contract (sibling context), or a provider description written by the adapter's owners in the provider's words and marked `assumed` (third party, legacy) | `adapters/…/provider/<upstream>/<version>/contract.toml`, or the provider area and capabilities with `assumed: true` |
| realisation lines | the adapter's own requirement lines, in port, provider and technical words | `adapters/…/spec/capabilities/realisation.md` |
| adapter entry | the adapter-owned object joining port things to provider things (its store) | `adapters/…/spec/model/adapter.md` |
| adapter decision | strategy, store, retry, transport: mechanisms | `adapters/…/adr/NNNN-<slug>.md` |
| trace | which provider operations each port operation uses, read off the realisation lines | derived by `spec trace`, not kept |
| realises result | for each port line: realised, with its chain of premises, or not, with the provider line where the chain stops | derived by `spec logic` or `spec realises` |
| drafted request | a request to the upstream for a gap, in the upstream's words, for the person to send | derived, then raised with `work request` |
| core stub, provider stub | generated fakes: the port for the core's scenarios, the provider for the adapter's realisation scenarios | generated into the test tree |
| conformance tests | the port contract's scenarios, run against each adapter with its provider | `features/<port>-port.feature`, run per adapter |

The layout of a downstream:

```text
spec/index.md                        composition: core areas, port areas (kind port)
spec/model/{orders,stock}.md         stock.md: kind: port
spec/vocabulary/{orders,stock}.md
spec/capabilities/{placing,…}.md     core
spec/capabilities/stock-port.md      port contract (Relied on by: on each line)
spec/adapters/cli.toml               driving adapter, unchanged
features/                            core scenarios + port conformance scenarios
adapters/stock-inventory/
  spec/index.md                      kind: adapter; realises: [stock-port#r1, …]; providers: [context@1.4.0]
  spec/model/{provider,adapter}.md   the port area and port capability read from the parent at its commit, never copied
  spec/vocabulary/{provider,adapter}.md   provider.md carries renames: (product → stocked product)
  spec/capabilities/{realisation,holding}.md   holding: generated from the pinned contract
  provider/inventory/1.4.0/contract.toml       pinned, obtained, read-only
  adr/0001-strategy.md …
  features/                          realisation and provider scenarios
adapters/stock-ledger/               the same shape; provider area and lines written by hand, assumed: true
```

The adapter's code lives wherever the project keeps code; the adapter spec says nothing about where.

A published contract and a port model must carry these properties (record 1 §a, record 2 §4):
- `idempotent by <parameter>`;
- `compensated by <operation>`;
- `followed by <event>`;
- for an event, its `delivery` (at least once, in order, within a time) and `when`.

They are written on the operation or event line of a `model` block and carried into `contract.toml`.

## 3. Design-decisions to write with `work decision`

| # | title | summary | tier | decision |
|---|---|---|---|---|
| D1 | The downstream keeps its terms behind a driven port | The core reads no upstream word; each upstream is reached through a port area in the downstream's own words. | check | A core area never imports a provider area or an upstream's vocabulary; each upstream is reached through a driven port, an area of kind `port`, whose words are the downstream's; v_m1 and the bound check refuse a core line using a word only a provider or adapter layer gives. |
| D2 | The core orchestrates and an adapter never decides business | Every step with a business outcome (refuse, retry for the business, compensate, wait) is a core line; an adapter only translates and carries. | judgement | Sagas are core lines over the core's own lifecycle. An adapter may emulate (a hold record, a timer, a dedupe store). It never chooses an outcome the port does not declare and never compensates on its own account. When the provider cannot answer, it fails as broken, never as refused. A reviewer checks each realisation line and adapter decision against this. |
| D3 | The port contract is the downstream's and bounded by the core | A port holds only what core lines use, and each port line names the core lines that rely on it. | check | The bound check reports three findings: a port operation no core line requests; a port outcome that no core line handles and no port line excludes; and a port line whose `Relied on by:` names no core line requesting that port. |
| D4 | An adapter is a nested context with its own spec | Each adapter is `adapters/<port>-<provider>/`, a context of kind `adapter` with its own grammar, where the port's, the provider's and technical words meet. | requirement | Its id is the parent's id with `/adapter/<name>`. It reads the parent's port area and port contract at the parent's commit, and holds its providers, realisation lines and `adr/`. It is never an area of the parent's model. |
| D5 | The upstream owns its contract's detail | A downstream obtains a published contract pinned at a version and never edits it; what it needs and cannot map becomes a request. | requirement | `provider/<upstream>/<version>/` is written only by obtaining, and a change to it in any other commit is refused. A gap the realises check finds is raised as `work request` to the upstream, in the upstream's words, for the upstream to reword. |
| D6 | Satisfiable is entailment over realisation and provider lines | A port line is satisfied when the realisation lines and the provider's lines together entail it, following each request the adapter makes. | check | The realises check runs entailment with request-following premises. A port line in `realises:` that is not entailed is a finding naming the provider line where the chain stops. One entailed by realisation lines alone, with no provider premise behind a provider request, is reported as "claimed, not backed". |
| D7 | Mechanisms live in adapter ADRs | Transport, retry, stores, timers, webhooks and polling are decided in an adapter's `adr/`, never in a core or port line. | judgement | A core or port contract line names no transport, protocol, product name or storage. An adapter's realisation lines may name its own technical things (entry, deadline); how they are kept is an ADR. |
| D8 | Conformance tests bind an adapter; the trace never does | An adapter is accepted by passing the port contract's scenarios with its provider; its trace is evidence and impact analysis only. | requirement | Every adapter of a port runs the same conformance scenarios. No declarative operation mapping binds an adapter: record 1's `stock.toml` form is not adopted (record 2 §6). |
| D9 | Assumed provider lines are evidence only when run | A provider description that is not a published contract is checked only by running its scenarios against the provider, on a schedule. | judgement | Static checks over assumed lines show only that the adapter is consistent with what its owners believe. Every assumed line has a scenario; its schedule and target (sandbox, staging) are an adapter ADR. |
| D10 | A port's outcomes are told apart by the core's statuses | A reply's meaning for a saga is told by the core's status, not by the reply. | check | Each core line triggered by a port outcome is guarded by a status of the saga object; two lines on one port outcome in one status are an L1, which `spec logic` already catches (record 1 §f, v1). |

## 4. Language track (every context)

★ marks an item of the first slice.

| id | title | what it is | size | depends on | order |
|---|---|---|---|---|---|
| L-1 ★ | A response can make a request with its parameters | A response act whose verb names an operation of another service is read as `request(e, O, …)` with `param`/`noparam`, using the trigger's Params syntax ("hold the stocked product of the entry with the quantity of the order and the number of the order as the reference"). Today it does not parse at `with` (records 1 §g, 3 §2). Requester facts then count it, which fixes v_m7 for ports (record 1 §g). A core line triggered on that request's refusal counts as stating its reasons, which fixes v_m4. It gives the trace directly and absorbs b363's `as_events`. | L | — | 1 |
| L-2 ★ | One actor across two vocabularies | Entries in different layers naming one element are one referent in the logical form and the facts. Today "the client" aliased to `service stock` stays its own constant (record 3, variant client-alias). It is needed so that a provider line on "the client holds …" applies to the adapter's request. | M | — | 1 |
| L-3 ★ | Entailment follows a request | `entail.lp` gains a stratum. A premise's act requesting operation O fires the lines whose trigger is a request of O by that requester (via L-2), and their outcomes (complete, refuse, return, notify on the request's thing) fire the lines triggered on them. The depth is bounded, and the chain of premises is kept so findings can print it. Today premises are only lines on the query's own trigger, so no provider line is ever a premise (record 3 §3). | L | L-1, L-2 | 2 |
| L-4 | State invariants (b542) | A line stating what always holds between two states ("an order has an entry exactly when a reservation for the order exists"). `check.lp` reads it as a constraint on worlds and `entail.lp` as a premise; scenarios check it after each step. It removes the store-against-port L1s of record 3 §3. Its own construct design goes under b542. | L | — | 2 |
| L-5 | Saga checks | Logic over a context's lifecycle and lines (`check.lp`/`model.lp`), so it belongs in this track:<br>• every outcome handled per status: each status an object can be in while a request is outstanding, times the request's outcomes, needs a line (record 1 §h.2);<br>• compensation coverage: an end status reached after a request with `compensated by` completed, without the compensating request (record 1 §f, v4);<br>• the lifecycle terminates: a non-final status with no line out that no single party can withhold forever is a warning (record 2 G6). | L | L-1, C-1's properties, C-3 | 3 |
| L-6 | An outcome trigger naming its request | Not needed now. Status guards (D10) and a port's thing being `kind of request` already tell outcomes apart (record 1 §h.1, record 3 §2). Reopen if two requests on one thing can be outstanding in one status. | S | — | later |
| L-7 | notify with a clause ("notifies … that an allocation lapses") | Noted only. "notify … of a thing whose state is v" says it (records 1 §g, 3 §2). | — | — | — |
| L-8 | A relation declared by a third area | Not adopted. The adapter's own entry object, its store, is the right place for correspondences (record 3 §2). | — | — | — |
| L-9 | Copying values and arithmetic | Noted only. Without it a provider line can say "keeps the line" but not "the units fall by the amount", so provider lines entail less and conformance carries more (record 3 §2). A later language item. | — | — | — |

Small fixes found on the way, each a small item of its own:
- `v_t13` refuses a frame that the grammar accepts ("reserves stock for <order>", record 1 §g).
- "the charge" in a response binds the trigger's new charge rather than the While's (record 2 §1).

## 5. Contract and adapter track

★ marks an item of the first slice.

| id | title | what it is | size | depends on | order |
|---|---|---|---|---|---|
| C-1 ★ | A contract says how its operations behave | The published contract form, `contract.toml`: objects; operations with parameters, outcomes and reasons; governing requirements, as `spec annotate` gathers them; events; and the properties idempotent, compensated by, followed by and delivery, written in the `model` block (record 1 §a). | M | — | 1 |
| C-2 | A context publishes its contract; a downstream obtains it (b348) | b348's r1-r17 as they stand: publish at a version, supersede, fetch without a context request, obtain and keep, refuse unknown versions. Obtaining writes `provider/<upstream>/<version>/` in an adapter spec. | L | C-1 | 3 |
| C-3 ★ | A port is an area and its needs are lines | An area kind `port`, and a port contract capability whose lines carry `Relied on by:`. Port operations are left out of v_a1 (the CLI's tables) and counted by v_m7 through L-1 or port lines (record 2 §1). | M | — | 1 |
| C-4 | The core bounds its ports | The bound check, both ways:<br>• the mechanical part: an outcome no core line handles must be excluded by a port line;<br>• the citation part: `Relied on by:` names lines that request the port;<br>• an unused port operation;<br>• a port line no core line relies on (record 2 §1). | M | C-3, L-1 | 2 |
| C-5 ★ | An adapter is a context of its own (b540) | Index `kind: adapter`; a nested id form (refused today, record 3 §7); `realises:` and `providers:` read; `adr/` and `provider/` accepted by the layout check; the port area and port capability read from the parent at its commit. | L | C-3 | 2 |
| C-6 ★ | An adapter speaks its provider's words | A pinned contract becomes a provider area and provider capabilities, with a rename map applied to element ids and words where they clash (record 3 §2: `product` refused twice, `units`). An assumed description is written by hand, with `assumed: true`. | M | C-1, C-5 | 2 |
| C-7 ★ | An adapter shows each port line is met | The realises check: each `realises:` id is entailed (L-3) by the realisation and provider lines, and printed with its chain. Its results are entailed, "not realised", or "claimed, not backed", the last naming the provider line where the chain stops. On record 3's adapters it should name holding#r9 for stock-port#r5. | M | L-1, L-2, L-3, C-5, C-6 | 3 |
| C-8 ★ | A gap becomes a request to the upstream | From a chain stopping at a provider line, a drafted request: the need in the port's words, and a proposed line in the upstream's words (the rename map applied in reverse). It is shown to the person and sent only with `work request`. A missing word travels as one of b42's term proposals. | S | C-7 | 4 |
| C-9 | An upstream's change names what it touches | `spec trace`, read off the realisation lines' request atoms (record 3 §4 did it with a 25-line script). An impact check diffing two pinned contract versions follows: provider operations, then realisation lines, then port lines, then core lines through `Relied on by:` (record 2 §6). | M | L-1, C-3, C-5, C-6 | 4 |
| C-10 | Stubs from contracts | The core's stub, generated from the port model and port contract: it records requests, replies only with allowed outcomes, refuses excluded replies and keeps idempotency (record 1 §d, record 2 §1). The adapter's provider stub, generated from the provider area and lines. Builds on b426's core driver. | L | C-3, C-6, b426 | 4 |
| C-11 | Every adapter of a port passes the same tests | Port conformance scenarios run per adapter, with adapter step handlers. Assumed provider scenarios run against a sandbox or staging on a schedule; the schedule and target are an ADR (D9). Results are kept as records of runs. | L | C-5, C-10 | 5 |
| C-12 | Docs and a two-context example | A reference page, and in `docs/examples/` ordering, inventory and one nested adapter, checked by the docs test. | M | C-7 at least | 5 |
| C-13 | Grammars stay affordable with nested contexts | Each adapter spec compiles its own grammar, so b447 (a narrow parse key) and b350 (bounded caches) matter more. An ordering note on those items, not new work. | — | — | — |

**The first slice.** "An adapter spec over an internal upstream whose realises check names a gap and drafts the request" needs L-1, L-2, C-1, C-3, C-5, C-6, L-3, C-7 and C-8.
- It does not need C-2 (b348): a hand-placed pinned `contract.toml` in C-1's form is enough.
- It needs L-3: without it the gap shows only as a missing L8 and cannot name holding#r9 (record 3 §3).
- It does not need L-4: until b542 lands, the slice shows the store-against-port L1 as a known finding.

**The order:**
1. L-1, L-2, C-1, C-3
2. L-3, L-4, C-4, C-5, C-6
3. L-5, C-7, C-2
4. C-8, C-9, C-10
5. C-11, C-12

## 6. Existing backlog items

| item | action | reason |
|---|---|---|
| b28 Tell another context what this context can do | withdraw into b348 | its decision (publish a contract of what exists today, quote-39) is b348's r1-r17 |
| b348 contracts | use as C-2 | its model already keeps requirements, terms, data schemas and interface contracts; C-1 adds the properties |
| b42 term proposals (delivered) | use as is | C-8's missing words travel as term proposals |
| b13 an item proposes a new capability or term | keep, unaffected | it is about this context's own items |
| b355 operation tables (delivered) | none | the CLI driving adapter is unchanged; upstream adapters get no declarative tables (D8) |
| b357 the envelope on every command | keep, independent | driving-adapter work |
| b358 handlers keyed on operations | keep, independent | helps C-10's scenarios, no dependency |
| b366 data schemas and OpenAPI | keep | attaches later to a published contract as its data schema and interface contract |
| b380 unlay re-annotates the adapter contract | keep, independent | a bug of the CLI contract's lay |
| b426 a core driver in process | use as C-10's dependency | the core's scenarios run in process against the generated port stub |
| b445 (delivered) | none | — |
| b363 stale text and dead code | split | L-1 absorbs `spec_lf_request.as_events`; the rest stays in b363 |
| b540 a port adapter's design artifact | use as C-5, the parent of C-6 to C-9 | its note is this design's request (quote-72) |
| b541 architecture description languages | out of scope | §7 |
| b542 state invariants | use as L-4 | quote-74 |
| b351 parsing after term changes | already withdrawn | b447 carries the work |
| b447 a narrow parse key | keep, noted under C-13 | nested contexts multiply grammars |
| b350 / b446 caches | b446 already withdrawn; keep b350, noted under C-13 | — |

## 7. Out of scope

- **Choreographed sagas between peers.** With no orchestrating core there are no core lines to bound a port (D3), and no single context to run the saga checks. A later design may model a choreography as a context of its own.
- **Architecture description languages (b541).** They would attach later as a derived view, exported to an ADL: each adapter spec a component, its trace the relationships, its ADRs the decisions. Nothing here depends on them.
- **Consumer-driven contract checking.** The upstream owns its contract (D5), downstream needs reach it as requests, and the impact check runs on the downstream's side (C-9). An upstream running its downstreams' realisation lines before it publishes is a possible later item.

## 8. Risks and open questions

Risks:
- **L-3's grounding cost.** Request-following premises could slow `spec logic`. Bound the depth, keep the chunked solve, and measure on record 3's adapters before widening.
- **L-2's identity across layers applies to every context.** Two words for one element become one actor wherever layers differ, and v_t20 guards only within a layer.
- **Rename-map fidelity.** Substituting words into an upstream's lines could change their meaning. Check that each renamed line parses to the same tree shape as the original does in the provider's own grammar.
- **Port drift.** An adapter reads the parent's port at a commit, so a port change must flag every adapter spec whose `realises:` no longer matches.
- **Weak provider lines.** Without values or arithmetic (L-9), static entailment proves less, and conformance stays the main evidence (D8).
- **Third-party providers have no static evidence.** Sandbox availability and cost are each adapter's risk, recorded in its ADR.

Open questions:
- Must every port line carry `Relied on by:`, or only the lines the mechanical bound check cannot see (record 2 §1)?
- Should the core stub produce "may" outcomes on its own, or only when a scenario asks for them (record 1 §d)?
- Should a port verb used as a state ("the stock service shall free the reservation", record 3 §4) get its own word in port contracts?
- Where does a downstream record which adapter is wired in for a deployment: a context-level ADR, or configuration?

The example context's business questions are not plugin work (record 2 §4): G3 (a card declined after confirmation), G6 (how long a held order holds stock), G7 (availability with a ledger that cannot be read), G9 (disputes and chargebacks after `paid`).
