---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/references-are-ids
summary: "Frontmatter names other files by id, never by path: a capability's feature file is features/<its name>.feature and formulated_as is not written; a decision's source lists ids, and where else it came from, in words, is its by."
date: 2026-10-19
status: accepted
source: [observation/2026-10-19-final-state-only]
by: "the person, 2026-10-19"
---

# 0047. References are ids

## Decision

A frontmatter field that names another file of the bounded context names it by its id, never by a path.

- `formulated_as` is gone: a capability `<name>` is formulated in `features/<name>.feature`, always.
- A decision's `source` is a list of ids of nodes in the repository: records (an observation, a measurement, a
  review-finding, a decision-argument, an initiative-archive), an initiative, another decision. Anything else
  it came from, such as the person and a date, a delegation, a release or commit, or a document outside the
  repository, is written in words in `by`, which `scripts/model` does not read.
- A record cited by id has one: every Markdown file under `.shop/records/` but `observations.md` and a
  `README.md` has frontmatter `id`, `kind` and `about`. Archived design notes are `decision-argument`s,
  archived plans, requests and reports `initiative-archive`s, test logs and batch files `measurement`s.

The one path left in frontmatter is a work-item's `fileset`, which claims files and names nothing in the
model. Ids keep the form of design-decision/capability-ids-are-context-scoped.
