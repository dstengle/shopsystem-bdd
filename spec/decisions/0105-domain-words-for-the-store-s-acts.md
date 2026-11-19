---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/domain-words-for-the-store-s-acts
summary: "The requirements say keep, share, workspace, shared store, submit, proposed change, entry and close for what git and the issue host do."
date: 2026-11-19
status: accepted
tier: judgement
---

# 0105. Domain words for the store's acts

## Decision

The requirements name the store's and the host's acts by domain words: keep (commit), share (push), workspace (branch and worktree), shared store (remote), submit and proposed change (pull request), entry (comment), close (issue closed). The adapters' contracts map each to its mechanism.
