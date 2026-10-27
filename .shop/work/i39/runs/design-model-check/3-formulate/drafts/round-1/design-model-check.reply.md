# design-model-check, round 1

## Coverage

| id | line | scenario |
|---|---|---|
| r120 | "a request neither is part of a job-thread, cites an origin nor is raised for a request" (v17) | a request that is part of no job-thread, cites no origin and is raised for no request is v17 |
| r121 | "an id in this context's files has another context's path on a kind kept in `.shop/work/`, judged from the id alone, other than the request a request is raised for" (v18) | none: returned as a question below |

The other lines are unchanged and keep their scenarios. The scenarios @r115 and @r117 formulate retired lines.

## Questions

- r121: "an id in this context's files has another context's path on a kind kept in `.shop/work/`, judged from the id alone, other than the request a request is raised for"
  - Reading 1: only a request's own naming of the request it is raised for is excused. If another file, such as the `source` of an initiative that fulfils that request, names the same other context's request, v18 names it.
  - Reading 2: an id that is the request some request in this context is raised for is excused wherever this context's files name it, including that initiative's `source`.
  - Why it matters: work-queue r22 writes an initiative's source from "the request's origins". If the request it is raised for counts as an origin, the two readings give different results for that initiative.

## Cases no line mentions

- A request raised for a request of this context, not another context's. r120 accepts it as raised for a request, but no line says whether a request may be raised for one of its own context.
- No line in requests or here says how a request comes to be raised for a request. `work request` (requests r1, r3) takes only `--source` or `--thread`, so `work request` cannot write a request that r120 lets through only because it is raised for a request.
- A request that is raised for a request and also cites an origin or is part of a job-thread.
- A request raised for an id that is not a request, for example an initiative of another context. r121 excuses only "the request a request is raised for".
- Under r121, an id of another context's path that names the request a request is raised for, but with a kind other than `request`.

## Drafts

- /home/vscode/shopsystem-bdd/.shop/worktrees/design-model-check-3-formulate/.shop/scratch/3-formulate/drafts/round-1/design-model-check.feature
- /home/vscode/shopsystem-bdd/.shop/worktrees/design-model-check-3-formulate/.shop/scratch/3-formulate/drafts/round-1/design-model-check.reply.md
