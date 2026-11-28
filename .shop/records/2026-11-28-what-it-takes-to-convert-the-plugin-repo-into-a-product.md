---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-28-what-it-takes-to-convert-the-plugin-repo-into-a-product
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-28
---

# What it takes to convert the plugin repo into a product

The person's ask (quote-123): "Please run a separate research study on what it will take to convert this plugin repo
into a product." It follows quote-113 ("This shop is not implemented as a product and must be converted"), which is
backlog item b867 "This shop is converted to a product". Only `main` was read. Nothing tracked was changed.

## 1. Which reading, and why

**Primary: a product in the system's own sense.** A product is the layer above bounded contexts. It holds the actors,
the jobs to be done, the subdomains, the domain map of bounded contexts with the job assigned to each, and the
mapping of product actors to each context's actors (`plays`). This reading comes first for three reasons:

- quote-113 and b867 ask for exactly this;
- the plugin now ships this layer (0.45.0: `shop spec product|actor|job|subdomain|context|assign|plays|trace`);
- a plugin whose docs are about to lead with the product (b862) should itself be a product its users can read.

**Secondary: the plain reading.** That is, shipping the plugin as an end-user product. It is covered briefly in §6.
Most of it already exists: a marketplace install, 56 release tags, CHANGELOG and `shop migrate upgrade`.

## 2. Where the repository stands today

