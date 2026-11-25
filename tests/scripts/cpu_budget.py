"""A CPU-time budget that holds under the full suite's parallel load (b574).

A command's CPU time grows with the load around it (shared cores, cache, clock), so a ceiling in seconds is
borderline under 32 workers. The command is measured against a fixed CPU-bound reference workload run as a child
process right before and after it: load inflates the reference alike, so the ratio of the command's CPU time to the
reference's holds, while a command that grew slower still fails. A budget given in seconds of a quiet machine is the
ratio it bears to the reference's quiet time, `QUIET`, calibrated once on a quiet machine."""
import dataclasses
import resource
import subprocess
import sys

# The reference workload: interpreter work of the kind the measured commands do (dicts, strings, sorting), fixed in
# size, run in a fresh interpreter so its start-up is counted as the command's is.
WORKLOAD = """\
table = {}
for i in range(2000000):
    key = "k%d" % (i % 5003)
    table[key] = table.get(key, 0) + len(key)
words = sorted(table, key=lambda k: (table[k], k))
assert len(words) == 5003
"""

# The reference's CPU time in seconds on a quiet machine (median of ten runs alone, b574).
QUIET = 0.35


def _children():
    usage = resource.getrusage(resource.RUSAGE_CHILDREN)
    return usage.ru_utime + usage.ru_stime


def cpu(run):
    """What `run` returns and the CPU time of the child processes it ran and waited for, in seconds."""
    before = _children()
    result = run()
    return result, _children() - before


def reference():
    """The reference workload's CPU time now, in seconds."""
    _, seconds = cpu(lambda: subprocess.run([sys.executable, "-c", WORKLOAD], check=True))
    return seconds


@dataclasses.dataclass(frozen=True)
class Used:
    seconds: float
    reference: float

    @property
    def ratio(self):
        return self.seconds / self.reference

    def within(self, ratio):
        return self.ratio < ratio

    def said(self, quiet_seconds):
        return ("took %.2f s of CPU time, %.1f references of %.2f s; the budget is %.1f references (%.1f s on a"
                " quiet machine, where the reference takes %.2f s)"
                % (self.seconds, self.ratio, self.reference, limit(quiet_seconds), quiet_seconds, QUIET))


def limit(quiet_seconds):
    """A budget of `quiet_seconds` on a quiet machine as a ratio to the reference."""
    return quiet_seconds / QUIET


def measured(run):
    """What `run` returns and its `Used`: its children's CPU time beside the mean of the reference run right before
    and right after it."""
    first = reference()
    result, seconds = cpu(run)
    last = reference()
    return result, Used(seconds=seconds, reference=(first + last) / 2)


def holds(run, quiet_seconds):
    """What `run` returns and its `Used`, `run` taken again once when it is over its budget (it may have warmed a
    cache)."""
    for _ in range(2):
        result, used = measured(run)
        if used.within(limit(quiet_seconds)):
            break
    return result, used
