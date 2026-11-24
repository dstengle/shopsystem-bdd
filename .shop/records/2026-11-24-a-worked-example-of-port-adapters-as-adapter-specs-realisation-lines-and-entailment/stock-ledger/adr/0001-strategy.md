# 0001 Decrement at reserve; take only marks; count not realised

Status: accepted. Scope: this adapter only.

The ledger has no holds and no read. A reservation is a decrement recorded in the adapter's entry; take marks the entry
and calls nothing; free and lapse increment back. stock-port#r6 (count) is not realised: the ledger cannot be read
without side effects. ordering decides whether browsing drops availability (the person's decision, G7).
