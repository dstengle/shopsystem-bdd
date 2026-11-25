---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-101/review-1
kind: review
batch: batch-101
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/124
head: f707a216ded6885b49941d801d5b23fbc0aec519
range: c399894e98afc17f8f83c0ab70954f477647a975..f707a216ded6885b49941d801d5b23fbc0aec519
result: fix-now
---

# batch-101 review 1

## Verdict

The batch builds all six lines. b654 counts an item's moves as its lines in `readiness_bar.well_formed`, which gives items r64 and r65. b647 adds four things: `left_out`, which names the member lines a restatement cuts (drafting r70); restating an event or an actor in place (`lone`, `lone_at`, `unrestate_lone`; batches r120, r121); keeping a member line on the unlay (`holding`, plus the `restates` guard against the base; batches r119); and the domain-model lines its items declare. No test is removed or weakened, and the features pass `features generate --check`.

One check fails at `Head:` that passed at the base: `tools check` reports ruff errors in a new b647 test module. That is one finding to fix. There is also one observation.

## Findings

### f1 Important fix now: `tools check` fails on ruff errors in the new batches_handlers_added.py
- item: b647
- where: tests/scenarios/batches_handlers_added.py:22
`python3 scripts/tools check --base c399894e9` exits 1 at `Head:` and exited 0 at the base. Its output:

```
tests/scenarios/batches_handlers_added.py:22:77: ISC004 Unparenthesized implicit string concatenation in collection
tests/scenarios/batches_handlers_added.py:25:68: ISC004 Unparenthesized implicit string concatenation in collection
tests/scenarios/batches_handlers_added.py:26:78: FLY002 Consider `f"{HEADER}\n{MEMBER}"` instead of string join
```

The cause is the `LINES` dict. Its two requirement texts are implicit string concatenations inside the dict, and `"\n".join((HEADER, MEMBER))` is a static join. Fix: put each concatenated requirement text in parentheses, or bind it to a name first. Write the join as `"%s\n%s" % (HEADER, MEMBER)` or as an f-string. Then run `tools check` again until it passes.

### f2 Minor observation: an event restated in place leaves its old continuation lines and drops the restatement's
- item: b647
- where: scripts/backlog_model.py:325
When `lone(header)` is true, `merged` replaces only `body[at]`, the event's or the actor's first line. The `members` that `chunks` gives the header are ignored, and nothing is done with `body[at + 1:_end(body, at)]`.

domain_model_parse joins indented continuation lines into one logical line, so an event can be written over two lines, for example:

```
event a note is added: raised by notes.add;
  delivery: at least once
```

Restating that event leaves the old continuation line under the new header. An item's own multi-line event loses its continuation. `unrestate_lone` likewise puts back only the one line.

No line of the batch names a multi-line event, and the fixture's events are single lines, so this does not hold the merge. Fix when such an event appears: treat the lone element as `body[at:_end(body, at)]`, and replace or restore it as header plus members.
