---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-25-a-worked-example-of-the-product-layer-in-a-compact-shop-jobs-assigned-to-contexts-and-served-by-capabilities
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-25
---

# A worked example of the product layer in a compact shop: jobs assigned to contexts and served by capabilities

## 1. What this example does and how it was made

This example tries the person's design of a compact shop's product layer on this repository's own product,
shopsystem. It covers:

- the product layer's files, sketched;
- six jobs to be done, each assigned to a context and served by one capability;
- the derived trace of one job (build and review ready work), computed by a script;
- the checks the layer makes possible, and what each finds today;
- what the tooling would need, and the open questions.

Only `main` was read: `spec/`, `scripts/` and one background record. Nothing tracked was changed. Two read-only
scripts in `support/` produce every figure below:

- `job_trace.py` imports the plugin's own reader (spec_language, spec_lf, spec_vocabulary, domain_model);
- `product_check.py` reads the product layer sketch and the capability files, and runs `job_trace.py` once per job.

`python3 scripts/spec facts` (all 17,820 facts, about 3 s with the parse cache warm) was used to cross-check what
model_domain_lines sees. `spec parse --form` was used twice, on batches#r100 and batches#r111.

The design stands on these decisions:

- 0128: the product declares the subdomains;
- 0129: a shop is a management and execution unit;
- 0130: the language toolchain is a context of a supporting subdomain;
- 0131: measurement sits in execution, opening a batch stays one commit, and the spec stays one flat `spec/`;
- 0133: tracking and execution are one work-management context with two modules;
- 0134: port request, long-running process and saga are derived, never labelled.

The product layer's words are kept apart from the mechanisms. Git, GitHub, pull requests and `gh` appear here only
where a finding names code or a capability's existing words.

## 2. The product layer, sketched

### 2.1 Where it lives in a compact shop

A compact shop is one repository that hosts its contexts and holds the product layer beside them. The proposal:

| path | form (proposed name) | holds |
|---|---|---|
| `product/index.md` | product identity | id (`product/missingmass.io/shopsystem`), purpose, actors |
| `product/jobs.md` | jobs to be done | one entry a job: id, actor, statement |
| `product/domain.md` | domain map | subdomains (type, jobs), contexts (subdomains addressed, hosting shop), assignments |
| `.shop/shop.toml` | shop | the shop's id, `product = "product/"` when it holds the layer, `[[hosts]]` (context id, spec root) |
| `spec/capabilities/<name>.md` | capability (existing) | new frontmatter `serves: job/missingmass.io/shopsystem/j<n>` |

Why these places:

- `product/` sits at the root, beside `spec/`, not under `.shop/`. The product layer is specification (standing
  artifacts), and `.shop/` is management (decision 0129 configures the shop in `.shop`, not the product).
- `.shop/shop.toml` names what the shop hosts. A shop that is not compact has no `product` key, and the product layer
  then lives in the product's own repository (question Q6).

The sketch files are in `support/product/` and `support/dot-shop/shop.toml`.

### 2.2 Product identity (`product/index.md`, excerpt)

```
---
id: product/missingmass.io/shopsystem
title: shopsystem
form: product identity
---
## Purpose
A behaviour-driven workflow for bounded contexts kept in repositories: ...
## Actors
- **the person** (actor/missingmass.io/shopsystem/the-person): the one who keeps a bounded context ...
- **a session** (actor/missingmass.io/shopsystem/session): an agent working for the person in a context ...
- **a downstream context** (actor/missingmass.io/shopsystem/downstream-context): another context that obtains
  published contracts and raises requests.
## Contexts' ids
`bounded-context/missingmass.io/shopsystem/<name>`, flat under the product, whatever shop hosts it (0129).
```

The actors are the product's. Each context still declares its own actor (today `spec/model/tracking.md` has the only
`actor the person`), and an adapter maps them. A product actor is then a name the contexts' actors are checked
against, not a model element of any context.

### 2.3 Jobs to be done (`product/jobs.md`)

