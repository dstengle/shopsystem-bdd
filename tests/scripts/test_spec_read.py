"""spec_read: the codified capability file (design §10.2, §13.4), spec/universal.md (§8.4) and spec/restated.json
(§8.3) read into groups, requirements, given blocks, restated and dropped ids, with malformed input reported by line."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

import spec_read

HEAD = """---
id: capability/ex.com/prod/ctx/work-queue
title: Work queue
narrator: the person
group: service
language: codified-1
retired: [r9, g4]
---

# Work queue

## Purpose

Prose, not read.

## Terms

- **initiative** (noun): not read here.

## Behaviour
"""

TAIL = """
## Implementation, may change

- Prose.

## Not yet

## Dropped

- r7@0.29: restated U3 (a refusal writes nothing).
- r12@0.29: moved to supervision.
"""

BODY = """
### [g1] `work start` starts a proposed initiative
Restates: r3@0.29, r4@0.29.
- [r1] When the person runs `work start` on an initiative that is `proposed`, `work` shall set its status to `started`.
- [r2] When the person runs `work start` on an initiative that is `proposed`,
  `work` shall commit the transition.

```given
an initiative i1 that is `proposed`
the file `spec/index.md` holds:
  # ctx
  some text
the work-items:
  | id | status |
  | w1 | `ready` |
```

### [g2] a moved line
Restates: formulation#r5@0.29
- [r3] `work` shall print the queue.
"""


def write(tmp_path, text, name="work-queue.md"):
    path = tmp_path / name
    path.write_text(text)
    return path


def read(tmp_path, body=BODY, head=HEAD, tail=TAIL):
    return spec_read.capability(write(tmp_path, head + body + tail))


def test_groups_and_ids(tmp_path):
    cap = read(tmp_path)
    assert cap.problems == []
    assert [g.id for g in cap.groups] == ["g1", "g2"]
    assert cap.groups[0].title == "`work start` starts a proposed initiative"
    assert [r.id for r in cap.groups[0].requirements] == ["r1", "r2"]
    assert cap.groups[1].requirements[0].text == "`work` shall print the queue."


def test_a_continuation_line_is_part_of_its_requirement_and_line_numbers_are_the_files(tmp_path):
    cap = read(tmp_path)
    r1, r2 = cap.groups[0].requirements
    assert r2.text == ("When the person runs `work start` on an initiative that is `proposed`, "
                       "`work` shall commit the transition.")
    lines = (HEAD + BODY).splitlines()
    assert lines[r1.line_no - 1].startswith("- [r1]")
    assert lines[r2.line_no - 1].startswith("- [r2]")


def test_restates_both_forms(tmp_path):
    cap = read(tmp_path)
    assert cap.groups[0].restates == [("work-queue", 3), ("work-queue", 4)]
    assert cap.groups[1].restates == [("formulation", 5)]


def test_given_block_with_a_docstring_and_a_table(tmp_path):
    given = read(tmp_path).groups[0].given
    assert [line for line, _ in given] == [
        "an initiative i1 that is `proposed`", "the file `spec/index.md` holds:", "the work-items:"]
    assert given[0][1] is None
    assert given[1][1].kind == "docstring" and given[1][1].lines == ["# ctx", "some text"]
    assert given[2][1].kind == "table" and given[2][1].rows == [["id", "status"], ["w1", "`ready`"]]
    assert read(tmp_path).groups[1].given == []


def test_dropped_retired_and_frontmatter(tmp_path):
    cap = read(tmp_path)
    assert cap.dropped == [("work-queue", 7, "restated U3 (a refusal writes nothing)."),
                           ("work-queue", 12, "moved to supervision.")]
    assert cap.retired == ["r9", "g4"]
    assert cap.frontmatter["group"] == "service"


def test_the_marker(tmp_path):
    assert spec_read.codified(write(tmp_path, HEAD + BODY))
    assert not spec_read.codified(write(tmp_path, HEAD.replace("language: codified-1\n", "") + BODY))
    assert not spec_read.codified(write(tmp_path, HEAD.replace("codified-1", "codified-2") + BODY))
    assert not spec_read.codified(tmp_path / "missing.md")


def test_an_uncodified_file_is_reported_and_not_read_as_groups(tmp_path):
    cap = read(tmp_path, head=HEAD.replace("language: codified-1\n", ""), body="\n- [r1] When asked, it answers.\n")
    assert cap.groups == []
    assert any("not codified" in p for p in cap.problems)


def problems(tmp_path, body):
    return read(tmp_path, body=body).problems


def test_malformed_input_is_reported_with_line_numbers(tmp_path):
    start = len(HEAD.splitlines()) + 1        # the first line of BODY is blank, at this number
    found = problems(tmp_path, "\n- [r1] outside any group.\n### no id here\n### [g1] ok\nRestates: r3, x@0.29\n"
                               "- [r2]\n- r3 no brackets\n- [r4] fine.\n### [g1] again\n- [r4] a duplicate.\n")
    assert found == [
        f"{start + 1}: a requirement outside a group",
        f"{start + 2}: a group heading is not '### [g<n>] <title>'",
        f"{start + 4}: Restates: 'r3' is not r<n>@0.29 or <capability>#r<n>@0.29",
        f"{start + 4}: Restates: 'x@0.29' is not r<n>@0.29 or <capability>#r<n>@0.29",
        f"{start + 5}: a requirement is not '- [r<n>] <statement>'",
        f"{start + 6}: a requirement is not '- [r<n>] <statement>'",
        f"{start + 8}: g1 appears a second time",
        f"{start + 9}: r4 appears a second time",
    ]


def test_a_retired_id_used_again_and_an_empty_group(tmp_path):
    start = len(HEAD.splitlines()) + 1
    assert problems(tmp_path, "\n### [g4] retired\n- [r9] retired too.\n### [g5] empty\n") == [
        f"{start + 1}: g4 is retired",
        f"{start + 2}: r9 is retired",
        f"{start + 3}: g5 has no requirement",
    ]


def test_a_malformed_given_block(tmp_path):
    start = len(HEAD.splitlines()) + 1
    body = "\n### [g1] t\n- [r1] `work` shall print the queue.\n```given\n  indented first\nthe rows:\n  | a |\n  text\n"
    assert problems(tmp_path, body) == [
        f"{start + 3}: a given block is not closed",
        f"{start + 4}: an indented line is under no given line ending in ':'",
        f"{start + 7}: a given block mixes table rows and text",
    ]


def test_a_malformed_dropped_line(tmp_path):
    text = HEAD + BODY + "\n## Dropped\n\n- r7: no version.\n- r8@0.29\n"
    n = len((HEAD + BODY).splitlines()) + 4
    assert spec_read.capability(write(tmp_path, text)).problems == [
        f"{n}: a dropped line is not '- r<n>@0.29: <reason>'",
        f"{n + 1}: a dropped line is not '- r<n>@0.29: <reason>'",
    ]


UNIVERSAL = """---
id: capability/ex.com/prod/ctx/universal
title: Universal conditions
group: guarantees
language: codified-1
---

