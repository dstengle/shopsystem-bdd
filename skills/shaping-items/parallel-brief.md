# Shaping brief: one item of a wave

The session that shapes several items at once fills this brief once per wave and dispatches one fresh agent per item, in parallel, each with this brief as its whole prompt and its own item named under "Your item". Fill every `<...>`; leave no placeholder.

## The wave

Repository: `<the repository's path>`, on `<the base branch>`. Scripts: `<the repository's path>/scripts/` (`python3 scripts/work ...`, `python3 scripts/spec ...`).

| Item | Title | What its lines are to say |
|---|---|---|
| `b<n>` | <title> | <the behaviour, in the person's words, citing quote-<k>> |

Your item: `b<n>`. The others are shaped by other agents at the same time; read them if you need to, never change them.

## What to do

Follow the shaping-items skill, steps 2-4, on your item: its terms and relation rows, then its lines (or `work chore` when nothing a scenario checks), then `work rate` when it has no rating, then `work ready`. Read raising-a-request's "Writing a line in grammar 4" before the first line.

## Rules

- Touch your own item only: every `work` command you run names `b<n>`. Never edit another item, `spec/`, `features/` or any file by hand.
- Add all your term bullets (and relation rows) before you check a line with `work ready`: each change to the glossary recompiles grammar 4, which takes minutes, so the terms go in at once.
- Run a long command (`work ready`, `spec logic`, `features generate`) with a timeout of a few minutes; past it, say which command and stop.
- No push, and no batch command: `work batch` is the session's, after the wave.
- Never use `git stash`: every worktree shares one stash list, and the other agents of the wave work at the same time.
- Never use Claude Code's memory. A direction that should outlast this brief is the session's to write as a directive; say it in your reply.
- The live directives, as `python3 scripts/work directives` printed them when the session filled this brief, apply to you verbatim:

```
<the output of python3 scripts/work directives>
```

## Your reply

Your item's number and its state (`ready`, or `shaped` with `work ready`'s refusal), its lines as `work show b<n>` prints them, and at most one question, never a guess.
