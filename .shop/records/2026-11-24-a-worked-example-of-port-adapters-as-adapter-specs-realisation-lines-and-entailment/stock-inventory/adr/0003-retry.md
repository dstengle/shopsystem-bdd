# 0003 Retry with the same reference; release and consume retried as they are

Status: accepted. Scope: this adapter only.

A hold that times out is sent again with the same reference. Release and consume are retried unchanged: inventory's
published contract says both are idempotent. Three tries, then the port's request fails as broken, never refused.