Each job is a structured entry, not a grammar-4 line:

```
## [j2] Build and review ready work as one change
- actor: the person
- statement: When items are ready, the person wants them built together, each in its own workspace, and reviewed
  once as one change, so they can merge behaviour whose scenarios pass and whose review findings are settled.
```

| job | title | actor |
|---|---|---|
| j1 | Shape work into checkable lines | the person |
| j2 | Build and review ready work as one change | the person |
| j3 | Exchange requests between contexts | the person |
| j4 | Publish and obtain contracts | the person |
| j5 | Upgrade a repository to a new release | the person |
| j6 | Measure a batch | the person |

Ids: `job/missingmass.io/shopsystem/j<n>`, short form `job/j<n>`. They follow `item/<path>/b<n>` (shop_ids), with the
product path in place of the context path.

### 2.4 Domain map (`product/domain.md`)

The subdomains are taken from the disentangling example's inventory, with one correction:

- s2 is **supporting**, as decision 0130 says. The example's table had it as core.

| subdomain | type | jobs |
|---|---|---|
| s1 requirements specification | core | j1, j4 |
| s2 controlled requirements language | supporting | j1, j4 |
| s3 work planning | supporting | j1 |
| s4 collaboration between contexts | supporting | j3, j4 |
| s5 the person's direction | supporting | (none) |
| s6 delivery | supporting | j2 |
| s7 delivery economics | generic | j6 |
| s8 codebase insight | generic | (none) |
| s9 release adoption | generic | j5 |

The contexts follow decisions 0130, 0131 and 0133. All five are hosted by `shop/missingmass.io/shopsystem-bdd`:

| context | addresses | today (where it sits in the one context `shopsystem-bdd`) |
|---|---|---|
| `.../specification` | s1 | area:specification |
| `.../language` | s2 | cap:parsing cap:reading cap:consistency (plus `grammar/`) |
| `.../work-management` | s3 s4 s5 s6 s7 | area:tracking area:execution area:measurement |
| `.../analysis` | s8, s1 | area:analysis |
| `.../upgrades` | s9 | area:upgrades |

The `today` column is the one concession to the present. Today a single context, `shopsystem-bdd`, holds every
capability. Without that column the checks would have nothing to resolve a capability's context by until the split.
An alternative is to assign every job to `shopsystem-bdd` now and reassign each job at the split (question Q7).

Assignments are the product's decision, kept in the domain map:

```
| job | assigned to |
|---|---|
| j1 | bounded-context/missingmass.io/shopsystem/work-management |
| j4 | bounded-context/missingmass.io/shopsystem/specification |
...
```

Relations between contexts are derived, never written. Today nothing can be derived:

- there is no driven port, and `spec/adapters/` holds only `cli.toml`;
- there is no obtained contract;
- there is no `## Upstreams` entry;
- the five future contexts reach each other through state (§4.4), not requests.

## 3. Jobs, their contexts and serving capabilities

Each capability below was picked from its `narrator:` and `## Purpose`. The serving lines are proposed in
`support/serves.overlay`; no capability has `serves:` today.

| job | assigned context | serving capability | narrator | actor matches | lines | notes |
|---|---|---|---|---|---|---|
| j1 | work-management | `items` | the person | yes | 60 | `drafting` (65 lines) writes the lines; `items` readies them. Neither requests the other. |
| j2 | work-management | `batches` | the person | yes | 46 | `reviews` (12) and `review-guarantees` (10) govern the same service's `submit` and `reopen` (§4). |
| j3 | work-management | `context-requests` | the person | yes | 57 | Both sides are "the person", of two different contexts. |
| j4 | specification | `checking` | the person | yes | 70 | Only about 19 of its lines are about contracts (prepare, publish, fetch, obtain). `checking#r78`/`r79`'s requester is `downstream context`, not the person. |
| j5 | upgrades | `upgrades` | the person | yes | 39 | |
| j6 | work-management | `measurement` | the person | yes | 9 | Measurement belongs to work management by 0131 and 0133. |

