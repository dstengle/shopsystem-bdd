---
id: model/example.org/fixture/request-4/work
area: work
kind: core
imports: []
---

# Work

## Purpose

Sessions that follow stages, write files into their worktrees and settle the lines a stage is to meet, and the work
service that answers their requests. Its rows give grammar 4's noun phrases: of, its, has, holds, compounds.

```model
object session kind of agent
  relations: has → worktree (one); follows → stage (many)

object file
  attributes: version: 1.0.0 < 2.0.0 < 2.5.0
  relations: covers → line (many)

object stage
  attributes: status: open | done; tier: test | review; priority: low < high < urgent
  relations: has → line (many)

object line
  attributes: verdict: proposed | accepted | refused | withdrawn

object worktree
  relations: holds → file (many); has → layout (one)

object layout kind of artifact

object stage form kind of artifact

object commit
  relations: has → push (one)

object push

service work
  operation open(summary (flag), interval, source, thread, cause, stage)
    outcomes: done | returned → every file | refused: no summary, source with a thread, stage not done
  operation write(file)  outcomes: done
  operation end(stage)  outcomes: done
  operation give(file)  outcomes: done
  operation settle(line, note)  outcomes: done | refused: no note
  operation assign(session)  outcomes: done
  operation inspect(worktree)  outcomes: returned → the worktree

actor the person kind of agent
```
