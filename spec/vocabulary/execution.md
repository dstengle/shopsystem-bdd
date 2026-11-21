---
id: vocabulary/missingmass.io/shopsystem/shopsystem-bdd/execution
area: execution
---

# The words of execution

## Terms

- **review** (noun) → object review. A reviewer's reading of commits against the spec and the repository's rules, written as graded findings: a pull request review or an architecture review.
- **batch plan** (noun) → object batch plan. The file `.shop/batches/<n>/plan.md`, with a batch's tasks and their statuses.
- **batch brief** (noun) → object batch brief. The brief `work batch start` writes for the one fresh agent that runs the batch: the batch, its tasks and worktrees, the skill it follows, the rules and the lessons, and where it stops.
- **review folder** (noun) → object review folder. The scratch directory `batch-<n>-review-<k>` under the batch's worktrees directory, which `work batch brief` writes a review's brief and change into and where the review's findings are saved, and which is never committed.
- **grade** (attribute) → attribute review finding.grade. 
- **Critical** (adjective) → value review finding.grade Critical.
- **Important** (adjective) → value review finding.grade Important.
- **Minor** (adjective) → value review finding.grade Minor.
- **building** (adjective) → value batch.status building.
- **in-review** (adjective) → value batch.status in-review.
- **awaiting-merge** (adjective) → value batch.status awaiting-merge.
- **merged** (adjective) → value batch.status merged.
- **abandoned** (adjective) → value batch.status abandoned.
- **pending** (adjective) → value task.status pending.
- **running** (adjective) → value task.status running.
- **done** (adjective) → value task.status done.
- **failed** (adjective) → value task.status failed.
- **triage** (attribute) → attribute review finding.triage. What a review asks of its finding: fixed on the branch before the merge, kept as an observation, or dropped.
- **fix now** (noun) → value review finding.triage fix now.
- **drop** (noun) → value review finding.triage drop.
- **touch** (verb, state) → relation kept change.touches. A commit's change adds, removes or alters a file. Forms: touches, touched. Frame: <kept change> touches <file>.
- **open** (verb, action) → operation batches.open. Forms: opens, opened. Frame: <actor> opens <batch>.
- **resume** (verb, action) → operation batches.resume. Forms: resumes, resumed. Frame: <actor> resumes <batch>.
- **finish** (verb, action) → operation batches.finish. Forms: finishes, finished. Frame: <actor> finishes <task>.
- **park** (verb, action) → operation batches.park. Forms: parks, parked. Frame: <actor> parks <item>.
- **submit** (verb, action) → operation batches.submit. Forms: submits, submitted. Frame: <actor> submits <batch>.
- **merge** (verb, action) → operation batches.merge. Forms: merges, merged. Frame: <actor> merges <proposed change>.
- **abandon** (verb, action) → operation batches.abandon. Forms: abandons, abandoned. Frame: <actor> abandons <batch>.
- **monitor** (verb, action) → operation batches.monitor. Forms: monitors, monitored. Frame: <actor> monitors <batch>.
- **review** (verb, action) → operation reviews.review. Forms: reviews, reviewed. Frame: <actor> reviews <thing>.
- **conclude** (verb, action) → operation reviews.conclude. Forms: concludes, concluded. Frame: <actor> concludes <review>.
- **the batches service** (proper noun) → service batches.
- **the reviews service** (proper noun) → service reviews.
- **the capability form** (proper noun) → object capability form. A capability file as 0.38 keeps it: its frontmatter names its `area:` and what it `specifies:`, and it holds no empty section.
- **the index form** (proper noun) → object index form. `spec/index.md` as 0.38 keeps it: one `## Composition` section, whose table `| area | kind | capabilities |` has a row for each area, naming its capabilities.
- **virtual environment** (noun) → object virtual environment. The directory `.venv` at the top of a workspace, whose `bin/python` runs the tests of a task and of a batch in place of the `python3` on `PATH`.
