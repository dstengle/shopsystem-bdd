"""grammar/check.lp at scale (b119): this repository's facts copied four times over, each copy with its own ids, codes
and command strings (every quoted constant renamed; events, kinds and the domain shared, as a growing spec shares
them), ground and solved within a time limit, and grounding near-linear in the lines. A join on a vocabulary word that
thousands of lines share (check.lp's header rule) passes at today's size and grows with the square of the lines: at
four copies the old encoding grounded 12 times the rules of one copy, the rewrite 5 times."""
import pathlib
import re
import sys
import time

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "tests"))
import toolchain

COPIES = 4
QUOTED = re.compile(r'"((?:[^"\\]|\\.)*)"')


@pytest.fixture(scope="module")
def context():
    toolchain.require()
    import spec_context
    ctx = spec_context.load(ROOT)
    return ctx.domain, [f for s in ctx.statements for f in ctx.facts[s.id]]


def copies(facts, k):
    """k copies of the facts, the i-th with every quoted constant (an id, a code, a command) given the suffix ~i."""
    return [QUOTED.sub(lambda m, i=i: '"%s~%d"' % (m.group(1), i), f) if i else f for i in range(k) for f in facts]


def ground(domain, facts):
    """(the rules grounded, the seconds to ground and solve) of check.lp over the facts, as `model logic` solves."""
    import clingo
    import spec_solve
    began = time.time()
    ctl = clingo.Control(["--warn=none", "--stats"])
    ctl.add("base", [], "\n".join(domain + facts + [spec_solve.CHECK.read_text()]))
    ctl.ground([("base", [])])
    _, done, sat = spec_solve._solve(ctl, spec_solve.LIMIT)
    assert done and sat
    return ctl.statistics["problem"]["lp"]["rules"], time.time() - began


@pytest.mark.live_logic
def test_a_four_times_scaled_spec_grounds_near_linear_and_in_time(context):
    domain, facts = context
    one, _ = ground(domain, facts)
    four, took = ground(domain, copies(facts, COPIES))
    assert took < 5.0, took
    assert four < 2 * COPIES * one, (one, four)     # a square would be 16 times
