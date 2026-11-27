"""plumbing.phases (b876, measurement r13): the stopwatch of an opening's phases, each phase's own time, the time of
the phases nested in it left out, nothing timed while it is stopped."""
import time

from plumbing import phases


def test_a_nested_phase_is_left_out_of_the_phase_around_it():
    phases.started()
    with phases.phase("pick"):
        time.sleep(0.05)
        with phases.phase("compile"):
            time.sleep(0.1)
    with phases.phase("compile"):
        time.sleep(0.05)
    found = phases.stopped()
    assert list(found) == ["pick", "compile"]
    assert 0.14 <= found["compile"] < 0.3 and 0.04 <= found["pick"] < 0.1


def test_nothing_is_timed_while_stopped():
    phases.started()
    phases.stopped()
    with phases.phase("lay"):
        pass
    assert phases.stopped() == {}
