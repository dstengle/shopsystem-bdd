---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-63/review-1
kind: review
batch: batch-63
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/87
head: c743adad11e924655207a90f25dab2103fbd82c0
range: 328a1cc3742ad91de0af294c597b41417d4ced36..c743adad11e924655207a90f25dab2103fbd82c0
result: fix-now
---

# batch-63 review 1

## Verdict

The batch builds the lines of b442, b466, b485, b489, b464 and b465. One finding to fix: b490's default base makes `tools check` lint files the branch never changed, which breaks code-analysis#r16.

## Findings

### f1 Important fix now: tools check with no paths lints files only the base branch changed
- item: b490
- where: scripts/tools_check.py:26
With no paths and no `--base`, `cmd_check` runs `git diff --name-only --diff-filter=d <base> -- *.py`. That compares the working tree with the tip of the base branch, not with the point the branch forked from. Once `main` gains a commit that changes a Python file after the branch forks, that file shows up in the diff, so ruff and vulture lint it. If the file holds a finding, the check fails.

The vocabulary entry this batch adds defines differ as "The kept changes of the branch checked out that its base branch does not hold add or alter the Python file". A file that only `main` changed does not differ from the base branch in that sense. code-analysis#r16 says linting such a file shall complete the request; here it fails the check. Uncommitted edits in the working tree are also counted, and they are not kept changes either.

The scenario for g16 (analysis_tools_world.branched) never moves `main` after the fork, so the suite does not see this.

Fix: diff the branch against its fork point, `git diff --name-only --diff-filter=d <base>...HEAD -- '*.py'` (or `git merge-base <base> HEAD`), and add a scripts test where `main` changes a file with a finding after the fork and the check completes.

### f2 Minor observation: the default base is read from the current directory and has no fallback when `main` does not exist
- item: b490
- where: scripts/tools_check.py:14
`base()` reads `Path(".shop/delivery.toml")` relative to the directory the command runs in, not the repository's top level. Run from a subdirectory, it ignores a configured `base` and falls back to `main`. In a repository with no `main` branch and no `base` setting, `tools check` with no arguments used to print "nothing to check" and exit 0; now it is refused with git's "unknown revision" error. No line names either case.

Reproduction: in a repository whose only branch is `master`, run `python3 scripts/tools check`.

### f3 Minor observation: the parse-time guard now catches only a slowdown as large as the grammar before b437
- item: b442
- where: tests/scripts/test_grammar4_guards.py:1155
The item asks for this change, so it does not need fixing. The budget went from 10 s to 25 s, and a parse over it now gets a second try. The line set parses in 1.6 s alone, so the guard fails only when a regression makes parsing about 15 times slower even without load. A generator that multiplies the parse time by 5 to 10 (8 to 16 s) passes both tries. The CLAUDE.md row for this test still says "each guard shown catching a multiplying generator". No test shows the parse-time guard catching anything below 25 s.

I checked that the retry cannot pass just by reading cached parses: `parse_time` calls `spec_grammar4._gf_trees` directly, so it skips spec_parse_cache.
