---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-25-a-worked-example-of-the-product-layer-on-a-notes-product-of-four-bounded-contexts
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-25
---

# A worked example of the product layer on a notes product of four bounded contexts

## 1. What this example does and how it was made

This is a second worked example of the product layer. The first was on the plugin itself. This one uses a product
that is not the plugin: the notes app of `docs/examples/notes-cli/`, grown into a small product called **Notes**. It
has four bounded contexts hosted in one compact shop, two third-party providers, six jobs to be done and seven
subdomains. It tests the minimum product layer (identity, jobs, domain map, assignment, `serves:`, derived traces,
derived coordination kind) on a fresh product. Every context's spec was written in the plugin's form and checked with
the plugin's own tools.

How it was made:

- The core context `notebook` is a copy of `docs/examples/notes-cli/`. Its id became
  `bounded-context/example.org/notes/notebook`. Its model, vocabulary and CLI contract were extended with seven
  operations that other contexts request, and four capabilities were added. `sharing`, `backup` and `accounts` were
  written from scratch, each small, each with driven ports, port capabilities and adapter specs (`kind: adapter`).
- Every candidate requirement line was first parsed with `spec parse` in its context (`parse_lines.sh`): 52 parsed
  and 20 were refused. The refused ones were alternates; their refusals are kept verbatim in `support/probes/`. The
  lines that parsed were filed in capabilities. Then each context went through `features generate`, `spec annotate`,
  `spec check`, `spec logic` and `spec explain`, and each adapter spec through `spec --root <adapter> check`.
- `notebook` published its contract with `spec publish`. `sharing`, `backup` and `accounts` obtained it with
  `spec obtain` through the stand-in gh of the plugin's tests (`tests/scripts/stub_gh.py`). For the two third-party
  providers, contracts were written by hand where `spec obtain` would have kept them.
- The product layer has no tooling. Two read-only scripts fill the gap. `job_trace.py` derives each job's trace and
  coordination kind from the lines' logical forms (`spec parse --form --file`) and the models, vocabularies and adapter
  specs. `product_check.py` runs the product checks over that trace.
- Nothing tracked in the repository was changed. Everything is under `support/`, a git repository of its own (the
  scratch shop) so that `spec publish` and `spec obtain` can commit.

## 2. The product

### 2.1 Identity

`product/example.org/notes`. Purpose: short notes a person keeps for themselves, finds again by tag, lets a colleague
read, keeps safe outside their device, and pays for when they need more room than the free allowance. Actors: **the
person** (keeps notes) and **the colleague** (someone the person lets read a note; they need not keep notes).

### 2.2 Domain map

| id | subdomain | type | addressed by |
|---|---|---|---|
| s1 | note keeping | core | notebook |
| s2 | collaboration | supporting | sharing |
| s3 | data safety | supporting | backup |
| s4 | plans and billing | generic | accounts |
| s5 | search | core | **none** (deliberately: exercises the check "a subdomain no context addresses") |
| s6 | object storage | generic | `bounded-context/example.net/vault/storage` (third party) |
| s7 | card payments | generic | `bounded-context/example.net/payco/payments` (third party) |

| bounded context | capabilities (service: s, port: p) | driven ports, adapter, provider |
|---|---|---|
| notebook | notes, tags, access, allowance, transfer (s) | none; CLI adapter `spec/adapters/cli.toml` |
| sharing | invitations (s); notebook-port (p) | notebook → adapter `notebook` → notebook@1.0.0 (obtained) |
| backup | backups, restores (s); notebook-port, storage-port (p) | notebook → notebook@1.0.0 (obtained); storage → vault/storage@2.0.0 (by hand) |
| accounts | plans (s); payments-port, notebook-port (p) | payments → payco/payments@1.0.0 (by hand); notebook → notebook@1.0.0 (obtained) |

Relations between contexts were derived, not written. `job_trace.py --relations` read them off the adapter specs'
`providers:`: accounts→payco, accounts→notebook, backup→vault, backup→notebook, sharing→notebook.

### 2.3 Jobs to be done

| job | actor(s) | statement (abridged) | subdomains | assigned | served by |
|---|---|---|---|---|---|
| j1 Jot a thought down | the person | When a thought comes up …, wants to add it as a note under a tag, so they can … find it later | s1 | notebook | notes |
| j2 Pick a topic up again | the person | When they come back to a topic, wants every note under its tag, so they can carry on | s1, s5 | notebook | notes |
| j3 Let a colleague read a note | the person, the colleague | When a colleague needs what the person wrote, the person wants to let them read one note and the colleague wants to take it up or turn it down, so … | s2, s1 | sharing | invitations |
| j4 Keep the notes safe | the person | When their device could be lost …, wants the notes kept somewhere else, so they can get them back | s3, s1, s6 | backup | backups |
| j5 Get more room | the person | When the free allowance is used up, wants to pay for a larger plan, so they can keep adding notes, and not to pay when the room is not given | s4, s7, s1 | accounts | plans |
| j6 Carry on on a new device | the person | When they start on a new device, wants the notes kept on the old one, so they can carry on there | s3, s1, s6 | backup | restores |

