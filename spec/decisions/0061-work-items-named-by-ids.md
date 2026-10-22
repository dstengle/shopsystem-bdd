---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/work-items-named-by-ids
summary: "A work-item is named by an id `w<n>`, the bounded context's and never repeated, and every command that names a work-item names it by that id."
date: 2026-10-22
status: accepted
source: [observation/2026-10-22-release-gate-0-23-0, measurement/2026-10-22-research-at-the-limit]
by: "the person, 2026-10-22, delegating the drafting decisions to the coordinator; on the design note work-item ids and plugin upgrades (0.24.0)"
---

# 0061. Work-items named by ids

## Decision

A work-item is named by its id `w<n>`: its file is `.shop/work/<initiative>/w<n>.md`, its frontmatter `id` is
`work-item/<context path>/w<n>`, and its title is the file's `# ` heading. `<n>` is one above the highest `<n>` of any
work-item under `.shop/work/`, in any initiative and any status: a work-item id is the bounded context's, never
repeated, as a requirement id is its capability's. Every command that names a work-item names it by its id
(`work retry`, `work withdraw`, pytest's `--work-item`, `work run`'s work-item branch `work/<work-item>` and its
stage directories `runs/<work-item>/`); nothing changes in those commands but what they are given.
