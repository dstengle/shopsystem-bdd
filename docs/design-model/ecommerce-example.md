# The language, read as sentences

Version 4, 2026-10-24. A small product written in the design, then read
back as statements. Every statement is one artifact or one edge from
`design-model.md`, in a sentence form from `grammar.md` §6. If a
statement can't be formed, the design is missing something; if one can be
formed that shouldn't be, the grammar is too loose. Both are at the end.

## 1. The product

**Product-vision.** A small online shop for one maker: shoppers find,
keep and buy what she has made; nothing a marketplace needs.

**Jobs.**

| job | when | narrator | wants |
|---|---|---|---|
| `keep-an-item-for-later` | she sees an item she isn't ready to buy | a shopper | to keep it so she can find it later |
| `buy-what-is-in-the-cart` | she has what she wants | a shopper | to pay and know it's coming |
| `sell-only-what-exists` | she finishes a batch | the maker | the shop to offer only what she has |

**Context-map.** Narrators are roles from the jobs, shared across seams;
each bounded-context names the ones its capabilities speak for.

| bounded-context | narrators | contract | owner |
|---|---|---|---|
| `shopping` | a shopper | — (nothing pins it) | us |
| `catalog` | a shopper; the maker | v5 | us |
| `account` | a shopper | v3.2 | us |
| `payments` | — | 2024-06 | external |

| context-seam | pattern | pin |
|---|---|---|
| `catalog–shopping` | open host, published language; customer/supplier | shopping pins catalog v5 |
| `account–shopping` | open host, published language; customer/supplier | shopping pins account v3.2 |
| `payments–shopping` | conformist | shopping pins payments 2024-06 |

**Capabilities**, with what stands on each.

| capability | narrator | serves | using |
|---|---|---|---|
| `shopping/browse-items` | a shopper | keep-an-item-for-later | catalog/item-lookup |
| | | buy-what-is-in-the-cart | catalog/item-lookup, catalog/stock-levels |
| `shopping/saved-items` | a shopper | keep-an-item-for-later | account/customer-lists, catalog/item-lookup |
| `shopping/cart` | a shopper | buy-what-is-in-the-cart | catalog/stock-levels, account/sessions |
| `shopping/checkout` | a shopper | buy-what-is-in-the-cart | payments/charge, account/sessions |
| `catalog/item-lookup` | a shopper | keep-an-item-for-later; buy-what-is-in-the-cart | — |
| `catalog/stock-levels` | the maker | buy-what-is-in-the-cart; sell-only-what-exists | — |
| `catalog/item-entry` | the maker | sell-only-what-exists | — |
| `account/customer-lists` | a shopper | keep-an-item-for-later | — |
| `account/sessions` | a shopper | buy-what-is-in-the-cart | — |
| `payments/charge` | (external) | buy-what-is-in-the-cart | — |

**Design-decisions** (a few; `summary` shown).

| design-decision | owner | summary | revisit_when |
|---|---|---|---|
| `saved-list-lives-in-account` | shopping | the list is per-customer state held by account; shopping holds none | a save has to work without a customer session |
| `no-guest-saving` | shopping | a shopper not signed in is asked to sign in before saving | sign-in prompts from Save are abandoned more than completed |
| `customer-state-is-opaque` | account | account never knows what a key means | — |
| `stock-is-the-makers-word` | catalog | stock levels come only from item-entry, never inferred | a channel other than the maker needs to adjust stock |
| `per-customer-state-includes-named-lists` | seam account–shopping | supersedes `per-customer-state-is-key-value`; cites request `account/q7` | — |

**Capability-requirements** (two).

- `shopping/saved-items#r1`: *When a signed-in shopper saves an item,
  shopping shall show it as saved wherever it appears and list it in her
  Saved list.* Formulated as acceptance-scenario "saving follows the
  shopper across devices".