The brief asked for four kinds of job, and each is covered:

- **A job crossing contexts with compensation (the saga candidate):** j5. Charge through payments, then enlarge the
  notebook's allowance; refund the charge if the allowance is refused.
- **A job with two actors:** j3.
- **A capability that serves two jobs:** `notebook:notes` serves j1 and j2.
- **A job the person coordinates:** j6. The person saves on the old device (capability `backups`, serving j4), then
  restores on the new one (capability `restores`).

## 3. The scratch compact shop

```
support/shop/                       one git repository: the compact shop
  .shop/shop.toml                   the shop: its id, the product folder, the hosted contexts and their folders
  product/index.md                  product identity: id, purpose, actors (each with the name each context calls it)
  product/jobs.md                   jobs to be done, one `## [j<n>]` entry each
  product/domain.md                 subdomains (type), bounded contexts (subdomains addressed, hosting shop)
  realisations.toml                 PROPOSED: port operation → provider operation, per adapter spec
  contexts/<name>/spec/...          each context's spec in the plugin's form; capability frontmatter `serves:`
  contexts/<name>/adapters/<port>/  each adapter spec: spec/index.md (kind: adapter), adr/, provider/<id>/<v>/contract.toml
  contexts/notebook/.shop/contracts/1.0.0/contract.toml   written by `spec publish` (see 7b-3)
```

These forms are proposed. None is a form `spec forms` knows (7b-6).

- **`.shop/shop.toml`** holds `id = "shop/example.org/notes/main"`, `product = "product"`, and a table
  `[contexts]` mapping each hosted context's id to its folder. Ids stay flat under the product (decision 0129).
- **`product/index.md`** holds `id: product/example.org/notes`, `## Purpose`, and `## Actors`. Each actor is a bullet
  with a `Called:` list giving the proper noun each context uses for it, for example "Called: the person (notebook,
  backup, accounts), the owner (sharing)". This list turned out to be necessary: the same human is "the owner" in
  sharing and "the person" everywhere else.
- **`product/jobs.md`** holds one entry per job:

  ```
  ## [j5] Get more room
  - actor: the person
  - statement: When the free allowance is used up, the person wants to pay for a larger plan, so they can keep adding
    notes, and not to pay when the room is not given.
  - subdomains: [s4, s7, s1]
  - assigned: bounded-context/example.org/notes/accounts
  ```

  Each job's id is `job/example.org/notes/j<n>`. The assignment is recorded in the product layer. The serving is
  recorded in the context, as `serves: [job/example.org/notes/j5]` in `plans.md`'s frontmatter.
- **`product/domain.md`** holds two tables, `| id | subdomain | type | purpose |` and
  `| bounded context | subdomains | shop |`. Third-party providers are rows too, with `third party` as their shop.
  `## Relations` is not written: it says only that relations are derived.
- **`realisations.toml`** is not part of the minimum layer. The trace needed it to cross from a port operation into
  the provider's operation (section 5.2, 7a-1). Today that mapping exists only as prose in each adapter's `adr/`.

## 4. The contexts' specs, and what the tools said

### 4.1 notebook (core)

The model gained `reader`, `allowance (size: number)` and `bundle (holds → note)`, a relation `note has → reader`,
and seven operations: `rename`, `open(note, reader)`, `close`, `enlarge`, `reduce`, `export`, `import`. It also gained
the actor `a client`, the requester of every operation the other contexts reach.

| capability | narrator | serves | lines |
|---|---|---|---|
| notes | the person | j1, j2 | r1-r4 as the example, plus r5 "When the person lists the notes with a tag, the notes service shall return every note under the tag." and r6 "While the number of notes is at least `100`, if the person adds a note, then the notes service shall refuse the request and name an allowance." |
| tags | the person | none | r1 "When the person renames a tag with the spelling `work`, the notes service shall keep the tag." |
| access | a client | none | r1 open → "keep a note that has the reader"; r2 open of a `removed` note refused; r3 "While a note has a reader, when a client closes the note to the reader, … complete the request." |
| allowance | a client | none | r1 enlarge → keep the allowance; r2 reduce → keep the allowance |
| transfer | a client | none | r1 "When a client exports the notes, the notes service shall return a bundle that holds every note whose status is `kept`."; r2 import → keep every note that the bundle holds; r3 import past `100` refused |