# Universal conditions

## Behaviour

- [U1] `work run` shall hold at most 4 worker slots.
- [U2] Only `work` shall write a status,
  every time.
- U3 no brackets
- [U2] again.
"""


def test_universal(tmp_path):
    (tmp_path / "spec").mkdir()
    write(tmp_path / "spec", UNIVERSAL, "universal.md")
    found = spec_read.universal(tmp_path)
    assert [(u.id, u.text, u.line_no) for u in found] == [
        ("U1", "`work run` shall hold at most 4 worker slots.", 12),
        ("U2", "Only `work` shall write a status, every time.", 13)]
    doc = spec_read.read_universal(tmp_path)
    assert doc.frontmatter["group"] == "guarantees"
    assert doc.problems == ["15: a universal condition is not '- [U<n>] <statement>'", "16: U2 appears a second time"]


def test_universal_without_the_marker_or_the_file(tmp_path):
    (tmp_path / "spec").mkdir()
    write(tmp_path / "spec", UNIVERSAL.replace("language: codified-1\n", ""), "universal.md")
    assert any("not codified" in p for p in spec_read.read_universal(tmp_path).problems)
    assert spec_read.universal(tmp_path / "nowhere") == []


def test_a_retired_universal_condition_used_again_is_a_problem(tmp_path):
    """A U<n> in universal.md's `retired:` is never used again (retire, never edit; plan-9 review S2)."""
    (tmp_path / "spec").mkdir()
    write(tmp_path / "spec", UNIVERSAL.replace("language: codified-1\n", "language: codified-1\nretired: [U2, U3]\n"),
          "universal.md")
    assert "14: U2 is retired" in spec_read.read_universal(tmp_path).problems


def test_restated(tmp_path):
    (tmp_path / "spec").mkdir()
    (tmp_path / "spec" / "restated.json").write_text(json.dumps({"work-queue#r3": {"text": "x", "line": 40}}))
    assert spec_read.restated(tmp_path) == {"work-queue#r3": {"text": "x", "line": 40}}
    assert spec_read.restated(tmp_path / "nowhere") == {}


def test_the_live_restated_file_is_keyed_by_capability_and_id():
    root = Path(__file__).resolve().parents[2]
    found = spec_read.restated(root)
    assert len(found) == 581
    assert all(set(v) == {"text", "line"} for v in found.values())
    assert found["work-queue#r1"]["line"] > 0


def test_example_data_is_known_by_its_shape():
    """v15m's shape test (design-r2 §9.1): no grammar, only the line and whether data follows it."""
    from spec_read_given import Block, example
    assert example("the file `a.md` holds:", Block("docstring", ["# ctx"]))
    assert example('the file `a.md` holds "x"') and example("the Python file `big.py` holds `x = 1`")
    assert example('the session file s-1 holds "not a session"')
    assert not example("the file `a.md` holds:")                      # nothing after it
    assert not example('the file `a.md` holds "x" and "y"')
    assert not example("a result r1") and not example("the result r1 is outputless")
    assert not example("the work-items:", Block("table", ["| id |"]))
