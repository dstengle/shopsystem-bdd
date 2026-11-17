---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-46/review-1
kind: review
batch: batch-46
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/69
head: 14e5ed4a337e17879b7d6f54f9e28d8553e5c143
range: f2b38597d68996d0ce83558fdfc9c60a2aa6ce12..14e5ed4a337e17879b7d6f54f9e28d8553e5c143
result: fix-now
---

# batch-46 review 1

## Verdict

The batch builds all four items. b289 and b346 meet their chore checks. b324's `as_laid` takes a parked item's lines out as `work batch start` laid them. b333 covers readiness#r58 and batches#r46-r49. One thing must be fixed now: the lint run passes at the base and fails at the head, on b333's code. The other three findings are observations.

## Findings

### f1 Important fix now: `tools check` fails at the head (ruff I001, RUF059) and passes at the base
- item: b333
- where: scripts/batch_start.py:9
`python3 scripts/tools check --base f2b38597d` exits 1 at the head and 0 at the base. Its output:

```
scripts/batch_start.py:9:1: I001 [*] Import block is un-sorted or un-formatted
tests/scenarios/batches_handlers_corpus.py:47:20: RUF059 Unpacked variable `n2` is never used
tests/scenarios/batches_handlers_corpus.py:61:20: RUF059 Unpacked variable `n2` is never used
```

The I001 is caused by `import batch_catalogues`, which sits between `import backlog_items` and `import backlog_lines`. `batch` sorts after `backlog`, so it belongs after `backlog_lines`, with the other `batch_*` imports. The RUF059s come from `has_given` and `holds_given` in tests/scenarios/batches_handlers_corpus.py: each unpacks `(k2, n2)` and never uses `n2`. Fix: move the import into its sorted place, and unpack `(k2, _)` in both handlers.

### f2 Minor observation: the change is over the size limit
- item: -
- where: -
The brief's `## Size` gives 34 files, +909 -107: 1016 changed lines against a limit of 1000. Most of it is b333's: two new modules (scripts/spec_corpus_write.py, scripts/batch_catalogues.py), tests/scenarios/batches_handlers_corpus.py, the readiness bar rework, and the corpus blocks and catalogue entries. b324 adds about 100 lines, and b289 and b346 add about 60 between them.

### f3 Minor observation: a design-decision edited by hand in the lay commit, for work outside the batch
- item: -
- where: spec/decisions/0097-while-alpha-a-change-breaks-consumers-cleanly-with-no-compatibility-path.md:7
The lay commit 0fd86032f was rewritten by the batch's driver, by its own message. Among other things it drops `source: [quote-48]` from decision 0097's frontmatter and raises test_decision_checks' totals ("main's failing decision checks mended ... b347"). CLAUDE.md says "A design-decision is written by `work decision` ..., never by hand". The change also belongs to b347, which is not in this batch. The test edit only adds an assertion and weakens nothing. It is recorded here because reverting it would break main's check again. b347 should carry the fix through `work`, or give the reason a hand edit was the only way.

### f4 Minor observation: the parallel shaping brief does not say what to do when another agent holds the git index
- item: b346
- where: skills/shaping-items/parallel-brief.md:31
Every agent of a wave runs committing `work` commands (`work line`, `work rate`, `work ready`) in one checkout. `shop_files.committed` (scripts/shop_files.py:72-89) runs `git add` and `git commit` with no lock. So two agents committing at once can collide on `.git/index.lock`. I checked: the losing command is refused and its files put back, so no data is lost. But the brief's rules do not tell the agent to run a command refused that way again, so an agent may stop with a question it does not need. Fix: add one rule to the brief, "a `work` command refused on `index.lock` is run again".
