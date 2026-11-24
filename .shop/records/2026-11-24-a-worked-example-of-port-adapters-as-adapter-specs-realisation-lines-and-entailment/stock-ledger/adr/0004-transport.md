# 0004 Plain HTTP calls with a timeout

Status: accepted. Scope: this adapter only.

decrement and increment are POST calls with a two-second timeout. A decrement that times out leaves its entry pending
(0002); an increment that times out is retried, since an increment counted twice only overstates stock until the next
reconciliation, which the shop accepts.
