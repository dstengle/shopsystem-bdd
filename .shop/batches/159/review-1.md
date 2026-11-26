---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-159/review-1
kind: review
batch: batch-159
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/182
head: c76c6b797c0b8b50acead5fc48056a0dbeac34b3
range: 6196df3ff37c05e40a5d97e9b2ecf834ded52a28..c76c6b797c0b8b50acead5fc48056a0dbeac34b3
result: fix-now
---

# batch-159 review 1

## Verdict

The batch builds b815's line, b810's two lines and b816's chore. It builds b814's line only in the case its title names, so there is one finding to fix, on b814. All five checks in the brief exit 0, as they did at the base. The change is 739 changed lines against a limit of 1000.

## Findings

### f1 Important fix now: product#r68 says more than the code does
- item: b814
- where: scripts/product_trace.py:165
The line reads:

```
While an item holds a requirement group that serves a job and no capability has the requirement group, if the person traces the job without an item, then the product service shall refuse the request and name the item.
```

Nothing in that condition says the item's group must be the only one that serves the job. The code refuses only inside `if found is None:`, that is, only when no live group serves the job. Take a job served by a live group of a capability and also by a group that an open item holds and that no capability has. Under the line, `spec trace <job>` is refused and names the item. Under the code, it returns the trace with exit 0. That is a wrong answer against the line. The one scenario (`features/product.feature`, `@g68`) builds only the case where nothing else serves the job, so this goes untested.

The code matches the item's title ("a job only an open item serves") and is the sensible behaviour. Refusing every trace of a job once an item serves it would break `spec trace` for any job that has a draft in progress. So the line is what should change, not the code. Fix: reword product#r68 on b814 so that its condition is that no capability has a requirement group serving the job, for example:

```
While an item holds a requirement group that serves a job and no capability has a requirement group that serves the job, if the person traces the job without an item, then the product service shall refuse the request and name the item.
```

Use `work line --reword`, then `work batch amend b814`, then regenerate the feature and the corpus block. If the line has to stay as written, the code has to refuse in the mixed case too.

### f2 Minor observation: three module-map rows still describe the old output
- item: b815
- where: CLAUDE.md:211
`work line` now prints each requirement line it adds with its id and its text (drafting r98). This goes through the new `backlog_lines.added` and through new prints in `backlog_relied.cmd` and `backlog_retirements.cmd`. The module-map rows of `scripts/backlog_lines.py`, `scripts/backlog_relied.py` and `scripts/backlog_retirements.py` name neither `added` nor the changed output, so the map no longer says where r98 is built. Fix when convenient: add `added` (drafting r98, b815) to backlog_lines' row, and note the printed line in the other two rows.

### f3 Minor observation: some lay failures would crash where the docstring says nothing is refused
- item: b810
- where: scripts/backlog_term_rules.py:706
`violations` catches only `Refused` and `OSError`. Its docstring, and the module map, say that "a lay or a read of the copy refused or failing on a file" refuses nothing. Any other exception raised by `lay_onto`, `spec_lexicon.read` or `spec_vocabulary.problems` on the copy would escape. A `ValueError` or `KeyError` on a malformed entry or model line is one example. `work line --term` would then crash with a traceback instead of committing the term, and the readiness bar would never get to report the problem. What I checked: both `problems` functions return `(code, term, message)` triples, so the filter on `f[1]` reads the word as intended. I found no input today that raises anything else, so this is hardening only.