What the table shows:

- **Every serving capability's narrator is "the person"**, so the narrator check passes for all six. It passes only
  because each job names one actor. j4 has two in practice: the person publishes, a downstream context fetches.
  j3 likewise has an asker and an upstream.
- **Narrators that are not the product's actors.** Six live capabilities are narrated by a session:
  - `request-watch`, `quotes` and `directives`: "a session";
  - `shaping-guarantees`: "the brainstorming session";
  - `review-guarantees`: "the session that started a review";
  - `trials`: "the session that started a trial".

  None of these is a model actor. `spec/model/` declares only `actor the person`.
- **Serving capability versus job.** `checking` serves j4, but most of its lines are about checking a spec as a whole.
  If a job's lines are all of its serving capability's lines, j4's derived requirements are about 70% unrelated
  (question Q2).
- **Index drift (unrelated to the design).** `spec/index.md` lists `reading` under specification and `parsing` under
  "Retired in 0.31.0". In fact `reading` retired every line (0 live) and `parsing` holds 22 live lines in area
  specification.

## 4. Job j2 in depth: the derived trace of "build and review ready work"

Run with:

```
python3 support/job_trace.py . batches --depth 3 --domain support/product/domain.md [--service]
```

The output is in `support/trace-batches.txt` and `support/trace-batches-service.txt`.

### 4.1 The serving capability's lines

`batches` (area execution, context work-management) holds 46 live lines. Their triggers:

| operation requested in the trigger | lines |
|---|---|
| batches.open | 22 |
| batches.finish | 7 |
| batches.amend | 4 |
| batches.park | 3 |
| batches.configure | 3 |
| batches.merge | 3 |
| batches.abandon | 2 |
| batches.monitor | 1 |
| batches.resume | 1 |

`batches.submit` and `batches.reopen` belong to the same service. Their lines live in `reviews` (reviews#r1-r12),
whose frontmatter says `specifies: ..., service batches: submit`. The `batches` capability says `service batches` as
a whole. So one service is split across two capabilities. With `--service`, the trace also seeds every line whose
trigger requests an operation of a service the serving capability specifies. That adds reviews#r1-r12 and
review-guarantees#r1 ("When the batches service submits a batch, `pr-reviewer` shall review the proposed change").

### 4.2 The operations its lines request

Eleven of `batches`' lines name another operation in their response:

| line | response act | operation | how the logical form holds it | seen by `spec facts` |
|---|---|---|---|---|
| r100 | deliver the item | backlog.deliver | `deliver(e2, subject, object)`, an event | no |
| r101 | reopen the item | backlog.reopen | event | no |
| r105 | resolve the context request | context requests.resolve | event | no |
| r106 | reopen the item | backlog.reopen | event | no |
| r108 | allocate the item | backlog.allocate | event | no |
| r109 | reopen the item | backlog.reopen | event | no |
| r111 | suspend the item with a question | backlog.suspend | `request(e2, backlog.suspend, ...)` + `param` | **yes**: `asks` |
| r112 | restore every item ... `in-batch` | backlog.restore | event | no |
| r107, r110 | not allocate the item | backlog.allocate | negated event | no (rightly) |
| r56 | not ask a question | context requests.ask | negated event (an accidental match of the verb) | no (rightly) |

With `--service`, review-guarantees#r1 adds `reviews.review`, the act `pr-reviewer` performs after a submit.

What the table shows:

- **b578's intent shows in the lines but not in the facts.** All four new operations (allocate, deliver, restore,
  suspend) and the two existing ones (reopen, resolve) are named as response acts. But only `suspend`, the one that
  carries a parameter, becomes a request in the logical form.
