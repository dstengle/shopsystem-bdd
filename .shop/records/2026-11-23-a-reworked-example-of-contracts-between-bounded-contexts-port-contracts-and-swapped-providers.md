---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-23-a-reworked-example-of-contracts-between-bounded-contexts-port-contracts-and-swapped-providers
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-23
---

# A reworked example of contracts between bounded contexts: port contracts and swapped providers

The person's concern after the first worked example (record 2026-11-23-a-worked-example-of-contracts-between-bounded-contexts-ordering-over-inventory-and-payments): its declarative upstream adapter contract (port op → upstream op) assumes like-for-like operations and makes the port inherit its meaning from one upstream, brittle on a provider swap or in any non-greenfield setting; the cross-context tracing is worth keeping.

The revised design tested here: (1) a **port contract** owned by the downstream, the port model plus a few port lines in its own terms stating only the guarantees the core relies on, bounded by the core both ways; (2) an **adapter is code** conforming to the port contract however it gets there, bound by **conformance tests** generated from the port contract and run against the adapter with its provider; (3) the **core tested against a stub** generated from the port contract; (4) a **trace** (which provider operations an adapter uses per port operation, many-to-many) as evidence and impact analysis, with satisfiable and impact checks where the provider is a sibling context with a published contract.

**[run]** = checked by main's `scripts/spec` and `scripts/features` on the folders in this record's folder of the same name (2026-11-23); **[paper]** = worked by hand. Folder: `ordering/` (the first example's ordering, core lines and port models byte-identical [run: diff], plus port contracts `spec/capabilities/stock-port.md`, `charges-port.md`, their conformance features, and four trace files `spec/adapters/stock-inventory.toml`, `stock-ledger.toml`, `charges-payments.toml`, `charges-processor.toml`; the first design's declarative `stock.toml`, `charges.toml` removed); `variants/b1-refunding/` (the core change if the processor charges at secure); `variants/lapse-deadline/` (the liveness guarantee with the time pack).

## Summary

