---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-103/review-1
kind: review
batch: batch-103
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/126
head: 64c750e7d4a4450f42cbcae2432e1b2983819cfd
range: 3c1bdf65471b6970c6eeb9e8d369d9efb9091870..64c750e7d4a4450f42cbcae2432e1b2983819cfd
result: fix-now
---

# batch-103 review 1

## Verdict

The batch builds all three of b641's lines: drafting#r71, batches#r124 and checking#r110. All five runs exit 0, and the change is 817 changed lines against a limit of 1000. One finding needs fixing: the unlay can take away a `serves:` job that its lay never added. There is also one observation.

## Findings

### f1 Important fix now: the unlay takes a job off a group even when the lay never wrote it
- item: b641
- where: scripts/backlog_serves.py:729
`lay` leaves the group's line alone when it already names the job:
```python
new = line if job in jobs else "%s %s" % (spec_read.SERVES, ", ".join(jobs + [job]))
```
`unlay` removes the job either way:
```python
jobs = [j for j in spec_read.jobs_of(line) if j != job]
```
Nothing refuses the pair beforehand. `dedicate` (scripts/backlog_serves.py:658) only checks that the group exists. So there are two cases where the job is lost:
- An item dedicates a live group to a job it already serves on main. `work batch start` lays nothing. When the item is parked, its unlay (`backlog_lines.unlay`, line 231, through batch_parked) deletes the job from the base's `serves:` line. The line goes entirely when that was its only job.
- Two items of one batch dedicate the same live group to the same job. Parking the second item takes away the job the first item laid.

Either way the capability file on the batch branch loses a `serves:` job it held, and `w_unserved_cap` can then report that capability. That is data lost.

Fix: in `dedicate`, refuse a pair whose live group already serves the job in the capability file, naming the group and the job. The unlay should also leave a job alone when the file at the batch's base, or another item's lay, put it there. Add a script test that lays and unlays an item over a group that already serves the job, and checks the job is still on the line afterwards.

### f2 Minor observation: `--serves` drops the other options it is given without saying so
- item: b641
- where: scripts/backlog_serves.py:675
`backlog_cli.cmd_line` sends any `work line` call that has `--serves` to `backlog_serves.cmd`, because `given` is true whenever `--serves` is set. Unlike the other modules in `EDITS` (backlog_area_move, backlog_model_edit, backlog_piece_edit), `cmd` never checks for other options. They are dropped without a word.

Reproduction: run `work line b1 --into work-queue --retires work-queue#r3 "<line>" --serves start-work`. The line is written and its group dedicated, but `r3` never goes under `retired:`. The same happens to `--term`, `--model` and `--relation`. In the same way, `--serves work-queue#g1 start-work --into drafting` uses work-queue and ignores `--into`. No client sends these today.

Fix: refuse `--serves` beside any piece other than a requirement line, `--into`, `--group` and `--in`, as the other edit modules do.