- `account/customer-lists#r2`: *When a shopper's named list is read,
  account shall return its keys newest first, with each key's time.*
  Formulated as "a list reads newest first".

## 2. Standing statements

**The product-vision orders job J before job J′.**
- The product-vision orders `buy-what-is-in-the-cart` before `keep-an-item-for-later`.

**Job J: when S, N wants O.**
- `keep-an-item-for-later`: when she sees an item she isn't ready to buy, a shopper wants to keep it so she can find it later.

**Bounded-context C is on the context-map; its contract is V.**
- `account` is on the context-map; its contract is v3.2.
- `payments` is on the context-map; it is external; its contract is 2024-06.

**Seam C1–C2 is P; C2 pins C1 at V.**
- `account–shopping` is open host with a published language, customer/supplier; `shopping` pins `account` at v3.2.

**Capability C/K has narrator N.**
- `catalog/item-entry` has narrator the maker.

**C/K has requirement #rN: R, formulated as S.**
- `account/customer-lists` has requirement #r2: "When a shopper's named list is read, account shall return its keys newest first, with each key's time", formulated as "a list reads newest first".

**C/K rests on D.**
- `shopping/saved-items` rests on `saved-list-lives-in-account` and `no-guest-saving`.

**D: summary; revisit when W. D supersedes D′.**
- `no-guest-saving`: a shopper not signed in is asked to sign in before saving; revisit when sign-in prompts from Save are abandoned more than completed.
- `per-customer-state-includes-named-lists` supersedes `per-customer-state-is-key-value`.

**C/K serves J using [C′/K′ …].**
- `shopping/saved-items` serves `keep-an-item-for-later` using `account/customer-lists` and `catalog/item-lookup`.
- `catalog/stock-levels` serves `sell-only-what-exists` using nothing.

**C/K depends on C′/K′.** *(derived)*
- `shopping/checkout` depends on `payments/charge` and `account/sessions`.
- `catalog/item-lookup` depends on nothing.

**The path of J.** *(derived)*
- The path of `keep-an-item-for-later` is `shopping/browse-items` → `catalog/item-lookup`; `shopping/saved-items` → `account/customer-lists`, `catalog/item-lookup`.
- The path of `sell-only-what-exists` is `catalog/item-entry`; `catalog/stock-levels`. It crosses no seam.

## 3. One job, as a chain of trees

The `keep-an-item-for-later` job, from the first remark to built. Three
trees, one a level, chained by two requests. No `part_of` crosses a seam.

```
product level
job-thread save-an-item-for-later   of keep-an-item-for-later; enters shopping       priority 2; built
  sources: observation 31 (support thread 2026-09-28)
  ├─ job-proposal "keep an item for later"                  approved 2026-09-29; merged
  └─ request shopping/q3                                     to shopping; delivered

shopping
initiative 12 (capability-change)   fulfils shopping/q3                                done
  └─ capability-proposal saved-items-2026-09-29              approved 2026-09-30; merged
     ├─ work-item shopping/saved-items/0   enabling, for /1: the suite under 60 s     green
     ├─ work-item shopping/saved-items/1   capability: cross-device save; raises account/q7    green
     └─ work-item shopping/saved-items/2   capability: item gone from the catalog     green

account
initiative 21 (capability-change)   fulfils account/q7                                 done
  └─ capability-proposal customer-lists-2026-10-01           approved; merged
     └─ work-item account/customer-lists/1                   capability: named lists  green
```

Read as statements:

**Job-thread T of J enters C, crosses S; priority N; sources R.**
- Job-thread `save-an-item-for-later` of `keep-an-item-for-later` enters `shopping`, crosses `account–shopping` and `catalog–shopping`; priority 2; sources observation 31.

**Job-proposal P argues job J, part of X.**
- Job-proposal "keep an item for later" argues job `keep-an-item-for-later`, part of job-thread `save-an-item-for-later`.