- **Why.** spec_lf_request reads a response's act as a request only "with its parameters" (module map). A
  parameterless `deliver the item` stays an ordinary event. So:
  - model_domain_lines' `asks` and model.lp's v_m7 see 1 of 8 requests;
  - spec_entail_chain's request chain (b545) follows 1 of 8.

  The script works around this. It maps a response verb to an operation through the vocabulary (`→ operation X.Y`),
  and picks the sense by the frame's object kind. For example, `reopen` names both `batches.reopen` and
  `backlog.reopen`; the object `item` picks `backlog.reopen`.

### 4.3 Capabilities and contexts reached

Depth 1 adds the lines that govern each operation reached:

- items#r56-r63 (allocate, deliver, restore, suspend) and items#r31, r32 (reopen);
- context-requests#r13, r51, r55 (resolve).

With `--service`, review-guarantees#r2, r4, r5, r7, r9 and r10 come in (they govern `reviews.review`). Nothing is
reached past depth 1.

Summary of the trace:

```
capabilities in the trace: batches, context-requests, items, review-guarantees, reviews
contexts in the trace: work-management
operations reached: backlog.allocate, backlog.deliver, backlog.reopen (3), backlog.restore, backlog.suspend,
                    context requests.resolve, reviews.review (6)
lines with no reading: none
```

So j2's derived requirement set is 46 + 12 + 10 + 10 + 3 = **81 lines across 5 capabilities, one context**. The
trace touches no other context, which fits j2's one subdomain, s6.

### 4.4 What the trace cannot see today

1. **Reads of another area's state where a request would be.** 24 of the 46 lines name objects declared by the
   specification model in their preconditions: requirement, scenario, rule, construct catalogue, corpus, adapter
   contract, operation table, pack. Many more name tracking's `readiness bar`. Examples:
   - r73: "a requirement of the item violates a rule";
   - r109: "a scenario of the item ... succeeds in a workspace of a batch".

   These are the places where execution today uses specification's work directly (laying lines, checking rules,
   generating scenarios, writing the corpus). After the split they would become requests to specification and
   language, as the disentangling example's ports propose. The trace lists them as `reads <kind>(<area>)` but cannot
   count them as reached contexts. A job trace that counted reads would place j2 in specification and language too.
2. **A state set on another area's object.** r64, when the person opens a batch, "set the language of `universal`
   to `codified-2`". The `capability` object is specification's. This is a set, not a request, so no operation, no
   capability and no context is reached.
3. **A negated set read as a set** (a defect in model_domain_lines). r111 says "... and not set the status of the
   batch to `abandoned`". `Lines.facts` flattens a `not` box (`_atoms` recurses into every box), so it emits
   `sets_from_any(batches#r111, batch, status, abandoned)`. model.lp's `caused/4` then counts the transition
   in-review → abandoned as caused by a line, which hides the w_m5 warning. No other live line sets a batch from
   `in-review` to `abandoned`; only r112 does, from `building`.
4. **The person's and a session's own acts are not requests of a line.** `reviews.conclude` (review-guarantees r6,
   r8) moves the batch to `building` or `awaiting-merge`. A session requests it; no line's response asks for it, so a
   trace that follows requests from `batches` never arrives there. The same holds for dispatching `pr-reviewer` and
   for the person's merge. The job's coordination partly lives in the actor, not in the serving capability.
5. **A verb repeated in a guarantee.** review-guarantees#r4 ("`pr-reviewer` shall review only kept changes ...")
   matches `reviews.review` again. It is a constraint on the act, not a new request. The verb fallback cannot tell
   the two apart.
6. **A service no capability specifies.** `reviews.review` and `reviews.conclude` belong to `service reviews`, and no
   capability's `specifies:` names that service. `reviews` names `service batches: submit`; `review-guarantees` says
   "guarantees of a review". So the trace cannot name an owner for `reviews.review` (`owner=None`).

### 4.5 Coordination kind (decision 0134), derived

