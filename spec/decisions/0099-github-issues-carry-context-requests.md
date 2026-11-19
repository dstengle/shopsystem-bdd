---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/github-issues-carry-context-requests
summary: "A context request's turns travel as entries on an issue of the upstream's repository; the issue host is a driven port that another channel can replace."
date: 2026-11-19
status: accepted
tier: judgement
---

# 0099. GitHub issues carry context requests

## Decision

A context request is sent as an issue on the upstream's GitHub repository and each turn as an entry (a comment) on it, through the gh program $SHOPSYSTEM_WORK_GH names. The issue host is a driven port: another channel replaces the adapter, not a requirement line.

## Alternatives

Naming issues and comments in the requirements: rejected, the channel is a mechanism (directive-7).
