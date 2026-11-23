---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-23-a-worked-example-of-contracts-between-bounded-contexts-ordering-over-inventory-and-payments
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-23
---

# A worked example of contracts between bounded contexts: ordering over inventory and payments

The person asked for a fully worked example before committing to the contracts design (2026-11-23, after deciding that a downstream keeps its own terms, quote-71). The design under test: the downstream's core orchestrates (sagas included) in its own lines; a driven port, an area of the downstream's model, only translates and faces one upstream; an adapter contract `spec/adapters/<port>.toml` of a new kind `upstream` maps port operations onto an upstream's published contract, read-only under `spec/upstreams/<id>/<version>/`; the upstream owns its contract's detail. The question it had to answer: does the downstream need lines for the driven port that mirror the upstream's contract?

Every claim about the plugin's tools is marked **[run]** (main's `scripts/spec` and `scripts/features` run on the contexts in this record's folder, 2026-11-23) or **[paper]** (worked by hand: a proposal, or an inference no tool checks today). The supporting contexts are in the folder of the same name beside this record: `inventory/`, `payments/` (upstreams), `ordering/` (downstream, with `spec/upstreams/` and `spec/adapters/{cli,stock,charges}.toml`), `variants/v1..v5/` (ordering broken or extended one way each) and `placing.form.txt` (`spec parse --form` of every placing line).

## Answer in brief

