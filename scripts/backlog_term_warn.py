"""The warning of `work line --term` (b801, drafting r94): a term the item now holds that violates v_t6 (two terms
that read the same, an actor that reads as a kind) kept in the item, and the rule named when it is written, not first
at `work ready`. The item is laid on a temporary copy of `spec/` (backlog_lines' `lay`) and the lexicon's v_t6
problems the lay brings that name a term of the bullets written are said, `work line: warning: v_t6: <message>`."""
import re
import shutil
import sys
import tempfile
from pathlib import Path

import backlog_lines
import spec_held
import spec_lexicon
import spec_rgl_vocab

RULE = "v_t6"
WORD = re.compile(r"^\s*-\s*\*\*(.+?)\*\*")


def _v_t6(root):
    return {p for p in spec_lexicon.problems(spec_lexicon.read(root), spec_rgl_vocab.outer(root)) if p[0] == RULE}


def warnings(root, item, bullets):
    """The v_t6 problems the item's lay onto a copy of `spec/` brings that name a word of `bullets`, as messages."""
    words = {found.group(1).strip() for found in map(WORD.match, bullets) if found}
    copy = Path(tempfile.mkdtemp(prefix="term-warn-"))
    try:
        shutil.copytree(Path(root) / "spec", copy / "spec")
        with spec_held.held(copy):
            before = _v_t6(copy)
            backlog_lines.lay_onto(copy, item)
            after = _v_t6(copy)
    except Exception:       # a warning never fails the write: the readiness bar checks the lexicon whole
        return []
    finally:
        shutil.rmtree(copy, ignore_errors=True)
    return ["%s: %s" % (code, message) for code, term, message in sorted(after - before) if term in words]


def warn(root, item, bullets):
    """`warnings` printed on stderr, each `work line: warning: <it>`; 0, the exit of the write."""
    for said in warnings(root, item, bullets or ()):
        print("work line: warning: %s" % said, file=sys.stderr)
    return 0
