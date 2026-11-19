"""The checks after a generated scenario (tests/scenarios/vocab.py, the domain contract design §9.3): U17, a refused
request names a reason and changes nothing; and the store's sharing, the check of the decision "Git is the store and
the isolation" (U13 retired into it), which store_git makes: a request's kept commit is on its upstream remote, not
asked under a remote the scenario made unpushable. U16's check left with U16, into the decision "The response
envelope" (tests/scripts/test_domain_envelope.py)."""
import importlib.util
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def vocab():
    spec = importlib.util.spec_from_file_location("shop_vocab_u17", REPO / "tests" / "scenarios" / "vocab.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


REFUSED = {"args": ["work", "decision", "A"], "returncode": 1, "stdout": "", "stderr": "work: give --tier\n",
           "changed": [], "unshared": None}


def test_a_refusal_that_names_a_reason_and_changes_nothing_passes():
    assert vocab().u_problems([REFUSED]) == []


def test_a_check_that_fails_saying_its_findings_on_stdout_passes():
    """Exit 1 is the CLI's refused, failed and broken alike (cli.toml's outcomes): the reason is said on either."""
    assert vocab().u_problems([dict(REFUSED, stderr="", stdout="v_d6  a check decision names no test\n")]) == []


def test_a_refusal_with_no_reason_fails_u17():
    problems = vocab().u_problems([dict(REFUSED, stderr="  \n")])
    assert len(problems) == 1 and problems[0].startswith("U17:") and "no reason" in problems[0]


def test_a_refusal_that_changed_the_store_fails_u17():
    problems = vocab().u_problems([dict(REFUSED, changed=["spec/decisions/0001-a.md"])])
    assert len(problems) == 1 and problems[0].startswith("U17:") and "spec/decisions/0001-a.md" in problems[0]


def test_a_kept_commit_not_shared_fails_the_store_check_unless_the_remote_is_unpushable():
    done = {"args": ["work", "idea", "x"], "returncode": 0, "stdout": "", "stderr": "", "changed": [".shop/b1.md"],
            "unshared": "origin"}
    problems = vocab().u_problems([done])
    assert len(problems) == 1 and "not shared" in problems[0] and "origin" in problems[0]
    assert vocab().u_problems([done], unpushable=True) == []
    assert vocab().u_problems([dict(done, unshared=None)]) == []


def test_json_output_is_no_longer_checked_after_a_scenario():
    done = {"args": ["model", "check", "--json"], "returncode": 0, "stdout": "{}\n{}\n", "stderr": "", "changed": [],
            "unshared": None}
    assert vocab().u_problems([done]) == []
