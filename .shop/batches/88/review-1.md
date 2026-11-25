---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-88/review-1
kind: review
batch: batch-88
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/111
head: c650e477dd8696bbc7fb4b88aba6c1c4a0d74663
range: 2ed1e36d4f447a772f3895925649e018225ba1e1..c650e477dd8696bbc7fb4b88aba6c1c4a0d74663
result: clean
---

# batch-88 review 1

## Verdict

The batch builds all fourteen requirement lines of b578. Tracking's four operations (`work allocate`, `deliver`, `restore`, `suspend`) move an item as items r56-r59 say. The batch commands now change an item's status only through them: start and pick through allocate and reopen, park through suspend, merged through deliver, abandon through restore. This builds batches r100, r101 and r105-r112. Every run exits 0, and the feature changes are what `features generate --check` expects. There is nothing to fix now. Three findings are recorded as observations and one as drop.

## Findings

### f1 Minor observation: the change is over the review limit
- item: b578
- where: -
`## Size` gives 26 files, +798 -532, which is 1330 changed lines against a limit of 1000. b578 is the only item, so all of it is b578's. Most of it is mechanical: 14 retired groups are taken out and laid again under new ids in `spec/capabilities/batches.md`, `features/batches.feature`, `grammar/corpus/spec/batches.md` and the `requirements` lists of `spec/adapters/cli.toml`. The code change itself is small (`scripts/backlog_lifecycle.py`, 68 lines, plus one-line swaps in batch_start, batch_pick, batch_tasks and batch_close). Splitting the retire-and-relay of execution's lines from tracking's new operations would have kept each part under the limit.

### f2 Minor observation: the merge's request check no longer asserts the side or the commit of the resolved request
- item: b578
- where: tests/scenarios/batches_handlers_request.py:56
The retired r65 had Thens for the request's side (`turn:` set to `asker`, the old `sets` handler) and for the request file being in the run's commits (the old `commits` handler). Its replacement, r105, says only "resolve the context request". The new `resolved` helper checks the status `delivered`, the `## Resolution` entries, the resolve comment and the closed issue. It no longer checks the side, and it reads the request from the working tree, not from a commit. The line changed, so this is not a weakened test of a live line. Still, context-requests' own resolve scenario (features/context-requests.feature:709-711) shows that resolving sets the side to `asker` and keeps an entry. A `work batch merged` that left the request uncommitted or kept the old side would now pass r105's scenario. Adding the two assertions back inside `resolved` would cost little.

### f3 Minor observation: the new operations declare no refusal, though their commands refuse
- item: b578
- where: spec/model/tracking.md:138
`allocate(item)`, `deliver(item)`, `restore(item)` and `suspend(item, question)` are modelled with `outcomes: done` only. But `backlog_moves.moved` refuses an item whose status is not the move's, for example `work deliver` on a `ready` item. `reopen(item)` beside them does declare `refused: item not ready`. So the model, the contract `spec prepare --contract` prints and the CLI's behaviour disagree about whether these operations can be refused. No line of b578 asks for the refusal, and items r3 covers it for the older moves. Declaring `refused: item not ready` and `refused: item not in-batch`, with lines for them in a later item, would keep the model honest.

### f4 Minor drop: an over-long docstring line in batch_close
- item: b578
- where: scripts/batch_close.py:5
The rewrapped module docstring now has a line of about 160 characters, which breaks the wrapping of the lines around it. ruff passes, so this is cosmetic.
