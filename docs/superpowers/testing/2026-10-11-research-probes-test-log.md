# Research probes: test log (0.16.0)

Spec: `docs/superpowers/specs/2026-10-11-research-probes-design.md`. Scripts: 93 OK, unchanged.

## The scout, before and after, on one model

Fixture `/home/vscode/scratch/shopsystem-bdd/probe/` (`make_probe.py`, `run.sh`): a `shelf` library with a command
line that keeps its items in the file `SHELF_FILE` names.

- `store.read(item_id, part=None)` gives the named part in its own code, but `shelf/__init__.py` applies a wrapper
  from `shelf/compat.py` that drops every argument after the first. So a read naming a part gives the whole item
  today.
- A duplicate is refused, the file written and an add counted only in `landing.land`.
- The command line catches `Refused` and nothing else: `add book` with no title is a `TypeError` traceback.

Two slices, each researched by its own `code-scout` on Haiku, three runs before (0.15.0) and three after: slice 3,
a read naming a part; slice 4, a `check-add` that drafts an add and never lands it.

| | 0.15.0, 3 runs | 0.16.0, 3 runs |
|---|---|---|
| a read with a part gives the whole item today | said in 3; shown by a run in 2, by reading in 1 | shown by a run in 3 |
| a section of probes, each with its command, what came back, and `run` | 0 | 6 of 6 notes |
| the nearest cases probed (item missing, part unknown, title empty, add twice, no file) | none set out | 6 of 6 notes |
| slice 4: what landing alone produces | the duplicate refusal, 3 of 3; the count and the write as effects, in passing | set out as a list in 3 of 3: the refusal, the write, the file's creation, the count, and that "no title" is not landing's |
| defects in today's behaviour, under their own heading | 0 | 6 of 6 notes: the argument dropped, an unknown part not refused, the `TypeError` on a missing argument, a latent `KeyError` |
| line count and room of the modules on the path | some lines, in 3 | every module, in 3 |
| the checkout after the run (`git status`) | clean, 3 | clean, 3: every probe's file under `.superpowers/scratch/` |
| the notes, both slices | 1,600 to 1,800 words | 2,200 to 2,600 words |

What the baseline shows is that a scout with no instruction to probe sometimes probes, finds the trap, and writes
it down as one sentence among its reading. With the instruction the same model probes every time, sets the probes
out so a reader can tell what was run, and reports four things wrong with today's behaviour that no baseline run
gave a heading to.

One probe went past the brief in a useful way: a run noted that the command line prints a part through
`json.dumps`, so the author comes out in quotes, and that whether the Then's `"Herbert"` means that is for the
plan.

The trap in this fixture was too shallow to separate the versions on the answer itself: all three baseline runs
named the wrapper. The difference measured is in what is run, recorded and reported.

## Not tested

- **The hand-off's new lines** (one scout a task; `0 production` only on a run probe; a skipped stage's refusals
  named in the task's decisions; a probe's defect triaged): no planning session ran.
- **A dry run agrees with the real run:** no fixture here has a dry run. kb's check and import are the case; the
  test is kb's next batch that touches either.
- **Fix rounds ending:** the re-reviewer's triage line and the controller's rule were not run.
- **The scout on Opus**, the model kb's batch 39 used. Whether Haiku's probes find what Opus's did on kb is what
  the spec's Not yet waits on.
- **A system whose data is not found through one environment variable.** Pointing a probe at scratch is said in
  the project's `CLAUDE.md`; a project that does not say how leaves the scout to work it out.
