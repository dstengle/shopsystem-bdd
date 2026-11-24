# 0003 The ledger's assumed lines are checked in its staging copy

Status: accepted. Scope: this adapter only.

The provider description (spec/model/provider.md, spec/capabilities/ledger.md) is assumed. Its scenarios
(features/ledger.feature) run nightly against the ledger's staging database: decrement keeps the line, a short line
refuses the decrement, increment keeps the line, and decrement refuses atomically below zero under two callers.