| question 0134 derives from | answer on today's model and lines |
|---|---|
| A request through a driven port? | None: no area of kind `port`, no driven adapter. Not a port request. |
| An object of the core whose lifecycle waits on replies to its requests? | `batch`: building → in-review (reviews#r5-r7, on submit); the review then comes back through `reviews.conclude` (review-guarantees#r6, r8) to in-review → building or → awaiting-merge. The batch waits on the review that its submit starts (review-guarantees#r1). **Long-running process**, the batch its process manager. |
| Two or more state-changing requests to other contexts, each compensated? | The requests to tracking (allocate on open, suspend on park, deliver and resolve on merge, restore on abandon) are module requests inside work-management (0133), not requests to other contexts. The model has no `compensated by` and no `followed by` anywhere (the only event is `contract published`). **Not a saga.** |

The derivation is only half mechanical today:

- **Mechanical:** the lifecycle and its `sets`.
- **Not mechanical:** the link from submit to review to conclude. It is an event trigger ("When the batches service
  submits a batch"), not a `followed by` property, and nothing marks conclude as a reply to submit.

If decision 0133's split ever happens, open (allocate), merge (deliver, resolve) and abandon (restore) become
state-changing requests to another context, and restore is the natural compensation of allocate. The derivation
would then report "a long-running process with uncompensated requests to another context", the shape of a saga
without its compensations. Decision 0131 keeps opening a batch one commit, so this is only a signal.

## 5. The checks the product layer enables, and what they report today

`product_check.py` runs each check. The left column is today's repository (no `serves:` anywhere). The right column
assumes the serves lines of `support/serves.overlay`.

| code | check | today | with the overlay |
|---|---|---|---|
| p1 | each job assigned to exactly one context | passes (6/6) | passes |
| p2 | each job served by exactly one capability | **6 findings**: no capability serves j1-j6 | passes |
| p3 | the serving capability is in the assigned context | n/a | passes |
| p4 | the serving capability's narrator is the job's actor | n/a | passes (all "the person") |
| p6 | every context of the map holds a capability | passes | passes |
| p7 | every context of the map is hosted by a shop's `[[hosts]]` | **5 findings**: the shop hosts only `shopsystem-bdd` | 5 |
| p8 | every subdomain is addressed by a context | passes | passes |
| p9 | a job's trace reaches a context addressing each subdomain it is mapped to | n/a | **2 findings** (below) |
| w1 | a live capability serves no job | 22 (every one) | **16** (below) |
| w2 | a subdomain serves no job | **s5** (supporting), **s8** (generic) | same |

The p9 findings:

```
j1: mapped to [s1, s2, s3], trace reaches [work-management] addressing [s3]; missing [s1, s2]
j4: mapped to [s1, s2, s4], trace reaches [specification] addressing [s1]; missing [s2, s4]
```

- **j1.** The readiness bar is specification's and language's work, but `items`' lines read it as a state ("the item
  meets the readiness bar") rather than requesting it. This is the §4.4 point 1 gap again, seen from the product.
- **j4.** `checking`'s contract lines do request nothing of language. s4 (collaboration) is reached only by
  `context-requests`, and publishing a contract is not a context request (`checking#r78`: "fetches ... without a
  context request"). Either the mapping of j4 to s4 is wrong, or the job belongs partly to collaboration.

The w1 findings with the overlay (16): `drafting`, `reviews`, `review-guarantees`, `decisions`, `records`,
`scenarios`, `consistency`, `parsing`, `directives`, `quotes`, `request-watch`, `shaping-guarantees`, `trials`,
`toolchain`, `code-analysis`, `feature-reading`.

- `reviews` and `review-guarantees` are in j2's trace with `--service`. A good w1 should leave out capabilities that
  are in some job's trace. The script does this only when it runs the trace without `--service`.
- The rest fall into three groups:
  - capabilities the person uses directly within a job (drafting within j1);
  - session-facing guarantees (directives, quotes, request-watch, shaping-guarantees, trials);
  - whole subdomains with no job (s5 direction, s8 codebase insight).

  This suggests either more jobs (for example "keep the person's direction for every session", or "know my code's
  coverage"), or a rule that guarantees capabilities are left out, as v_s3 already leaves them out of scenario
  checks.

Two checks are not built:

- **p5 (a job served twice):** p2 covers it.
- **"A capability serving a job of another context's assignment":** this is p3.

## 6. What it needs from the tooling

### 6.1 Forms and `spec forms` entries

| form | path | writer (proposed) |
|---|---|---|
| product identity | `product/index.md` | `shop product init --id <product id> --purpose ...` (or `migrate init --product`) |
| job | `product/jobs.md ## [j<n>]` | `shop job "<title>" --actor <actor> --statement "<text>"` |
| subdomain | `product/domain.md ## Subdomains` row | `shop subdomain <name> --type core\|supporting\|generic` |
| context entry | `product/domain.md ## Bounded contexts` row | `shop context <id> --addresses s<n>,... --shop <shop id>` |
| assignment | `product/domain.md ## Assignments` row | `shop assign j<n> <context id>` (reassigning writes a new row, with the old one kept as history) |
| shop | `.shop/shop.toml` | `migrate init` (hosts and product keys) |
| capability's `serves:` | `spec/capabilities/<name>.md` frontmatter | `work line --capability ... --serves j<n>` and a `work line --serves` for an existing capability, through an item |

The command name `shop` follows decision 0132 (one command, a subcommand per concern). Each row is one more
`FORMS` entry in model_forms, so `spec forms --check` keeps naming hand-written files.

### 6.2 Ids and references

- `product/<product path>`, `job/<product path>/j<n>`, `subdomain/<product path>/s<n>` (or a slug), and
  `shop/<domain>/<name>`.
- shop_ids' `held` gains the job and subdomain kinds, so that `serves:` and a record's `--about` resolve.
- `serves:` takes the short form `job/j<n>` inside a compact shop and the full id elsewhere.

### 6.3 Where the checks run

- **p1, p7, p8, w2 (the product's own consistency)** run in a product check: `spec check` with the product layer as
  its root, or a `shop check`.
- **p2, p3, p4, w1, p9** need each hosted context's capabilities and lines.
  - In a compact shop they run in the shop over its `[[hosts]]`.
  - When the product has its own repository, the product cannot ask the contexts (it never polls them). The checks
    would then run on what each context publishes: its contract would carry each capability's `serves:` and the
    trace's line ids. The product checks the contracts it obtains, as a downstream does.
- **p9's trace** needs the request chain to see parameterless response requests (§4.2) before it says anything
  reliable.

### 6.4 Candidate design-decisions (not written)

1. **The product assigns a job to one context, and one capability of it serves the job:** assignment is a row of the
   product's domain map; `serves:` is the capability's frontmatter; the product never asks a context.
2. **A job is a structured entry, not a requirement line:** its statement is read by no grammar and checked only for
   its form (actor, When/wants/so they can).
3. **A job's requirement lines are derived, never listed:** the serving capability's lines plus every line reached
   through the requests they make, to a fixed depth, across contracts and ports.
4. **The product layer of a compact shop lives under `product/`, beside the hosted contexts' specs:** `.shop/shop.toml`
   names it and the contexts the shop hosts.
5. **A context's own actors are mapped to the product's actors:** a capability's narrator is checked against the
   product's actors through that mapping, not by string.
6. **A response's act of an operation's verb is a request whatever its parameters:** this extends the meaning of
   decision 0110 and b543 so that parameterless acts like "deliver the item" are requests.

### 6.5 Candidate backlog items (not written)

1. *A response's act of an operation's verb with no parameters is read as a request:* spec_lf_request (and the
   facts, `asks`, the entailment chain) treats "the batches service shall deliver the item" as a request of
   `backlog.deliver`.
2. *A negated set in a response is no `sets` fact:* model_domain_lines' `Lines.sets` skips `initiates` under a `not`
   box, so batches#r111 stops masking w_m5 for batch in-review → abandoned.
3. *Every operation's service is specified by one capability:* `service reviews` (review, conclude) is named by no
   `specifies:`; a rule names such services.
4. *The product layer's forms and their writers:* product identity, job, subdomain, context entry, assignment, shop,
   with `spec forms` entries.
5. *A capability serves a job:* `serves:` frontmatter, written through an item, read into facts.
6. *The product checks p1-p9, w1, w2:* run on a compact shop over its hosts.
7. *A job's derived trace:* `spec trace job/j<n>` prints the serving lines, the requests, the reached capabilities
   and contexts, and the reads of other contexts' state, from the logical forms (support/job_trace.py as the sketch).
8. *Execution's reads of specification's state become requests:* the 24 batches lines naming specification's objects
   are recast against specification's operations (lay, check, generate, write corpus) before a split.
9. *The index's composition lists the live capabilities:* `parsing` (22 live lines) appears as retired and `reading`
   (0 live) as live in `spec/index.md`.

## 7. Open questions for the person

Each question has a short answer space.

- **Q1. One capability, several jobs?** Can one capability serve two jobs (yes/no)? For example, `checking` could
  serve both j4 (contracts) and a job "check a context's spec as a whole". If no, is `checking` split into a
  `contracts` capability for j4?
- **Q2. A job's lines: all of the serving capability's, or only some groups'?** All 70 of `checking`'s lines, or
  `serves:` on a group (e.g. `checking#g73-g79`)?
- **Q3. Is the job statement checked?** Pick one: not at all / its form only (actor among the product's, the three
  clauses present) / against the serving capability's lines.
- **Q4. Jobs with several actors?** j3 (asker and upstream) and j4 (publisher and downstream context) have two. Allow
  `actor:` to list several, or split each into one job per actor (e.g. j4a publish, j4b obtain)?
- **Q5. When the actor is the coordinator.** In j1 and j2 the person drives several capabilities in turn: drafting
  then items; batches then a session's conclude. Is the serving capability the entry point of the person's first act,
  or must a job's coordination be in the serving capability's lines? (Today it is not.)
- **Q6. Where does the product layer live when the product has its own repository?** In the product's shop under
  `product/`, with each context's contract carrying its `serves:` lines (so the checks run on obtained contracts)?
  Or does the product keep a mirror of the hosted contexts?
- **Q7. Assignments before the split.** Assign today's jobs to the one context `shopsystem-bdd` and reassign at the
  split? Or assign to the target contexts now, with a `today` mapping of areas and capabilities as sketched?
- **Q8. Do reads count in a trace?** Should a trace count a precondition that names another context's object (e.g.
  "meets the readiness bar", "violates a rule") as reaching that context? Or only requests (so that p9 is a pressure
  to turn reads into requests)?
- **Q9. Subdomains with no job.** s5 (the person's direction) and s8 (codebase insight) serve none of the six jobs.
  Add jobs for them, or accept a supporting or generic subdomain that serves only other subdomains?
- **Q10. Guarantees capabilities.** Do session-narrated guarantees capabilities (review-guarantees,
  shaping-guarantees, trials) take part in w1? Or are they left out as v_s3 leaves them out today?

## Support files

All are under `support/`. None is tracked, and the scripts write nothing.

- `product/index.md`, `product/jobs.md`, `product/domain.md`: the product layer sketch.
- `dot-shop/shop.toml`: the proposed `.shop/shop.toml`.
- `serves.overlay`: the proposed `serves:` lines, one per serving capability.
- `job_trace.py`: a job's derived trace, read-only, over the plugin's own readers (`--service`, `--depth`,
  `--domain`).
- `product_check.py`: checks p1-p9, w1 and w2 (`--serves`, `--shop`).
- `trace-batches.txt`, `trace-batches-service.txt`, `trace-items.txt`, `trace-context-requests.txt`,
  `trace-checking.txt`, `trace-upgrades.txt`, `trace-measurement.txt`: the traces as run.
- `check-today.txt`, `check-overlay.txt`: the checks as run.
- `facts.txt`: `spec facts` of `main`, used to cross-check `requester`, `asks` and `sets`.