Final state of `spec check`: 0 violations, 3 warnings (`w_example`: `100`, `work`). `spec logic`: no findings.
`spec publish --version 1.0.0` printed `published .shop/contracts/1.0.0/contract.toml`, under `contexts/notebook/`.

The tools said this on the way:

- The attribute `name` (of tag) collides with the request pack's verb "name":
  `v_t16 … term/example.org/notes/notebook/name, request` and
  `v_p1 … notes#r2, does not parse at name (token 20 of 23)`. Renamed to `spelling`.
- New operations with no CLI command gave `v_a1`. Listing them under `[unexposed]` in `cli.toml` cleared it. The
  operations other contexts request are not CLI operations: the contract has no notion of "reached through a
  published contract".

### 4.2 sharing (supporting)

The model has `invitation` (address; status sent → accepted | declined | withdrawn; `has → note`), the operations
`share(note, address)`, `accept`, `decline` and `withdraw`, and the actors **the owner** and **the colleague**. The
port area `notebook` (kind port) declares `show(note)` and `hide(note)`.

`invitations` (narrator the owner, serves j3):

- r1: When the owner shares a note with an address, the sharing service shall keep an invitation that has the note.
- r2: If the owner shares a note without an address, then … refuse the request and name the address.
- r9: When the colleague accepts an invitation, the sharing service shall set the status of the invitation to
  `accepted` and show the note of the invitation.
- r5: A `withdrawn` invitation accepted is refused.
- r6, r7: declined and withdrawn set the status.
- r8: While an invitation is `accepted`, when the owner withdraws the invitation, the sharing service shall hide the
  note of the invitation.

`notebook-port` (narrator the sharing service): r1 "When the sharing service shows a note, the notebook service shall
complete the request.", r2 the same for hides.

The tools said this:

- r3 and r4 were first two groups on one trigger. That gave `v15l` (more than one statement in a group), then `v15n`
  (two groups sharing a trigger). The way out was one line with two acts (r9), with r3 and r4 retired.
- With the port area importing nothing, `v_m1 … notebook-port#r1, the sharing service, the sharing service is a word
  of sharing, which the area notebook does not read`. The port area must import its core area (`imports: [sharing]`),
  as the plugin's fixture does.
- The port's refusal reason `removed note` gave `v_m4`, and no line could state it (7c-1). It was dropped from the
  port.
- Adapter spec, run from inside its folder with no `--root`: `file: spec/index.md: id
  'bounded-context/example.org/notes/sharing/adapter/notebook' does not match the adapter spec: it names no folder
  adapters/notebook/, the adapter spec is kept at adapters//` (7b-1). With `--root <absolute>`: `the provider
  bounded-context/example.org/notes/notebook has no contract the adapter spec holds under
  provider/example.org/notes/notebook/1.0.0/`, until `spec obtain` printed `obtained
  adapters/notebook/provider/example.org/notes/notebook/1.0.0/contract.toml`. Then 0 problems.

### 4.3 backup (supporting)

The model has `snapshot` (status taken → stored | lost; `has → bundle`) and the operations `save()` and
`restore(snapshot)`. The ports are `notebook` (`export()` returned → the bundle; `import(bundle)`) and `storage`
(`store(snapshot)`; `fetch(snapshot)` returned → the snapshot).

| capability | narrator | serves | lines |
|---|---|---|---|
| backups | the person | j4 | r1 "When the person saves the notes, the backup service shall export the notes and keep a snapshot."; r2 "When the notebook service returns a bundle, the backup service shall store a snapshot that has the bundle."; r3 "If the storage service refuses the request, then the backup service shall keep the request." |
| restores | the person | j6 | r1 "When the person restores a snapshot, the backup service shall fetch the snapshot."; r2 "When the storage service returns a snapshot, the backup service shall import the bundle of the snapshot."; r3 a `lost` snapshot refused |
| notebook-port, storage-port | the backup service | none | one "When the backup service <verb>s …, the … service shall complete the request / return …" line per operation |

`spec check`: 0 violations, 2 warnings, `w_m5 a lifecycle transition no line causes: snapshot, status, taken, lost`
and `… taken, stored`. No line could make a snapshot `stored` once the storage service completes its store (7c-2).
The vault provider's contract was written by hand, in a shape the contract form does not accept. `spec check` on the
adapter spec still said 0 problems (7b-4).

### 4.4 accounts (generic): the saga

The model has `plan` and `subscription` (status requested → charged → active; charged → refunded; `has → plan`), and
the operation `subscribe(plan)`. The ports are `payments` (`charge(subscription) idempotent by subscription;
compensated by refund`, refused: card declined; `refund(subscription)`) and `notebook` (`entitle(subscription)`,
refused: no allowance).