- **Brittleness: the person is right.** The first design's mapping copied payments' authorise/void/capture into the port's meaning; a card processor with no authorise and no void has no honest mapping. Under the revised design, a code adapter plus conformance tests serves both stock providers and both payment providers; the port contract replaces the generated projection; the trace keeps the cross-context tracing.
- **No core change was needed to add the port contracts.** 10 port lines (stock 6, charges 4), all parse [run]. With them `v_m7` is gone (port lines whose trigger is ordering's own request satisfy it) [run]; `spec logic` finds nothing [run]; `features generate` wrote 10 conformance scenarios [run].
- **13 unstated guarantees found** that the core silently took from inventory and payments: 6 became port lines, 4 are business decisions, 3 need nothing (every saga line is guarded by the order's status, which absorbs duplicate and out-of-order replies). Making them explicit worked: the processor's charge-at-secure adapter fails charges-port r2, r3; the legacy ledger fails stock-port r6.
- **A swap changes more than the adapter when the new provider lacks a capability** the core used (count on the ledger) or changes the business (money moving at secure). Those surface as conformance failures and become a person's decision or a core change, not silent drift.
- **Weakness:** "satisfiable" cannot be true entailment without a term translation, which would be the old mapping back as evidence; it degrades to a citation check plus a person's review. The impact check works fully. "Bounded both ways" works mechanically only for outcome-exclusion lines; guarantee lines need a `Relied on by:` citation.

## 1. The port contracts (owned by ordering)

A capability in the port's area, narrator "the ordering service", group `service`, `specifies: service stock` / `service charges`. Its scenarios are the conformance tests.

**stock-port** (all parse [run]):
- [r1] While a reservation for an order exists, when the ordering service reserves stock for the order, the stock service shall return the reservation and change nothing.
- [r2] When the ordering service frees a reservation, the stock service shall complete the reservation.
- [r3] While the state of a reservation is `made`, when the ordering service takes the reservation, the stock service shall complete the reservation.
- [r4] While the state of a reservation is `lapsed`, when the ordering service takes the reservation, the stock service shall refuse the reservation.
- [r5] When the stock service notifies the ordering service of a reservation whose state is `lapsed`, the stock service shall free the reservation.
- [r6] When the ordering service counts a product, the stock service shall return the availability of the product.

**charges-port** (all parse [run]):
- [r1] While a charge for an order exists, when the ordering service secures a charge for the order, the charges service shall change nothing.
- [r2] When the ordering service secures a charge for an order, the charges service shall not collect the charge.
- [r3] When the ordering service cancels a charge, the charges service shall complete the charge and not notify the ordering service of the charge.
- [r4] When the ordering service collects a charge, the charges service shall complete the charge.

Found while writing them [run]: "While a reservation is for an order" does not parse at "for" (the existence construct does); charges' "shall return the charge" bound the trigger's charge (`return(e2, …, object: x4)`), so r1 says only "shall change nothing", which is the business guarantee (no second charge); cancel split into two lines gave `v15n` (two groups on one trigger), so they are one line.

Reliance [paper]:

| port line | relied on by | kind |
|---|---|---|
| stock r1 | placing#r1 on a retry | implementation: no line's text shows it |
| stock r2 | placing#r6, withdrawing#r1 (no line handles a refused free) | outcome exclusion |
| stock r3, r4 | placing#r7, r8 | outcome by state |
| stock r5 | placing#r9 (cancels the charge, never frees the stock) | unstated, now stated |
| stock r6 | browsing#r1 | outcome |
| charges r1 | placing#r3 on a retry | implementation |
| charges r2 | placing#r6, r8, r9, withdrawing#r1 (end orders cancelled/expired/withdrawn assuming no money moved) | unstated, now stated |
| charges r3 | placing#r8, r9, withdrawing#r1 | outcome exclusion and finality |
| charges r4 | placing#r7 | outcome exclusion |

The bound check [paper]: mechanically, for each port operation a core response requests, every outcome the port model declares that no core line triggers on must be excluded by a port line (this calls for stock r2, charges r3, r4 and finds nothing else); the other lines (idempotency, "secure collects nothing", "lapse frees") rest on meaning or implementation, so each needs `Relied on by: <core ids>` (like `rests_on:`), the check confirming the cited lines exist and request that port's operations; without it a port line with no relying core line is a finding.

Today's tools on the port contracts [run]: `spec check` 11 violations (`v_a1` ×7 wanting CLI tables for port operations, `v_m4` ×3 port refusal reasons, `v_t13` ×1 the first example's frame quirk); `v_m7` gone (port triggers read as `request(e1, stock.reserve, subject: the ordering service …)`); `spec logic` no findings; `features generate` wrote both conformance features. Samples [run]:

```gherkin
  @g1 @r1
  Scenario: Reserving again for the same order gives the same reservation
    Given a reservation r1
    And an order o1
    And the reservation r1 is for the order o1
    And the reservation r1 exists
    When the ordering service reserves stock for the order o1
    Then the stock service returns the reservation r1
    And the stock service changes nothing

  @g2 @r2
  Scenario: Securing a charge collects nothing
    Given an order o1
    When the ordering service secures a charge c1 for the order o1
    Then the charges service does not collect the charge c1
```

These are adapter-neutral: each adapter supplies step handlers that set up the Givens with its provider (sandbox, fake, real system) and observe the Thens ("does not collect" = no money moved, by the provider's balance or ledger). The core stub [paper] is generated from the port model plus these lines: it records requests, replies with outcomes the lines allow, refuses ones they exclude, and keeps reserve and secure idempotent. The core's scenarios are the first example's, unchanged.

## 2. The providers

- **stock A, inventory:** the first example's context and published contract (hold, release, consume, query, lapse event, idempotent by reference).
- **stock B, a legacy stock ledger** (no spec): `table stock(product PRIMARY KEY, units INTEGER CHECK (units >= 0))`; `POST /stock/{product}/decrement {n} -> 200 {units} | 409 insufficient` (atomic); `POST /stock/{product}/increment {n} -> 200 {units}`. No read, holds, lapse, idempotency keys or transactions across calls.
- **charges A, payments:** the first example's (authorise, void, capture; settle and reverse events).
- **charges B, an invented card processor** (no published contract): `POST /payments {card_token, amount_minor, currency, dedupe_key} -> 202 {payment_id, state: pending}`, webhooks `payment.cleared | payment.declined` (seconds to minutes, at least once, any order), later `payment.clawed_back` (chargeback, weeks); `POST /payments/{id}/returns -> 202 {return_id}`, webhooks `return.completed` (2-5 days) | `return.rejected` (e.g. card closed); 0.30 EUR per return, the payment's fee not given back. No authorise, void or capture.

## 3. Each adapter

**stock A over inventory:** reserve → hold (reference = order number), free → release, take → consume, count → query, lapse event → lapse notification. r1-r4, r6 pass; r5 passes only if inventory returns a lapsed allocation's units, which its published lines do not say (holding#r9 only sets `lapsed` and notifies), and needs a sandbox with an advanceable clock.

**stock B over the ledger:** reserve = a `pending` record in the adapter's own store, decrement, mark `made` (409 → refused `order out of stock`; idempotency from the store); free = increment, mark `freed`; take = mark `taken`, no ledger call; lapse = the adapter's own timer, at the deadline a `made` record → increment, mark `lapsed`, notify. r1 passes normally but fails fault injection (a crash between decrement and marking leaves a `pending` record that cannot tell whether the decrement happened; unrepairable without keys at the ledger → business decision: accept rare drift and reconcile by stock count). r2-r4 pass. r5 passes, emulated (against a fake ledger with the adapter's clock; the real ledger only in staging). **r6 fails**: the ledger cannot count; decrement-then-increment as a probe has side effects and is refused.

**charges A over payments:** secure → authorise (reference = order number, currency EUR), cancel → void, collect → capture, settle/reverse events → settled/bounced. r1-r4 pass [paper] against payments' published test double. charges r1 rests on a published property ("idempotent by reference"), not a line; payments should state it as a line, as inventory does in holding#r2.

**charges B over the processor**, two strategies a code adapter may choose:

| test | B1: charge at secure | B2: charge at collect |
|---|---|---|
| how | secure = POST /payments; cancel = a return; collect = no-op | secure = a pending record; cancel = drop it; collect = POST /payments, cleared/declined → settled/bounced |
| r1 | pass (dedupe_key) | pass (store + dedupe_key) |
| r2 | **fail**: money moves at secure | pass |
| r3 | **fail**: a return is async, 2-5 days, can be rejected, costs a fee, notifies later | pass |
| r4 | pass | pass (202, then a webhook) |

Any of these runs needs the processor's sandbox; webhooks need a reachable endpoint or a replay tool (a mechanism: an ADR).

Trace files (`ordering/spec/adapters/`): `[uses]` each port operation → the provider operations its code calls, many-to-many; for sibling providers `[stands-on]` each port line → the provider lines it rests on. Excerpt:

```toml
adapter = "provider"
port = "stock"
provider = "legacy: stock ledger (decrement, increment over HTTP)"
[uses]
"stock.reserve" = ["decrement", "adapter store: reservation record"]
"stock.count" = []                        # nothing the ledger offers can count
"notify lapsed" = ["adapter timer", "increment", "adapter store"]
```

## 4. Unstated guarantees

| # | the core assumed | broken by | decision |
|---|---|---|---|
| G1 | cancelling a charge is immediate, certain, free, leaves the shopper's money alone | B1 (a return: days, can fail, fee) | port line charges r3, B1 fails it; then B2, or a core change (§5), or a business decision. The fee itself is no line: ADR or business decision |
| G2 | money moves only at collect, after the stock is taken | B1 | port line charges r2, B1 fails it |
| G3 | a secured charge is good money | B2 (the card first tried at collect; declines arrive as `bounced` after `confirmed`) | not strict even for payments (the network can reverse): rates, not a test → **business decision**: more `unpaid` after confirmation, or wait for `settled` before taking stock, which clashes with a lapse of minutes when settlement takes days |
| G4 | reserve and secure idempotent, even across a crash | the ledger (no keys) | port lines stock r1, charges r1; the ledger adapter fails fault injection → business decision (drift + reconciliation) or ask the legacy team for keys |
| G5 | a lapsed reservation's stock comes back by itself (placing#r9 never frees) | inventory states nothing; the ledger has no lapse | port line stock r5; for inventory a satisfiable finding → request "a lapsed allocation's units are on hand again"; for the ledger the adapter emulates it |
| G6 | a held order cannot wait forever (inventory's 15-minute lapse ended stalled sagas) | the ledger (no lapse) | the duration was inventory's policy, silently ordering's business → a port line with a deadline (variant lapse-deadline parses with the time pack, needs a `deadline` object in the port model; `spec logic` cannot read time). Its duration is a **business decision** |
| G7 | count is possible and reflects holds | the ledger (no read) | port line stock r6, the ledger fails it → **business decision**: browsing drops availability (browsing#r1 retired, count leaves the port, no ripple to inventory's adapter) or the legacy team adds a read |
| G8 | free and cancel never fail | B1's cancel (return.rejected) | port lines stock r2, charges r3 |
| G9 | paid is final | payments' disputes (unmapped); the processor's chargebacks | **business decision**, the same for both; today's core ignores both |
| G10 | each reply arrives once and in order | both payment providers at least once, the processor in any order | none: every saga line is guarded by the order's status, a duplicate or late reply matches no line [paper; e.g. r11 only while `confirmed`] |
| G11 | synchronous replies within seconds | the processor | none: the core is driven by reply triggers already |
| G12 | reserving sets stock aside without consuming it | the ledger (decrements at once) | none: the same for availability |
| G13 | the amount charged equals `order.total` | the processor (fees deducted from payouts) | finance: ADR or business decision, not a line |

## 5. The core change if B1 is chosen (variant b1-refunding; all parse, logic clean [run])

Model: port `charges` `cancel(charge) outcomes: done | notifies → the charge`, the charge's state gains `refunded | unrefunded`; core order status gains `refunding`, `unrefunded`; a new actor, the clerk. placing#r8 retired; new lines:
- placing#r12: While the status of an order is `charged`, if the stock service refuses a reservation for the order, then the ordering service shall cancel every charge for the order and set the status of the order to `refunding`.
- placing#r13: While the status of an order is `refunding`, when the charges service notifies the ordering service of a charge for the order whose state is `refunded`, the ordering service shall set the status of the order to `expired` and notify the shopper of the order.
- placing#r14: … whose state is `unrefunded`, … set the status of the order to `unrefunded` and notify the clerk of the order.

charges r3 retired for r5: When the ordering service cancels a charge, the charges service shall complete the charge and notify the ordering service of the charge.

Still uncovered under B1: a cancel while `held` (placing#r9, withdrawing#r1) hits a payment in flight; the refund must wait for `payment.cleared` (the first report's race, with money at stake). Ripple: payments' adapter must send a "refunded" notification after a successful void, a code change its conformance test would demand; no change to payments, inventory or other core lines. B2 avoids all this but brings G3; B1 or B2 is the person's call.

## 6. Satisfiable and impact checks

**Sibling providers [paper].** Satisfiable as true entailment ("inventory's lines, translated, imply stock r1") needs the term correspondence (allocation ≈ reservation, reference ≈ order number); the trace does not carry it, and if it did it would be the first example's mapping back as evidence. Without it, the check degrades to: each `stands-on` line exists and is live in the pinned published contract, its operation is among `[uses]`, and published properties match the port line's kind (idempotent for r1, a compensation for r2, r3). It still found that charges r1 rests on a property, not a line, and (only by a person reading it) that stock r5 rests on holding#r9, which says nothing of stock coming back; either way a request to the upstream. Verdict: a citation check plus review; conformance tests decide.

Impact works fully on the many-to-many trace: inventory 1.5 retires holding#r2 → stock r1 → placing#r1 → finding; inventory adds refusal "warehouse closed" to hold → `[uses]` names stock.reserve → placing#r1, r3, r4 → the adapter must map it to `order out of stock` or treat it as broken; a new refusal on audit or a new operation touches no `[uses]` entry → silent.

**Ledger and processor:** nothing static; the trace is documentation, and conformance tests against a sandbox, a fake built from observation, or staging are the only evidence. Their version changes reach ordering only as failing conformance runs, so those runs belong on a schedule, not only at build.

## 7. Ordering's committed files on a swap

| swap | files |
|---|---|
| stock: inventory → ledger | adapter code; trace (stock-inventory.toml → stock-ledger.toml); the inventory entry under `## Upstreams`; `spec/upstreams/inventory/` removed; **also** G7 (browsing#r1 retired, or wait on the legacy team) and G6's duration unless the deadline port line was already there |
| charges: payments → processor, B2 | adapter code; trace; the `## Upstreams` entry; `spec/upstreams/payments/` removed; the person's G3 decision |
| charges: payments → processor, B1 | all of the above, plus the port model, port contract, three core lines, a core model change, and payments' adapter code |

## 8. Brownfield: ordering already calls the ledger directly [paper]

Today's code decrements at checkout, increments on payment failure or cancel, shows nothing on the product page, has no lapse. (1) Name each call site by its business intent in ordering's terms: decrement = reserve, increment = free, no take (the decrement consumed already), so the first port model is reserve and free only. (2) Write the port lines the existing code relies on (likely §4's list); absent behaviour becomes an explicit gap (no lapse: orders stuck awaiting payment keep their stock forever). (3) Extract an adapter wrapping the current calls unchanged, generate the conformance tests, run them against the wrapper in staging: passes characterise guarantees that hold today, failures the real behaviour (a double checkout decrements twice: r1 fails), each failure a port line rewritten to the truth, a known limitation, or a backlog item. (4) Only then add lines (lapse, count) and grow the adapter. The port contract first describes the legacy behaviour, then improves on it.

## 9. The first example's open questions revisited

| question | now |
|---|---|
| 1 correlation | remains: the core's, guarded by status |
| 2 races | remains, worse under B1 |
| 3 at-least-once, idempotency | into port lines (stock r1, charges r1) and adapters' stores; status guards absorb duplicates |
| 4 `unreachable` needs a proof | gone: no declarative outcome mapping; an adapter turns an impossible provider outcome into `broken` |
| 5 a missing upstream compensation | a conformance failure (B1 against charges r3), decided per G1 |
| 6 choreographed peers | remains |
| 7 unmapped events | remains as G9 |
| 8 where the projection lives | gone: the committed port contract replaces it |
| 9 delivery times | ordering's own business (G6); the time pack parses it but needs a model object; `spec logic` cannot read it |
| 10 port parameter shape | remains; with code adapters the coupling is just code |
| `v_m7` pushes to mirroring | resolved by the port contract [run]; `v_m4` still needs teaching (a core trigger on a refusal should count as stating it) |

## 10. Runs

Port lines 10/10 parse [run]. `spec check` on `ordering/`: 11 violations (`v_a1` ×7, `v_m4` ×3, `v_t13`), `v_m7` and `v_s3` gone [run]. `spec logic`: no findings [run]. `features generate` wrote stock-port.feature and charges-port.feature [run]. b1-refunding: r12-r14 and charges r5 parse, logic clean, same 11 violations [run]. lapse-deadline: "When the clock reaches the deadline of a reservation whose state is `made`, the stock service shall free the reservation and notify the ordering service of the reservation." parses once the index imports `[request, time]` and the port model has a `deadline` object [run]. No tool yet for: trace reading, satisfiable and impact checks, the bound check and `Relied on by:`, conformance runs per adapter, stub generation [paper].

## 11. Open questions for the person

1. G3: a card declined after confirmation acceptable (B2), or money certain before stock is taken (a saga change, clashing with a short lapse)?
2. G6: how long does a held order hold stock, now the number is ordering's?
3. G7: with the ledger, does browsing drop availability, or wait for a read from the legacy team?
4. G9: what happens to an order whose payment is disputed or clawed back?
5. B1 or B2 for the processor, and who handles a failed refund (the clerk in b1-refunding)?
6. Accept "satisfiable" as a citation check plus review rather than true entailment?
7. Adopt `Relied on by:` on port lines so the bound check sees guarantees no core line's text shows?
