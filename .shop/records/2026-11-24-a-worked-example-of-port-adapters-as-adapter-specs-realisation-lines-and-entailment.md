---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-24-a-worked-example-of-port-adapters-as-adapter-specs-realisation-lines-and-entailment
kind: analysis
about: item/missingmass.io/shopsystem/shopsystem-bdd/b540
date: 2026-11-24
---

# A worked example of port adapters as adapter specs: realisation lines and entailment

The third worked example of contracts between bounded contexts (after the two of 2026-11-23), for b540 "A port adapter's design artifact". The person's framing (2026-11-24, quote-72): three layers of requirements — core (business, the context's terms), port (the core's needs, the context's terms), adapter (technical: how providers meet the port's lines, in the port's and the providers' terms plus technical words); the adapter is the anti-corruption layer where the vocabularies meet, and the mapping of downstream requirements onto an internal upstream's contract tells the context when to request a capability change. The design tested: one folder per adapter holding what it realises (port line ids), its providers (a pinned published contract, or an assumed provider description), realisation lines in an isolated spec, adapter-scoped decisions, and the derived trace, entailment result and requests.

**[run]** = main's `scripts/spec` and `scripts/features` run on the folders in this record's folder of the same name (2026-11-24); **[paper]** = by hand. Folder: `stock-inventory/` (adapter A: `spec/` with models `port`, `provider`, `adapter`, vocabularies, capabilities `stock-port`, `holding`, `realisation`; `features/` generated; `provider/inventory/1.4.0/contract.toml` pinned; `adr/0001-0004`), `stock-ledger/` (adapter B, same layout, its provider area and `ledger` capability the assumed provider description), `variants/client-alias/` (inventory's "the client" aliased to `service stock`), `tools/trace.py` (a scratch script reading the trace off `spec parse --form`, not plugin code). The optional card-processor adapter was done on paper only (§8).

## Summary

- **The two vocabularies coexist in one isolated spec, under four rules** [run]: model element names are global (a second `object product` is `v_m8`, so the provider's is `stocked-product`); a word on both sides becomes two kinds (`product_port`, `product_provider`) and a line using it is refused as two meanings, fixed by a qualified provider word ("stocked product"); attribute and value words shared by kinds are fine (`quantity`, `lapsed`); a parameter named like an attribute is not (the ledger's `units` renamed `amount`). The sides meet only through an adapter-owned object, `entry` ("the allocation of the entry of the reservation"): a third area cannot relate two other areas' objects.
- **Every realisation line parses**, once worded right; refused: arguments of a request in a response (`with`), "at the inventory service", "notifies ... that an allocation lapses", copying another thing's value, and "refuses the allocation" until `entry` is `kind of request`.
- **Entailment works one step deep.** With port, realisation and provider lines in one spec, `spec logic` prints L8 on stock-port r1-r4, r6 (A) and r1-r5 (B) [run], but each premise is a realisation line on the port line's own trigger restating the port's response; provider lines are never premises (`entail.lp` takes only lines on the query's trigger, untriggered ones and refusals) and "the client" stays a constant apart from "the stock service" even when aliased [run]. So L8 checks the adapter has *claimed* each port line, not that the provider backs the claim.
- **It found two real correspondence holes** [run]: an L1 between "an order has no entry" (the adapter's store) and stock-port r1 "a reservation for the order exists" (the port's state), and in a draft a lapsed reservation beside a placed allocation. These are invariants the adapter must keep, and grammar 4 has no form for a state invariant.
- **The known gap surfaced only by absence**: stock-port#r5 gets no L8 in A, but does in B (the adapter increments the stock back itself). Making it a finding needs a "realises" rule plus multi-hop premises, so that inventory's silence in holding#r9 is named.
- **The trace** can be read off `spec parse --form` today with a 25-line script [run].
- **Recommended placement**: a nested context per adapter inside the downstream's repository, its own spec root, `adr/` and `provider/`, the port read from the parent. Today a nested id is refused [run].

## 1. The adapter folder, as built for A

1. **What it realises**: `spec/index.md` says `kind: adapter`, `realises: … port stock`, `providers: [bounded-context/example.org/shop/inventory@1.4.0]`; the realisation capability lists `realises: [stock-port#r1 … stock-port#r6]`. Tools accept the three keys and read none [run].
2. **Providers**: A has the pinned published contract under `provider/inventory/1.4.0/contract.toml`, and inventory's model and lines as a `provider` area and a `holding` capability (verbatim but "product" written "stocked product", §2). B has a provider description by its owners, frontmatter `assumed: true`, read by no tool.
3. **Realisation lines**: capability `realisation`, area `adapter`, narrator "the stock adapter".
4. **Adapter-scoped decisions**, short texts in `adr/` (a root `decisions/` folder makes `spec check` report `file: decisions/: the layout has no decisions/; run scripts/migrate` [run]). A: hold at reserve, consume at take, release at free; the entry store plus inventory's reference as idempotency; retries with the same reference; lapse events by subscription. B: decrement at reserve; take only marks the entry; count not realised; a write-ahead store and a deadline sweep; nightly tests of the assumed lines against the ledger's staging copy; HTTP with timeouts.
5. **Derived**: the trace (§4), the entailment result and requests (§3).

A's models (port and provider copied; the adapter area its own):

```model
# port.md (kind: port), copied from ordering
object order        attributes: quantity (number); number (text)   relations: for → product (one)
object product
object reservation kind of request   attributes: state: made | lapsed   relations: for → order (one)
object availability attributes: units (number)   relations: of → product (one)
service ordering
service stock   reserve(order) | free(reservation) | take(reservation) | count(product)

# provider.md (kind: provider), inventory 1.4.0
object stocked-product   attributes: stock (number); supply: available | exhausted
object allocation        attributes: quantity (number); reference (text)
  lifecycle status: placed → consumed | released | lapsed      relations: on → stocked-product (one)
service inventory   hold(stocked-product, quantity, reference) | release | consume | query | lapse
actor the client, the clock

# adapter.md (kind: adapter)
object entry kind of request
  attributes: reference (text)
  relations: of → order | reservation (one); has → allocation (one); has → stocked-product (one); has → reservation (one)
```

A's realisation lines (all parse [run]):
- r1 While an order has no entry, when the ordering service reserves stock for the order, the stock service shall keep an entry of the order and hold the stocked product of the entry.
- r2 While a reservation for an order exists, when the ordering service reserves stock for the order, the stock service shall return the reservation and change nothing.
- r3 When the inventory service keeps the allocation of an entry, the stock service shall complete the reservation of the entry.
- r4 If the inventory service refuses an entry, then the stock service shall refuse the reservation of the entry.
- r5 When the ordering service frees a reservation, the stock service shall release the allocation of the entry of the reservation and complete the reservation.
- r6 While the state of a reservation is `made`, when the ordering service takes the reservation, the stock service shall consume the allocation of the entry of the reservation and complete the reservation.
- r7 While the state of a reservation is `lapsed`, when the ordering service takes the reservation, the stock service shall refuse the reservation.
- r8 When the inventory service notifies the client of the allocation of the entry of a reservation, the stock service shall set the state of the reservation to `lapsed` and notify the ordering service of the reservation.
- r9 When the ordering service counts a product, the stock service shall query every stocked product of an entry and return the availability of the product.

B's realisation lines (all parse [run]; imports `[request, time]`): r1 reserve with no entry → keep an entry and decrement the line of the entry; r2 idempotency as A; r3 if the ledger service refuses an entry → refuse the reservation; r4 free → increment the line of the entry, set its progress to `returned`, complete; r5 take a `made` reservation → set the entry's progress to `taken`, complete; r6 take a `lapsed` one → refuse; r7 "When the clock reaches the deadline of an entry whose progress is `decremented`, the stock service shall set the state of the reservation of the entry to `lapsed` and notify the ordering service of the reservation."; r8 on that notification, increment the line of the entry and free the reservation. Its assumed provider: `object line (code, units)`, `ledger.decrement(line, amount)` refused `amount short`, `ledger.increment(line, amount)`, actor the caller, lines ledger#r1-r3.

## 2. Claim 1: two vocabularies in one isolated spec [run]

| clash | what happened | resolution |
|---|---|---|
| object `product` on both sides | `v_m8 … the object product is declared again` | rename the provider's element `stocked-product` |
| the word "product" on both sides | kinds `product_port`, `product_provider`, both spelled "product"; holding#r3 refused `more than one meaning: "the product" reads 2 ways` | a qualified provider word, "stocked product", substituted word for word into the provider's lines, recorded in the vocabulary entry ("inventory's 'product'") |
| `quantity` (order, allocation), `lapsed` (reservation.state, allocation.status) | no problem: scoped by kind | none |
| `state` vs `status`; `reference` | no clash | none |
| the ledger parameter `units` beside the attribute and the time pack's "unit" | "with units" does not parse | parameter renamed `amount` |
| inventory's "the client" vs the port's "the stock service" | the alias is accepted, no `v_t20` (different layers), but the form keeps a separate constant (`x1: service the client`) | none today: actor identity across sides is not expressible |
| a relation between a port object and a provider object | a third area cannot declare an object again | the adapter's own `entry`, with rows to both sides |

`Redefines:` is only for pack words; a separate area per side is needed and works; the qualified word resolves the clash.

Refused [run]: "… hold the stocked product of the entry of the order **with the quantity of the order**" → `does not parse at with`; "… **at the inventory service**" → at `at`; "When the inventory service notifies the client **that an allocation lapses**" → at `that` (notify takes "of <thing>" only); "… set the quantity of the allocation … **to the quantity of the order**" → at `the`; "If the inventory service refuses **the allocation of an entry**" → `the verb refuse takes as its object request or a kind of it` (fixed by `entry kind of request`); "While no entry of an order exists" → R2 `"the order" has no antecedent … made inside "no entry ..."` (reworded "While an order has no entry"); "While a reservation is the reservation of an entry" → does not parse; "the stock adapter" is no proper noun.

The grammar lacks: arguments of a request in a response; "at <service>"; notify with a clause; copying values and arithmetic (the ledger's lines can say "shall keep the line", not "the units fall by the amount"); actor identity across vocabularies; a relation between two areas' objects declared by a third; state invariants.

## 3. Claim 2: does `spec logic` show the port lines guaranteed?

Port, provider and realisation lines all as capabilities of the one adapter spec. A [run]:

```text
L1 realisation#r1 and #r2 clash: on "the ordering service reserves stock for the order", r1 obliges the stock service to keep an entry and r2 changes nothing
L1 realisation#r1 and stock-port#r1 clash: on "the ordering service reserves stock for the order", realisation#r1 obliges the stock service to keep an entry and stock-port#r1 changes nothing
L2 realisation#r2 and stock-port#r1 say the same thing
L2 realisation#r7 and stock-port#r4 say the same thing
L8 stock-port#r1 says nothing other requirements do not: Then 1 by realisation#r2; Then 2 by realisation#r2
L8 stock-port#r2 says nothing other requirements do not: Then 1 by realisation#r5
L8 stock-port#r3 says nothing other requirements do not: Then 1 by realisation#r6
L8 stock-port#r4 says nothing other requirements do not: Then 1 by realisation#r7
L8 stock-port#r6 says nothing other requirements do not: Then 1 by realisation#r9
```

(and the reverse L8s, realisation#r2 and r7 entailed by port lines). `spec check`: 4 violations (`v_m4` ×3, `v_t13` ×1) [run]. B [run]: L8 on stock-port r1, r2 (by realisation#r4), r3 (r5), r4 (r6), **r5 (by r8)**; the same L1s and L2s; r6 not realised, no L8.

| port line | A | B |
|---|---|---|
| r1 idempotent reserve | by realisation#r2, which only restates it (L2); clashes with r1 (missing invariant) | the same |
| r2 free completes | r5 | r4 |
| r3 take made | r6 | r5 |
| r4 take lapsed refused | r7 | r6 |
| r5 a lapsed reservation is freed | **not entailed**: no realisation line on its trigger says it; inventory's holding#r9 only sets `lapsed` and notifies | r8: the adapter increments back itself |
| r6 count | r9 | not realised (adr/0001) |

**How much is checked.** Every L8 premise is a realisation line on the port line's own trigger stating the port's response itself; no holding or ledger line is ever a premise. So the check confirms the adapter's claims cover the port, not that the provider makes them true (realisation#r5 says "release the allocation … and complete the reservation"; nothing checks inventory's holding#r5, r6 let the release succeed). `grammar/entail.lp` takes the lines on the query's trigger (stratum A) plus untriggered lines and lines on a refusal (stratum B); it never turns a response act into another line's trigger. The chain wanted is port request → adapter's provider request → provider line → provider reply → realisation trigger → port response, and it needs actor identity too. Asked of today's tools, "put the port line in a capability and see whether L8 fires" answers "is it entailed by some other line on its trigger": the adapter claims it. `spec explain` printed only the line itself for every stock-port line [run].

**What the check caught that matters [run]**: the L1 between realisation#r1 and stock-port#r1 — nothing ties "an order has no entry" (the store) to "a reservation for the order exists" (the port's state), so a world with a reservation and no entry obliges both "keep an entry" and "change nothing". A draft conditioning take on the allocation's status gave L1s pairing a `lapsed` reservation with a `placed` allocation. Both are correspondence invariants, the adapter's real correctness obligations; grammar 4 has no form for a state invariant (R12 needs a trigger, or always/never with a response).

**The gap** surfaces only as a missing finding (no L8 on stock-port#r5 in A, one in B). With a "realises" rule [paper] (every `realises:` id L8-entailed, else `stock-port#r5 is realised by no line of realisation`) it becomes a finding; naming inventory as its cause needs multi-hop premises, the chain for r5 then stopping at holding#r9.

The request it would raise [paper], for inventory to reword:

```text
work request bounded-context/example.org/shop/inventory "A lapsed allocation's units are on hand again"
  Need: a client is told an allocation has lapsed (holding#r9) but not that its units can be held again; the
  stock adapter of ordering frees the reservation on that basis (stock-port#r5).
  Proposed line: When the clock lapses an allocation whose status is `placed`, the inventory service shall set the
  status of the allocation to `lapsed`, release the allocation and notify the client of the allocation.
```

The proposed line has its own problem: inventory's lifecycle has no `lapsed → released`, so `v_m6` [paper]; inventory may prefer a line on its `stock` attribute, which needs arithmetic. Inventory's call.

**B against its provider description [run]**: the assumed ledger lines generate `features/ledger.feature`, e.g. "Given a line l1 / When the caller decrements the line l1 with an amount / Then the ledger service keeps the line l1". Statically no part (no chaining). The sandbox tests of adr/0003 run them against the ledger's staging copy, plus what the lines cannot say: the units fall by the amount, a decrement below zero refuses atomically under two callers, an increment raises the units. `spec check` on B: 5 violations (`v15n` ledger r1 and the may-refuse r2 share a trigger, `v_m4` ×2, `v_s3` ×1 the may-line's group has no scenario, `v_t13`) [run].

## 4. The trace [run]

`tools/trace.py` runs `spec parse --form` on `realisation.md`, takes the trigger's `request(e1, <port op>, …)` and maps each response act's verb to an operation through the vocabulary:

```text
A                                        B
  25  stock.reserve -> inventory.hold      25  stock.reserve -> ledger.decrement
  40  stock.free    -> inventory.release   36  stock.free    -> ledger.increment
  44  stock.take    -> inventory.consume   40  stock.take    -> -
  56  stock.count   -> inventory.query     48  reach (clock) -> -
  52  notify (inventory's) -> -            52  notify (lapse) -> ledger.increment, stock.free
```

A tool can do this today; a response act is still an event atom, so the script maps verbs itself. The port verb "free" in port r5 and ledger r8 shows as `stock.free`: the port operation's verb doubles as "the units are back", an overload that should get its own word in the port.

## 5. Adapter scenarios vs port conformance scenarios [run]

Realisation (A, @r5): "Given a reservation r1 / When the ordering service frees the reservation r1 / Then the reservation r1 has the entry e1 / And the stock service releases the allocation a1 / And the entry e1 has the allocation a1 / And the stock service completes the reservation r1". Port conformance (stock-port @r2): "Given a reservation r1 / When the ordering service frees the reservation r1 / Then the stock service completes the reservation r1".

| | conformance | realisation |
|---|---|---|
| perspective | black-box | white-box |
| words | the port's only | provider calls and the adapter's store |
| same for every adapter | yes | no |
| run against | the adapter with its provider (sandbox, published stub, real) | the adapter with a provider stub generated from the provider area |
| checks | the port lines hold | the adapter does what its lines say, call by call |

## 6. A swap of provider

A for B: a new folder `stock-ledger/`, and above it ordering's choice of adapter (a context-level ADR or configuration) [paper]; port and core untouched while the new adapter realises every port line. B does not realise stock-port#r6, which shows as a missing `realises:` id: the count decision reaches ordering through the adapter folder, not by surprise. Ordering's `## Upstreams` entry and `spec/upstreams/` move into the adapter folder as `provider/…` and leave with the old adapter.

## 7. Placement

| option | verdict |
|---|---|
| an area of kind adapter in ordering's spec | no: provider words enter the core's grammar (the "product" clash would hit ordering's own lines) and core lines could use them; `v_m1` guards only areas' imports |
| a separate repository | no: the port and its adapters change together, the port contract is ordering's |
| **a nested context per adapter in ordering's repository** (`ordering/adapters/<name>/` with `spec/`, `features/`, `adr/`, `provider/`) | **recommended**: an isolated grammar, so the vocabularies meet only there; the port area and capability read from the parent at its commit (copied here); the adapter's code beside it |

Today a nested id is refused: `id … is not bounded-context/<owner>/<product>/<context name>` [run]; the example used a sibling-style id.

## 8. The card processor, charge at collect [paper]

The provider area carries the processor's assumed words (payment, return, webhooks as notifications), the adapter area a "pending charge" entry; secure keeps an entry and completes, cancel drops it and completes, collect creates the payment, cleared → `settled`, declined → `bounced`. Every charges-port line would be L8-entailed by realisation lines alone; the business change of the second example (declines only after confirmation) is again invisible to the check: it is frequency, not lines.

## 9. What the plugin would need, in order

1. An adapter spec kind: `kind: adapter`, a nested id form, `realises:`, `providers:`, `assumed:` read, `adr/` and `provider/` accepted by the layout check.
2. Port import: the parent's port area and capability read by path and commit, not copied.
3. Provider import: a published contract turned into a provider area and capability, with a recorded word-rename map for clashes ("product" → "stocked product"); assumed descriptions marked.
4. Requests in a response read as requests, with arguments ("hold … with the quantity of the order"); this also fixes `v_m7`/`v_m4` for ports and gives the trace without a script.
5. Actor identity across vocabularies ("the client" is the stock adapter), and an adapter area relating a port object to a provider object.
6. A realises check: every `realises:` id L8-entailed, else a finding; multi-hop premises (an adapter act requesting a provider operation fires the provider's lines, a provider response fires realisation triggers), which makes stock-port#r5's gap name holding#r9.
7. State invariants (port state ↔ adapter store), so the L1s found here can be stated and used as premises.
8. Trace and impact: a `spec trace` command, and an impact check of a new provider contract version against it.
9. Requests from gaps: a draft `work request` from each port line not entailed for want of a provider line.
10. Conformance running: the port's scenarios against each adapter, assumed provider scenarios against a sandbox on a schedule, realisation scenarios against a stub generated from the provider area.
