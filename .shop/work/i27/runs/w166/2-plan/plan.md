# w166 plan: work start commits the initiative (work-queue#r25)

From the research notes at `.shop/work/i27/runs/w166/1-research/notes.md`. Their file:line references are to base 3cbd0c52.

## 1. What goes green

- **work-queue#r25**: scenario "start commits the initiative it writes on the current branch" (features/work-queue.feature:46-54). It is red today for three reasons (notes §1):
  - `work start q1` exits 1 with "spec/index.md, which names the context, is missing". The scenario's Givens write no index.
  - `workqueue_start.start` writes `initiative.md` but never commits it (probe a).
  - The Then phrases "the new initiative's initiative.md" and "the new initiative's directory under .shop/work/" are not mapped to a path. The first runs `git show main:<the phrase>`. The second passes on any path, because it checks a path that does not exist (probe h, D3).
- The work-item retires no scenarios. It has no Retires section and no Rulings.

## 2. Where the change lands

- `scripts/workqueue_start.py`:
  - `start` writes the initiative through `workqueue.committed`, as `work add`, `note`, `answer`, `request` and `resolve` already do. The rels are the new `initiative.md`. The message names the initiative, in the style of the other writers' messages.
  - Everything that can refuse runs before anything is written. That includes the request checks and `workqueue.context_path`.
  - The directory is made inside the write `committed` performs. If the commit is refused, the directory `start` made is removed again.
  - The module docstring stops saying "Written, not committed".
- `tests/scenarios/work_queue_start_steps.py`: the Given "a request q1 that is accepted, whose origins are o1 and o2" also writes `spec/index.md` (conftest's `INDEX`), as the `initiative` helper does.
- `tests/scenarios/work_queue_git_steps.py`:
  - The path resolution used by "main has a new last commit, which holds {rel} …" and "nothing under {where} differs …" also resolves "the new initiative's initiative.md" and "the new initiative's directory under .shop/work/". It resolves them to the one initiative that is new against `context["before"]`, reusing `new_initiatives` from the start steps, and asserts there is exactly one.
  - The directory phrase must resolve to a directory that exists, which fixes D3.
  - The step signatures gain `context` where they need it.

Removed from the researcher's set: `features/work-queue.feature`. The accepted scenario's text stays as accepted (decision 2).

Unchanged, on the path:
- `scripts/workqueue.py` (`committed` is reused; there are only 10 lines of room).
- `scripts/work`.
- `scripts/supervise.py`, `scripts/supervise_brief.py` and `scripts/workqueue_status.py`. These are old-assumption rows only: they now see a committed initiative, which is what they already expect.
- `tests/scenarios/test_work_queue.py`.
- `tests/scenarios/conftest.py`.

## 3. Decisions

1. **`start` commits through `workqueue.committed` and refuses before writing.** It rests on work-queue#r25 and work-queue#r7.
   - A directory that is not a git repository is now refused, and nothing is written (D2, probe b). Today it gets rc 0.
   - A failed commit leaves nothing behind: no file, no empty directory.
   - Only the new `initiative.md` is committed. A change someone else has staged stays out of the commit, as with r9 and r20.
2. **The scenario's missing index is supplied by the step definitions, not by editing the accepted feature.** The request Given writes `spec/index.md`, because a request "kept in this context" presumes the context that `spec/index.md` names. This does not change what the narrator observes in r22: its `initiative` Given already writes the same index. It rests on work-queue#r25: its scenario is accepted as written.
3. **The "new initiative" phrases resolve to the single initiative directory added since the When's snapshot.** The steps assert there is exactly one. It rests on work-queue#r25 and on r22's own "one new initiative".

## 4. Tests the decisions break

None. What I verified, from the notes §4 and from reading the steps:
- The only tests that run `work start` are the r25 scenario and the r22 scenario.
- r22's Givens call `initiative`, which runs `init`, so its repository is a git repository. r20's scenario (work note) shows that `committed` works on a repository with no commit yet.
- r22's Thens read fields, the printed id and `.shop/work/i1/`, never git state.
- Writing the index a second time in r22 writes the same text.
- No test found asserts an uncommitted start, or a start outside git.

The notes report that only one of `test_work_queue.py`'s 65 tests collects in the research run. The implementer should run r22 together with r25 and confirm both are green.

## 5. Open cases (the scenarios are silent; the implementer names them, does not choose)

- **Detached HEAD (probe c).** `committed` commits there today, as it does for r9 and r20. Whether a detached HEAD counts as "the current branch" for r25 is not settled by the scenario.
- **D1.** An existing `.shop/work/i<n>/` with no `initiative.md` crashes with `FileExistsError` (probe f). This is not caused by r25 and is not fixed here. Note it as a defect.
- **Commit refused, for example no git identity.** This case is not probed. Decision 1 says nothing is left behind; name it if a test is added.