`plans` (narrator the person, serves j5):

- r1: When the person subscribes to a plan, the accounts service shall charge a subscription that has the plan.
- r2: While a subscription is `requested`, when the payments service completes the request, the accounts service shall
  set the status of the subscription to `charged` and entitle the subscription.
- r3: While a subscription is `requested`, if the payments service refuses the request, then the accounts service
  shall notify the person of the subscription.
- r4: While a subscription is `charged`, when the notebook service completes the request, the accounts service shall
  set the status of the subscription to `active`.
- r5: While a subscription is `charged`, if the notebook service refuses the request, then the accounts service shall
  refund the subscription and set the status of the subscription to `refunded`.

The tools said this:

- `spec check`: `v_m4 … notebook.entitle, no allowance` and `payments.charge, card declined`. These remain open
  (7c-1).
- `compensated by unentitle`, written before the operation existed, gave `v_m8 … refers to unentitle, which is not an
  operation the model declares`. That is correct.
- `spec logic`: no findings.
- `spec explain plans#r1` printed only the line: nothing chained into the payments port. The facts show why.
  `spec facts` has `requester(...)` for every port line and for plans#r1's trigger, but **no `asks` fact** for any of
  the six response requests in the product (charge, entitle, refund, show, hide, export/store/fetch/import). The
  logical form prints them as plain events: `refund(e2, subject: x4, object: x1)`, not `request(e2,
  payments.refund, …)`. This is backlog item b604, and it makes the request chain and `spec explain` blind to every
  coordination line in this product (7b-2).

## 5. Per job: assignment, serving capability, trace, coordination kind

### 5.1 Summary