| piece | what the system offers | this repository |
|---|---|---|
| product file `.shop/product/product.toml` | written by `shop spec product`, `actor`, `job`, `subdomain`, `context`, `assign`, `plays` (spec/capabilities/product.md, 70 live lines) | **absent** |
| context configuration `.shop/contexts.toml` | `shop work context keep` (spec/capabilities/shop.md r1-r6, scripts/shop_contexts.py) | **absent** (`context list` prints only this context's id) |
| a group's `serves: <job>` | `shop work line <b> --serves <cap>#g<n> <job>` on an item; the batch applies it (decision 0140, scripts/backlog_serves.py) | **none** in spec/capabilities/ |
| product checks | w_unserved_job, w_unserved_cap, w_unplayed_actor, w_unreached_sub, checking r115-r123 (scripts/model.lp:595-649) | silent: with no job node, nothing fires |
| job trace and coordination kind | `shop spec trace <job> [--item b<n>]` (product r26-r36, r58) | nothing to trace |
| a shop hosting several contexts | decision 0129 (shop is not a context; ids flat under the product); `contexts.toml` lists ids | one context, `bounded-context/missingmass.io/shopsystem/shopsystem-bdd`, one flat `spec/` (decision 0131) |

The spec is 25 live capabilities with about 872 live lines:

| area | live lines |
|---|---|
| specification | 402 |
| tracking | 262 |
| execution | 97 |
| analysis | 49 |
| upgrades | 43 |
| measurement | 14 |
| registry | 5 |

The domain model declares two actors: `the person` (spec/model/tracking.md:197) and `the driver`
(spec/model/execution.md:113).

The layer's design was already worked out on this repository's own product, in two analysis records:

- `.shop/records/2026-11-25-a-worked-example-of-the-product-layer-in-a-compact-shop-...md` gives six jobs (j1-j6),
  nine subdomains (s1-s9) and five target contexts, with checks run by a script;
- `.shop/records/2026-11-24-a-worked-example-of-disentangling-this-repository-into-hosted-bounded-contexts.md`.

Since then, the decisions those examples asked for have been written. They are 0128 (subdomains are the product's),
0129-0133, and 0140-0144 (a group serves a job, actor mapping, third-party providers, orphan capabilities). The
tooling has been built and has been through four new-user trials and two docs trials. **This repository is the one
shop that has not adopted the layer.**

## 3. Concrete gaps

1. **No product is declared.** That means no product id (presumably `missingmass.io/shopsystem`, which covers this
   context's id), no purpose, no actors, no jobs, no subdomains, no domain map, no assignments and no `plays`.
2. **No context configuration.** `.shop/contexts.toml` does not exist. No health check fails on that, or on a missing
   product file (b866).
3. **Actors.** The product actors the worked example proposes are the person, a session and a downstream context.
   The model holds only `the person` and `the driver`. Six live capabilities are narrated by a session (request-watch,
   quotes, directives, shaping-guarantees, review-guarantees, trials). None of these narrators is a model actor, so
   `spec plays` refuses to map them (product r61), and w_unplayed_actor fires for any job naming them. Either:
   - the jobs name only `the person`, and session-narrated capabilities are participants or guarantees (decision
     0144, checking r122); or
   - the model gains session actors before `plays`.
4. **Jobs do not cover every subdomain.** In the worked example, s5 (the person's direction) and s8 (codebase
   insight) serve no job. The product capability itself ("say what the product is for") also has no job there. These
   need new jobs, or an accepted warning.
5. **Serving groups are not dedicated.** Each job needs its entry-point groups (decision 0140) dedicated on an item
   and applied by a batch. Expect 6-9 jobs, each with a handful of groups, across items, batches, drafting,
   context-requests, checking (its contract groups only), upgrades and measurement. w_unserved_cap will then name
   the remaining orphan capabilities. Each one must be served, reached by a trace, a port, or a guarantees
   capability; the worked example counted 16 of them.
6. **Traces are under-read.**
   - A response act with no parameters is still an event, not a request (scripts/spec_lf_request.py docstring: "one
     with none keeps its event atom"). So a trace from `batches` follows about 1 of 8 internal requests (worked
     example §4.2).
   - Preconditions that read another area's state, such as "meets the readiness bar", are not counted as reaching
     anything.
   - Until both are fixed, `spec trace` and w_unreached_sub under-report for this repository.
7. **The split is declared, not built.** Decision 0130 accepts that the language toolchain is its own bounded context
   of a supporting subdomain. Decision 0133 makes tracking and execution one work-management context. But:
   - the tooling has one spec root per repository (decision 0131);
   - batches, readiness and `spec check` work on that one root;
   - `shop spec coupling` shows heavy cross-area coupling: tracking uses 390 requirements of specification, and
     specification uses 140 of tracking, through 66 imports.
   - checking r123 fails a group here that serves a job held by another context.

   So jobs cannot be assigned to target contexts that have no spec of their own yet without the check failing.
8. **Index and docs do not name the product.** spec/index.md's Purpose and README.md say "a Claude Code plugin" and
   never name the product this context belongs to. The `.claude-plugin/plugin.json` description still says "for the
   shopsystem harness" and "GF". b862-b864 reorder the docs around the product, but for a user's product, not for
   the plugin's own.
9. **Product repository versus compact shop (open).** Other products already ask this context for work from their
   own repositories (`.shop/requests/q14.md`: asker `product/missingmass.io/subscriptions-viewer`). It is undecided
   whether shopsystem's product layer lives here, in a compact shop, or in a product repository of its own. That
   choice is the worked example's Q6.

## 4. Ordered steps (recommended path: declare compactly now, split later)

| # | step | rough size | depends on |
|---|---|---|---|
| 1 | **Decide the shape** (questions in §7). I recommend a compact shop: this repository holds the product file, one context `shopsystem-bdd` addresses every subdomain (decision 0128 allows "a repository that is many things at once"), and every job is assigned to it. The target contexts of 0130/0133 are a later reassignment (b677). Record it as a design-decision. | small (one decision) | the person, or my call under directive-15 |
| 2 | **Context configuration and health check:** `work context keep` this context; b866's shop health check (product file, contexts.toml, plugin version). | small to medium | - |
| 3 | **Declare the product** (b867, part 1): `spec product missingmass.io/shopsystem --purpose ...`, actors, 6-9 jobs with statements and `--needs` (e.g. j2 build needs j1 shape), subdomains s1-s9 with types, `spec context bounded-context/missingmass.io/shopsystem/shopsystem-bdd --addresses s1..s9 --shop missingmass.io/shopsystem/shop`, `assign` each job, `plays "the person" --as "the person"`. About 30 commands, one commit each, run by a session. | small (one session hour) | 1 |
| 4 | **Settle the non-person actors:** either the jobs name the person alone, or an item adds model actors (a session, a downstream context) and `plays` them. | small, or medium with model lines | 3 |
| 5 | **Dedicate the serving groups** (b867, part 2): one item per job, or a few, with `--serves` pairs; `spec check --item` and `spec trace --item` reviewed before ready; one or two batches. | medium (2-3 items, 1-2 batches) | 3 |
| 6 | **Clear the product warnings:** for each remaining w_unserved_cap, decide whether it is a new job (direction, codebase insight, declaring a product), a participant or a retirement. For w_unreached_sub, accept or fix. | medium | 5 |
| 7 | **Make the trace honest:** read a response act with no parameters as a request (worked example item 1). Optionally count reads of another context's state (that example's Q8). | medium to large (grammar and facts change, many scenarios re-run) | none, but it sharpens 5-6 |
| 8 | **Say it in the spec and docs:** spec/index.md names its product and the jobs it holds, README and plugin.json name the product, and `docs/` links this repository as the worked example of a product (b862's direction applied to the plugin itself). | small | 3, 5 |
| 9 | **Later, the real split** (not part of the conversion): per-context spec roots in one shop, batches per context, published contracts between language, specification and work-management replacing in-process reads, then reassignment of jobs. | large (a design of its own) | 0131 revisited |

Steps 1-6 and 8 make the repository a product in the system's sense. Step 7 makes its traces trustworthy. Step 9 is
the disentangling, which decisions 0131 and 0133 deliberately postpone.

## 5. Risks

- **Self-hosting churn.** The product capability and the checks are themselves specified here. Dedicating groups
  touches checking, product and drafting while their own lines change, so readiness refusals and renumbering
  (backlog_renumber) may interfere with open items.
- **Many warnings.** With jobs declared, `spec check` will print every orphan capability at once. Unless step 6
  follows promptly, that noise can mask real findings for weeks.
- **False confidence from traces.** Until step 7, a job's trace here is mostly its serving groups, and the
  coordination kinds say little.
- **Assigning to target contexts too early.** Declaring language, specification and work-management as separate
  contexts now, with no specs of their own, makes r123 failures and w_unreached_sub findings that no line can clear.
- **Id lock-in.** The product id and job ids are hard to change once requests and other products cite them, as
  q14's asker already does with a product id.
- **The person's actor model.** If sessions must be actors of the product, the model changes in tracking and
  execution ripple into many narrators.

## 6. The plain reading: the plugin as an end-user product (brief)

What exists:

- install: `/plugin marketplace add dstengle/shopsystem-bdd`, `/plugin install` (README.md "Install");
- setup: "Set up this repository for the plugin" runs `migrate init`;
- releases: 56 tags up to v0.45.0, a CHANGELOG with one section per release, docs/upgrading.md and
  `shop migrate upgrade`;
- docs: docs/index.md by reader, troubleshooting and recipes;
- versioning: 0.y.z until 1.0 (decision 0092), and clean breaks while alpha (decision 0097).

Gaps:

- **Platform and dependencies.** GF is only downloaded on Linux x86_64. clingo, pytest 9.1.1 and pytest-bdd 8.1.0
  are pinned (b256 is pytest-bdd 9). `gh` is required for batches and requests.
- **The release is a hand act.** It is a commit, a tag and a CHANGELOG section. No capability, command or check
  holds it: version bumps, the marketplace entry, tag and notes agree only by care.
- **No 1.0 criteria and no support policy.** Nothing says how a user reports a defect, or what alpha breakage
  covers.
- **Onboarding** is in flight (b862-b864, b868 tutorial as end-to-end test, b869 tutorial skill), and
  `plugin.json`'s description is stale.
- **The `shop` CLI is a deliberate non-gap.** It is not on PATH by design: the session runs it. A "support of
  `shop`" story is therefore docs plus `--help` correctness (b841).

## 7. Open questions that need the person

1. **Product id and scope.** Is the product `missingmass.io/shopsystem`? Does it hold other bounded contexts or
   repositories (for instance "the shopsystem harness" plugin.json names) that the domain map must list, hosted by
   other shops or as third-party providers?
2. **Where the layer lives.** Is it here (compact shop), or in a product repository of its own, as
   subscriptions-viewer has (Q6)?
3. **Assignments.** Should every job be assigned to `shopsystem-bdd` now and reassigned at a split (recommended), or
   should the 0130/0133 target contexts be declared now?
4. **Actors.** Should sessions and downstream contexts be product actors (with model actors to play them), or should
   the person be the only product actor?
5. **Jobs.** Is the six-job list right? Should jobs be added for "keep the person's direction for every session",
   "know my code" and "declare what my product is for"?
6. **Plain reading.** Should releases become a specified capability (a `shop` release command with its checks)? Is
   there a 1.0 bar?

## 8. Recommended backlog items (not created)

| # | title | note |
|---|---|---|
| 1 | The shape of shopsystem's product is decided: compact shop, one context, jobs reassigned at the split | A design-decision for open questions 1-3. It precedes b867. |
| 2 | (existing b867) This shop is converted to a product | Refine its notes with steps 3-6 above. Split it into declaring the product (commands only) and dedicating the serving groups (items through batches). |
| 3 | (existing b866) A shop health check fails when the shop keeps no context configuration | Do it first. The conversion then has a check to pass. |
| 4 | This context is kept in its shop's context configuration | `work context keep` of shopsystem-bdd, so b866's check passes here. |
| 5 | The product's jobs cover direction, codebase insight and the product layer itself | Jobs for s5 and s8 and for the product capability, or a decision accepting their warnings. |
| 6 | A session is an actor of the model that a product actor can play | Only if question 4 says sessions are product actors. Needs model actors and `plays` mappings. |
| 7 | Each live capability is an entry point, a participant, a port or a guarantees capability of a job | Work through w_unserved_cap after the dedication, until no orphan is left unexplained. |
| 8 | A response act of an operation's verb with no parameters is read as a request | spec_lf_request's "one with none keeps its event atom". Traces and v_m7 see 1 of 8 internal requests. |
| 9 | spec/index.md, README and plugin.json name the product this context belongs to | Purpose, Composition and the jobs held. plugin.json drops "harness" and "GF". |
| 10 | A release is made by a command whose checks hold the version, tag, marketplace entry and CHANGELOG together | The plain reading. Releases are a hand act today. |
| 11 | The plugin says how a user reports a defect and what alpha breakage covers | Support policy, linked from README and troubleshooting. |
| 12 | Design: one shop hosts several bounded contexts, each with its own spec root | Step 9, for later. Revisits decision 0131. Needed before jobs move to language, specification and work-management. |
