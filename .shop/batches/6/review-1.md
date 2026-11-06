---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-6/review-1
kind: review
batch: batch-6
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/21
head: 6f0a50d5b836dc82b26bc9ff6ca75a75e5e8f1ec
range: 0e59811411755e15a4e889c582518dc4612016fc..6f0a50d5b836dc82b26bc9ff6ca75a75e5e8f1ec
result: fix-now
---

# batch-6 review 1

## Verdict

The batch builds both of b31's lines on a first watch, and the skills and module map follow. One finding to fix: a comment that a watch has printed is never printed by a later watch, even while it is still unrecorded. That goes against requests#r42, and neither a line nor the Implementation section asks for that behaviour or the other new behaviour of `work watch`. The runs at `Head:` all exit 0.

## Findings

### f1 Important fix now: a later watch hides a comment that is still unrecorded, against r42, and nothing in the spec asks for it
- item: b31
- where: scripts/request_watch.py:90
r42 says: "While a comment is unrecorded, when a session runs `work watch`, `work` shall print the comment and exit successfully". `watch` first drops every URL kept in `<git dir>/shopsystem/watched.json`:

```
before = kept(root)
new = [(url, line) for url, line in found(root) if url not in before]
```

So a comment that a first watch printed, and that is still unrecorded, is not printed by a second watch. That happens when `work sync` was never run after the first watch, or the comment is unreadable. The second watch does not exit successfully: it polls forever, or with `--polls` exits 1. `tests/scripts/test_request_watch.py:60` asserts exactly this for the unrecorded comment `#issuecomment-2` (the second watch has `returncode == 1` and empty stdout). Untaken asks are treated the same way (r43).

Several observable behaviours are asked for by no line of b31 and given by no part of `spec/capabilities/requests.md`'s `## Implementation, may change`, which this change leaves untouched:
- the kept file;
- `--every`;
- `--polls` ending with exit 1;
- a gh failure said on stderr and the poll retried.

The capability's `## Not yet` (spec/capabilities/requests.md:244) still says "nothing polls … the backlog's b31", which is no longer true.

Fix, on b31's branch, in one of two ways:
- Keep the de-duplication. Then r42 must say so: retire r42 and write a new line whose condition excludes a comment a watch has already printed (requirements-retired-never-edited).
- Drop the kept file, so every unrecorded comment wakes the watch, and deal with the loop on an unreadable comment some other way.

In either case, add an Implementation bullet for `work watch` (`--every`, `--polls`, the kept file in the git dir, the gh retry) and remove the b31 bullet from `## Not yet`.

### f2 Minor observation: `--polls` exits 1 on an empty answer
- item: b31
- where: scripts/request_watch.py:102
Decision 0058 (query-commands-answer-in-their-output) says an empty answer exits successfully. `work watch --polls n` that finds nothing prints "nothing new after n polls" on stderr and exits 1. A watch is a wait more than a query, and the item's notes call `--polls` a test aid, so this is arguable. It is still the one place where the change reads against a judgement decision. Either say in the Implementation bullet why a bounded watch with nothing to report is an error, or exit 0 with that message on stdout.

### f3 Minor drop: leftover `unbuilt: []` and a stray blank line in requests.md
- item: b31
- where: spec/capabilities/requests.md:9
The build left `unbuilt: []` in the frontmatter, which the base did not have. The new `untaken` term bullet sits after a blank line, apart from the other `## Terms` bullets (line 43). This is cosmetic.
