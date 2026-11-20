---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-53/review-1
kind: review
batch: batch-53
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/77
head: a86d6cc26c48ee41484f43f220b84b5ebf5fbc59
range: ec2d60f591cdcf848fb97b26e95bfd50344da612..a86d6cc26c48ee41484f43f220b84b5ebf5fbc59
result: clean
---

# batch-53 review 1

## Verdict

The batch builds b419's chore: `work_items` registers each `@g<n>` and `@r<n>` tag as a mark, and the conftest that `migrate init` writes loads `work_items`. It finds the plugin's scripts on PYTHONPATH, then in `$CLAUDE_PLUGIN_ROOT`, then in the plugin cache folder for the release `.shop/plugin-version` names. The chore's check covers both ways of finding the plugin and the strict xfail. Every run exits 0 at the head, and the change touches only the chore's four files. No test was removed or weakened, no `.feature` file was changed, and the change goes against no judgement decision. It is 193 changed lines, well under the limit. There is nothing to fix now; two observations follow.

## Findings

### f1 Minor observation: the module map rows of work_items and migrate_init no longer give their whole concern
- item: b419
- where: CLAUDE.md:1
CLAUDE.md's module map binds every module to its concern. The row for `scripts/work_items.py` still says the plugin only marks an unbuilt scenario as a strict xfail. It does not say the plugin now also registers each `@g<n>` and `@r<n>` tag of `features/*.feature` as a mark (`pytest_configure`, scripts/work_items.py:41). The row for `scripts/migrate_init.py` says it writes `tests/scenarios/conftest.py`. It does not say that conftest now loads `work_items` and how it finds the plugin's scripts (scripts/migrate_init.py:83). The chore's `Files:` list does not include CLAUDE.md, so `work batch done` would have refused a commit that touched it. That is why this is an observation and not a fix. Fix: put both rows right in a later item that lists CLAUDE.md, or give this chore that path.

### f2 Minor observation: contexts founded before this change keep the old conftest and still warn
- item: b419
- where: scripts/migrate_init.py:167
`migrate init` writes `CONFTEST_TEXT` only into a new context, and only when `tests/scenarios/conftest.py` does not exist (the module docstring, scripts/migrate_init.py:6-7). No upgrade step rewrites the conftest of an existing context. The checklists context from the UX trial named in the item's notes is one of these. Running plain `python -m pytest` there still gives one PytestUnknownMarkWarning per tag. The item asks only about a fresh context, so this is outside its lines. Reproduction: in a context founded at 0.40.0, run `.venv/bin/python -m pytest -q tests`. The warnings are still there, because its conftest does not load `work_items`.
