---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/superpowers-dependency
summary: "The plugin declares superpowers@claude-plugins-official as a string dependency and assumes its brainstorming, writing-plans and subagent-driven-development around its own skills."
date: 2026-09-22
status: accepted
revisit_when: "the plugin no longer invokes a superpowers skill"
revisit_signal: requests
by: "README, Requires; .claude-plugin/plugin.json"
---

# 0019. Superpowers dependency

## Decision

`dependencies: ["superpowers@claude-plugins-official"]`, string form with the marketplace suffix. slicing-into-increments and integrating-a-proposal invoke `superpowers:writing-plans`; three skills supersede `superpowers:test-driven-development`.

## Context

The workflow began as a layer on superpowers' pipeline.

## Alternatives

A self-contained plugin.

## Consequences

Initiative i4 (work-items) removes the writing-plans hand-off, the last invocation; i7 then drops the dependency.
