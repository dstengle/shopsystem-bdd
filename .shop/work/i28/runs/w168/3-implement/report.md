## Budget
scripts/workqueue_answer.py, README.md

## Changed
`work answer` takes `<initiative>/<name>`: splits, checks each part with `workqueue.entry`, uses that initiative's file; bare form unchanged. README line names the form.

## Red / green
Red: `python3 -m pytest -q --work-item w168` -> 2 failed (both rows of the outline; `there is no work-item i2/<name>`), expected because `find` refuses `/`.
Green: same command after the change, with tests/scenarios/test_work_queue.py: 2 passed.
Suite at start: 858 passed, 3 failed (the two w168 rows and one supervision test); not run by me.
`tools size --limit 300`: prints nothing.

## Tests changed under an allowance
none

## Open questions
Glob characters in the name part of the prefixed form; initiative done/archived; wording of unknown-initiative refusal (it uses the existing "does not exist" text). Left unchosen.

Plan contained no code. Commit fa6929fb.
Note: the bare-name answer scenarios are deselected by pytest.ini, so I did not see them run.
