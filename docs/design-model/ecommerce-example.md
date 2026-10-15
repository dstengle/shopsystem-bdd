# The language, read as sentences

Version 3, 2026-10-15. A small product written in the design, then read
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

**Context-map.**

| bounded-context | narrator | contract | owner |
|---|---|---|---|
| `shopping` | a shopper | — (nothing pins it) | us |
| `catalog` | a client of the catalog API; the maker, at the admin command line | v5 | us |
| `account` | a client of the account API | v3.2 | us |
| `payments` | a client of the payments API | 2024-06 | external |

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
| `catalog/item-lookup` | a client of the catalog API | keep-an-item-for-later; buy-what-is-in-the-cart | — |
| `catalog/stock-levels` | a client of the catalog API | buy-what-is-in-the-cart; sell-only-what-exists | — |
| `catalog/item-entry` | the maker | sell-only-what-exists | — |
| `account/customer-lists` | a client of the account API | keep-an-item-for-later | — |
| `account/sessions` | a client of the account API | buy-what-is-in-the-cart | — |
| `payments/charge` | (external) | buy-what-is-in-the-cart | — |

**Design-decisions** (a few; `summary` shown).

| design-decision | owner | summary | revisit_when |
|---|---|---|---|
| `saved-list-lives-in-account` | shopping | the list is per-customer state held by account; shopping holds none | a save has to work without a customer session |
| `no-guest-saving` | shopping | a shopper not signed in is asked to sign in before saving | sign-in prompts from Save are abandoned more than completed |
| `customer-state-is-opaque` | account | account never knows what a key means | — |
| `stock-is-the-makers-word` | catalog | stock levels come only from item-entry, never inferred | a channel other than the maker needs to adjust stock |
| `per-customer-state-includes-named-lists` | seam account–shopping | supersedes `per-customer-state-is-key-value`; cites cross-context-request 7 | — |

**Capability-requirements** (two).

- `shopping/saved-items#r1`: *When a signed-in shopper saves an item,
  shopping marks it saved wherever it appears this session, and it is in
  her Saved list.* Formulated as acceptance-scenario "saving follows the
  shopper across devices".
- `account/customer-lists#r2`: *When a client reads a customer's named
  list, account returns its keys newest first, with each key's time.*
  Formulated as "a list reads newest first".

## 2. Standing statements

**The product-vision orders job J before job J′.**
- The product-vision orders `buy-what-is-in-the-cart` before `keep-an-item-for-later`.

**Job J: when S, N wants O.**
- `keep-an-item-for-later`: when she sees an item she isn't ready to buy, a shopper wants to keep it so she can find it later.

**Bounded-context C is on the context-map; its narrator is N; its contract is V.**
- `account` is on the context-map; its narrator is a client of the account API; its contract is v3.2.
- `payments` is on the context-map; it is external; its contract is 2024-06.

**Seam C1–C2 is P; C2 pins C1 at V.**
- `account–shopping` is open host with a published language, customer/supplier; `shopping` pins `account` at v3.2.

**Capability C/K has narrator N.**
- `catalog/item-entry` has narrator the maker.

**C/K has requirement #rN: R, formulated as S.**
- `account/customer-lists` has requirement #r2: "When a client reads a customer's named list, account returns its keys newest first", formulated as "a list reads newest first".

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

## 3. One initiative, as its tree

The `keep-an-item-for-later` job, from intake to done.

```
initiative 12 (job)                                        product intake; priority 2
  sources: observation 31 (support thread 2026-09-28)
  └─ job-proposal "keep an item for later"                  approved 2026-09-29
     └─ job-thread save-an-item-for-later                   enters shopping; built
        ├─ capability-proposal saved-items-2026-09-29       approved 2026-09-30; merged
        │  ├─ work-item shopping/saved-items/0   enabling, for /1: the suite under 60 s     green
        │  ├─ work-item shopping/saved-items/1   capability: cross-device save              green
        │  └─ work-item shopping/saved-items/2   capability: item gone from the catalog     green
        └─ cross-context-request 7                          across account–shopping; delivered v3.2
           └─ capability-proposal customer-lists-2026-10-01  owned by account; merged
              └─ work-item account/customer-lists/1         capability: named lists                green
```

Read as statements:

