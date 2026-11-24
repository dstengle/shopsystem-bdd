---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-downstream-keeps-its-terms-behind-a-driven-port
summary: "The core reads no upstream word; each upstream is reached through a port area in the downstream's own words."
date: 2026-11-24
status: accepted
tier: judgement
source: [quote-71, quote-75, quote-77]
---

# 0122. The downstream keeps its terms behind a driven port

## Context

Three worked examples (an ordering saga over inventory and payments, the same with swapped providers, and two stock adapters written as adapter specs) settled how a bounded context depends on another; the person accepted the shape (quote-75) and asked for the work to start (quote-77).

## Decision

A core area never imports a provider area or an upstream's vocabulary. Each upstream is reached through a driven port, an area of kind port, whose words are the downstream's. The bound check and v_m1 will refuse a core line using a word only a provider or adapter layer gives. Until the item that checks it is delivered this decision is a judgement; that item writes its successor at its own tier, naming its enforcer.
