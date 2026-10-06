# Agent Efficiency Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Cut the wall-clock, tokens and repeated work a shopsystem-bdd batch spends on the same outcome: a fast suite before the batch, each suite run counted once, dependencies probed at the pin, fewer round trips, a smaller controller context, and two scripts for the plan and feature edits that went wrong by hand.

**Architecture:** Two standard-library Python scripts under `scripts/` (`features`, `plan`), each with unittest tests under `tests/scripts/`. Skills and agents change in prose, each change pressure-tested with a headless baseline before the edit and the same prompt after, as this repository's skills are. Skills reach the scripts relative to their own base directory; agents reach them through `Scripts:` in the plan's Global Constraints, which slicing writes.

**Tech Stack:** Python 3.11 standard library (`argparse`, `re`, `pathlib`, `subprocess`, `unittest`); Claude Code plugin markdown (skills, agents); Gherkin with pytest-bdd in the fixtures; headless `claude -p` for baseline and green runs.

**Spec:** `docs/superpowers/specs/2026-10-06-agent-efficiency-design.md`. Evidence: `~/.superpowers/diagnosing-superpowers/875cf22f-366c-4628-b5b9-c0e63fb6c61d/report.md`.

## Global Constraints

- Every skill and agent change is written test-first per superpowers:writing-skills: a headless baseline before the edit, the same prompt after, logged under `docs/superpowers/testing/2026-10-06-*.md`. A baseline that already passes is logged as such; the edit still lands, since the evidence is the shop-knowledge session.
- Headless runs: cwd is the fixture, never this repository; `claude -p --model opus --plugin-dir /home/vscode/shopsystem-bdd` plus superpowers from the installed marketplace; fixtures live under `$SCRATCH` (the executing session's scratchpad). A run that read any file of this repository other than the plugin's own skills, agents and scripts is contaminated and discarded.
- Scripts: plain Python 3 from the standard library, `#!/usr/bin/env python3`, executable, no `.py` extension, `--help` as the contract. Exit status 0 on success, 1 when a check fails or an edit is refused, 2 on bad usage. An edit that would leave its file invalid is refused and the file is left as it was.
- Script tests: `python3 -m unittest discover -s tests/scripts -v` from the repository root, each test in a temporary directory, the script run as a subprocess.
- Skills name a script as `python3 <this skill's base directory>/../../scripts/<name>`; agents as `python3 <Scripts>/<name>`, `Scripts:` read from the plan's Global Constraints.
- A suite record is the log line `Suite: <N> passed, <M> failed at <short hash> in <seconds> s`, with `; failing: <titles>` when M is not 0. It holds at `HEAD` while nothing outside `docs/superpowers/plans/` differs between its commit, `HEAD` and the working tree.
- A request to another repository is the log line `REQUEST <repository>: <what is needed>`.
- The slow-suite bound is 60 s.
- Drafts path for spec agents: `.superpowers/spec-drafts/<run>/`, git-ignored in the consuming repository.
- House style: terse, rule-and-table, as the existing skills; Common Mistakes and Rationalizations rows only from baseline evidence.
- Review-by-risk (0.9.0) is unchanged: no task here adds per-task review.
- No commit, push or tag of any consuming repository. `shopsystem-knowledge` and `shopsystem-kb` are only ever copied.

## Review Focus

1. A scenario title present in two feature files: `features tag` must refuse and name both files, never tag the first it finds (pytest-bdd binds one and drops the other). Pinned in Task 1.
2. A living plan with a section the script does not know (`## Requests`, `## Notes`): every edit must leave it byte for byte. Pinned in Task 2.
3. A suite record whose commit is no longer in the repository (rebased or amended away): `--current` says stale and names the commit, never crashes and never says current. Pinned in Task 2.
4. The first slice of a fresh plan, with no suite record yet: the implementer runs the whole suite once at the start to make one, and only then. Pinned in Task 3's wording and green run.
5. A spec agent that writes outside the drafts path: the controller's check (`git status --porcelain` clean apart from ignored paths) stops it before the gate. Pinned in Task 5.

---

### Task 1: The `features` script

**Files:**
- Create: `scripts/features`
- Test: `tests/scripts/test_features.py`

**Interfaces:**
- Produces: `features [--dir DIR] count --by-tag` (lines `<tag> <n>` in natural order, then `total <n>`); `features list (--tag T | --title S)` (lines `<path>: <title>`, exit 1 when none); `features tag "<title>" slice-<n>`; `features move "<title>" --to FILE [--inline-background]`; `features verify-moved --from DIR` (`<n> scenarios match`, or lines `missing:`, `added:`, `changed: <title> (<tags|description|steps>)`, `duplicate title before|after:` and exit 1). Default `--dir` is `features`.

- [ ] **Step 1: Write the failing tests**

`tests/scripts/test_features.py`:

```python
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parents[2] / "scripts" / "features"

CART = '''# formulated from spec/capabilities/cart.md
@cart
Feature: Cart
  Narrator: a shopper

  Background:
    Given an empty cart

  @slice-1
  Scenario: Adding a product
    When the shopper adds a "pen"
    Then the cart holds 1 item

  @slice-2 @wip
  Scenario Outline: Adding several
    When the shopper adds <n> pens
    Then the cart holds <n> items

    Examples:
      | n |
      | 2 |
      | 3 |

    @slow
    Examples:
      | n  |
      | 10 |

  Scenario: A note that mentions keywords
    Given a note
      """
      Scenario: not a scenario
      @slice-9
      """
    Then nothing happens
'''


class FeaturesTest(unittest.TestCase):
    def setUp(self):
        self.tmp = pathlib.Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        (self.tmp / "features").mkdir()
        self.cart = self.tmp / "features" / "cart.feature"
        self.cart.write_text(CART)

    def run_script(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *args], cwd=self.tmp,
                              capture_output=True, text=True)

    def test_count_by_tag_counts_outline_rows_and_inherits_tags(self):
        done = self.run_script("count", "--by-tag")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(done.stdout, "cart 5\nslice-1 1\nslice-2 3\nslow 1\nwip 3\ntotal 5\n")

    def test_docstring_text_is_not_a_scenario_or_tag(self):
        done = self.run_script("list", "--tag", "slice-9")
        self.assertEqual(done.returncode, 1)
        self.assertEqual(done.stdout, "")

    def test_list_by_tag(self):
        done = self.run_script("list", "--tag", "@slice-2")
        self.assertEqual(done.stdout, "features/cart.feature: Adding several\n")

    def test_list_by_title(self):
        done = self.run_script("list", "--title", "note")
        self.assertEqual(done.stdout, "features/cart.feature: A note that mentions keywords\n")

    def test_tag_replaces_slice_tag_and_nothing_else(self):
        done = self.run_script("tag", "Adding a product", "slice-3")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(self.cart.read_text(), CART.replace("  @slice-1\n", "  @slice-3\n"))

    def test_tag_keeps_other_tags(self):
        self.run_script("tag", "Adding several", "slice-5.1")
        self.assertEqual(self.cart.read_text(), CART.replace("  @slice-2 @wip\n", "  @slice-5.1 @wip\n"))

    def test_tag_adds_a_tag_line_where_there_is_none(self):
        self.run_script("tag", "A note that mentions keywords", "slice-4")
        self.assertEqual(self.cart.read_text(), CART.replace(
            "  Scenario: A note that mentions keywords\n",
            "  @slice-4\n  Scenario: A note that mentions keywords\n"))

    def test_tag_refuses_an_unknown_title(self):
        done = self.run_script("tag", "Removing a product", "slice-3")
        self.assertEqual(done.returncode, 1)
        self.assertEqual(self.cart.read_text(), CART)

    def test_tag_refuses_a_title_in_two_files(self):
        other = self.tmp / "features" / "other.feature"
        other.write_text("Feature: Other\n\n  Scenario: Adding a product\n    Given x\n")
        done = self.run_script("tag", "Adding a product", "slice-3")
        self.assertEqual(done.returncode, 1)
        self.assertIn("cart.feature", done.stderr)
        self.assertIn("other.feature", done.stderr)
        self.assertEqual(self.cart.read_text(), CART)

    def test_tag_rejects_a_malformed_slice(self):
        self.assertEqual(self.run_script("tag", "Adding a product", "3").returncode, 2)

    def _before_and_checkout(self, header="@cart\nFeature: Checkout\n  Narrator: a shopper\n"):
        shutil.copytree(self.tmp / "features", self.tmp / "before")
        checkout = self.tmp / "features" / "checkout.feature"
        checkout.write_text(header)
        return checkout

    def test_move_with_background_inlined_verifies(self):
        checkout = self._before_and_checkout()
        done = self.run_script("move", "Adding a product", "--to", "features/checkout.feature",
                               "--inline-background")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertIn('    Given an empty cart\n    When the shopper adds a "pen"\n', checkout.read_text())
        self.assertNotIn("Adding a product", self.cart.read_text())
        done = self.run_script("verify-moved", "--from", "before")
        self.assertEqual((done.returncode, done.stdout), (0, "3 scenarios match\n"))

    def test_verify_catches_a_lost_background(self):
        self._before_and_checkout()
        self.run_script("move", "Adding a product", "--to", "features/checkout.feature")
        done = self.run_script("verify-moved", "--from", "before")
        self.assertEqual(done.returncode, 1)
        self.assertIn("changed: Adding a product (steps)", done.stdout)

    def test_verify_catches_a_lost_feature_tag(self):
        self._before_and_checkout(header="Feature: Checkout\n  Narrator: a shopper\n")
        self.run_script("move", "Adding a product", "--to", "features/checkout.feature",
                        "--inline-background")
        done = self.run_script("verify-moved", "--from", "before")
        self.assertEqual(done.returncode, 1)
        self.assertIn("changed: Adding a product (tags)", done.stdout)

    def test_verify_catches_a_changed_step(self):
        shutil.copytree(self.tmp / "features", self.tmp / "before")
        self.cart.write_text(CART.replace("holds 1 item", "holds one item"))
        done = self.run_script("verify-moved", "--from", "before")
        self.assertEqual(done.returncode, 1)
        self.assertIn("changed: Adding a product (steps)", done.stdout)

    def test_verify_catches_a_duplicate_title(self):
        shutil.copytree(self.tmp / "features", self.tmp / "before")
        (self.tmp / "features" / "other.feature").write_text(
            "Feature: Other\n\n  Scenario: Adding a product\n    Given x\n")
        done = self.run_script("verify-moved", "--from", "before")
        self.assertEqual(done.returncode, 1)
        self.assertIn("duplicate title after: Adding a product", done.stdout)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python3 -m unittest discover -s tests/scripts -v`
Expected: every test fails or errors, the script not existing (`can't open file '.../scripts/features'`).

- [ ] **Step 3: Write the script**

`scripts/features`:

```python
#!/usr/bin/env python3
"""Read and edit Gherkin feature files without the test runner.

Commands:
  features count --by-tag
  features list (--tag TAG | --title TEXT)
  features tag TITLE slice-N
  features move TITLE --to FILE [--inline-background]
  features verify-moved --from DIR

Each command reads the *.feature files under --dir (default: features), recursively.
A Scenario Outline counts once per Examples row, as the test runner collects it;
feature tags apply to every scenario in the file, Examples tags to their rows.
`tag` replaces or adds one scenario's @slice tag and changes no other line.
`move` moves a scenario verbatim; --inline-background inserts its source Background's
steps as its first steps. `verify-moved` checks every scenario under --from equals
one under --dir: tags, description, and Background steps followed by its own.
Exit status: 0 on success, 1 when a check fails or an edit is refused, 2 on bad usage.
"""
import argparse
import pathlib
import re
import sys

FEATURE_RE = re.compile(r"^\s*Feature:")
BACKGROUND_RE = re.compile(r"^\s*Background:")
SCENARIO_RE = re.compile(r"^\s*(Scenario Outline|Scenario Template|Scenario|Example):\s*(.*?)\s*$")
EXAMPLES_RE = re.compile(r"^\s*(Examples|Scenarios):")
RULE_RE = re.compile(r"^\s*Rule:")
STEP_RE = re.compile(r"^\s*(Given|When|Then|And|But|\*)\s")
TAG_TOKEN_RE = re.compile(r"@[^\s#]+")
SLICE_TOKEN_RE = re.compile(r"@slice-\d+(?:\.\d+)*")
SLICE_ARG_RE = re.compile(r"slice-\d+(?:\.\d+)*")


class Refused(Exception):
    pass


def tags_in(lines):
    return {t[1:] for line in lines for t in TAG_TOKEN_RE.findall(line)}


def indent_of(line):
    return line[: len(line) - len(line.lstrip(" \t"))]


def classify(lines, path):
    kinds, fence = [], None
    for line in lines:
        s = line.strip()
        if fence:
            kinds.append("doc")
            if s.startswith(fence):
                fence = None
        elif s.startswith('"""') or s.startswith("```"):
            fence = s[:3]
            kinds.append("doc")
        elif not s:
            kinds.append("blank")
        elif s.startswith("#"):
            kinds.append("comment")
        elif s.startswith("@"):
            kinds.append("tag")
        elif s.startswith("|"):
            kinds.append("table")
        elif FEATURE_RE.match(line):
            kinds.append("feature")
        elif BACKGROUND_RE.match(line):
            kinds.append("background")
        elif SCENARIO_RE.match(line):
            kinds.append("scenario")
        elif EXAMPLES_RE.match(line):
            kinds.append("examples")
        elif RULE_RE.match(line):
            raise Refused(f"{path}: Rule: blocks are not supported")
        elif STEP_RE.match(line):
            kinds.append("step")
        else:
            kinds.append("text")
    return kinds


def kept(lines, kinds):
    """The lines that carry meaning, stripped: no blanks, no comments."""
    return [l.strip() for l, k in zip(lines, kinds) if k not in ("blank", "comment")]


class Feature:
    def __init__(self, path):
        self.path = pathlib.Path(path)
        text = self.path.read_text(encoding="utf-8")
        if text and not text.endswith("\n"):
            text += "\n"
        self.lines = text.splitlines(keepends=True)
        self.kinds = classify(self.lines, self.path)
        self.tags, self.background, self.scenarios = set(), None, []
        for i, k in enumerate(self.kinds):
            if k == "feature":
                self.tags = tags_in(self.lines[self.tag_start(i):i])
                break
        heads = [i for i, k in enumerate(self.kinds) if k in ("background", "scenario")]
        starts = [self.tag_start(i) for i in heads]
        for n, i in enumerate(heads):
            end = starts[n + 1] if n + 1 < len(heads) else len(self.lines)
            if self.kinds[i] == "background":
                self.background = (i, end)
            else:
                keyword, title = SCENARIO_RE.match(self.lines[i]).groups()
                outline = keyword in ("Scenario Outline", "Scenario Template")
                self.scenarios.append(Scenario(self, starts[n], i, end, title, outline))

    def tag_start(self, i):
        while i > 0 and self.kinds[i - 1] == "tag":
            i -= 1
        return i

    def first_step(self, begin, end):
        return next((i for i in range(begin, end) if self.kinds[i] == "step"), end)

    def background_steps(self):
        if not self.background:
            return []
        kw, end = self.background
        first = self.first_step(kw + 1, end)
        return kept(self.lines[first:end], self.kinds[first:end])

    def write(self):
        self.path.write_text("".join(self.lines), encoding="utf-8")


class Scenario:
    def __init__(self, feature, start, kw, end, title, outline):
        self.feature, self.start, self.kw, self.end = feature, start, kw, end
        self.title, self.outline = title, outline

    def own_tags(self):
        return tags_in(self.feature.lines[self.start:self.kw])

    def examples(self):
        """(tags, rows) for each Examples table; the header row is not a row."""
        f, found, i = self.feature, [], self.kw + 1
        while i < self.end:
            if f.kinds[i] != "examples":
                i += 1
                continue
            tags = tags_in(f.lines[f.tag_start(i):i])
            rows, j = 0, i + 1
            while j < self.end and f.kinds[j] in ("table", "blank", "comment"):
                rows += f.kinds[j] == "table"
                j += 1
            found.append((tags, max(rows - 1, 0)))
            i = j
        return found

    def collected(self):
        """(tags, count) for what the test runner collects from this scenario."""
        base = self.feature.tags | self.own_tags()
        if not self.outline:
            return [(base, 1)]
        return [(base | tags, rows) for tags, rows in self.examples()]

    def all_tags(self):
        tags = self.feature.tags | self.own_tags()
        for t, _ in self.collected():
            tags |= t
        return tags

    def signature(self):
        f = self.feature
        first = f.first_step(self.kw + 1, self.end)
        return {
            "tags": sorted(self.all_tags()),
            "description": kept(f.lines[self.kw + 1:first], f.kinds[self.kw + 1:first]),
            "steps": f.background_steps() + kept(f.lines[first:self.end], f.kinds[first:self.end]),
        }


def load(directory):
    root = pathlib.Path(directory)
    if not root.is_dir():
        raise Refused(f"{root}: no such directory")
    return [Feature(p) for p in sorted(root.rglob("*.feature"))]


def the_scenario(features, title):
    found = [s for f in features for s in f.scenarios if s.title == title]
    if len(found) != 1:
        where = ", ".join(str(s.feature.path) for s in found) or "no feature file"
        raise Refused(f"{len(found)} scenarios titled {title!r}: {where}")
    return found[0]


def natural(tag):
    return [int(p) if p.isdigit() else p for p in re.split(r"(\d+)", tag)]


def cmd_count(args):
    counts, total = {}, 0
    for f in load(args.dir):
        for s in f.scenarios:
            for tags, n in s.collected():
                total += n
                for t in tags:
                    counts[t] = counts.get(t, 0) + n
    for t in sorted(counts, key=natural):
        print(f"{t} {counts[t]}")
    print(f"total {total}")
    return 0


def cmd_list(args):
    tag = args.tag.lstrip("@") if args.tag else None
    hits = [s for f in load(args.dir) for s in f.scenarios
            if (tag and tag in s.all_tags()) or (args.title and args.title in s.title)]
    for s in hits:
        print(f"{s.feature.path}: {s.title}")
    if not hits:
        print("no scenarios match", file=sys.stderr)
    return 0 if hits else 1


def cmd_tag(args):
    if not SLICE_ARG_RE.fullmatch(args.slice):
        print(f"features: {args.slice!r} is not slice-<n> or slice-<n>.<m>", file=sys.stderr)
        return 2
    s = the_scenario(load(args.dir), args.title)
    f, new, placed = s.feature, "@" + args.slice, False
    for i in range(s.start, s.kw):
        tokens = f.lines[i].split()
        if not any(SLICE_TOKEN_RE.fullmatch(t) for t in tokens):
            continue
        rest = []
        for t in tokens:
            if not SLICE_TOKEN_RE.fullmatch(t):
                rest.append(t)
            elif not placed:
                rest.append(new)
                placed = True
        f.lines[i] = indent_of(f.lines[i]) + " ".join(rest) + "\n" if rest else ""
    if not placed:
        if s.kw > s.start:
            last = s.kw - 1
            f.lines[last] = f.lines[last].rstrip("\n") + " " + new + "\n"
        else:
            f.lines.insert(s.kw, indent_of(f.lines[s.kw]) + new + "\n")
    f.write()
    print(f"{f.path}: {s.title} -> {new}")
    return 0


def cmd_move(args):
    features = load(args.dir)
    s = the_scenario(features, args.title)
    source, target_path = s.feature, pathlib.Path(args.to).resolve()
    if source.path.resolve() == target_path:
        raise Refused(f"{args.title!r} is already in {args.to}")
    target = next((f for f in features if f.path.resolve() == target_path), None)
    if target is None:
        if not target_path.exists():
            raise Refused(f"{args.to} does not exist: write its header first")
        target = Feature(target_path)
    block = source.lines[s.start:s.end]
    while block and not block[-1].strip():
        block.pop()
    if args.inline_background and source.background:
        kw, end = source.background
        first = source.first_step(kw + 1, end)
        steps = source.lines[first:end]
        while steps and not steps[-1].strip():
            steps.pop()
        at = source.first_step(s.kw + 1, s.end)
        if steps and at < s.end:
            have, want = indent_of(steps[0]), indent_of(source.lines[at])
            steps = [want + l[len(have):] if l.startswith(have) else l for l in steps]
            block[at - s.start:at - s.start] = steps
    del source.lines[s.start:s.end]
    if target.lines and target.lines[-1].strip():
        target.lines.append("\n")
    target.lines.extend(block)
    source.write()
    target.write()
    print(f"{source.path} -> {target.path}: {s.title}")
    return 0


def signatures(features):
    sigs, dupes = {}, []
    for f in features:
        for s in f.scenarios:
            if s.title in sigs:
                dupes.append(s.title)
            sigs[s.title] = s.signature()
    return sigs, dupes


def cmd_verify_moved(args):
    before, dupes_before = signatures(load(args.from_dir))
    after, dupes_after = signatures(load(args.dir))
    problems = [f"duplicate title before: {t}" for t in dupes_before]
    problems += [f"duplicate title after: {t}" for t in dupes_after]
    for title, sig in before.items():
        if title not in after:
            problems.append(f"missing: {title}")
        elif sig != after[title]:
            parts = [k for k in sig if sig[k] != after[title][k]]
            problems.append(f"changed: {title} ({', '.join(parts)})")
    problems += [f"added: {t}" for t in after if t not in before]
    for p in problems:
        print(p)
    if problems:
        return 1
    print(f"{len(before)} scenarios match")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(prog="features", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dir", default="features", help="the feature directory (default: features)")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("count", help="scenarios collected per tag")
    p.add_argument("--by-tag", action="store_true", required=True)
    p.set_defaults(run=cmd_count)
    p = sub.add_parser("list", help="scenarios by tag or by title")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--tag")
    g.add_argument("--title", help="a substring of the title")
    p.set_defaults(run=cmd_list)
    p = sub.add_parser("tag", help="replace or add one scenario's slice tag")
    p.add_argument("title")
    p.add_argument("slice", help="slice-<n> or slice-<n>.<m>")
    p.set_defaults(run=cmd_tag)
    p = sub.add_parser("move", help="move a scenario verbatim to another feature file")
    p.add_argument("title")
    p.add_argument("--to", required=True)
    p.add_argument("--inline-background", action="store_true",
                   help="insert the source Background's steps as the scenario's first steps")
    p.set_defaults(run=cmd_move)
    p = sub.add_parser("verify-moved", help="every scenario under --from equals one under --dir")
    p.add_argument("--from", dest="from_dir", required=True)
    p.set_defaults(run=cmd_verify_moved)
    args = parser.parse_args(argv)
    try:
        return args.run(args)
    except Refused as e:
        print(f"features: refused: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
```

Then `chmod +x scripts/features`.

- [ ] **Step 4: Run the tests to verify they pass**

Run: `python3 -m unittest discover -s tests/scripts -v`
Expected: 15 tests, OK.

- [ ] **Step 5: Run it on a real repository's features, read-only**

Run: `cd $SCRATCH && git clone --local /home/vscode/shopsystem-knowledge sk && cd sk && python3 /home/vscode/shopsystem-bdd/scripts/features count --by-tag`, then for three slice tags compare with `python -m pytest --collect-only -q -m slice-<n> | tail -1` in that clone's environment (skip the comparison if the clone's environment will not install; say so in the commit message).
Expected: the same count per tag.

- [ ] **Step 6: Commit**

```bash
git add scripts/features tests/scripts/test_features.py
git commit -m "scripts/features: count, list, tag, move and verify-moved without the test runner"
```

---

### Task 2: The `plan` script

**Files:**
- Create: `scripts/plan`
- Test: `tests/scripts/test_plan.py`

**Interfaces:**
- Produces: `plan [--file F] check | log TEXT [--date D] | backlog TEXT [--date D] | status N STATUS | add-slice N NAME --kind K (--scenarios S | --check C) --observable O [--unknown U] [--needs N] | archive BATCH [--date D] | show (--open | --backlog | --requests | --last-suite [--current])`. Default file: the one `docs/superpowers/plans/*-slices.md` under the current directory. `show --last-suite --current` prints the record, then `current` (exit 0) or `stale: <reason>` (exit 1).

- [ ] **Step 1: Write the failing tests**

`tests/scripts/test_plan.py`:

```python
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parents[2] / "scripts" / "plan"

PLAN = '''# Cart slices

## Slice 1: Add a product
- Kind: capability
- Scenarios: cart / Adding a product
- Observable: a shopper sees one item in the cart
- Unknown: none
- Needs: none
- Status: green

## Slice 2: Several products
- Kind: capability
- Scenarios: cart / Adding several
- Observable: a shopper sees the count
- Unknown: none
- Needs: none
- Status: planned

## Satisfied by existing behaviour

## Log
- 2026-10-01 Suite: 3 passed, 1 failed at abc1234 in 12 s
- 2026-10-02 REQUEST shopsystem-kb: kb serve is not built
'''


class PlanTest(unittest.TestCase):
    def setUp(self):
        self.tmp = pathlib.Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        plans = self.tmp / "docs" / "superpowers" / "plans"
        plans.mkdir(parents=True)
        self.plan = plans / "cart-slices.md"
        self.plan.write_text(PLAN)

    def run_script(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *args], cwd=self.tmp,
                              capture_output=True, text=True)

    def git(self, *args):
        return subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", *args],
                              cwd=self.tmp, check=True, capture_output=True, text=True).stdout.strip()

    def test_check_accepts_a_valid_plan(self):
        done = self.run_script("check")
        self.assertEqual((done.returncode, done.stdout), (0, "ok\n"))

    def test_check_refuses_sections_out_of_order(self):
        self.plan.write_text(PLAN.replace("## Satisfied by existing behaviour\n\n", "") +
                             "\n## Satisfied by existing behaviour\n")
        done = self.run_script("check")
        self.assertEqual(done.returncode, 1)
        self.assertIn("out of order", done.stderr)

    def test_log_appends_a_dated_line(self):
        self.run_script("log", "slice 2 green", "--date", "2026-10-03")
        self.assertEqual(self.plan.read_text(), PLAN + "- 2026-10-03 slice 2 green\n")

    def test_backlog_is_created_before_the_log(self):
        self.run_script("backlog", "slow lookup on 10k items", "--date", "2026-10-03")
        self.assertIn("## Satisfied by existing behaviour\n\n## Backlog\n"
                      "- 2026-10-03 slow lookup on 10k items\n\n## Log\n", self.plan.read_text())

    def test_status_sets_one_slice(self):
        self.run_script("status", "2", "in progress")
        text = self.plan.read_text()
        self.assertEqual(text, PLAN.replace("- Status: planned\n", "- Status: in progress\n"))

    def test_status_refuses_an_unknown_status(self):
        done = self.run_script("status", "2", "done")
        self.assertEqual(done.returncode, 1)
        self.assertEqual(self.plan.read_text(), PLAN)

    def test_status_may_carry_a_note(self):
        done = self.run_script("status", "2", "in progress: waits on slice 1")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(self.run_script("show", "--open").stdout,
                         "2 Several products: in progress: waits on slice 1\n")

    def test_status_refuses_a_missing_slice(self):
        self.assertEqual(self.run_script("status", "7", "green").returncode, 1)

    def test_add_slice_goes_in_number_order(self):
        done = self.run_script("add-slice", "1.1", "Remove a product", "--kind", "capability",
                               "--scenarios", "cart / Removing a product",
                               "--observable", "a shopper removes a pen")
        self.assertEqual(done.returncode, 0, done.stderr)
        text = self.plan.read_text()
        self.assertLess(text.index("## Slice 1:"), text.index("## Slice 1.1: Remove a product"))
        self.assertLess(text.index("## Slice 1.1:"), text.index("## Slice 2:"))
        self.assertIn("- Needs: none\n- Status: planned\n\n## Slice 2:", text)

    def test_add_slice_refuses_an_enabling_slice_without_a_check(self):
        done = self.run_script("add-slice", "3", "Fast suite", "--kind", "enabling",
                               "--scenarios", "x", "--observable", "y")
        self.assertEqual(done.returncode, 1)
        self.assertEqual(self.plan.read_text(), PLAN)

    def test_add_slice_refuses_an_existing_number(self):
        done = self.run_script("add-slice", "2", "Again", "--kind", "capability",
                               "--scenarios", "x", "--observable", "y")
        self.assertEqual(done.returncode, 1)

    def test_an_unknown_section_survives_every_edit(self):
        notes = "## Notes\nfree text the script does not own\n\n"
        self.plan.write_text(PLAN.replace("## Log\n", notes + "## Log\n"))
        self.run_script("status", "2", "green")
        self.run_script("log", "x", "--date", "2026-10-03")
        self.assertIn(notes + "## Log\n", self.plan.read_text())

    def test_show_open(self):
        self.assertEqual(self.run_script("show", "--open").stdout, "2 Several products: planned\n")

    def test_show_requests(self):
        self.assertEqual(self.run_script("show", "--requests").stdout,
                         "- 2026-10-02 REQUEST shopsystem-kb: kb serve is not built\n")

    def test_show_last_suite(self):
        self.assertEqual(self.run_script("show", "--last-suite").stdout,
                         "- 2026-10-01 Suite: 3 passed, 1 failed at abc1234 in 12 s\n")

    def test_archive_moves_green_slices_and_log_keeping_requests(self):
        done = self.run_script("archive", "14", "--date", "2026-10-06")
        self.assertEqual(done.returncode, 0, done.stderr)
        archived = (self.plan.parent / "archive" / "cart-slices-14.md").read_text()
        self.assertIn("## Slice 1: Add a product", archived)
        self.assertIn("- 2026-10-01 Suite: 3 passed", archived)
        text = self.plan.read_text()
        self.assertNotIn("## Slice 1:", text)
        self.assertTrue(text.endswith(
            "## Log\n- 2026-10-02 REQUEST shopsystem-kb: kb serve is not built\n"
            "- 2026-10-06 Batch 14 archived to archive/cart-slices-14.md; "
            "last 2026-10-01 Suite: 3 passed, 1 failed at abc1234 in 12 s\n"))

    def test_last_suite_holds_until_code_changes(self):
        self.git("init", "-q")
        (self.tmp / "code.txt").write_text("one\n")
        self.git("add", "code.txt")
        self.git("commit", "-qm", "code")
        tested = self.git("rev-parse", "--short", "HEAD")
        self.plan.write_text(PLAN.replace("abc1234", tested))
        self.git("add", "-A")
        self.git("commit", "-qm", "checkpoint")
        done = self.run_script("show", "--last-suite", "--current")
        self.assertEqual(done.returncode, 0, done.stdout + done.stderr)
        self.assertTrue(done.stdout.endswith("current\n"))
        (self.tmp / "code.txt").write_text("two\n")
        done = self.run_script("show", "--last-suite", "--current")
        self.assertEqual(done.returncode, 1)
        self.assertIn("stale: 1 files changed since", done.stdout)

    def test_last_suite_on_a_commit_not_in_the_repository_is_stale(self):
        self.git("init", "-q")
        self.git("add", "-A")
        self.git("commit", "-qm", "plan")
        self.plan.write_text(PLAN.replace("abc1234", "deadbee"))
        done = self.run_script("show", "--last-suite", "--current")
        self.assertEqual(done.returncode, 1)
        self.assertIn("stale: commit deadbee is not in this repository", done.stdout)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python3 -m unittest tests/scripts/test_plan.py -v`
Expected: every test fails or errors, the script not existing.

- [ ] **Step 3: Write the script**

`scripts/plan`:

```python
#!/usr/bin/env python3
"""Read and edit the living slice plan, keeping its shape valid.

Commands:
  plan check
  plan log TEXT [--date YYYY-MM-DD]
  plan backlog TEXT [--date YYYY-MM-DD]
  plan status N STATUS
  plan add-slice N NAME --kind KIND (--scenarios S | --check C) --observable O [--unknown U] [--needs N]
  plan archive BATCH [--date YYYY-MM-DD]
  plan show (--open | --backlog | --requests | --last-suite [--current])

The plan is --file, or the one docs/superpowers/plans/*-slices.md under the current directory.
A request to another repository is a log line "REQUEST <repository>: <what is needed>".
A suite record is a log line "Suite: <N> passed, <M> failed at <commit> in <seconds> s".
--current: the record holds while nothing outside docs/superpowers/plans/ differs between
its commit, HEAD and the working tree.
`archive` moves the green slices and the log, except requests, to archive/<plan>-<batch>.md.
An edit that would leave the plan invalid is refused, and the file is left as it was.
Exit status: 0 on success, 1 when refused or a check fails, 2 on bad usage.
"""
import argparse
import datetime
import pathlib
import re
import subprocess
import sys

SLICE_HEAD_RE = re.compile(r"^## Slice (\d+(?:\.\d+)*): (.+?)\s*$")
FIELD_RE = re.compile(r"^- (Kind|Scenarios|Check|Observable|Unknown|Needs|Status): ?(.*?)\s*$")
STATUS_RE = re.compile(r"^(planned|in progress|green)(: .+)?$|^blocked: .+$")
REQUEST_RE = re.compile(r"^- \S+ REQUEST ")
SUITE_AT_RE = re.compile(r"Suite: .*\bat ([0-9a-f]{7,40})\b")
KINDS = ("capability", "enabling", "stack")
SECTIONS = ("Satisfied by existing behaviour", "Backlog", "Log")
PLANS_DIR = "docs/superpowers/plans/"


class Refused(Exception):
    pass


def number_key(number):
    return tuple(int(p) for p in number.split("."))


def is_green(block):
    return (block.field("Status") or "").split(":")[0] == "green"


class Block:
    def __init__(self, lines):
        self.lines = lines
        m = SLICE_HEAD_RE.match(lines[0])
        self.number, self.title = (m.group(1), m.group(2)) if m else (None, None)
        self.section = None if m else lines[0][3:].strip()

    def field(self, name):
        for line in self.lines[1:]:
            m = FIELD_RE.match(line)
            if m and m.group(1) == name:
                return m.group(2)
        return None

    def set_field(self, name, value):
        for i, line in enumerate(self.lines):
            m = FIELD_RE.match(line)
            if i and m and m.group(1) == name:
                self.lines[i] = f"- {name}: {value}\n"
                return
        raise Refused(f"slice {self.number} has no {name} line")

    def items(self):
        return [l.rstrip("\n") for l in self.lines[1:] if l.startswith("- ")]

    def append(self, line):
        i = len(self.lines)
        while i > 1 and not self.lines[i - 1].strip():
            i -= 1
        self.lines.insert(i, line)


class Plan:
    def __init__(self, path):
        self.path = pathlib.Path(path)
        text = self.path.read_text(encoding="utf-8")
        if text and not text.endswith("\n"):
            text += "\n"
        self.head, self.blocks = [], []
        for line in text.splitlines(keepends=True):
            if line.startswith("## "):
                self.blocks.append(Block([line]))
            elif self.blocks:
                self.blocks[-1].lines.append(line)
            else:
                self.head.append(line)
        self.validate()

    def slices(self):
        return [b for b in self.blocks if b.number]

    def slice(self, number):
        found = next((b for b in self.slices() if b.number == number), None)
        if not found:
            raise Refused(f"no slice {number}")
        return found

    def section(self, name, create=False):
        found = next((b for b in self.blocks if b.section == name), None)
        if found or not create:
            return found
        found = Block([f"## {name}\n"])
        later = [i for i, b in enumerate(self.blocks)
                 if b.section in SECTIONS and SECTIONS.index(b.section) > SECTIONS.index(name)]
        self.blocks.insert(later[0] if later else len(self.blocks), found)
        return found

    def validate(self):
        problems = []
        if not self.head or not self.head[0].startswith("# "):
            problems.append("the first line is not the plan's '# ' title")
        after_sections, previous = False, None
        for b in self.blocks:
            if not b.number:
                after_sections = True
                continue
            name = f"slice {b.number}"
            if after_sections:
                problems.append(f"{name} comes after a section")
            if previous and number_key(b.number) <= number_key(previous):
                problems.append(f"{name} is out of order after slice {previous}")
            previous = b.number
            kind, status = b.field("Kind"), b.field("Status")
            scenarios, check = b.field("Scenarios"), b.field("Check")
            if kind not in KINDS:
                problems.append(f"{name}: Kind is {kind!r}, not one of {', '.join(KINDS)}")
            if status is None or not STATUS_RE.match(status):
                problems.append(f"{name}: Status is {status!r}")
            if scenarios is not None and check is not None:
                problems.append(f"{name} has both Scenarios and Check")
            elif kind == "capability" and scenarios is None:
                problems.append(f"{name} ({kind}) has no Scenarios")
            elif kind in ("enabling", "stack") and check is None:
                problems.append(f"{name} ({kind}) has no Check")
        named = [b.section for b in self.blocks if b.section in SECTIONS]
        if len(named) != len(set(named)):
            problems.append("a section appears twice")
        order = [SECTIONS.index(n) for n in named]
        if order != sorted(order):
            problems.append("sections are out of order: " + ", ".join(SECTIONS))
        if problems:
            raise Refused("; ".join(problems))

    def text(self):
        if self.head and self.head[-1].strip() and self.blocks:
            self.head.append("\n")
        for b in self.blocks[:-1]:
            if b.lines[-1].strip():
                b.lines.append("\n")
        return "".join(self.head) + "".join("".join(b.lines) for b in self.blocks)

    def save(self):
        self.validate()
        self.path.write_text(self.text(), encoding="utf-8")


def last_suite(items):
    return next((l for l in reversed(items) if "Suite:" in l), None)


def git(*argv):
    done = subprocess.run(["git", *argv], capture_output=True, text=True)
    if done.returncode:
        raise Refused(f"git {' '.join(argv)}: {done.stderr.strip()}")
    return done.stdout


def staleness(record):
    m = SUITE_AT_RE.search(record)
    if not m:
        return "the record names no commit (at <hash>)"
    commit = m.group(1)
    known = subprocess.run(["git", "rev-parse", "--verify", "--quiet", commit + "^{commit}"],
                           capture_output=True)
    if known.returncode:
        return f"commit {commit} is not in this repository"
    changed = git("diff", "--name-only", commit, "HEAD").splitlines()
    changed += [l[3:].split(" -> ")[-1] for l in git("status", "--porcelain").splitlines()]
    outside = sorted({p for p in changed if p and not p.startswith(PLANS_DIR)})
    if not outside:
        return None
    return f"{len(outside)} files changed since {commit}: {', '.join(outside[:5])}"


def cmd_check(plan, args):
    print("ok")
    return 0


def cmd_append(section):
    def run(plan, args):
        line = f"- {args.date} {args.text}\n"
        plan.section(section, create=True).append(line)
        plan.save()
        print(line, end="")
        return 0
    return run


def cmd_status(plan, args):
    if not STATUS_RE.match(args.status):
        raise Refused(f"status {args.status!r} is not planned, in progress or green (each with an optional ': <note>'), or blocked: <why>")
    plan.slice(args.number).set_field("Status", args.status)
    plan.save()
    print(f"slice {args.number}: {args.status}")
    return 0


def cmd_add_slice(plan, args):
    if any(b.number == args.number for b in plan.slices()):
        raise Refused(f"slice {args.number} exists")
    lines = [f"## Slice {args.number}: {args.name}\n", f"- Kind: {args.kind}\n"]
    if args.scenarios is not None:
        lines.append(f"- Scenarios: {args.scenarios}\n")
    if args.check is not None:
        lines.append(f"- Check: {args.check}\n")
    lines += [f"- Observable: {args.observable}\n", f"- Unknown: {args.unknown}\n",
              f"- Needs: {args.needs}\n", "- Status: planned\n"]
    at = next((i for i, b in enumerate(plan.blocks)
               if not b.number or number_key(b.number) > number_key(args.number)), len(plan.blocks))
    plan.blocks.insert(at, Block(lines))
    plan.save()
    print(f"slice {args.number} added")
    return 0


def cmd_archive(plan, args):
    green = [b for b in plan.slices() if is_green(b)]
    if not green:
        raise Refused("no green slices to archive")
    target = plan.path.parent / "archive" / f"{plan.path.stem}-{args.batch}.md"
    if target.exists():
        raise Refused(f"{target} exists")
    log = plan.section("Log", create=True)
    items = log.items()
    requests = [l for l in items if REQUEST_RE.match(l)]
    moved = [l for l in items if not REQUEST_RE.match(l)]
    body = [f"# {plan.head[0][2:].strip()}: batch {args.batch}\n", "\n"]
    for b in green:
        body += b.lines if not b.lines[-1].strip() else b.lines + ["\n"]
    body += ["## Log\n"] + [l + "\n" for l in moved]
    note = f"- {args.date} Batch {args.batch} archived to archive/{target.name}"
    suite = last_suite(moved)
    if suite:
        note += f"; last {suite[2:]}"
    plan.blocks = [b for b in plan.blocks if b not in green]
    log.lines = ["## Log\n"] + [l + "\n" for l in requests] + [note + "\n"]
    plan.validate()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("".join(body), encoding="utf-8")
    plan.save()
    print(f"{len(green)} slices and {len(moved)} log lines -> {target}")
    return 0


def cmd_show(plan, args):
    if args.open:
        for b in plan.slices():
            if not is_green(b):
                print(f"{b.number} {b.title}: {b.field('Status')}")
        return 0
    if args.backlog:
        section = plan.section("Backlog")
        for item in section.items() if section else []:
            print(item)
        return 0
    log = plan.section("Log")
    items = log.items() if log else []
    if args.requests:
        for item in items:
            if REQUEST_RE.match(item):
                print(item)
        return 0
    record = last_suite(items)
    if not record:
        print("no Suite: line in the log", file=sys.stderr)
        return 1
    print(record)
    if not args.current:
        return 0
    stale = staleness(record)
    print(f"stale: {stale}" if stale else "current")
    return 1 if stale else 0


def slice_number(text):
    if not re.fullmatch(r"\d+(?:\.\d+)*", text):
        raise argparse.ArgumentTypeError(f"{text!r} is not <n> or <n>.<m>")
    return text


def plan_file(given):
    if given:
        path = pathlib.Path(given)
    else:
        found = sorted(pathlib.Path(PLANS_DIR).glob("*-slices.md"))
        if len(found) != 1:
            print(f"plan: {len(found)} *-slices.md files under {PLANS_DIR}; name one with --file",
                  file=sys.stderr)
            sys.exit(2)
        path = found[0]
    if not path.is_file():
        print(f"plan: {path}: no such file", file=sys.stderr)
        sys.exit(2)
    return path


def main(argv=None):
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--file", help="the plan (default: the one docs/superpowers/plans/*-slices.md)")
    parser = argparse.ArgumentParser(prog="plan", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    today = datetime.date.today().isoformat()
    p = sub.add_parser("check", parents=[common], help="validate the plan")
    p.set_defaults(run=cmd_check)
    for name, section in (("log", "Log"), ("backlog", "Backlog")):
        p = sub.add_parser(name, parents=[common], help=f"append a dated line to the {section}")
        p.add_argument("text")
        p.add_argument("--date", default=today)
        p.set_defaults(run=cmd_append(section))
    p = sub.add_parser("status", parents=[common], help="set a slice's Status")
    p.add_argument("number", type=slice_number)
    p.add_argument("status")
    p.set_defaults(run=cmd_status)
    p = sub.add_parser("add-slice", parents=[common], help="add a slice in number order")
    p.add_argument("number", type=slice_number)
    p.add_argument("name")
    p.add_argument("--kind", required=True, choices=KINDS)
    p.add_argument("--scenarios")
    p.add_argument("--check")
    p.add_argument("--observable", required=True)
    p.add_argument("--unknown", default="none")
    p.add_argument("--needs", default="none")
    p.set_defaults(run=cmd_add_slice)
    p = sub.add_parser("archive", parents=[common], help="move green slices and the log to archive/")
    p.add_argument("batch")
    p.add_argument("--date", default=today)
    p.set_defaults(run=cmd_archive)
    p = sub.add_parser("show", parents=[common], help="print part of the plan")
    g = p.add_mutually_exclusive_group(required=True)
    for flag in ("--open", "--backlog", "--requests", "--last-suite"):
        g.add_argument(flag, action="store_true")
    p.add_argument("--current", action="store_true",
                   help="with --last-suite: exit 1 unless the record holds at HEAD")
    p.set_defaults(run=cmd_show)
    args = parser.parse_args(argv)
    path = plan_file(args.file)
    try:
        return args.run(Plan(path), args)
    except Refused as e:
        print(f"plan: refused: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
```

Then `chmod +x scripts/plan`.

- [ ] **Step 4: Run the tests to verify they pass**

Run: `python3 -m unittest discover -s tests/scripts -v`
Expected: 33 tests (15 + 18), OK.

- [ ] **Step 5: Run it on the real living plan, read-only**

Run: in `$SCRATCH/sk` (Task 1's clone; clone it if absent), `python3 /home/vscode/shopsystem-bdd/scripts/plan check` and `python3 /home/vscode/shopsystem-bdd/scripts/plan show --open`.
Expected: `ok` and the open slices as the file lists them. If `check` refuses, the refusal names a shape the slicing skill's template allows: fix the script (and add a test for that shape), never the clone's plan.

- [ ] **Step 6: Commit**

```bash
git add scripts/plan tests/scripts/test_plan.py
git commit -m "scripts/plan: edit and read the living slice plan, keeping its shape; suite records checked against HEAD"
```

---

### Task 3: Suite runs count once; rule-decided splits; behaviour defects never Minor

**Files:**
- Modify: `skills/bdd-red-green/SKILL.md` (cycle step 4 paragraph, new section "The Suite Record", "Slices Verified by a Check" steps 3–4, Rationalizations, Red Flags)
- Modify: `agents/bdd-implementer.md` (How you work, git, Stopping, Reporting)
- Modify: `agents/bdd-task-reviewer.md` (Tests, Issues)
- Modify: `agents/bdd-branch-reviewer.md` (How you review, Output)
- Create: `docs/superpowers/testing/2026-10-06-suite-runs-and-round-trips-test-log.md`
- Scratchpad: `run_headless.sh`, `count_runs.py`, `reply_sizes.py`, `fixtures/impl/`, `fixtures/review/`

**Interfaces:**
- Consumes: `scripts/plan` (`show --last-suite [--current]`, `log`) from Task 2.
- Produces: the suite record convention in `bdd-red-green` ("The Suite Record"), which Task 4 cites; the implementer's two commits per task (the change, then the checkpoint with its record).

- [ ] **Step 1: Harness.** In `$SCRATCH`:

`run_headless.sh`:

```bash
#!/usr/bin/env bash
# run_headless.sh <fixture dir> <run name> <prompt file> [session id to resume]
set -euo pipefail
fixture=$1; name=$2; prompt=$3; resume=${4:-}
mkdir -p "$SCRATCH/runs"
cd "$fixture"
claude -p --model opus --plugin-dir /home/vscode/shopsystem-bdd \
  --output-format stream-json --verbose --dangerously-skip-permissions \
  ${resume:+--resume "$resume"} < "$prompt" > "$SCRATCH/runs/$name.jsonl"
grep -o '"session_id":"[^"]*"' "$SCRATCH/runs/$name.jsonl" | head -1
```

`count_runs.py` (whole-suite runs in a transcript, subagents included):

```python
import json, re, sys
whole = 0
for line in open(sys.argv[1]):
    try:
        event = json.loads(line)
    except ValueError:
        continue
    for block in (event.get("message") or {}).get("content") or []:
        if isinstance(block, dict) and block.get("type") == "tool_use" and block.get("name") == "Bash":
            cmd = block["input"].get("command", "")
            if re.search(r"pytest|make test", cmd) and not re.search(
                    r"\s-[mk]\s|::|--collect-only|tests/\S+\.py|features/", cmd):
                whole += 1
                print(cmd)
print("whole-suite runs:", whole)
```

`reply_sizes.py` (bytes each subagent returned to the controller):

```python
import json, sys
names = {}
for line in open(sys.argv[1]):
    try:
        event = json.loads(line)
    except ValueError:
        continue
    for b in (event.get("message") or {}).get("content") or []:
        if not isinstance(b, dict):
            continue
        if b.get("type") == "tool_use" and b.get("name") in ("Agent", "Task"):
            names[b["id"]] = b["input"].get("subagent_type", "?")
        if b.get("type") == "tool_result" and b.get("tool_use_id") in names:
            print(names[b["tool_use_id"]], len(json.dumps(b.get("content"))))
```

- [ ] **Step 2: Fixture `impl`.** Copy `skills/bdd-red-green/example/` to `$SCRATCH/fixtures/impl/`, `git init`, and add:
  - `spec/capabilities/cart.md` with a Behaviour line "When the shopper asks for a receipt, it lists each line with its quantity and price, then the total."
  - a `@slice-3` scenario "Asking for a receipt" in `features/cart.feature` formulating it, red (undefined steps).
  - `CLAUDE.md`: a module map table (`cart/__init__.py`: the cart and its lines), and two rules: "No module over 40 lines." and "A new concern gets a new module and a row in the module map."
  - `cart/__init__.py` brought to 38 lines with the existing behaviour (docstrings on each method).
  - `docs/superpowers/plans/cart-slices.md` in the template's shape: slices 1–2 green, slice 3 planned; committed, then the log's suite record written with `scripts/plan log "Suite: <N> passed, 1 failed at <short HEAD> in <s> s; failing: Asking for a receipt"` and committed.
  - `.superpowers/briefs/task-3.md` (git-ignored via `.gitignore`): Global Constraints including `Scripts: /home/vscode/shopsystem-bdd/scripts`; the scenario; why red; "lands in `cart/__init__.py`, beside the cart"; marker `slice-3`, expected count 1; checkpoint line.
  Check `python -m pytest -q` gives the recorded counts.

- [ ] **Step 3: Fixture `review`.** Copy the example to `$SCRATCH/fixtures/review/` and add a capability Behaviour line "When the shopper removes a product, the cart no longer holds it and still holds every other product it held." with one scenario: a cart holding one pen, the pen removed, the cart empty. Commit. Then commit a change implementing removal as removing the last line whatever the product (the scenario passes). Write the brief, an implementer report claiming the scenario green, and a review package (`git log --oneline BASE..HEAD`, `git diff --stat`, `git diff -U10`) to `.superpowers/review/`.

- [ ] **Step 4: Baselines (RED).** On the current agents:
  - `impl`: prompt "Dispatch the shopsystem-bdd:bdd-implementer agent with the brief .superpowers/briefs/task-3.md, report to .superpowers/reports/task-3.md, on branch main." Score with `count_runs.py`: whole-suite runs (expected 2: at the start and before commit); whether it handed back for size (`BLOCKED` or `NEEDS_CONTEXT` naming the limit); commits made; suite record written or not.
  - `review`: prompt "Dispatch the shopsystem-bdd:bdd-task-reviewer agent with the brief, report and package under .superpowers/review/." Score: the removal defect found or not; its grade (expected Minor, or missed, because no scenario covers it).
  Record verbatim evidence in the test log.

- [ ] **Step 5: Edit `skills/bdd-red-green/SKILL.md`.**
  - After "Before the slice's last commit, run the whole feature suite once. Everything previously green stays green." add: "That run is the slice's suite record (below)."
  - New section after "Keep the Suite Fast":

    ```
    ## The Suite Record

    A whole-suite run is recorded once and used while it holds. After the
    slice's change is committed, record the run in the plan's log with the
    plugin's `scripts/plan log`, as `Suite: <N> passed, <M> failed at <short
    hash of the commit that was run> in <seconds> s`, with `; failing:
    <titles>` when M is not 0, and commit the log with the checkpoint. A
    record holds while nothing outside `docs/superpowers/plans/` has changed
    since its commit: `scripts/plan show --last-suite --current` says
    `current` or `stale`.

    - A slice starts from the last record; its failing list is the scenarios
      already red. Do not run the whole suite at a slice's start. Only when
      the plan has no record yet, run it once to make one.
    - Whoever needs the suite's result (a reviewer, slicing, the controller
      before a push) and finds a record that holds uses it.
    - Installing or upgrading a dependency without a commit makes every
      record stale.
    ```
  - "Slices Verified by a Check" step 3 becomes: "**Run the check again**, and the test modules the work touches and any the check's failure names. Iterate on those. Once the check gives its result, run the whole feature suite once: everything previously green stays green. That run is the record." Step 4 unchanged.
  - Rationalizations row (from the baseline's words where they exist): "I'll run the whole suite first to see where we start" | "The last record is where you start. A start-of-slice run is one run too many."
  - Red Flags: "A whole-suite run before a slice's first scenario, with a record that holds".

- [ ] **Step 6: Edit `agents/bdd-implementer.md`.**
  - Replace "While you iterate, run the focused markers the brief gives. Run the whole suite at the start and once before you commit." with: "Runs follow `bdd-red-green`: the slice's marker and the scenario's test module while you iterate, the whole suite once before the slice's last commit. The task starts from the last suite record, `python3 <Scripts>/plan show --last-suite` (`Scripts:` is in the plan's Global Constraints); do not run the whole suite at the start unless there is none."
  - Git section, first bullet becomes: "Commit exactly as the brief says, its identity and its message trailer, in two commits: the change; then the checkpoint, written with `python3 <Scripts>/plan log` and holding the checkpoint line and the suite record for the change's commit."
  - Stopping: "a file would cross the repository's size limit;" becomes "a file would cross the repository's size limit and no rule in `CLAUDE.md` says where the code goes. Where a rule does (a new concern gets a new module and a row in the module map), make the split, add the row, and say so in the checkpoint;"
  - Reporting: add "the suite record line;" after "each check command with its output before and after;", and the reply's "a one-line test summary" becomes "the suite record line".

- [ ] **Step 7: Edit `agents/bdd-task-reviewer.md`.**
  - Tests: "Do not re-run the whole suite to confirm the report." becomes "Do not re-run the whole suite to confirm the report: the implementer's suite record is the run. Check it names the task's change commit."
  - Issues: before "A hardening finding", insert: "Behaviour that contradicts a Behaviour line or the capability's Purpose is Important, whether or not a scenario covers it. When none does, say so and mark it `spec question`, so the controller has the line's scenario formulated with the fix. It is never Minor and never carried to a later task."

- [ ] **Step 8: Edit `agents/bdd-branch-reviewer.md`.**
  - "Run the suite and every check the plan states, yourself." becomes: "**Run the suite once, at the batch's head, and every check the plan states, yourself.** Paste the summary lines and the suite's wall time. Give the record line for the controller to log, `Suite: <N> passed, <M> failed at <HEAD short hash> in <seconds> s`: the controller pushes on it while `plan show --last-suite --current` says it holds, without running the suite again. A check you did not run…" (rest unchanged).
  - New bullet after the shape bullet: "**Check the suite is fast.** Say whether the project's test command runs in parallel and whether the step definitions drive the entry point in-process (one test per command as a program). A suite over 60 s that fails either, with no reason in `CLAUDE.md`, is a finding, given as an enabling slice: the same counts, the wall time under a stated bound."
  - "Behaviour lines are the contract." bullet, add: "Behaviour that contradicts a line or a capability's Purpose is Important whether or not a scenario covers it."
  - Output: add "**Suite record:** the line for the controller to log, and the wall time."

- [ ] **Step 9: Green runs.** Same prompts, plugin loaded.
  - `impl` passes when: whole-suite runs = 1; no hand-back; `cart/receipt.py` (or similar) created with a module-map row added and the split named in the checkpoint; two commits, the second holding the checkpoint and `Suite: … at <the first commit's short hash> in <s> s`; `plan show --last-suite --current` in the fixture prints `current`.
  - `impl-norecord` (the `impl` fixture with the log's record removed): whole-suite runs = 2, the first before any step definition (Review Focus 4).
  - `review` passes when: the removal defect is Important, marked `spec question`, not Minor.
  Iterate wording until each passes; log every iteration.

- [ ] **Step 10: Commit** the skill, the three agents and the test log.

```bash
git add skills/bdd-red-green/SKILL.md agents/bdd-implementer.md agents/bdd-task-reviewer.md agents/bdd-branch-reviewer.md docs/superpowers/testing/2026-10-06-suite-runs-and-round-trips-test-log.md
git commit -m "Suite runs count once (records by commit), rule-decided splits, behaviour defects never Minor"
```

---

### Task 4: Slicing: fast suite first, probes at the pin, the scripts, a fresh session

**Files:**
- Modify: `skills/slicing-into-increments/SKILL.md` (Overview: scripts; Process steps 1–5; The Hand-off to writing-plans; The Plan File's archive paragraph; Rationalizations; Red Flags)
- Create: `docs/superpowers/testing/2026-10-06-slicing-efficiency-test-log.md`
- Scratchpad: `fixtures/slice/`, `fixtures/stock/`

**Interfaces:**
- Consumes: `scripts/features` (Task 1), `scripts/plan` (Task 2), the suite record (Task 3).
- Produces: `Scripts: <absolute path>` in every plan's Global Constraints; `Probe:` and `REQUEST <repository>:` log lines; the fast-suite enabling slice placed first.

- [ ] **Step 1: Fixtures.**
  - `$SCRATCH/fixtures/stock/`: a dependency with `spec/capabilities/stock-levels.md` whose Behaviour includes "When a client runs `stock reserve <sku> <n>`, the stock level falls by n and the reservation is listed." and whose Not yet says "`stock reserve`: specified, not built. Promoted when a shop reserves stock."; and `bin/stock`, a bash script answering `stock level <sku>` with `5` and anything else with `stock: unknown command` and exit 2.
  - `$SCRATCH/fixtures/slice/`: the cart example with `spec/` (index, ledger, `cart.md`, and an approved `reserve-at-checkout.md` whose Behaviour needs reserving stock), `features/reserve-at-checkout.feature` with two untagged scenarios, `CLAUDE.md` saying "Depends on stock (../stock), installed on PATH as `stock`." and nothing about the suite's speed, a `tests/conftest.py` whose `pytest_sessionstart` sleeps 65 s, `pytest.ini` without `-n`, and `docs/superpowers/plans/cart-slices.md` with slices 1–2 green and a current record `Suite: <N> passed, 2 failed at <hash> in 66 s; failing: …`, made as in Task 3 Step 2. Runs put `$SCRATCH/fixtures/stock/bin` on `PATH`.

- [ ] **Step 2: Baseline (RED).** Prompt: "The reserve-at-checkout features are approved. Slice them and plan the batch." Score: suite run although the record holds (`count_runs.py`); a fast-suite enabling slice, and where; a probe of `stock reserve` run, or the dependency's spec read (and how: whole or a range); the reserve slice planned as buildable; plan and tag edits by `sed`, heredoc or one-off Python; the writing-plans plan restating run rules; `Scripts:` absent; fresh session not recommended.

- [ ] **Step 3: Edit the skill.**
  - Overview, one paragraph: "Scripts: this plugin's `scripts/`, at `<this skill's base directory>/../../scripts/`, run with `python3`. `plan` edits and reads the living plan; `features` counts, lists and tags scenarios. Their `--help` is their contract."
  - Step 1 becomes "**Take the suite's result.** If `plan show --last-suite --current` says `current`, that record is this step's run. Otherwise run the feature suite (`python -m pytest -q`, or the project's equivalent), timed, and record it with `plan log` as bdd-red-green's suite record. Every scenario that passes is credited… (rest unchanged)." Then a second paragraph: "**Check the suite is fast.** If the record's time is over 60 s and the project's test command does not run in parallel, or the step definitions start the entry point as a program in more than one test per command, and `CLAUDE.md` gives no reason, the batch needs an enabling slice that makes it fast: `Check: the suite -> <N> passed, <M> failed, in under <bound> s`."
  - Step 2, add: "**Probe what a dependency provides.** A slice whose Needs names something another project provides gets a probe: a command run now, against the installed version, whose result shows the thing exists (`<command> --help` exits 0; a call returns). Log it, `plan log "Probe: <command> -> <result>"`. A failing probe makes the slice `blocked: awaiting <project>`, with `plan log "REQUEST <project>: <what is needed>"`; no task is written for it. Reading the project's spec is not a probe. Where you read it, read the capability file whole: what is not built is listed under Not yet."
  - Step 3, first sentence becomes: "First the enabling slice that makes the suite fast, when step 1 calls for one; then the enabling slice the skeleton stands on, if any."
  - Step 4, add: "Every edit goes through `plan` (`add-slice`, `status`, `log`, `backlog`); never `sed`, a heredoc or a one-off script on the plan."
  - Step 5, add: "Tag with `features tag "<title>" slice-<n>`; `features count --by-tag` gives each slice's count."
  - Hand-off: in "What each task carries instead", "(`pytest --collect-only -q -m slice-N`)" becomes "(`features count --by-tag`)". Replace the bullet "Each task's verification runs the slice's marker… once before the slice's last commit." with: "Each task names its markers and expected counts. When to run what is bdd-red-green's and the agents': a plan that says when to run the suite, or to record a failing list, is wrong." Add: "The plan's Global Constraints carry `Scripts: <absolute path of this plugin's scripts/>`, so every task brief carries it." After the bullets add: "When writing-plans asks how to execute, recommend a new session that reads the plan file. This session holds integration, formulation and slicing, which no task needs and every later turn would re-read."
  - The Plan File: the archive paragraph's "move that batch's green slices and their log lines to …" becomes "run `plan archive <batch>`, which moves the green slices and the log (requests stay) to `docs/superpowers/plans/archive/<plan name>-<batch>.md` and leaves one log line naming the file and the batch's last `Suite:` line".
  - Rationalizations rows from baseline evidence, at least: "The dependency's spec describes the command, so it is there" | "A spec says what is meant; its Not yet says what is not built; only a probe at the installed version says what is there. Probe it." and "The suite is slow but it works" | "Every run in the batch pays for it. Over 60 s and serial, it is the batch's first slice."
  - Red Flags: "A slice planned on a dependency's command with no `Probe:` line"; "A dependency's capability read by a section range"; "`sed`, a heredoc or `python -c` on the slice plan or on a tag line"; "A plan task that says when to run the whole suite".

- [ ] **Step 4: Green run.** Same prompt. Passes when: no suite run (the record holds) and no `pytest --collect-only` loop; slice 3 (the first new one) is the fast-suite enabling slice with a bound; a `Probe: stock reserve … -> exit 2` line, the reserve slice `blocked: awaiting stock`, a `REQUEST stock:` line, no task for it in the writing-plans plan; tags via `features tag`; every plan edit via `plan` (`plan check` says `ok` at the end); the writing-plans plan has `Scripts:` in Global Constraints and no run protocol; the final message recommends a new session. Iterate; log each iteration.

- [ ] **Step 5: Commit**

```bash
git add skills/slicing-into-increments/SKILL.md docs/superpowers/testing/2026-10-06-slicing-efficiency-test-log.md
git commit -m "slicing: the suite fast first, dependencies probed at the pin, plan and tags through the scripts, a fresh session for execution"
```

---

### Task 5: Spec agents draft to files; migration through `features`

**Files:**
- Modify: `agents/capability-writer.md` (tools; read/write paths; What you return)
- Modify: `agents/feature-formulator.md` (tools; write path; return)
- Modify: `skills/integrating-a-proposal/SKILL.md` (Process steps 1, 2, 4; The Brief; The Question Brief; Common Mistakes)
- Modify: `skills/formulating-features/SKILL.md` (Process steps 1, 2, 4; The Brief's Return paragraph; The Hand-back Brief; Common Mistakes)
- Modify: `skills/migrating-to-capabilities/SKILL.md` (Preconditions baseline; step 4 re-pairing; step 5 verify)
- Create: `docs/superpowers/testing/2026-10-06-spec-agent-drafts-test-log.md`
- Scratchpad: `fixtures/spec/`, `fixtures/legacy/`

**Interfaces:**
- Consumes: `scripts/features` (`count --by-tag`, `move`, `verify-moved`) from Task 1.
- Produces: drafts under `.superpowers/spec-drafts/<run>/` (new files whole; changed capability files as their changed sections; changed features as their new and changed scenarios; ledger entries as `decisions.append.md`); a reply holding only the change list, questions, cut sentences and the paths.

- [ ] **Step 1: Fixtures.**
  - `spec`: the cart example with a `spec/` of three capabilities (`cart.md`, `checkout.md`, `receipt.md`, each with Purpose, five Behaviour lines, Implementation, Not yet), `decisions.md` with five entries, the three formulated feature files, and an approved note `docs/superpowers/specs/2026-10-06-gift-wrap-design.md` adding one rule to checkout ("gift wrap adds 3.00 to the total") and one decision. No `.gitignore` line for `.superpowers/`.
  - `legacy`: the cart example with two feature files for one capability (`add-products-to-a-cart.feature`, `see-what-the-cart-costs.feature`) with different Backgrounds and `@slice-<n>` tags, a living slice plan, a note under `docs/superpowers/specs/`, and no `spec/`. Suite green.

- [ ] **Step 2: Baseline (RED).**
  - `spec`, prompt "The gift-wrap design is approved; carry on." to the gate. Score with `reply_sizes.py`: the capability-writer's reply bytes (expected all three capability files and the ledger in full); then resume with "Yes, the lines are approved." through formulation: the feature-formulator's reply bytes; the controller's context at the end (last `cache_read_input_tokens` in the transcript).
  - `legacy`, prompt "Migrate this repository to capability files." through the gate and, resumed with approval, re-pairing. Score: how the baseline and the counts per tag were taken (`--collect-only` loop or not); how scenarios were moved (hand edits, heredocs); how the move was verified.

- [ ] **Step 3: Edit the agents.**
  - `capability-writer.md`: `tools: Read, Glob, Grep, Write`. Replace "You write no files: you return them as text." with: "You write only under the drafts path the brief names (`.superpowers/spec-drafts/<run>/`), nothing anywhere else, `spec/` included." What you return, item 1 becomes: "Drafts, written under the drafts path: a new file whole at its `spec/` path under the drafts path; for a changed capability file, only its changed sections, each headed by the section's heading; new ledger entries only, in `decisions.append.md`. Never an unchanged file or section." Then: "Your reply holds the change list, questions and cut sentences (items 2, 4 and 5) and the paths of the drafts. No file content."
  - `feature-formulator.md`: `tools: Read, Glob, Grep, Write`. Replace "return them as text in your reply… You do not write files." with: "Write them under the drafts path the brief names and nowhere else: a new feature file whole; for an existing one, only the new and changed scenarios, each headed by the line it formulates. Your reply holds the coverage table, the questions, the cases no line mentions, and the drafts' paths. No file content."

- [ ] **Step 4: Edit the skills.**
  - `integrating-a-proposal`: step 1 adds "Choose the drafts path `.superpowers/spec-drafts/<date>-<note name>/` and name it in the brief. If `.gitignore` lacks `.superpowers/`, add it and commit that line alone." Step 2 adds, first: "Check `git status --porcelain` shows nothing but that `.gitignore` line: an agent that wrote outside the drafts path goes back with its files removed." and "compare each returned capability file's Behaviour section" becomes "compare each drafted Behaviour section". Step 4 becomes "**Apply the drafts** exactly as approved: new files copied in, changed sections replaced in place, `decisions.append.md` appended to `spec/decisions.md`; never edit an existing entry. Commit `spec/` alone…". The Brief and The Question Brief each gain "Write your drafts under <DRAFTS PATH> and nowhere else." and "Return" becomes "Write the drafts and reply with". Common Mistakes rows from the baseline (e.g. "Whole capability files and the whole ledger returned on every round" | "Changed sections and new entries only, to the drafts path; the reply is the change list").
  - `formulating-features`: the same drafts path rule and porcelain check at step 1 and 2; step 4 "A new feature file is written as returned" becomes "A new feature file is copied from its draft"; The Brief's Return paragraph becomes "Write to <DRAFTS PATH>: (1) for a new feature, the file; for an existing one, only the new and changed scenarios, each headed by the line it formulates. Reply with (2) a coverage table…, (3) questions…, (4) cases…, and the drafts' paths."; the Hand-back Brief "Return the scenario rewritten" becomes "Write the rewritten scenario to <DRAFTS PATH>".
  - `migrating-to-capabilities`: Preconditions baseline becomes "the summary line; the passing tests (`-q -rA`); a copy of `features/` in the baseline directory; and `features count --by-tag` (this plugin's `scripts/features`, at `<this skill's base directory>/../../scripts/`)". Step 4's "Move each mapped scenario in…" adds "with `features move "<title>" --to features/<name>.feature`, adding `--inline-background` where the capability's source files did not share one Background". Step 5 becomes "**Verify** against the baseline: `features verify-moved --from <baseline>/features` prints `<n> scenarios match`; the same summary line (warnings aside); the same passing scenarios by title through the mapping table; `features count --by-tag` equal to the baseline's. Any difference: stop and report it. Never edit a scenario to make the numbers match. Commit…".

- [ ] **Step 5: Green runs.**
  - `spec` passes when: the capability-writer's reply is under 4 KB; drafts exist only under `.superpowers/spec-drafts/…/` and only for `checkout.md`'s changed sections and the new ledger entry; `.gitignore` has `.superpowers/`; `git status --porcelain` is clean at the gate (Review Focus 5); after approval, `spec/` matches the approved lines with the other two capability files and the five earlier ledger entries byte-identical; the feature-formulator's reply is under 4 KB; the feature file's other scenarios byte-identical. Log the controller's final context against the baseline's.
  - `legacy` passes when: the baseline is a copy of `features/` plus `features count --by-tag`; scenarios moved by `features move`, with `--inline-background` for the differing Backgrounds; `features verify-moved` prints `<n> scenarios match`; the suite's summary unchanged.
  Iterate; log each iteration.

- [ ] **Step 6: Commit**

```bash
git add agents/capability-writer.md agents/feature-formulator.md skills/integrating-a-proposal/SKILL.md skills/formulating-features/SKILL.md skills/migrating-to-capabilities/SKILL.md docs/superpowers/testing/2026-10-06-spec-agent-drafts-test-log.md
git commit -m "Spec agents draft to .superpowers/spec-drafts and reply with the change list; migration moves and verifies through scripts/features"
```

---

### Task 6: Docs and release

**Files:**
- Modify: `README.md` (a 0.10.0 section; the agents table rows for `capability-writer` and `feature-formulator` gain Write and their drafts path; a short Scripts section)
- Modify: `.claude-plugin/plugin.json` (version `0.10.0`)

- [ ] **Step 1: README.** Add a "Fewer runs, fewer round trips (0.10.0)" section after the 0.9.0 one, one bullet per spec change (fast suite first; a suite record per commit; probes at the pin; rule-decided splits and behaviour defects; spec agents' drafts and a fresh session), and a "Scripts" section: `scripts/features` and `scripts/plan`, one line each, "`--help` is the contract; tests: `python3 -m unittest discover -s tests/scripts`". Update the two agents table rows: tools `Read, Glob, Grep, Write`, "writes only under `.superpowers/spec-drafts/`".
- [ ] **Step 2: Version.** `"version": "0.10.0"` in `.claude-plugin/plugin.json`.
- [ ] **Step 3: Verify.**
  Run: `python3 -m unittest discover -s tests/scripts -v` → 33 tests OK.
  Run: `claude --plugin-dir /home/vscode/shopsystem-bdd plugin details shopsystem-bdd` → parses, 6 agents, 5 skills.
  Run: `grep -rn "Run the whole suite at the start\|collect-only -q -m slice-N\|You write no files\|You do not write files" skills agents` → nothing.
- [ ] **Step 4: Commit**

```bash
git add README.md .claude-plugin/plugin.json
git commit -m "0.10.0: fewer runs, fewer round trips (fast suite first, suite records, probes, drafts to files, two scripts)"
```

---

## After the batch

On the next shop-knowledge batch, run superpowers:diagnosing-superpowers and compare with the 875cf22f report: whole-suite runs (at most one per slice plus one by the branch reviewer) and their total time; hand-backs for a missing dependency capability or a rule-decided split (none); the controller's peak context; spec agents' replies (under a few KB each); one-off plan or feature edits in the controller's Bash calls (none).
