---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/versions-are-0-y-z-until-1-0
summary: "Until the 1.0 release the plugin is versioned 0.y.z: y for a large or incompatible change, counting past .9 to .10, and z for a non-breaking update."
date: 2026-11-11
status: accepted
tier: judgement
by: "the person, 2026-11-11 (quote-27, quote-28)"
---

# 0092. Versions are 0.y.z until 1.0

## Context

The plugin jumped from 0.29 to 1.0.0 and then through four majors in a few weeks while still alpha; the person asked for semantic versioning without big major jumps, back in a 0.y.z series before 1.0 (quote-27), starting at 0.30 (quote-28).

## Decision

Through the alpha and beta periods the plugin's version is 0.y.z, with semantic versioning's meaning for a 0.x series. y goes up for a large or incompatible change (a language change that refuses lines that parsed, a changed file form, a removed command) and counts as high as needed: 0.9 is followed by 0.10, never 1.0. z goes up for a non-breaking update (a fix, a new command, a new optional field). 1.0.0 is a decision of its own, not a count. The series continues the tagged 0.1-0.29 releases: the releases made as 1.0.0, 2.0.0, 3.0.0, 3.0.1, 4.0.0 and 4.1.0 are 0.30.0, 0.31.0, 0.32.0, 0.32.1, 0.33.0 and 0.34.0, and the next release is 0.34.1.

## Alternatives

Restart at 0.1.0: collides with the tagged 0.1-0.29 releases and breaks migrate's numeric order for repositories that recorded them. Keep the 1.0-4.1 numbers and only slow down: 4.x would still claim a stability the plugin does not have.
