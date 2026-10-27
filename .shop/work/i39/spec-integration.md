---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/i39-spec-integration
kind: capability-proposal
part_of: initiative/missingmass.io/shopsystem/shopsystem-bdd/i39
status: awaiting-answer
argues: [spec-integration]
adds: [spec-integration#r44]
changes: []
removes: []
date: 2026-10-27
---

# spec-integration

The drafts of this proposal are in .shop/work/i39/runs/i39/1-integrate/drafts/round-1/.

## Questions
- spec-integration r44 (new line): "[r44] **Where** `spec/index.md` names an upstream bounded-context, **when** a round of the kind `integrate` drafts a line that needs what the upstream does not yet give, `initiative-round` shall give in its result the lines of a request into that upstream, in the upstream's terms." (request q14, line 23). The line says `spec/index.md` names an upstream but not how. Readings: (a) no further line; how the index names an upstream is Implementation only (recommended: the line already fixes the behaviour and the lines of q14 do not ask for a format); (b) a field: the frontmatter of `spec/index.md` lists `upstreams: [bounded-context/<context path>, ...]` (Implementation), and the index gains an "Upstreams" section. Answer (a) gives the line as drafted; answer (b) gives the line as drafted plus that Implementation entry and index section.
