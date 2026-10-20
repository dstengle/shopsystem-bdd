---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/delivery-1
kind: work-item
part_of: capability-proposal/delivery-on-v3-delivery
status: done
wkind: capability
under: delivery
accepts: [delivery#r1-r7]
blocked_by: [work-item/supervision-1]
risk: none
---

# delivery-1

## Observable
`delivering-an-initiative` drafts the work-items of an initiative's formulated proposals from the spec alone,
commits them, starts `work run`, and shows the person what `work run` printed.

## Unknown
Whether a session waits on a background `work run` without reading its output (the reply-file wait of
initiative-round is the pattern).

## What changes
New `skills/delivering-an-initiative/SKILL.md`: drafting with `work add` from `spec/`, `features/` and
`.shop/work/`, the commit, `work run`, its printout shown.

## Fixture cases
The session's `work run` uses the stand-in `claude`, whose script turns every item green; the fixture harness is
outside this repository (formulation-1 is deferred).
| requirements | case | what the fixture holds |
|---|---|---|
| r1, r2, r3, r4, r5, r6 | deliver | an initiative with two formulated proposals (lend-items, keep-items' changes) |
| r7 | deliver-unclean | an uncommitted change |

## Files, roughly
`skills/delivering-an-initiative/SKILL.md`, the fixture cases.
