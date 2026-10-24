# Design state and initiatives

A model for specifying a software system and running the work that
changes it: standing artifacts that describe the design, initiatives
that change it through trees of parts, requests that carry work between
bounded-contexts, records of what was noticed, and a pull-based
work-queue. Written across sessions in September and 13–24 October 2026,
against the shopsystem-kb and shopsystem-bdd repositories.

The reference is **version 4, 2026-10-24**. The model is a product-level
artifact, and the product level has no repository yet, so it stays here;
its move to a product-level repository is a later request.

The plugin's scripts (`model check`) still check the version 3 rules
until a later release implements version 4.

## Read in this order

| file | what it is | read when |
|---|---|---|
| `how-we-got-here.md` | the conversation condensed: what was decided, what it replaced, and why | first, for orientation |
| `design-model.md` | **the reference** (version 4): standing artifacts and edges; requests, initiatives and parts; records; the three structures; the grammar; flow diagrams; the questions the model answers | to learn or apply the model |
| `ecommerce-example.md` | a small shop written in the model and read back as sentences; refused statements with their corrections | to check your understanding, or to test a change to the grammar |
| `grammar.md` | the grammar formally: edge schema, Datalog integrity constraints, lifecycles, sentence forms that map to facts | to build a validator, or to check a change to the model for consistency |
| `kb-and-bdd-assessment.md` | the 13 October review of the plugin and kb that motivated the work layer: findings, numbers, recommendations in order. Predates the scoped vocabulary | for the evidence behind the pull model and the plugin critique |

## Not included

The September documents these build on — `spec-method.md` (the five-part
method, learning path, use-case traces and FAQ) and
`stage-1-capabilities-and-features.md` (the first adoption step) — were
produced in the earlier session and are referenced by name.

## The model in one paragraph

A product is described by **standing artifacts**: the design as it is,
rewritten in place, read to learn the system — the product-vision, jobs,
the context-map of bounded-contexts and context-seams; and in each
bounded-context, capabilities with their capability-requirements,
acceptance-scenarios and design-decisions. Work enters a bounded-context
only as a **request**: lines in EARS, negotiated between asker and
upstream. Each request is fulfilled by one **initiative** of that context
(`fulfils`), realised by a tree of **parts** — capability-proposal,
work-item — that never leaves the context. A job-thread at the product
level raises requests; a context's work-items may raise requests into
the next; done-ness composes through requests only. **Records** — origins
(observations, measurements, review-findings) and history
(decision-arguments, initiative-archives) — are dated and never edited;
only origins may be a request's or an initiative's `source`. A capability
`serves` jobs `using` named dependencies; `depends_on` is derived from
that; the path of a job is the walk along `using`. Work-items are pulled
from the work-queue by fresh workers; a script supervises; language
models do only the judgment steps; every exchange with a person is a
question on a node and its answer.
