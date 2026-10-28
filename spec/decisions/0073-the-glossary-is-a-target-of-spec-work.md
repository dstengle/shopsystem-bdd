---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-glossary-is-a-target-of-spec-work
summary: "The glossary is a target of spec work in its own right, beside the capabilities: its terms are proposed by a glossary-proposal of their own, approved at the gate before they are applied to spec/index.md, and its questions are always the person's."
date: 2026-10-28
status: proposed
supersedes: [design-decision/missingmass.io/shopsystem/shopsystem-bdd/glossary-terms-are-standing]
source: [request/missingmass.io/shopsystem/shopsystem-bdd/q30]
by: "the person's ruling, given as the accepted lines of q30, 2026-10-28"
---

# 0073. The glossary is a target of spec work

## Decision

Each bullet of `spec/index.md`'s Glossary, `- **<term>**: <definition>. Not: <word>, <word>.`, is a term of the bounded context with the id `term/<context path>/<term>`, standing and approved at the gate like a Behaviour line; renaming one is removing one and adding another, and `model check` judges requirements and scenarios against the terms and the words they avoid (`v_t1` to `v_t3`). The glossary is a target of spec work in its own right, beside the capabilities: an `integrate` round's change list gives the terms it adds, changes and removes in an entry for the glossary and in no capability's; `work run` writes a glossary-proposal for that entry, whose terms the gate approves before they are applied to `spec/index.md` and which `model check` checks as it checks a capability-proposal's terms; an initiative that changes only the glossary is delivered with no capability-proposal; and a question that names a term or a glossary-proposal is the person's, never answered under a delegation.

## Context

Under decision 0033 a term change could only ride with the capability-proposal that needed it, and every entry of a change list named a capability, so a change to the glossary alone had no proposal to go in.

## Alternatives

A term change riding with a capability-proposal, listed in its `adds`, `changes` or `removes` (decision 0033's consequence), kept: rejected by the person's ruling.