**Initiative I (K): summary; priority N; sources R.**
- Initiative 12 (job): a shopper keeps an item she isn't ready to buy; priority 2; sources observation 31.

**Job-proposal P argues job J, part of X.**
- Job-proposal "keep an item for later" argues job `keep-an-item-for-later`, part of initiative 12.

**Job-thread T of J enters C, crosses S needing N, part of X.**
- Job-thread `save-an-item-for-later` of `keep-an-item-for-later` enters `shopping`, crosses `account–shopping` needing a saved list that follows the shopper across devices, and `catalog–shopping` needing today's price and stock with a gone item shown as gone; part of the job-proposal.

**Capability-proposal P argues C/K, adds/changes/removes [#r…], part of X.**
- Capability-proposal `saved-items-2026-09-29` argues `shopping/saved-items`, adds r1–r7, part of job-thread `save-an-item-for-later`.
- Capability-proposal `customer-lists-2026-10-01` argues `account/customer-lists`, adds r1–r6, part of cross-context-request 7.

**Cross-context-request Q from C/K across S needs N, part of X.**
- Cross-context-request 7 from `shopping/saved-items` across `account–shopping` needs an ordered per-customer list that survives saves from two devices, part of job-thread `save-an-item-for-later`. Its Need cites "saving follows the shopper across devices" going red against account v3. Account answered with `account/customer-lists#r1`, "When a client appends a key to a customer's named list, account stores it with the time of the append"; delivered at v3.2.

**Work-item W is K, accepts A, blocked by B, depends on D, for W′, part of X.**
- Work-item `shopping/saved-items/1` is a capability work-item, accepts "saving follows the shopper across devices", depends on `account/customer-lists`, part of capability-proposal `saved-items-2026-09-29`.
- Work-item `shopping/saved-items/0` is an enabling work-item, check "the suite runs under 60 s in parallel", for `shopping/saved-items/1`, part of the same proposal.
- Work-item `account/customer-lists/1` is a capability work-item, accepts "a list reads newest first" and "appending a held key changes nothing", part of capability-proposal `customer-lists-2026-10-01`.

**What each left standing.**
- Job-proposal → the job, ordered by the product-vision.
- Job-thread → `serves keep-an-item-for-later using account/customer-lists, catalog/item-lookup` on `shopping/saved-items`; `serves keep-an-item-for-later` on `account/customer-lists` and `catalog/item-lookup`; the entry scenario as the job's acceptance test.
- Capability-proposals → `shopping/saved-items#r1`–`#r7` and two design-decisions; `account/customer-lists#r1`–`#r6`; then their scenarios, once `formulated`.
- Cross-context-request 7 → the seam decision `per-customer-state-includes-named-lists`.
- Work-items → scenarios green.

The trace from `account/customer-lists/1` back: part_of `customer-lists-2026-10-01` → part_of request 7 → part_of job-thread → part_of job-proposal → initiative 12 → source observation 31. Nobody wrote it.

Three other initiatives, one line each:

- Initiative 14 (defect), owner shopping, source review-finding 8: one work-item `shopping/cart/4`, accepts "an out-of-stock item cannot be added", part of initiative 14.
- Initiative 15 (capability-change), owner catalog, source measurement `bench-2026-10-05`: capability-proposal `stock-levels-cache` arguing `catalog/stock-levels`, part of initiative 15; two work-items under it, one a guarantee with check "a stock read under 20 ms at 10,000 items".
- Initiative 16 (job), owner product, source observation 40 (the maker's email): job-proposal `see-what-sold-today` with narrator the maker; its job-thread enters `catalog`; crosses nothing.

## 4. Questions the language answers

| question | read | answer |
|---|---|---|
| What breaks if account changes `customer-lists`? | every `serves … using` naming it | `shopping/saved-items`, hence `keep-an-item-for-later` |
| What does the shop do for `buy-what-is-in-the-cart`? | the path | browse-items → item-lookup, stock-levels; cart → stock-levels, sessions; checkout → charge, sessions |
| Why does `customer-lists` have named lists? | `#r1` → proposal `customer-lists-2026-10-01` → part_of request 7 → … → initiative 12 → source | the support thread of 2026-09-28 |
| What is account being asked for right now? | parts in account awaiting acceptance | none; request 7 delivered |
| What should shopping start next? | shopping's intake backlog, ranked | initiative 14 (defect), then whatever product ranks |
| Is initiative 12 done? | its status; every part closed | done |
| Which jobs cross no seam? | paths within one context | `sell-only-what-exists`, `see-what-sold-today` |
| What would reopen `no-guest-saving`? | its `revisit_when` | sign-in prompts from Save abandoned more than completed |

## 5. Statements the grammar refuses

Each with the rule and the corrected form.

- *Acceptance-scenario "saving follows the shopper across devices" needs `account/customer-lists`.* — A scenario is evidence, never on a `needs` edge. It went red against account v3; the need was the capability's, carried by the request.
  → Cross-context-request 7 from `shopping/saved-items` across `account–shopping` needs an ordered per-customer list; its Need cites the scenario going red as evidence.
- *Cross-context-request 7 depends on `account/customer-lists`.* — A request needs; only a capability depends.
  → Cross-context-request 7 needs `account/customer-lists`; `shopping/saved-items` depends on `account/customer-lists`.
- *Work-item `shopping/saved-items/1` serves `keep-an-item-for-later`.* — Parts are `part_of`; capabilities serve jobs.
  → Work-item `shopping/saved-items/1` is part of capability-proposal `saved-items-2026-09-29`; `shopping/saved-items` serves `keep-an-item-for-later`.
- *`shopping/saved-items` depends on `sharing/share-links`.* — No `serves … using` names it.
  → For it to, a job-thread must cross a `sharing–shopping` seam and leave `serves <job> using sharing/share-links`.
- *`shopping/saved-items` needs `account/customer-lists`.* — Standing artifacts don't need.
  → `shopping/saved-items` serves `keep-an-item-for-later` using `account/customer-lists`.
- *Work-item `shopping/saved-items/1`, part of job-thread `save-an-item-for-later`.* — Job-threads own no work-items.
  → Work-item `shopping/saved-items/1`, part of capability-proposal `saved-items-2026-09-29`, which is part of the job-thread.
- *Cross-context-request 7, priority 1, in account's intake.* — A part has no priority and is never in intake; account's fulfilment of it is part of initiative 12.
  → Cross-context-request 7 is a part awaiting acceptance in `account`; account sequences it by initiative 12's priority.
- *Initiative 12, part of job-proposal "keep an item for later".* — An initiative is the root; nothing is above it.
  → Job-proposal "keep an item for later", part of initiative 12.
- *Initiative 15 sources decision-argument `stock-is-the-makers-word`.* — Only an origin is a source.
  → Initiative 15 sources measurement `bench-2026-10-05`; the decision-argument is read when the decision is questioned.
- *`catalog/item-lookup` serves `keep-an-item-for-later` using `shopping/saved-items`.* — `using` points the way the pin points.
  → `catalog/item-lookup` serves it using nothing; `shopping/saved-items` serves it using `catalog/item-lookup`.
- *Job-thread `save-an-item-for-later` crosses `shopping–sharing`.* — No such seam; a map-escalation is raised and the thread stays proposed.
  → Map-escalation 9, no-seam, part of job-thread `save-an-item-for-later`, asks the product role for a `sharing–shopping` seam.
- *Capability-proposal `saved-items-2026-11-02` changes "When a signed-in shopper saves an item…".* — Requirements are referenced by id, never by text.
  → Capability-proposal `saved-items-2026-11-02` changes `shopping/saved-items#r1`.
- *Acceptance-scenario "a list reads newest first" tests `account/customer-lists`.* — A scenario tests one requirement, by id; the capability is reached through it.
  → Acceptance-scenario "a list reads newest first" is formulated from `account/customer-lists#r2`.

## 6. What the exercise found

- Upstream capabilities need `serves` entries too, written at the
  job-thread's close for every capability its path reached.
- An external bounded-context's capability (`payments/charge`) is a node
  we don't own but must name, so `using` can point at it.
- A job inside one bounded-context still has a path.
- A part owned by another bounded-context (account's capability-proposal)
  is still in the initiative's tree; "what is account being asked for" is
  a query over parts, not a backlog.
- A defect initiative is one record above one work-item; the price of a
  clean schema, and it keeps `priority` on exactly one kind.
- With requirement ids, the gate approves a list of ids and a scenario's
  title can change without anything rebinding; the plugin's `rebind`
  tool was compensating for the absence of ids.
