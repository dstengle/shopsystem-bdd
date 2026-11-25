---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/an-adapter-is-a-nested-context-with-its-own-spec-checked
summary: "An adapter spec is a context nested in its parent's spec, its id the parent's with /adapter/<name>, whose realised ids are the parent's live requirements and whose providers' contracts are kept; spec check enforces it."
date: 2026-11-25
status: accepted
tier: requirement
enforced_by: [checking#r84, checking#r85, checking#r86, checking#r87]
verified_by: [scenario]
supersedes: [design-decision/missingmass.io/shopsystem/shopsystem-bdd/an-adapter-is-a-nested-context-with-its-own-spec]
---

# 0135. An adapter is a nested context with its own spec, checked

## Context

Decision 0123 was a judgement until the item that checks adapter specs was delivered; b540 delivered it in batch-93.

## Decision

An adapter is a nested context with its own spec (spec/index.md kind: adapter). Its id is the parent's id with /adapter/<name>. It reads the parent's port and port contract, holds its providers, its realisation lines and its adapter decisions, and is never a part of the parent's model. Every id it realises is a live requirement of the parent, and every provider it names has its contract kept. spec check enforces these (checking r84-r87, b540).
