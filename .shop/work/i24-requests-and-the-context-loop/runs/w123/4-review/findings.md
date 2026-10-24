# Review of w123: work status and work note

**Verdict: DONE.** No Critical finding and none triaged fix now. Five Minor findings: three observations and two drops.

## Commits reviewed

The branch `work/w123` is gone. These are the commits between `9b90ff4 work: w123 ready -> claimed` and `74afc0d work: w123 claimed -> done` on the checked-out history, less `work run`'s `work:` commits and other work-items' commits (6f87fa1 w122, 9e99ba6 measure, 7d7cd16 w121):

- `75d470b` work note: append a dated line to an initiative's ledger and commit it (r19-r21)
- `2305b9e` work status: where an initiative stands, as text or JSON (r16-r18); model check leaves ledger.md out of the parts

The implementer's result lists `4fc0429` and `34a232c` with the same two subjects. The hashes differ (see F5). The eight files changed are the work-item's fileset, the same as the plan's section 2. Nothing under `features/` changed.

## Removed and weakened tests

None. I searched the diff (`git diff 7d7cd16 2305b9e`) for removed lines in `tests/`. The only change to an existing test file is two added `import *` lines in `tests/scenarios/test_work_queue.py`. No test function was deleted, no parametrize case or assertion was removed, and no skip or xfail was added. The two step modules are new. The plan's "Tests the decisions break" says none, and that matches.

## Allowances

The report's `## Tests changed under an allowance` says "none". Nothing to verify; the diff agrees.

## Cannot verify

- The report's red runs for r16-r18: it says the stub-first red run "was not captured separately". The commits do not show it.
- The report's "suite at the start: 721 passed, 12 failed at 464a900".
- `work status`'s push check against a real remote over the network (the origin in this checkout is https GitHub without credentials, per the work-item's Faults). The scenario covers it only with a local bare remote.

## Findings

### F1. Minor (observation): an unused step parameter, flagged by vulture
`tests/scenarios/work_queue_status_steps.py:72-76`. `ledger_of_twelve` takes `notes` and ignores it, using the hard-coded `NOTES` list. `tools check` reports `unused variable 'notes' (100% confidence)`. The feature's text is a description ("eight notes that do not begin next:"), so hard-coding is defensible. But check's vulture heading is not clean.
Fix: rename it `_notes`, or assert that `notes` begins with `"next: plan w1", "planned w1"`.
Reproduction: `python3 <Scripts>/tools check --base 9b90ff4` gives `== vulture == tests/scenarios/work_queue_status_steps.py:74: unused variable 'notes'`.

### F2. Minor (observation): "pushed" is False, not unknown, when the remote's head is not in the local repository
`scripts/workqueue_status.py:56-57`. `branch()` takes the remote's head sha from `ls-remote` and runs `merge-base --is-ancestor HEAD <sha>`. When that sha is not in the local object store (the remote has commits not fetched yet), merge-base fails, and `git()` returns None. The code then sets `pushed = False`, so it prints "the remote does not have every commit of it". That may be wrong: HEAD can be an ancestor of the remote's head. The honest answer there is None ("the remote cannot be compared with it").
Why it matters: r16's "whether the remote has every commit of it" could be answered falsely. The only effect is a session pushing when it need not, which is why this is not fix now. No scenario covers it.
Fix: when `git cat-file -e <sha>` fails, give `pushed = None`.
Reproduction: not run. The review shell refuses `git init` and the scripts needed to build a two-clone fixture. This is a reading of the code path: the `is not None` test on line 57 turns any merge-base failure into False.

### F3. Minor (observation): `note` and `status` disagree on what an initiative is
`scripts/workqueue_note.py:16`. `note` accepts any directory `.shop/work/<initiative>/`. `status` (`workqueue_status.py:113`) requires `initiative.md`. So `work note x "..."` on a directory with no `initiative.md` writes and commits a ledger there, and `work status x` refuses that same initiative. No client sends this today; `model check` already reports such a directory under r27.
Fix: test for `directory / "initiative.md"`, as status does.
Reproduction: not run (the shell refuses running `scripts/work`). From the code: line 16 tests `is_dir()` only.

### F4. Minor (drop): an odd import layout in a step
`tests/scenarios/work_queue_status_steps.py:21-28`. `with_state` imports from `.test_work_queue` twice inside the function, with the text build between the imports. Polish only.

### F5. Minor (observation): the commit hashes differ from the implementer's result
The result lists `4fc0429` and `34a232c`; the history has `75d470b` and `2305b9e`, with identical subjects and the fileset's eight files. They were most likely rebased when `work run` merged the branch. The content was reviewed from the history. Nothing to fix in the work-item.

### Checked and not a finding
- `model_work.py` leaving `ledger.md` out of the parts: r27's file problems are about initiatives and parts. design-decision/the-ledger-is-tracked fixes the ledger's name, and the ledger is not a part. The change serves r27 and the decision (plan D4). It is not code that no line asks for.
- `note`'s order: the line-break check (r21) runs before any write. `committed` refuses before writing when git cannot commit, and puts the ledger back when the commit fails (r7, r20). `entry` refuses `..` and paths.
- The status output and JSON (r16-r18, D1-D9) match the scenarios. r17 joins the blocks of each open initiative. A named initiative is printed whatever its status.
- No behaviour beyond r16-r21. The help texts and the "none" and "cannot be compared" wordings are mechanism (messages).

## tools check
- ruff: All checks passed!
- vulture: `tests/scenarios/work_queue_status_steps.py:74: unused variable 'notes'` (F1)
- import-linter: the project states no import contracts

## tools size --limit 300
No output: no file over the limit. The touched files' line counts: work 97, workqueue_status.py 129, workqueue_note.py 21, model_work.py 213, work_queue_status_steps.py 157, work_queue_note_steps.py 53, test_work_queue.py 286.

## Commands run
- `git log --format=%H -1 --grep="^work: w123 ready -> claimed$" work/w123` (the branch is gone)
- `git log --oneline -15`
- `git show --stat --format="%H %s" 75d470b 2305b9e`
- `git diff 7d7cd16 2305b9e`
- `sed -n 235,315p features/work-queue.feature`
- a grep for `committed|entry|append|context["head"]|[r27]`, and a read of `scripts/workqueue.py` 56-63 and 150-262
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 9b90ff4`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`
- `wc -l` of the touched files
- `python3 -m pytest -q -p no:warnings -n 0 tests/scenarios/test_work_queue.py -k "status or note"`: 12 passed
- (refused by the shell: running `scripts/work status/note` as refusal probes)
