# 0002 Write-ahead entries and a deadline sweep

Status: accepted. Scope: this adapter only.

An entry is written 'pending' before the decrement and 'decremented' after it. A sweep every minute lapses each
decremented entry past its deadline (15 minutes after the reserve: ordering's number, G6). A pending entry found after a
crash cannot tell whether the ledger decremented: it is reported for reconciliation, never retried (G4).
