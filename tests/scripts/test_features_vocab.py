"""The fixed step vocabulary (design §14.1, §14.3): the typed Steps funs and their patterns, a step read back into its
template, kind and arguments, `features vocab --check`, the post-scenario U checks, and a fixture repository whose
generated feature passes under pytest with its handlers."""
import importlib.util
import pathlib
import re
import shutil
import subprocess
import sys

import features_vocab
import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import toolchain

REPO = pathlib.Path(__file__).resolve().parents[2]
FEATURES = REPO / "scripts" / "features"
FIXTURES = REPO / "tests" / "scripts" / "fixtures" / "generate"
E2E = FIXTURES / "e2e"


@pytest.fixture(scope="module")
def vocab():
    toolchain.require()
    return features_vocab.load(FIXTURES / "repo")


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


def test_two_kinds_with_the_same_template_give_two_distinct_patterns(vocab):
    rows = {r.kind: r for r in features_vocab.rows(vocab) if r.template == "ThenK_A" and " not " not in r.pattern}
    assert rows["initiative"].pattern != rows["work-item"].pattern
    assert re.fullmatch(rows["initiative"].regex, "the initiative i1 is `started`")
    assert not re.fullmatch(rows["work-item"].regex, "the initiative i1 is `started`")
    assert rows["initiative"].pattern == "the initiative {n1} is {x1}"


def test_every_row_names_its_template_kind_and_fun(vocab):
    rows = features_vocab.rows(vocab)
    given = [r for r in rows if r.template == "GivenK_A" and r.kind == "initiative" and r.attribute == "status"]
    assert given and given[0].pattern == "an initiative {n1} that is {x1}"
    assert {r.keyword for r in rows} == {"given", "when", "then"}
    assert any(r.template == "WhenRuns" and r.kind is None for r in rows)


@pytest.mark.parametrize("keyword, text, expected", [
    ("then", "the initiative i1 is `started`",
     {"template": "ThenK_A", "kind": "initiative", "attribute": "status", "term": "initiative", "names": ["i1"],
          "values": ["`started`"]}),
    ("given", "the initiative i1 is `started`", {"template": "GivenK_A", "kind": "initiative", "term": "initiative"}),
    ("given", "an initiative i1 that is `proposed`", {"template": "GivenK_A", "names": ["i1"], "values": ["`proposed`"]}),
    ("when", "the person runs `work start` on the initiative i1",
     {"template": "WhenRuns", "kind": "initiative", "term": "`work start`", "subject": "the person", "names": ["i1"]}),
    ("when", "the person runs `work list`", {"template": "WhenRuns", "kind": None, "term": "`work list`"}),
    ("then", "`work run` takes the initiative i1", {"template": "ThenDoes", "term": "take", "kind": "initiative"}),
    ("when", "`work run` starts the stage s1", {"template": "WhenHappens", "term": "start", "kind": "stage"}),
    ("then", "`work` prints the work-item w1", {"template": "ThenPrints", "term": "`work`", "nps": ["the work-item w1"]}),
    ("then", "`work` exits with an error naming the status of the initiative i1",
     {"template": "ThenExitsErr", "term": "`work`", "names": ["i1"]}),
    ("given", "the file `notes.md` holds:", {"template": "GivenCodeText", "kind": "file", "names": ["`notes.md`"]}),
    ("given", "the work-item w1 is under the capability-proposal p1",
     {"template": "GivenR", "kind": "work-item", "term": "under", "names": ["w1", "p1"]}),
])
def test_a_step_is_read_back_into_its_template_and_arguments(vocab, keyword, text, expected):
    call = features_vocab.step(vocab, keyword, text)
    for field, value in expected.items():
        assert getattr(call, field) == value, (field, call)


def test_a_step_that_does_not_parse_is_refused(vocab):
    with pytest.raises(features_vocab.StepError, match="does not parse"):
        features_vocab.step(vocab, "then", "the initiative i1 is happy")


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


def test_the_u3_and_u8_checks_after_a_scenario():
    vocab = load_vocab_module()
    refused = {"args": ["work", "start", "i1"], "returncode": 1, "stdout": "", "changed": [".shop/work/i1.md"]}
    json_ok = {"args": ["model", "check", "--json"], "returncode": 0, "stdout": '{"a": 1}\n', "changed": []}
    json_bad = {"args": ["model", "check", "--json"], "returncode": 0, "stdout": '{"a": 1}\n{"b": 2}\n',
                "changed": []}
    problems = vocab.u_problems([refused, json_ok, json_bad])
    assert len(problems) == 2
    assert problems[0].startswith("U3:") and ".shop/work/i1.md" in problems[0]
    assert problems[1].startswith("U8:")
    assert vocab.u_problems([json_ok, dict(refused, changed=[])]) == []


def test_marks_come_from_the_spec():
    vocab = load_vocab_module()
    marks = vocab.marks(FIXTURES / "repo")
    assert {"g1", "g2", "g3", "r1", "r4"} <= set(marks)
    assert "r5" not in marks
