"""A stopwatch of named phases (b876, measurement r13): while it runs (`started` .. `stopped`), each block a `phase`
wraps adds its own time to its name's, the time of the phases nested in it left out (a compile inside the pick is
the compile's, not the pick's), so the phases' times add up to the time they were run for. Not running, a `phase`
times nothing. Kept for one process; the phases a subprocess runs are its caller's phase. Standard library only."""
import contextlib
import time

# the phases of `work batch start`'s opening, each a name of the timings line batch_timings keeps of it
PICK, COMPILE, PARSE, LAY = "pick and readiness checks", "grammar 4 compile", "line parse", "lay"
FEATURES, CATALOGUES = "features and corpus written again", "catalogues and Composition"
CHECK, SCENARIOS, COMMIT = "item check", "laid scenarios run", "worktree and commit"

_totals = {}
_stack = []
_running = [False]


def started():
    """The stopwatch started afresh."""
    _totals.clear()
    _stack.clear()
    _running[0] = True


def stopped():
    """{name: seconds} of each phase run since `started`, in the order each first began; the stopwatch stopped."""
    _running[0] = False
    _stack.clear()
    return dict(_totals)


@contextlib.contextmanager
def phase(name):
    """The block's time, less its nested phases', added to `name`'s while the stopwatch runs."""
    if not _running[0]:
        yield
        return
    _totals.setdefault(name, 0.0)
    frame = [time.monotonic(), 0.0]
    _stack.append(frame)
    try:
        yield
    finally:
        elapsed = time.monotonic() - frame[0]
        if _stack and _stack[-1] is frame:
            _stack.pop()
            _totals[name] = _totals.get(name, 0.0) + elapsed - frame[1]
            if _stack:
                _stack[-1][1] += elapsed
