"""cpu_budget (b574): a command's CPU time measured against a fixed reference workload run beside it, so that a load
that inflates CPU time inflates the reference alike and a budget holds under the full suite's parallel run."""
import pathlib
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import cpu_budget

REFERENCE = [sys.executable, "-c", cpu_budget.WORKLOAD]


def test_a_budget_in_quiet_seconds_is_a_ratio_to_the_reference():
    assert cpu_budget.limit(5.0) == 5.0 / cpu_budget.QUIET


def test_the_reference_is_cpu_bound_and_measured_in_a_child():
    seconds = cpu_budget.reference()
    assert seconds > 0.1


def test_the_reference_itself_is_about_one_reference():
    _, used = cpu_budget.measured(lambda: subprocess.run(REFERENCE, check=True))
    assert 0.5 < used.ratio < 2, used


def test_twice_the_reference_is_about_two_references():
    def twice():
        subprocess.run(REFERENCE, check=True)
        subprocess.run(REFERENCE, check=True)
    _, used = cpu_budget.measured(twice)
    assert 1.2 < used.ratio < 3.5, used


def test_what_the_run_returns_is_given_back():
    done, used = cpu_budget.measured(lambda: subprocess.run([sys.executable, "-c", "print(1)"],
                                                            capture_output=True, text=True))
    assert done.stdout == "1\n"
    assert used.seconds >= 0 and used.reference > 0


def test_a_run_within_its_budget_passes_and_one_over_it_fails():
    within = cpu_budget.Used(seconds=2.0, reference=0.5)
    over = cpu_budget.Used(seconds=2.0, reference=0.1)
    assert within.ratio == 4.0 and within.within(4.01)
    assert over.ratio == 20.0 and not over.within(4.01)
    assert "quiet" in over.said(5.0)


def test_a_run_over_its_budget_is_taken_again_once(monkeypatch):
    calls = []
    def measured(run):
        calls.append(run)
        return run(), cpu_budget.Used(seconds=100.0, reference=1.0)
    monkeypatch.setattr(cpu_budget, "measured", measured)
    done, used = cpu_budget.holds(lambda: "ran", 5.0)
    assert done == "ran" and len(calls) == 2 and not used.within(cpu_budget.limit(5.0))
