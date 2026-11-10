"""The step vocabulary (design §14.1, §14.3): a step read back through the step grammar 4 into its template, kind and
arguments, `features vocab` and `features vocab --check`, the post-scenario U checks, and a fixture repository whose
generated feature passes under pytest with its handlers."""
import importlib.util
import pathlib
import shutil
import subprocess
import sys

import features_vocab4
import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import toolchain

REPO = pathlib.Path(__file__).resolve().parents[2]
FEATURES = REPO / "scripts" / "features"
FIXTURES = REPO / "tests" / "scripts" / "fixtures" / "generate"
E2E = FIXTURES / "e2e"


@pytest.fixture(scope="module")
def root():
    toolchain.require()
    return str(FIXTURES / "repo")


@pytest.fixture
def repo(tmp_path):
    toolchain.require()
    shutil.copytree(FIXTURES / "repo", tmp_path / "repo")
    root = tmp_path / "repo"
    done = features(root, "generate", "work-queue")
    assert done.returncode == 0, done.stderr
    return root


def features(root, *args):
    return subprocess.run([sys.executable, str(FEATURES), *args], cwd=root, capture_output=True, text=True)


def scenarios_dir(root, handlers):
    tests = root / "tests" / "scenarios"
    tests.mkdir(parents=True, exist_ok=True)
    (tests / "work_queue_handlers.py").write_text(handlers)
    return tests


@pytest.mark.parametrize("keyword, text, expected", [
    ("given", "an initiative i1", {"template": "GivenK", "kind": "initiative", "term": "initiative", "names": ["i1"]}),
    ("given", "the initiative i1 is `proposed`",
     {"template": "GivenK_A", "kind": "initiative", "attribute": "status", "names": ["i1"], "values": ["`proposed`"]}),
    ("when", "the person runs `work start` on the initiative i1",
     {"template": "WhenRuns", "term": "`work start`", "command": "`work start`", "names": ["i1"]}),
    ("when", "the person runs `work list`", {"template": "WhenRuns", "kind": None, "term": "`work list`"}),
    ("then", "`work` sets the status of the initiative i1 to `started`",
     {"template": "ThenDoes", "term": "set", "names": ["i1"], "values": ["`started`"]}),
    ("then", "`work` takes the initiative i1", {"template": "ThenDoes", "term": "take", "names": ["i1"]}),
    ("when", "`work` starts the stage s1", {"template": "WhenHappens", "term": "start", "names": ["s1"]}),
    ("then", "`work` prints the work-item w1", {"template": "ThenPrints", "term": "`work`", "nps": ["the work-item w1"]}),
    ("then", "`work` exits with an error naming the status of the initiative i1",
     {"template": "ThenExitsErr", "term": "`work`", "names": ["i1"]}),
    ("given", "the file `notes.md` holds:", {"template": "GivenCodeText", "kind": "file", "names": ["`notes.md`"]}),
    ("given", "the stage s1 is for the work-item w1",
     {"template": "GivenDoes", "term": "for", "names": ["s1", "w1"]}),
])
def test_a_step_is_read_back_into_its_template_and_arguments(root, keyword, text, expected):
    call = features_vocab4.step(root, keyword, text)
    for field, value in expected.items():
        assert getattr(call, field) == value, (field, call)


def test_a_step_that_does_not_parse_is_refused(root):
    with pytest.raises(features_vocab4.StepError, match="does not parse"):
        features_vocab4.step(root, "then", "the initiative i1 is happy")


def test_vocab_prints_the_functions_of_the_step_grammar_4(repo):
    done = features(repo, "vocab")
    assert done.returncode == 0, done.stderr
    assert "k_initiative_Given : k_initiative_N -> Name -> Step" in done.stdout.splitlines()


def test_vocab_check_names_a_missing_handler_and_passes_with_every_one(repo):
    handlers = (E2E / "work_queue_handlers.py.in").read_text()
    missing = handlers.replace('@handler("WhenRuns", "`work start`")\n', "")
    scenarios_dir(repo, missing)
    done = features(repo, "vocab", "--check", "--tests", "tests/scenarios", "features/work-queue.feature")
    assert done.returncode == 1
    assert "no handler for WhenRuns `work start`" in done.stdout
    assert "the person runs `work start` on the initiative i1" in done.stdout
    scenarios_dir(repo, handlers)
    ok = features(repo, "vocab", "--check", "--tests", "tests/scenarios")
    assert ok.returncode == 0, ok.stdout + ok.stderr


def test_vocab_check_wants_no_handler_for_an_unbuilt_scenario(repo):
    handlers = (E2E / "work_queue_handlers.py.in").read_text()
    scenarios_dir(repo, handlers.replace('@handler("WhenRuns", "`work start`")\n', ""))
    cap = repo / "spec" / "capabilities" / "work-queue.md"
    cap.write_text(cap.read_text().replace("retired: []\n", "retired: []\nunbuilt: [r1, r2, r3]\n", 1))
    done = features(repo, "vocab", "--check", "--tests", "tests/scenarios", "features/work-queue.feature")
    assert done.returncode == 0, done.stdout + done.stderr


def test_vocab_check_names_two_handlers_that_claim_one_key(repo):
    handlers = (E2E / "work_queue_handlers.py.in").read_text()
    tests = scenarios_dir(repo, handlers)
    (tests / "more_handlers.py").write_text(
        'from vocab import handler\n\n\n@handler("ThenExitsOk")\ndef again(step):\n    pass\n')
    done = features(repo, "vocab", "--check", "--tests", "tests/scenarios")
    assert done.returncode == 1
    assert "two handlers claim ThenExitsOk" in done.stdout


def test_a_generated_feature_with_its_handlers_passes_under_pytest_end_to_end(repo):
    tests = scenarios_dir(repo, (E2E / "work_queue_handlers.py.in").read_text())
    (tests / "conftest.py").write_text((E2E / "conftest.py.in").read_text().replace("@PLUGIN@", str(REPO)))
    (tests / "test_work_queue.py").write_text((E2E / "test_work_queue.py.in").read_text())
    (repo / "pytest.ini").write_text("[pytest]\ntestpaths = tests\nbdd_features_base_dir = features/\n")
    done = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"], cwd=repo,
                          capture_output=True, text=True)
    assert done.returncode == 0, done.stdout[-3000:] + done.stderr[-2000:]
    assert "3 passed" in done.stdout


def load_vocab_module():
    spec = importlib.util.spec_from_file_location("shop_vocab_test", REPO / "tests" / "scenarios" / "vocab.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_the_u11_and_u8_checks_after_a_scenario():
    vocab = load_vocab_module()
    refused = {"args": ["work", "start", "i1"], "returncode": 1, "stdout": "", "changed": [".shop/work/i1.md"]}
    json_ok = {"args": ["model", "check", "--json"], "returncode": 0, "stdout": '{"a": 1}\n', "changed": []}
    json_bad = {"args": ["model", "check", "--json"], "returncode": 0, "stdout": '{"a": 1}\n{"b": 2}\n',
                "changed": []}
    problems = vocab.u_problems([refused, json_ok, json_bad])
    assert len(problems) == 2
    assert problems[0].startswith("U12:") and ".shop/work/i1.md" in problems[0]
    assert problems[1].startswith("U16:")
    assert vocab.u_problems([json_ok, dict(refused, changed=[])]) == []


def test_marks_come_from_the_spec():
    vocab = load_vocab_module()
    marks = vocab.marks(FIXTURES / "repo")
    assert {"g1", "g2", "g3", "r1", "r4"} <= set(marks)
    assert "r5" not in marks
