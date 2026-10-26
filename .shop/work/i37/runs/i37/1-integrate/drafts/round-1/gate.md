# Gate, round 1: requests

## requests (drafts/round-1/spec/capabilities/requests.md)

Added:
- [r23] **When** the upstream ends its turn on a request and `work` sets the request's status to `accepted`, `work` shall keep the request's turn the upstream's.
- [r24] **When** `work` sets a request's status to `delivered`, `work` shall pass the request's turn to its asker.

Changed:
- [r7] **When** `work turn <request>` is run on a request that it does not set to `accepted`, `work` shall pass the request's turn to the other side.
  Was: **When** `work turn <request>` is run, `work` shall pass the request's turn to the other side.

Removed: none. Glossary: none changed. Decisions: none.

## Questions

1. r7: narrow r7 as drafted (recommended: r7 and r23 otherwise contradict for an upstream that accepts), or leave it, with r23 and r7 contradicting? Narrowed gives the changed r7 above; unchanged gives no change to r7.
2. term/turn: change the entry to "- **turn**: the side of a request, its asker or its upstream, whose part of the request is to be written next, passed to the other side by `work turn` unless the request becomes accepted, and to the asker when the request is delivered." (recommended, as the definition otherwise disagrees with r23, r24), or leave the entry as it is?
3. Not yet, "The detail of turns, which the person reserved": remove the entry, if this note gives that detail, or keep it (recommended: the note settles two transitions, not the detail)?
4. An already `accepted` request in the asker's turn (q15 itself): add "**While** a request is `accepted` and its turn is the asker's, **when** `work turn <request>` is run, `work` shall pass the request's turn to its upstream." (not in the note), or no line (recommended)?
5. r10: keep "whichever side's turn it is" (recommended; the r10 scenario's given is an accepted request in the asker's turn, narrowing would break it), or narrow to "in the upstream's turn": "**When** `work resolve <request>` is run in the upstream's turn on an `accepted` request with each accepted line's requirement id and the version that holds it, `work` shall write them as the request's resolution."?

## Cut sentences

- The title "An accepted request stays in the upstream's turn until delivered" (r23, r24 give it).
- The delegation text (instruction, not spec).
