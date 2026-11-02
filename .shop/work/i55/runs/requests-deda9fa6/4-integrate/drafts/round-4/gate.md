# Gate: requests-deda9fa6, round 4

## requests
Removed (retired):
- [r52] **While** an answer or a turn the asker has sent has not been taken in by the upstream, `work show <request>` shall print the request on either side as awaiting the upstream and not yet taken in.

Added:
- [r73] **While** a turn the asker has passed to the upstream, with any answers sent with it, has not been taken in by the upstream, `work show <request>` run on either side shall print the upstream as the side that acts next and that the turn is not yet taken in.
  (from the answer of 2026-11-02: "Reading 2: only a sent turn (with any answers sent with it) makes the request await the upstream ... 'awaiting the upstream' is only the description printed of who acts next, not a new status named awaiting-upstream.")

Glossary: no change. Decisions: none. Questions: none.
Draft: .shop/scratch/4-integrate/drafts/round-4/spec/capabilities/requests.md