| job | assigned | serving capability | trace reaches (contexts) | coordination (derived) | product checks failing |
|---|---|---|---|---|---|
| j1 | notebook | notes (6 lines) | notebook | local | none |
| j2 | notebook | notes (the same 6 lines) | notebook | local | p7: s5 search addressed by no context reached |
| j3 | sharing | invitations (7 lines) | sharing → notebook (access#r1-r3) | port request (show, hide; no line waits on a reply) | p4: narrator the owner, but the colleague is also an actor |
| j4 | backup | backups (3) | backup → notebook (transfer#r1) → vault (stops) | long-running process by the lines; **not** by decision 0134's lifecycle reading (see below) | none |
| j5 | accounts | plans (5) | accounts → payco (stops), → notebook (allowance#r1) | **saga**: 2 state-changing forward requests (charge, entitle), charge compensated by refund (declared and requested on a refusal) | none |
| j6 | backup | restores (3) | backup → vault (stops) → notebook (transfer#r2, r3) | long-running process (fetch then import) | none; but its trace misses `backups`, which the person must run first |

Checks that pass for every job: p1 (assigned to exactly one context), p2 (served by exactly one capability), p3
(serving capability in the assigned context), p8 (actor among the product's), p9 (statement form only).

### 5.2 j5 in depth (`support/traces.txt`, abridged)

```
== j5 Get more room: accounts, served by ['plans']
   coordination: saga (2 state-changing forward requests ['notebook.entitle', 'payments.charge'];
                 compensated: ['payments.charge'] by declaration, ['payments.refund'] requested on a refusal)
   accounts:plans#r1  When the person subscribes to a plan, … shall charge a subscription that has the plan.
     -> port request payments.charge (changes; idempotent by subscription; compensated by refund)
        port line accounts:payments-port#r1  When the accounts service charges a subscription, … complete the request.
        adapter payments -> provider bounded-context/example.net/payco/payments@1.0.0 op charges.create; contract held
        (provider outside the shop: trace stops)
   accounts:plans#r2  [on payments complete]  While a subscription is `requested`, when the payments service …
     -> port request notebook.entitle (changes)
        port line accounts:notebook-port#r1  …
        adapter notebook -> provider bounded-context/example.org/notes/notebook@1.0.0 op notes.enlarge; contract held
        notebook:allowance#r1  When a client enlarges an allowance, the notes service shall keep the allowance.
   accounts:plans#r3  [on payments refuse]  …
   accounts:plans#r4  [on notebook complete]  …
   accounts:plans#r5  [on notebook refuse]  … shall refund the subscription and set the status … to `refunded`.
     -> port request payments.refund (changes) …
```

How each hop was derived, and how reliable it is:

- **Serving capability → port request.** A verb in the response maps, through the vocabulary, to an operation of an
  area of kind `port`. This is reliable, and works even though the plugin's facts miss it (b604).
- **Port request → port line.** The port capability's lines whose trigger is `request(e1, <op>, …)` in `spec parse
  --form`. Reliable.
- **Port line → adapter spec → provider.** Through `realises:` and `providers:`. Reliable, and checked by `spec check`
  on the adapter.
- **Provider → provider operation.** Only through the proposed `realisations.toml`. Nothing in the plugin records
  that `notebook.entitle` is `notes.enlarge`; the adapter's `adr/` says it in prose. The script also checked that the
  provider operation is in the held contract. That check would catch a renamed upstream operation, which `spec check`
  does not.
- **Provider operation → provider lines.** The provider's lines triggered on a request of that operation. Reliable
  inside the shop. For a third party the trace stops: it has no lines.
- **Lines on a reply** (`[on payments complete]`). Read by service only. The language cannot tie "the request" to the
  subscription it was made for. The form shows `x3: request "the request the trigger makes" (indexical)`, which
  points at the reply's own trigger, not at the charge (7c-3). So r2's "while a subscription is `requested`, when the
  payments service completes the request" is satisfied by any completion of any payments request while any
  subscription is requested.

Coordination kind, applying decision 0134's definitions:

- j5 is a saga. Its object `subscription` has a lifecycle that waits on replies (requested → charged → active |
  refunded), it makes two state-changing requests to other contexts, and the earlier one is compensated when the
  later one fails. Both the lifecycle reading and the line reading agree.
- j4 is where the two readings part. The lines wait on a reply (r2 on the notebook's return), but the snapshot's
  lifecycle has no transition any line causes (`w_m5`). By 0134's wording ("an object whose lifecycle waits on replies
  to its requests"), j4 is not a long-running process. That is only because the language cannot say "stored once the
  storage service completes" (7c-2).
- j3 is a single port request per trigger. Its refusal path (notebook refuses `show`, so the invitation should become
  `declined`) could not be stated (7c-3). Had it been stated, j3 would be a long-running process too.

### 5.3 Product checks as run (`support/check.txt`)

```
p7 j2: names s5 (search), which no context its trace reaches addresses (reached: ['notebook'])
p4 j3: invitations's narrator is 'the owner'; the actor 'the colleague' is called 'the colleague' in sharing
p5 notebook:access serves no job (reached by a trace)
p5 notebook:allowance serves no job (reached by a trace)
p5 notebook:tags serves no job (reached by nothing)
p5 notebook:transfer serves no job (reached by a trace)
p5 sharing:notebook-port serves no job (a port capability)
p5 backup:notebook-port serves no job (a port capability)
p5 backup:storage-port serves no job (a port capability)
p5 accounts:notebook-port serves no job (a port capability)
p5 accounts:payments-port serves no job (a port capability)
p6 s5 (search, core) is addressed by no bounded context
12 findings
```

Only three of the twelve are real problems: p6/p7 on s5 (planted), p4 on j3 (a real modelling question) and p5 on
`tags` (planted). The other eight p5 findings are noise unless p5 tells the three cases apart. "Serves no job" is
wrong for a port capability, and wrong for a capability a trace reaches (the provider side of a job). p5 must exclude
both, or it buries `tags`, the one capability nothing reaches.

p4 also needed the `Called:` mapping. Without it, j1, j2, j4, j5 and j6 pass only because every one of those contexts
happens to call the person "the person", while j3's context says "the owner".

## 6. The sibling's open questions, tested against this product

- **Q1. One capability, several jobs?** Yes, it must be allowed. `notes` is the natural entry point for both j1 (add)
  and j2 (list), and splitting the CLI's one capability in two would be artificial.
- **Q2. All lines of the serving capability, or only some groups?** With `serves:` on the capability, j1's trace holds
  the list lines (r3, r5) and j2's holds the add lines (r1, r2, r6). Both traces are too wide. This product suggests
  `serves:` on groups (`Serves: job/…/j1.` under `### [g1]`) or on the capability with a group filter. One test:
  writing `Serves: job/example.org/notes/j1.` under a group was silently accepted by `spec check` and `features
  generate --check` (`support/variant-group-serves/`), as was the frontmatter `serves:`. Either form is free today
  and unchecked (7b-5).
- **Q3. Is the job statement checked?** Checking the form only (p9: "When …, <actor> wants …, so they can …") passed
  all six statements, including j3, which names two actors with two motivations, and j5, which carries a negative
  outcome ("and not to pay when the room is not given"). Checking against the lines is out of reach: j5's "not to pay
  when the room is not given" is exactly the compensation the language could only half say (r5 refunds; nothing ties
  the refund to the failed entitlement). Recommendation: check the form only, plus "actor among the product's".
- **Q4. Jobs with two actors?** j3 is one job with two actors. Splitting it into "let a colleague read" (the person)
  and "take up an invitation" (the colleague) gives two jobs served by the same capability, each with a narrator
  problem. A capability has one narrator, but `invitations` has lines triggered by both. This suggests `actor:` may
  list several actors, with p4 relaxed to "each actor is the narrator or a trigger's subject in a served line". The
  data to check that exists: the logical form names each trigger's subject.
- **Q5. When the actor is the coordinator.** j6 is coordinated by the person: save on the old device (`backups`),
  then restore on the new one (`restores`). Its derived trace from `restores` never reaches `backups`, so a change to
  `backups` would not show as touching j6. Either the job names its entry steps in order (`steps: [backups,
  restores]`, a person-coordinated job) or j6 depends on j4 (`needs: [j4]`). This product suggests the latter: it is
  smaller and checkable (the trace of j6 is the trace of restores plus j4's).
- **Q6. Where the product layer lives with several shops.** The published contract (`notebook`'s 1.0.0) carries every
  requirement with its capability prefix, but no capability frontmatter: no `serves:`, no narrator. A product layer in
  another repository could not run p2-p5 on obtained contracts. Either the contract form gains `serves` per
  capability, or the product layer keeps assignments and the contexts keep `serves:` with the checks run in each
  shop. Third-party providers (vault, payco) have no shop and no contract in the form. The product layer has to list
  them as contexts addressing a subdomain (s6, s7) anyway, or p7 cannot pass for j4, j5 and j6.
- **Q7. Assignments before the split.** Not exercised: this product was laid out split from the start.
- **Q8. Do reads count?** This product needed no read of another context's state, because every cross-context fact
  came back as a reply. Replies, though, cannot be tied to the object they are about (7c-3). A trace that counts
  requests only is complete here. The pressure is on the language, not on the trace rule.
- **Q9. Subdomains with no job.** None here: the generic s6 and s7 are each named by jobs (j4, j6, j5) because the job
  cannot be done without them. That suggests a job's `subdomains:` should list the generic ones it needs, and p7 then
  covers them.
- **Q10. Guarantees capabilities.** None in this product. The analogue is the port capabilities, which p5 must
  exclude, as v_s3 excludes guarantees capabilities.

## 7. Issues found

### 7a. Design issues of the product layer

1. **The port-to-provider mapping is not data.** An adapter spec has `realises:` (port lines) and `providers:` (a
   context and a version), but which provider operation realises which port operation is only adr prose. Without it,
   a job's trace stops at the adapter, and a provider's renamed or removed operation goes unseen.
   `realisations.toml` stood in. The mapping belongs in the adapter spec.
2. **Actors are named per context.** The product's "the person" is "the owner" in sharing. p4 needs a mapping (the
   proposed `Called:`). Alternatively, a context's actor entry names the product actor it plays.
3. **p5 must tell three cases apart:** port capabilities, capabilities a trace reaches (provider side), and
   capabilities nothing reaches. Only the last is a finding. Here, 8 of 9 p5 findings were noise.
4. **One narrator per capability does not fit a two-actor job** (j3, p4). Either relax p4 to trigger subjects or split
   the capability by actor.
5. **Person-coordinated jobs need a link between jobs** (j6 needs j4), or traces miss capabilities.
6. **`serves:` granularity.** At capability level, j1 and j2 get identical traces. Group level is more precise.
7. **Third parties are part of the domain map** (subdomains s6, s7) but have no shop, no lines and no contract in the
   form. The layer should say how they are listed and what p7 expects of them.
8. **Two readings of a long-running process disagree** (j4): 0134's "lifecycle waits on replies" against "a line is
   triggered on a reply". The derivation should name which one it uses. Today only the line reading is computable,
   because of 7c-2.
9. **"kind" is overloaded.** The model's `kind:` and the composition table's `kind` column carry `core`, `generic`
   and `port`. Decision 0128 says subdomain types belong to the product. Only `port` is read by any tool:
   `kind: banana` passed `spec check` with nothing new (`support/probes/variant-kind-banana.out`). The area kind
   should be `port` or nothing (or `adapter`), with the subdomain type left to `product/domain.md`.
10. **Where a compact shop's contracts live.** A compact shop holds several contexts in one repository, but
    `spec publish` writes `<context>/.shop/contracts/`, a second `.shop` inside the shop, and `spec obtain` reads
    `.shop/contracts/` at the repository root (7b-3). Decision 0129 puts `.shop` at the shop. The contract's place
    needs deciding for a shop that hosts several contexts.

### 7b. Defects or missing features of the plugin's tooling

1. **An adapter spec checked from its own folder without `--root`.** Command (cwd `contexts/sharing/adapters/notebook`):
   `python3 …/scripts/spec check`. Output: `file: spec/index.md: id
   'bounded-context/example.org/notes/sharing/adapter/notebook' does not match the adapter spec: it names no folder
   adapters/notebook/, the adapter spec is kept at adapters//` (`probes/sharing-adapter-check-1.out`). `--root .` is
   likely the same. The root is not resolved before `root.name` is read in `model_adapter.path`. With an absolute
   `--root` it works.
2. **Response requests are not requests in the facts or the logical form** (b604, confirmed on a fresh product). In
   accounts, `spec facts` has 4 `requester` facts and 0 `asks` facts. `spec parse --form` of plans#r5 prints
   `refund(e2, subject: x4, object: x1)`. `spec explain plans#r1` prints only the line. All six coordination lines of
   the product are invisible to the request chain, `spec explain`, and v_m4's "a response asks O" path.
3. **`spec obtain` cannot obtain within a compact shop.** Command (in a copy of sharing, its upstream's `github:` the
   shop repository): `spec obtain bounded-context/example.org/notes/notebook`. Output: `spec: the bounded context
   bounded-context/example.org/notes/notebook has no contract` (`probes/obtain-from-compact-shop.out`). The contract is
   at `contexts/notebook/.shop/contracts/1.0.0/contract.toml`, and obtain reads `repos/<r>/contents/.shop/contracts`.
   The obtain that worked needed a fake repository per context (a symlink served by the stand-in gh). Obtaining
   between two contexts of one shop also has no local path: it always goes to GitHub.
4. **A provider's held contract is not checked against the contract form.** The hand-written vault contract fails
   `contract_form.problems` (`['operations.objects.put: parameters is not a list of strings', …]`,
   `probes/vault-contract-form.out`), but `spec --root …/adapters/storage check` says `0 violations, … 0 file
   problems`. Checking r86 checks only that a file exists.
5. **Unknown keys and lines are silently accepted.** Frontmatter `serves:` on a capability and a group line `Serves:
   job/….` both pass `spec check` with no file problem. That is good for proposals, but a typo in `restates:` would
   pass the same way.
6. **`spec forms` lists no adapter spec form** (`adapters/<name>/spec/index.md`, `adr/`), no port capability form, and
   no shop or product form (`probes/spec-forms-grep.out`). The adapter spec index has no writer, and isn't even listed
   as written by hand.
7. **`spec parse --file` resolves the file against the cwd, not `--root`, and crashes.** Command (cwd `support/`):
   `spec --root shop/contexts/accounts parse --form --file spec/capabilities/plans.md`. Output: a Python traceback
   ending `FileNotFoundError: [Errno 2] No such file or directory: 'spec/capabilities/plans.md'`, exit 1
   (`probes/defect-parse-file-root.out`). It should be read under `--root`, and a missing file refused, not a
   traceback.
8. **Nothing works at the shop root.** `spec check` in `support/shop/`: `file: spec/index.md is missing: no
   bounded-context is named`. `work backlog` there and in a context both say `the backlog is empty` (there is no
   `.shop/backlog/` in either). A compact shop has no command that iterates its hosted contexts.
9. **Port refusal reasons force v_m4.** `payments.charge, card declined` and `notebook.entitle, no allowance` cannot
   be stated by any line the core can write (see 7c-1). The rule fires on ports where only the core's reaction is
   specifiable.
10. **The port and the provider's operation are not compared.** The accounts port says `entitle … refused: no
    allowance`, while notebook's `notes.enlarge` has only `done`. Nothing reports that the port expects a refusal the
    provider never gives. This depends on 7a-1.

### 7c. Language gaps (lines that could not be said in grammar 4)

1. **A reply cannot be tied to what it is about.** "If the notebook service refuses a note, then the sharing service
   shall set the status of the invitation to `declined`." Refused: `the verb refuse takes as its object request or a
   kind of it`. "If the notebook service refuses the request, then … the invitation …" Refused: `"the invitation" has
   no antecedent` (R2). "When the payments service completes the charge of a subscription" Refused: `the verb complete
   takes as its object request or a kind of it`. The only workaround is a While clause on the object's status, which
   is loose: it is not linked to the request.
2. **The success of one's own state-changing request cannot be named with its object.** "When the storage service
   completes the request, the backup service shall set the status of the snapshot to `stored`." Refused: `"the
   snapshot" has no antecedent`. Hence `w_m5` on backup.
3. **"the request" in a reply trigger is the indexical "the request the trigger makes"**, so a refusal or completion
   by an upstream reads as a request of its own, not the downstream's earlier request.
4. **A count cannot be compared with another thing's attribute.** "While the number of notes is at least the size of
   an allowance, …" `does not parse at the (token 9 of 30)`. A literal `` `100` `` stands in (w_example).
5. **An attribute cannot be set to a request's parameter or a text value.** "… shall set the spelling of the tag to
   the spelling." `does not parse at the (token 22 of 24)`; "… to `work`." `does not parse at `work``. `set` takes
   only listed values.
6. **A relation phrase cannot be a state verb.** A relation phrase like "open to" or "readable by" collides with the
   action verb or is not read in a While clause. "While a note is readable by a reader, …" `does not parse at
   readable (token 5 of 27)`; "keep the note open to the reader" `refused: the verb open to is a state, and a response
   takes an action`. The relation had to become `has → reader`.
7. **An adjective of a past participle cannot be used in a quantifier.** "every kept note": `does not parse at kept`;
   "every note whose status is `kept`" works.
8. **A state such as "used up" is not sayable** without a value: "While an allowance is used up" `does not parse at
   used`.
9. **Vocabulary collides with the pack.** An attribute word `name` is the pack's verb "name" (v_t16, v_p1).

## 8. Candidate design-decisions and backlog items

Design-decisions (not written):

- **An adapter spec records which provider operation realises each port operation.** The mapping is data in the
  adapter spec, read by traces and by a check against the held contract.
- **A job is served by groups of a capability, not the whole capability.** `serves:` (or `Serves:`) at group level,
  so that two jobs of one capability get distinct traces.
- **A product actor is mapped to each context's actor term.** The product layer names, per context, the proper noun
  that plays each product actor; p4 compares through it.
- **A job may name several actors, each a trigger subject of its served lines.** p4 becomes "every actor triggers a
  served line, and the narrator is one of them".
- **A person-coordinated job names the jobs it needs.** `needs: [j4]` joins their traces.
- **A third-party provider is a bounded context of the domain map without a shop.** It addresses a subdomain, and its
  contract is kept by hand in the adapter spec in the contract form.
- **The long-running process is read off the lines that wait on a reply.** Decision 0134's lifecycle wording is
  restated to what is derivable, or the language gains 7c-2 first.
- **A compact shop keeps each hosted context's published contracts at one place in the shop.** For example,
  `.shop/contracts/<context path>/<version>/`, and obtain within a shop is local.
- **An area's kind is port or nothing; subdomain types are only the product's** (completing decision 0128).

Backlog items (title, then one sentence):

- **spec check of an adapter spec resolves its root.** `model_adapter` reads `root.name` of an unresolved root, so a
  check run in the adapter's folder names `adapters//`.
- **spec parse --file reads under --root and refuses a missing file.** Today it resolves against the cwd and raises
  `FileNotFoundError`.
- **A held provider contract conforms to the contract form.** `spec check` of an adapter spec runs
  `contract_form.problems` on each held contract.
- **spec obtain from a context of the same shop.** Obtain reads a hosted upstream's published contract locally,
  without GitHub, and where publish wrote it.
- **The product layer's forms and their checks.** `.shop/shop.toml`, `product/index.md`, `product/jobs.md` and
  `product/domain.md` become forms `spec forms` lists, with p1-p9 run by a product command.
- **p5 tells port and reached capabilities apart.** A capability serving no job is reported only when no job's trace
  reaches it and it specifies no port.
- **v_m4 on a port operation is met by a core line on its refusal.** A port's declared reason counts as stated when a
  line of the core is triggered on that refusal.
- **A reply trigger names the request's object.** Grammar 4 gains "when the S service completes the <op> of x" or an
  equivalent, so lifecycles can wait on replies (7c-1, 7c-2).
- **A count compared with an attribute's value.** "the number of Ks is at least the T of x".
- **Set an attribute of a text type to a request's parameter.** "set the T of x to the T".
- **spec forms lists the adapter spec, its adr and the port capability.** With their writers, or "by hand".
- **A context's area kind is checked.** Only `port` (or none) is accepted, as anything is today.

## Support files

All under `support/`. Nothing is tracked by the plugin's repository.

- `shop/`: the scratch compact shop, its own git repository (commits by `spec publish` and `spec obtain` included):
  `.shop/shop.toml`, `product/{index,jobs,domain}.md`, `realisations.toml`, and
  `contexts/{notebook,sharing,backup,accounts}/` with specs, features, adapter specs, held contracts and notebook's
  published contract.
- `product_lib.py`, `job_trace.py`, `product_check.py`: read-only readers, the derived trace and coordination kind,
  and checks p1-p9.
- `traces.txt`, `check.txt`, `final-checks.txt`: the trace of every job, the product checks, and each context's and
  adapter's `spec check` / `spec logic` as run.
- `parse_lines.sh` and `probes/*.txt`, `probes/*.out`: each candidate line and its parse (52 parsed, 20 refused), and
  every tool output quoted above.
- `gh/`: the stand-in gh's repositories (symlinks) and calls.
- `variant-group-serves/`: the notebook with `Serves:` lines under groups.
