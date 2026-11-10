---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-24/review-2
kind: review
batch: batch-24
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/36
head: c0b83608f94dd3e15de26cba412eb92d8a96904d
range: 19df9bd1b7e43a0f5e86a9b8a750ede0c25d8f59..c0b83608f94dd3e15de26cba412eb92d8a96904d
result: clean
---

# batch-24 review 2

## Verdict

The fix commit fixes f1: `re.M` is now `re.MULTILINE`, and `tools check` exits 0 at Head. That commit changes nothing else. One run, `features generate --check`, exits 1 at Head and 0 at the base. The batch's own code did not cause it: the check ran the base checkout's scripts against the batch's spec. Recorded below as an observation.

## Findings

### f5 Minor observation: the `features generate --check` run used the base checkout's scripts, not the batch tree's
- item: -
- where: .shop/worktrees/batch-24/scripts/spec_lexicon.py:31
`## Runs` says `features generate --check` exited 1 at Head (base: 0). It refused each `(verb, action)` and `(verb, state)` term with "is no part of speech". The risk was that the batch's spec labels terms in a way its own lexicon reader refuses.

What I checked:
- The command in the run is `python3 /home/vscode/shopsystem-bdd/scripts/features`, the base checkout's script, not the one in the batch worktree `.shop/worktrees/batch-24/scripts/`.
- The batch tree's `spec_lexicon.py` declares the aspects:

```python
ASPECTS = ("state", "action")
```

  Its `aspect` field reads `(verb, state)` and `(verb, action)`. The base checkout's `scripts/spec_lexicon.py` has neither.
- So the refusal comes from old code reading the batch's new spec labels. It says nothing about the batch.

What would fix it: `work batch brief` should run the `[review] checks` with the worktree's own scripts, so that a run at Head tests Head's code. That is outside this batch's items. The fix commit under review (c2d2af91) does not touch it.

## Earlier findings
- f1: fixed