**Request Q from A to C, part of T: lines.**
- Request `shopping/q3` from the product level to `shopping`, part of job-thread `save-an-item-for-later`: "When a signed-in shopper saves an item, shopping shall list it in her Saved list on every device she signs in on"; "When a saved item is no longer in the catalog, shopping shall show it in her Saved list as gone."

**Initiative I (K) in C fulfils Q: summary.**
- Initiative 12 (capability-change) in `shopping` fulfils `shopping/q3`: a shopper keeps an item she isn't ready to buy; sources observation 31.
- Initiative 21 (capability-change) in `account` fulfils `account/q7`: named per-customer lists.

**Capability-proposal P argues C/K, adds/changes/removes [#r…], part of X.**
- Capability-proposal `saved-items-2026-09-29` argues `shopping/saved-items`, adds r1–r7, part of initiative 12.
- Capability-proposal `customer-lists-2026-10-01` argues `account/customer-lists`, adds r1–r6, part of initiative 21.

**Work-item W is K, accepts A, blocked by B, depends on D, for W′, raises Q, part of X.**
- Work-item `shopping/saved-items/1` is a capability work-item, accepts "saving follows the shopper across devices", depends on `account/customer-lists`, raises `account/q7`, part of capability-proposal `saved-items-2026-09-29`.
- Work-item `shopping/saved-items/0` is an enabling work-item, check "the suite runs under 60 s in parallel", for `shopping/saved-items/1`, part of the same proposal.
- Work-item `account/customer-lists/1` is a capability work-item, accepts "a list reads newest first" and "appending a held key changes nothing", part of capability-proposal `customer-lists-2026-10-01`.

### Request 7, negotiated

**Request Q from A to C, raised for Q0: lines.** Shopping's work-item
`shopping/saved-items/1` found that "saving follows the shopper across
devices" goes red against account v3, which holds one key-value map per
customer. Shopping writes request `account/q7` from `shopping` to
`account`, raised for `shopping/q3`, through account's tool. Its lines
are in the job's narrator (a shopper) and account's published terms
(named list, key); the red scenario is evidence in its text:

1. When a shopper saves an item, account shall append its key to her named list with the time of the save.
2. When a shopper's named list is read, account shall return its keys newest first, with each key's time.
3. When a shopper saves one item from two devices at once, account shall keep it in her named list once.

Status `open`; account's turn.

**Line Q#N is O.** Account answers each line:
- Line `account/q7`#1 is accepted.
- Line `account/q7`#2 is accepted.
- Line `account/q7`#3 is rewritten: "When a key already in a named list is appended, account shall leave the list unchanged." Account knows keys, not devices.

Status `awaiting-asker`. Shopping confirms the rewrite of line 3 still
meets its need: two devices saving one item append one key twice. Status
`awaiting-upstream`; account marks line 3 accepted. Every line is final
and one is accepted, so the request is `accepted`, and account starts
initiative 21 to fulfil it. Account's gate judges its own
capability-proposal `customer-lists-2026-10-01`, which the three accepted
lines became.

**Request Q is resolved by RID at V.**
- Request `account/q7` is resolved by `account/customer-lists#r1` at v3.2, `account/customer-lists#r2` at v3.2, `account/customer-lists#r4` at v3.2.

When initiative 21 is done, `account/q7` is `delivered`. Shopping bumps
its pin to v3.2; `shopping/saved-items/1` goes green; initiative 12 is
done, since the one request it raised is delivered; `shopping/q3` is
delivered; the job-thread is built, since every request part of it is.
Account never read shopping's work-items, and shopping never read
account's: each read its own files and the status of the requests it
raised.

**What each left standing.**
- Job-proposal → the job, ordered by the product-vision.
- Delivery of `shopping/q3` → `serves keep-an-item-for-later using account/customer-lists, catalog/item-lookup` on `shopping/saved-items`, written by shopping; the entry scenario as the job's acceptance test.
- Delivery of `account/q7` → `serves keep-an-item-for-later` on `account/customer-lists`, written by account, which reached the job through `raised_for` and `shopping/q3`.
- Capability-proposals → `shopping/saved-items#r1`–`#r7` and two design-decisions; `account/customer-lists#r1`–`#r6`; then their scenarios, once `formulated`.
- Request `account/q7` → the seam decision `per-customer-state-includes-named-lists`.
- Work-items → scenarios green.

The trace from `account/customer-lists/1` back: part_of `customer-lists-2026-10-01` → part_of initiative 21 → fulfils `account/q7` → raised for `shopping/q3` → part_of job-thread `save-an-item-for-later` → source observation 31. Nobody wrote it, and it never passes through shopping's work-items.

Three other pieces of work, one line each:

- Request `shopping/q5` from shopping itself, sources review-finding 8: "If an item is out of stock, then shopping shall refuse to add it to the cart." Initiative 14 (defect) fulfils it: one work-item `shopping/cart/4`, accepts "an out-of-stock item cannot be added", part of initiative 14.
- Request `catalog/q2` from catalog itself, sources measurement `bench-2026-10-05`. Initiative 15 (capability-change) fulfils it: capability-proposal `stock-levels-cache` arguing `catalog/stock-levels`, part of initiative 15; two work-items under it, one a guarantee with check "a stock read under 20 ms at 10,000 items".
- Job-thread `see-what-sold-today`, sources observation 40 (the maker's email): a job-proposal with narrator the maker, part of it; the thread enters `catalog` and raises request `catalog/q4`; it crosses nothing.

## 4. Questions the language answers

| question | read | answer |
|---|---|---|
| What breaks if account changes `customer-lists`? | every `serves … using` naming it | `shopping/saved-items`, hence `keep-an-item-for-later` |
| What does the shop do for `buy-what-is-in-the-cart`? | the path | browse-items → item-lookup, stock-levels; cart → stock-levels, sessions; checkout → charge, sessions |
| Why does `customer-lists` have named lists? | `#r1` → proposal `customer-lists-2026-10-01` → initiative 21 → fulfils `account/q7` → raised for `shopping/q3` → job-thread → source | the support thread of 2026-09-28 |
| What is account being asked for right now? | account's requests, by status and turn | none open; `account/q7` delivered |
| What should shopping start next? | shopping's accepted requests with no initiative, ranked | `shopping/q5` (initiative 14), then whatever is ranked next |
| Is initiative 12 done? | its parts closed; the requests it raised delivered | done |
| Which jobs cross no seam? | paths within one context | `sell-only-what-exists`, `see-what-sold-today` |
| What would reopen `no-guest-saving`? | its `revisit_when` | sign-in prompts from Save abandoned more than completed |

## 5. Statements the grammar refuses

Each with the rule and the corrected form.

- *Request `account/q7` from `shopping/saved-items` needs an ordered per-customer list.* — `needs TEXT` is gone; a request is lines in EARS, and it carries the asker's context, not a capability.
  → Request `account/q7` from `shopping` to `account`, raised for `shopping/q3`: "When a shopper saves an item, account shall append its key to her named list with the time of the save"; ….
- *Capability-proposal `customer-lists-2026-10-01`, part of request `account/q7`.* — A request has no parts; a request's fulfilment is account's own initiative (v18b).
  → Capability-proposal `customer-lists-2026-10-01`, part of initiative 21, which fulfils `account/q7`.
- *Work-item `account/customer-lists/1` blocked by `shopping/saved-items/1`.* — No id but a request's crosses a seam (v18c). Account's work does not wait on shopping's.
  → Shopping's `shopping/saved-items/1` raises `account/q7`; shopping's initiative waits on the request's status.
- *Initiative 12 (job): a shopper keeps an item.* — `job` is not an initiative kind; a job is a job-thread at the product level.
  → Job-thread `save-an-item-for-later` of `keep-an-item-for-later`; initiative 12 (capability-change) in `shopping` fulfils `shopping/q3`, part of it.
- *Initiative 12 (capability-change) in `shopping`*, fulfilling nothing. — Every initiative fulfils exactly one request (v16a).
  → Initiative 12 (capability-change) in `shopping` fulfils `shopping/q3`.
- *Request `shopping/q5` from shopping itself.* — Neither part of a thread nor citing an origin (v17).
  → Request `shopping/q5` from shopping itself; sources review-finding 8.
- *Request `account/q7` is resolved by "a list reads newest first".* — A resolution names a requirement by id, never a scenario (v3).
  → Request `account/q7` is resolved by `account/customer-lists#r2` at v3.2, ….
- *Work-item `shopping/saved-items/1` serves `keep-an-item-for-later`.* — Parts are `part_of`; capabilities serve jobs.
  → Work-item `shopping/saved-items/1` is part of capability-proposal `saved-items-2026-09-29`; `shopping/saved-items` serves `keep-an-item-for-later`.
- *`shopping/saved-items` depends on `sharing/share-links`.* — No `serves … using` names it.
  → For it to, a request must cross a `sharing–shopping` seam and its delivery leave `serves <job> using sharing/share-links`.
- *Work-item `shopping/saved-items/1`, part of job-thread `save-an-item-for-later`.* — Job-threads own no work-items (v_b3).
  → Work-item `shopping/saved-items/1`, part of capability-proposal `saved-items-2026-09-29`, part of initiative 12.
- *Job-thread `save-an-item-for-later`, part of initiative 12.* — Both are roots; nothing is above either (v9f).
  → Initiative 12 fulfils `shopping/q3`, which is part of the job-thread.
- *Initiative 15 sources decision-argument `stock-is-the-makers-word`.* — Only an origin is a source.
  → Request `catalog/q2` and initiative 15 source measurement `bench-2026-10-05`; the decision-argument is read when the decision is questioned.
- *`catalog/item-lookup` serves `keep-an-item-for-later` using `shopping/saved-items`.* — `using` points the way the pin points.
  → `catalog/item-lookup` serves it using nothing; `shopping/saved-items` serves it using `catalog/item-lookup`.
- *Request `sharing/q1` from `shopping` to `sharing`.* — No `sharing–shopping` seam (v7); a map-escalation is raised.
  → Map-escalation 9, no-seam, part of initiative 12, asks the product role for a `sharing–shopping` seam.
- *Capability-proposal `saved-items-2026-11-02` changes "When a signed-in shopper saves an item…".* — Requirements are referenced by id, never by text.
  → Capability-proposal `saved-items-2026-11-02` changes `shopping/saved-items#r1`.
- *Acceptance-scenario "a list reads newest first" tests `account/customer-lists`.* — A scenario tests one requirement, by id; the capability is reached through it.
  → Acceptance-scenario "a list reads newest first" is formulated from `account/customer-lists#r2`.

## 6. What the exercise found

- Upstream capabilities need `serves` entries too. Under v4 each context
  writes them on its own capabilities when a request it fulfilled is
  delivered, reaching the job through the request chain.
- An external bounded-context's capability (`payments/charge`) is a node
  we don't own but must name, so `using` can point at it.
- A job inside one bounded-context still has a path.
- Account's capability-proposal is in account's own tree, under its own
  initiative; "what is account being asked for" is a read of its
  requests, by status and whose turn it is.
- The negotiation did work v3 hid: account could not promise anything
  about devices, so it rewrote line 3 in its own terms and shopping
  confirmed the rewrite.
- Narrators are the jobs' roles. Where v3 named account's narrator "a
  client of the account API", v4's request lines kept the job's narrator,
  a shopper, so account's capabilities speak for a shopper too.
- A defect is one request, one initiative and one work-item; the price of
  a clean schema.
- With requirement ids, the gate approves a list of ids, a request's
  resolution names them, and a scenario's title can change without
  anything rebinding.
