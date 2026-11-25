---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-command-is-shop-with-a-subcommand-per-concern
summary: "The plugin's one command is shop (shop work, shop spec, shop model, ...), since work no longer names what it covers."
date: 2026-11-25
status: accepted
tier: judgement
source: [quote-83]
---

# 0132. The command is shop with a subcommand per concern

## Context

Open question Q10 of the disentangling worked example: whether work stays one command over tracking and execution.

## Decision

The plugin keeps one command over the contexts a shop hosts, named shop, with the present commands as its subcommands (shop work, shop spec, shop model, and so on).

## Alternatives

A command per context: rejected for now. Keeping work: rejected, the name does not fit what it covers.