- **No port lines are needed** (confirmed, with corrections). Ordering's port areas have no capabilities; every port operation is requested by a core line and every port outcome the core reacts to is a core trigger. The projection (the upstream's lines for the mapped operations, translated) written out as lines parses in ordering's grammar today (12/12) and makes `spec logic` find nothing new [run]: it is derivable, so writing it by hand is duplication.
- **Correction 1:** the projection is mostly "may", not "shall": an upstream refusal's condition is usually in the upstream's terms (inventory's `supply`), so only its outcome survives translation.
- **Correction 2:** correlating a reply to its request is the core's job, done by the saga's status. One reply phrase answers both `reserve` and `take`; take the While out of placing#r7 and `spec logic` reports L1 r3/r7 [run].
- **Today's checks push towards mirroring** [run]: `v_m7` flags all 7 port operations and `v_m4` all 3 port refusal reasons, since only a trigger counts as a request; adding the projection as lines makes `v_m7` go away.
- **Today's tools cannot tell the broken variants apart** [run]: an unhandled refusal gives the same `v_m4` as the correct context, an unused port op is listed among the used ones, a missing compensation passes silently.
- **The first saga draft needed a refund payments does not have**; taking stock before collecting the charge made every failure compensable. A saga check should find this.
- **Async races and at-least-once delivery are real, and nothing checks them.**

## a. The files

**inventory** (upstream). Model: `allocation` (quantity, reference; lifecycle `placed → consumed | released | lapsed`); operations `hold(product, quantity, reference, warehouse)` by the client, refused `product out of stock`, `no quantity`; `release` (refused `consumed allocation`), `consume` (refused `lapsed allocation`), `query(product)`, `lapse` (by the clock), and `restock`, `transfer`, `audit` (by the stock keeper); event `an allocation lapses`. Lines (all parse [run]): holding#r1 "When the client holds a product with a quantity and a reference, the inventory service shall keep an allocation on the product."; holding#r2 the same reference returns the allocation and changes nothing (idempotency stated); r3 refused when the product's supply is `exhausted`; r4 without a quantity; r5-r8 release and consume; r9 "When the clock lapses an allocation whose status is `placed`, the inventory service shall set the status of the allocation to `lapsed` and notify the client of the allocation."; r10 query; stockkeeping#r1-r4.

**payments** (upstream). `authorise(card, amount, currency: EUR|USD|GBP, reference)` refused `card declined`, `amount over limit`; `capture` (refused `voided authorisation`), `void` (refused `captured authorisation`), `settle` and `reverse` by the network (async outcomes), `disburse`, `contest` (by the cardholder), `resolve`. charging#r1-r9, payouts#r1-r3 parse [run]; r8, r9 the network's settle and reverse, notifying the merchant.

Upstream checks [run]: inventory `spec check` 0 violations, 0 warnings; payments 0 violations, 2 warnings (`w_example` 10000, `w_value_kind` currency); `spec logic` nothing on either; `spec annotate` filled every cli operation table with its governing requirements (b368's mechanism).

**Published contracts** [paper: form proposed] (`ordering/spec/upstreams/...`): adapter-neutral, in the upstream's words; per operation `by`, `parameters`, `outcomes`, `requirements` (exactly what `spec annotate` gathers), plus what today's model cannot say: `idempotent`, `compensated-by`, `followed-by`, `reply` (sync/async, time limit), `limits`; `[events.*]` with `delivery`, `when` (e.g. `an allocation lapses`: async, at least once, 15 minutes after the hold). Operations of the upstream's own actors (clock, network, cardholder) are published as events only.

**ordering** (downstream). Composition: core area `orders` (`placing`, `withdrawing`, `browsing`); port areas `stock`, `charges`, no capabilities. Core model: `order` (quantity, number, card, total; lifecycle `placed → held | rejected`, `held → charged | cancelled | withdrawn | expired`, `charged → confirmed | expired`, `confirmed → paid | unpaid`); `place(product, quantity, card)` (refused `no quantity`), `withdraw(order)` (refused `confirmed order`), `view(product)`, by the shopper. Port models in ordering's words: stock `object reservation kind of request` (state made | lapsed, `for → order`), `reserve(order)` done → the reservation | refused `order out of stock`, `free(reservation)`, `take(reservation)` (refused `lapsed reservation`), `count(product)` → availability; charges `object charge kind of request` (state settled | bounced), `secure(order)` (refused `charge declined`), `cancel(charge)`, `collect(charge)` (notifies → the charge). Declaring a port's request object `kind of request` is what lets "the stock service refuses a reservation for the order" parse with the pack's `refuse` frame [run].

The saga, placing (all parse [run]):
- r1 When the shopper places an order with a product and a quantity and a card, the ordering service shall keep the order and reserve stock for the order.
- r2 refused without a quantity.
- r3 While the status of an order is `placed`, when the stock service completes a reservation for the order → `held` and secure a charge for the order.
- r4 While `placed`, if the stock service refuses a reservation for the order → `rejected`, notify the shopper.
- r5 While `held`, when the charges service completes a charge for the order → `charged`, take every reservation for the order.
- r6 While `held`, if the charges service refuses a charge → free every reservation for the order, `cancelled`, notify.
- r7 While `charged`, when the stock service completes a reservation for the order → `confirmed`, collect every charge for the order.
- r8 While `charged`, if the stock service refuses a reservation → cancel every charge for the order, `expired`, notify.
- r9 While `held`, when the stock service notifies the ordering service of a reservation for the order whose state is `lapsed` → cancel every charge, `expired`, notify.
- r10, r11 While `confirmed`, a notification of a charge for the order whose state is `settled` → `paid`; `bounced` → `unpaid`, notify.

withdrawing#r1 a `held` order withdrawn → free every reservation, cancel every charge, `withdrawn`; r2 a `confirmed` one refused. browsing#r1 When the shopper views a product, the ordering service shall count the product and return the availability of the product.

The first draft collected and took in one step; a refused `take` then had no compensation (payments has no refund, void works only before capture). Taking first and collecting last made every failure compensable with operations that exist.

**Adapter contracts** [paper: form proposed]. `stock.toml`: `adapter = "upstream"`, `port = "stock"`, `contract = "1.4.0"`; `[objects] reservation = "allocation"`; `stock.reserve` calls `inventory.hold` with `product = order.product`, `quantity = order.quantity`, `reference = order.number`, `warehouse` omitted (optional upstream); outcomes done → done, `product out of stock` → `order out of stock`, `no quantity` `unreachable` citing placing#r1, r2; `[notifications]` `an allocation lapses` → notifies the reservation with state `lapsed`. `charges.toml`: `[fixed] currency = "EUR"`; `card declined` and `amount over limit` both → `charge declined`; void's and capture's refusals `unreachable` citing core lines; `a dispute is opened` not mapped.

## b. The projection

Per port operation: the mapped upstream operation's `requirements` from the published contract, translated through the adapter's objects, parameters and outcomes, keeping what can still be said in ordering's terms; events come in through `[notifications]`. All translated lines parse in ordering's grammar [run] (v5).

- stock.reserve ← inventory.hold: r1 → "When the ordering service reserves stock for an order, the stock service shall complete a reservation for the order."; r2 → same order, same reservation (retry-safe since `reference ← order.number`) [paper]; r3 → "... the stock service **may** refuse a reservation for the order" (the supply condition, in inventory's terms, dropped; reason `order out of stock`); r4 dropped as unreachable; r9 via `followed-by` → "... may notify the ordering service of a reservation for the order whose state is `lapsed`" (async, 15 minutes).
- stock.free ← release: shall complete; `consumed` refusal unreachable.
- stock.take ← consume: whose state is `made` → shall complete; `lapsed` → shall refuse (survives because the state is mapped).
- stock.count ← query: shall return the availability (`units ← product.stock`).
- charges: secure shall complete or may refuse (r2, r3 merged into one reason; the 10000 limit visible as `limits`); cancel shall complete (refusal unreachable); collect shall complete, may notify of the charge settled or bounced within 3 days (refusal unreachable).

Ignored, and why: restock, transfer, audit and stockkeeping#r1-r4 (no port maps them); `inventory.lapse` as an operation (the clock's; only its event is mapped); `warehouse`, `supply`, `stock` but `units` (optional, or a cause in inventory's terms); disburse, resolve, payouts#r1, r3 (not mapped); `a dispute is opened` and payouts#r2 (not in `[notifications]`); settle and reverse as operations (their events mapped). None of these appear in ordering's model, vocabulary, scenarios or projection; they exist only in the read-only published contract.

## c. Does the downstream need lines for the port?

No. Every port operation is requested by a core response: reserve (placing#r1), secure (r3), take (r5), collect (r7), cancel (placing#r8, r9, withdrawing#r1), free (placing#r6, withdrawing#r1), count (browsing#r1 only). Every outcome the core depends on is a core trigger. The generated core scenarios already split what the core asked (Thens) from what the port answered (Whens) [run]: @r3 has "When the stock service completes the reservation r1" then "Then ... sets the status of the order o1 to held" and "And the ordering service secures the charge c1 for the order o1". In v5 the projection as lines parses and `spec logic` finds nothing new [run].

Today's checks disagree [run]: `v_m7` flags all 7 port operations and `v_m4` all 3 port refusal reasons, since only a trigger counts as a request; in v5 `v_m7` disappears once projection lines put the port operations in triggers. The current rules push towards mirroring.

Edge cases:
- **An upstream outcome the core does not handle.** Mapped to a port outcome but no core line reacts: should be a finding (v2 removes r4; today `v_m4` is identical with and without r4 [run]). Mapped to nothing: a finding unless marked `unreachable`. Collapsing two upstream reasons into one is translation, allowed.
- **An upstream rule the core relies on implicitly.** Idempotent hold: the projection pulls holding#r2 in, making the reliance explicit. The 15-minute lapse: the projection's may-notify line puts it before the core, which handles it in r8, r9. The payment limit: only "may refuse"; a limit of ordering's own would be a core line. Rules an upstream does not publish stay invisible; the remedy is a request asking it to state them.
- **A port op used by two core capabilities** (`free`, `cancel`; `count` by browsing only): nothing special.
- **An upstream parameter the downstream does not have.** Optional (`warehouse`): omitted. A constant of the context (`currency`): `[fixed]`, visible in the adapter contract. Per-order data (`card`): never an adapter default; it became `order.card` and placing#r1 gained "with a card". A choice (which warehouse ships): a core line.
- **One port op needing two upstream calls.** Allowed only when nothing between them can need compensation (a read, or idempotent with no `compensated-by`): `count` summing a query over two warehouses yes; `reserve` as two holds no, since the second can be refused after the first succeeded and needs `release`, a saga step that belongs in the core. Checkable from `compensated-by` [paper].

## d. Testing

| layer | generated from | written by hand |
|---|---|---|
| core scenarios with port stubs | core lines (`features generate`, today [run]) | step handlers |
| port stub | port model + projection [paper] | nothing |
| adapter contract tests (mapped ops only) | each projection line mapped back through the adapter contract [paper] | fixtures if the upstream has no test double |
| the upstream's own tests | its own lines [run] | its handlers |
| end-to-end (optional) | nothing | a smoke saga |

Sample generated scenario, @r8 today [run]: Given an order o1 whose status is `charged`, a reservation r1 for it, charges c1 and c2 for it and c3 not for it; When the stock service refuses the reservation r1; Then the ordering service cancels c1 and c2, does not cancel c3, sets the status of o1 to `expired` and notifies the shopper of the order o1.

Sample stub [paper]: `reserve(order)` records "reserves stock for <order>", may reply complete or refuse `order out of stock`, later may notify a lapsed reservation (async, at least once), and a second reserve for the same order returns the same reservation; `free` replies complete only, and a scenario injecting a refusal fails with "inventory 1.4.0 never refuses release as ordering uses it"; `take` completes when made, refuses when lapsed; `count` returns the availability. "may" lines get no scenario today (I17), so the stub's may-replies need a generator of their own.

Sample adapter test [paper]: Given inventory holds an allocation a1 whose status is `lapsed`; When the stock adapter takes the reservation a1 (→ `inventory.consume`); Then it replies refused `lapsed reservation`. 10 such tests for both ports, not the 26 lines the upstreams have.

## e. Implementation

Ordering writes: the core (the saga's state machine, the handlers of the shopper's operations, the handlers of each port reply and notification, a reply matched to its order through `reservation for order` or `charge for order` and dispatched on the order's status); the port interfaces (generated from the port models); two adapters (translation, the `[fixed]` value, the reason mapping, receiving the upstream's events; the transport in an ADR and the adapter, never in a line, directive-7). It writes nothing for restock, transfer, audit, payouts or disputes, and no port lines, stubs, adapter tests, published contracts or copied upstream vocabulary.

## f. Checks on broken variants

| variant | today | proposed [paper] |
|---|---|---|
| v1: r7 without its While | `L1 placing#r3 and #r7 clash: on "the stock service completes a reservation for the order" with an order that is placed, r3 sets the status of an order to held and r7 to confirmed` [run] | the same |
| v2: r4 removed | `v_m4`, identical to the correct context's [run] | "the port outcome refused: order out of stock of stock.reserve, which placing#r1 requests, has no core line while the order is placed" |
| v3: an unused `stock.restock` | `v_m7` lists it among all 8 [run] | only stock.restock: "requested by no core line: take it out of the port" |
| v4: r6 does not free | nothing [run] | "placing#r6 ends the order cancelled from held, after stock.reserve completed, without stock.free, which inventory.hold's compensated-by maps to" |
| a port op that maps to nothing | not checkable: no tool reads `stock.toml` [run] | "stock.extend has no calls and inventory 1.4.0 publishes nothing it could map to: raise a request" |

The request of the last case [paper]: to inventory, "Keep a reservation standing while a charge is secured": in ordering's words, securing a charge can outlast a reservation, so ordering needs to extend one once before it lapses; a proposed line for inventory to reword, "When the client extends an allocation whose status is `placed`, the inventory service shall keep the allocation.", with a term proposal for `extend`.

Upstream version change [paper]: the projection recomputed on each new version and diffed against the pinned one. Breaking: inventory 1.5.0 adds `refused: warehouse closed` to `hold` ("inventory 1.5.0's inventory.hold may refuse warehouse closed, which stock.toml maps to no outcome of stock.reserve"); `warehouse` made required; holding#r2 (idempotency) retired; `query` renamed; the lapse time changed (a warning). Silent: a new refusal on `audit`, a new operation, stockkeeping#r2 retired; silent because the projection is unchanged. An upstream change reaches ordering only through the operations ordering uses.

## g. What runs today

Parses [run]: inventory 14/14, payments 12/12, ordering 14/14, projection (v5) 12/12.

Refused along the way and reworded [run]:

| line tried | refusal | lesson |
|---|---|---|
| "puts a hold on a product" | does not parse at hold | a frame's fixed words cannot repeat a noun; the object renamed `allocation` |
| "keep the hold" | `"the allocation" has no antecedent` (R2) | "keep an allocation on the product" |
| "with an amount, a currency and a reference" | does not parse at currency | parameters joined "and ... and" |
| "a charge whose state is `settled` for an order" | does not parse at for | "whose" last |
| a charge's state with no `state` entry in the charges layer | does not parse at state | each layer needs its own attribute word |
| "keep a dispute over the authorisation" | does not parse at over | relation phrases are a fixed list |
| "whose stock is `0`" | does not parse at `0` | a number compared with a literal is no construct; a `supply` value used instead |

Needs new constructs or checks:
- An outbound request as a response: today an event atom, `reserve(e3, subject: x4, stock for: x2)` [run]; "... reserve stock for the order with a quantity" refused at `with` [run].
- An outcome as a trigger: read today as `complete` or `refuse` of a `kind of request` object, with no link to the request that made it [run]; "refuses to collect a charge" refused, "the verb collect takes as its subject agent or a kind of it" [run].
- Async notifications work through the pack's `notify`; model events cannot be verbs.
- Port areas: `kind: port` ignored, `v_a1` demands CLI tables for all 7 port operations [run].
- The `adapter = "upstream"` kind: ignored by every tool; `spec annotate` reports only `cli.toml` [run].
- A published-contract form, with model declarations the model lacks: `idempotent`, `compensated-by`, `followed-by`, delivery.
- Saga checks: none exist (compensation, unhandled outcome per status, may-coverage).
- A tool quirk: grammar 4 accepts the frame "reserves stock for <order>" but the lexicon check reports `v_t13` [run].

Totals [run]: ordering's `spec check` 18 violations (`v_a1` ×7, `v_m7` ×7, `v_m4` ×3, `v_t13` ×1); `spec logic` no findings, nothing unread; `features generate` wrote all seven features.

## h. Open questions and what the design was missing

1. Correlation: status dispatch works and `spec logic` guards it (v1). A construct naming which operation an outcome answers? Status dispatch fails when two requests on one object are in flight in one status.
2. Races: in r9 a lapse cancels every charge while `secure` may still be in flight with no authorisation to void yet; a late completion finds the order `expired` and matches no line. A check of "every reply handled in every status it can arrive in" would have found it.
3. At-least-once delivery: r8 and r9 can both fire for one lapse and cancel twice. Require every compensation to be idempotent, read from the published contract?
4. `unreachable` needs a proof: a property of the core's state machine. Checked, or reviewed by a person?
5. A missing upstream compensation (payments has no refund): a saga check reading `compensated-by` should turn the gap into a request.
6. Choreographed sagas between peers: with no orchestrator, no core lines bound the ports. Out of scope, or a second pattern?
7. Unmapped events: payments publishes disputes on captures ordering made, and ordering ignores them. A warning?
8. Where the projection lives: generated and uncommitted, like the parse cache; the published contract and the adapter contract are the committed inputs.
9. Delivery times: properties, or time lines `spec logic` cannot read?
10. Port parameters: whole core objects (`reserve(order)`) keep core lines short but couple the adapter to the core model; port parameters in the port's own words need "with ..." in a response, which grammar 4 does not allow.
