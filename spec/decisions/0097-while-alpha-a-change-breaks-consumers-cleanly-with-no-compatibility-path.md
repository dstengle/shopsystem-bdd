---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/while-alpha-a-change-breaks-consumers-cleanly-with-no-compatibility-path
summary: "While the plugin is alpha, a fix that changes generated features, refuses lines that used to parse or changes a command is made cleanly, with no compatibility shim, deprecation period or warning-first phase; its version bump says what changed, not a promise."
date: 2026-11-17
status: accepted
tier: judgement
by: "the session, 2026-11-17"
---

# 0097. While alpha, a change breaks consumers cleanly, with no compatibility path

## Context

The person, 2026-11-11 (quote-48), asked whether the generator fix of PR #51 should ship as a patch for consumers: "This is still alpha, so there should not be any implementations that will have broken gherkin". Kept until now only in a session's memory, which the person has ruled out (quote-38, directive-2); moved here 2026-11-17 (quote-45).

## Decision

The plugin is alpha: no implementation depends on its generated Gherkin or its language staying stable. A change that alters generated features, refuses lines that used to parse, or changes a command needs no compatibility path, warning-first phase or release kept back for consumers' sake: make the clean change. Versions still follow decision 0092 (a y release when consumers must change something, so the release notes and the plugin cache say so), as a record of what changed, not as a compatibility promise. Revisit when the person says the plugin is no longer alpha.
