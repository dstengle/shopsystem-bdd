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
- **amend** (verb, action) → operation batches.amend. An item's lines laid again on the workspaces of its batch and of its task after they changed. Forms: amends, amended. Frame: <actor> amends <item>.
- **configure** (verb, action) → operation batches.configure. Forms: configures, configured. Frame: <actor> configures <setting>.
- **setting** (noun) → object setting. One key of `.shop/delivery.toml` that the plugin reads, under the table it belongs to, as `batch_size` or `[review] checks`. Plural: settings.
- **setting value** (noun) → object setting value. The value a setting is given, of the type the plugin reads it as, as `7` for `batch_size`. Plural: setting values.
- **settings file** (noun) → object settings file. The file `.shop/delivery.toml` of a bounded context, which holds its settings. Plural: settings files.
- **the delivery settings form** (proper noun) → object delivery settings form. The settings the plugin reads in `.shop/delivery.toml`: each key under its own table and its value of its own type.
- **conflict** (verb, state) → relation kept change.conflicts with. A task's kept change alters a part of a file, other than a capability's `unbuilt:` line, that a kept change of an earlier task in the batch alters otherwise, so that merging the task branches in task order, each after the ones before, with git's recorded resolutions, leaves the part unsettled. Forms: conflicts, conflicted. Frame: <kept change> conflicts with <kept change>.
- **base merge** (noun) → object base merge. A kept change on a batch's branch that merges the branch the batch started from into it, made after the batch's last review. Plural: base merges.
- **batch rule** (noun) → object batch rule. A rule of a bounded context's own setup that every agent running a batch follows, kept as one entry of the setting `[batch] rules` of `.shop/delivery.toml` and never in the plugin's code. Plural: batch rules.
