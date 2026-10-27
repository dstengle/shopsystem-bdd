## Budget
scripts/workqueue_request.py

## Changed
`_refuse_upstream_part` read the repository's context (`workqueue.context_path`) before checking whether it lists upstreams, so a repository with no spec/index.md was refused ("spec/index.md, which names the context, is missing"). It now reads it only when upstreams are listed.

## Red/green
Suite record: 982 passed, 7 failed at 7b3f8f29 (7 test_requests tests of older scenarios that build a repo without spec/index.md).
Red: `python3 -m pytest -q -n auto -rfEx -p work_items --work-item w211 --whole-suite tests/scenarios/test_requests.py` showed those failures (refusal above).
Green: same command: 43 passed, 11 xfailed. `--work-item w211`: 165 passed, 1 skipped. tests/scenarios/test_work_queue.py and tests/scripts pass. `tools size` prints nothing.

## Tests changed under an allowance
none
## Open questions
none
The plan's code was not pasted; no plan code was involved.
## Outside the file set
none
Commit: cb1aaaef
