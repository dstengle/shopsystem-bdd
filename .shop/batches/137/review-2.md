---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-137/review-2
kind: review
batch: batch-137
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/160
head: 3dfa70b124c77dbcadc5c68bef10df980a065af3
range: bb74f7cec8f04b7408ec5dc33267c485775f088b..3dfa70b124c77dbcadc5c68bef10df980a065af3
result: clean
---

# batch-137 review 2

## Verdict

The fix for f1 is right. Commit 06536c3b3 renames the stub's parameters to `*_args, **_kwargs` and changes nothing else in the test. The test still makes `subprocess.run` raise and still asserts the same `GenerateError` message. The review check `python3 scripts/tools check --base 48c0c318d` now exits 0, and vulture reports `clean`. Every other run exits 0, as it did at the base. The range changes one line in one file, well under the size limit. No test was weakened, and the change goes against no rule or judgement decision.

## Findings

None.

## Earlier findings
- f1: fixed
