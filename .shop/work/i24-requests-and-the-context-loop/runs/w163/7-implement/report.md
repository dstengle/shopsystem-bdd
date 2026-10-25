## Budget
- tests/scenarios/supervision_rounds_steps.py
- scripts/supervise_rounds.py

# Report
Changed: two steps bound in supervision_rounds_steps.py (Given "the integrate round for i1 gives DONE, and every round ends"; Then "the initiative branch has a commit of the integrate round's stage directory with i1's change to started"); in supervise_rounds.py an integrate round that ends DONE now commits its stage directory and log.jsonl (Rounds.round, via `commit(name, after, after)`).
Red: `python3 -m pytest -q -x -k leaves_nothing_uncommitted` first failed on the undefined Given; after the Given, on the Then: `AssertionError: ([], 'work run: ...')` (stage list from `git ls-files` empty: stage directory untracked). Expected: the DONE path committed nothing.
Green: `python3 -m pytest -q --work-item w163`: 147 passed, 1 skipped; tests/scenarios/test_supervision.py: 5 passed.
Suite at start: 849 passed, 1 failed (this scenario) at 27f26a0d.
Size check: nothing printed.
## Tests changed under an allowance
none
## Open questions
- The scenario says one commit of the stage directory "with i1's change to started". I could not make it literally one commit: deferring the started commit until after the round makes the worker guard (supervise_worker.py:185-195, "changed in the repository's own checkout and not committed") fault the round and put initiative.md back (this broke the :1056 scenario). So started is committed before the session as before, and the stage directory in a second commit after it; the Then step checks the commit touching the stage directory holds an initiative.md with status started. Person to rule if a single commit is wanted (would need the guard to exempt it).
- Commit message of the DONE integrate commit is "work: i1 started -> started"; push follows commit as in other moves.
- A second `work run i1` on a started initiative: not refused (scenario only).
## Other
The plan contained no code. Commit: acb76107.
Files changed: scripts/supervise_rounds.py, tests/scenarios/supervision_rounds_steps.py. Now an integrate round ending DONE leaves nothing uncommitted under .shop/work/, so the next `work run` is not refused.
