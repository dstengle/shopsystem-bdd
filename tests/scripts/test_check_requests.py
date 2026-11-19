"""`model logic` on requests (the domain contract design, §5.2, §5.3; grammar/check.lp, grammar/entail.lp): an L1 between
two lines on one operation and parameter set, none when one line gives a parameter the other leaves absent, an L3 from
the domain model's lifecycle, and an L8 of a line whose Then a refusal's universal condition entails, refuse being
primitive (no bridge), on copies of tests/scripts/fixtures/domain-model/."""
import pathlib
import shutil
import subprocess
import sys

import pytest
import toolchain

REPO = pathlib.Path(__file__).resolve().parents[2]
FIXTURE = REPO / "tests" / "scripts" / "fixtures" / "domain-model"
UNIVERSAL = ("---\nid: universal/x\nlanguage: codified-2\nretired: []\n---\n\n# Universal conditions\n\n## Behaviour\n\n"
             "- [U1] If the notes service refuses a request, then the notes service shall change nothing.\n")


@pytest.fixture(scope="module", autouse=True)
def tools():
    toolchain.require()


def logic(tmp_path, *lines, universal=False):
    """`model logic` on the fixture with `lines` (r10, r11, ...) added in one group: (its exit, its output)."""
    root = tmp_path / "ctx"
    shutil.copytree(FIXTURE, root)
    cap = root / "spec" / "capabilities" / "notebook.md"
    cap.write_text(cap.read_text() + "\n### [g10] Added\n" + "".join(
        "- [r%d] %s\n" % (n, line) for n, line in enumerate(lines, 10)))
    if universal:
        (root / "spec" / "universal.md").write_text(UNIVERSAL)
    done = subprocess.run([sys.executable, str(REPO / "scripts" / "model"), "--root", str(root), "logic"],
                          capture_output=True, text=True)
    return done.returncode, done.stdout + done.stderr


def test_two_ends_of_one_request_on_one_parameter_set_clash(tmp_path):
    code, out = logic(tmp_path, "When the person adds a note, the notes service shall refuse the request.",
                      "When the person adds a note, the notes service shall complete the request.")
    assert code == 1
    assert "L1 notebook#r10 and #r11 clash: on \"the person adds a note\", r10 refuses the request and r11 completes " \
           "the request" in out


def test_an_act_obliged_and_forbidden_on_one_parameter_set_clashes(tmp_path):
    _, out = logic(tmp_path, "When the person adds a note with a text and the priority `high`, the notes service "
                                "shall not keep the note.")
    assert "L1 notebook#r3 and #r10 clash" in out and "the notes service to keep a note" in out


def test_a_parameter_given_in_one_line_and_absent_in_another_is_two_requests(tmp_path):
    code, out = logic(tmp_path, "When the person adds a note without a text, the notes service shall refuse the "
                                "request.",
                      "When the person adds a note with a text, the notes service shall complete the request.")
    assert code == 0 and "no findings" in out.lower(), out


def test_a_set_the_model_lifecycle_does_not_allow_is_an_L3(tmp_path):
    _, out = logic(tmp_path, "While a note is `active`, when the person files the note, the notes service shall "
                                "set the status of the note to `draft`.")
    assert "L3 notebook#r10 sets the status of a note from `active` to `draft`, which no transition allows" in out
    _, out = logic(tmp_path / "2", "While a note is `draft`, when the person files the note, the notes service "
                                      "shall set the status of the note to `active`.")
    assert "L3" not in out, out


def test_a_refusal_fires_the_universal_condition_with_no_bridge(tmp_path):
    _, out = logic(tmp_path, "If the person adds a note without a text and the reminder, then the notes service "
                                "shall not change the note.", universal=True)
    assert "L8 notebook#r10 says nothing other requirements do not: Then 1 by U1" in out
    assert "definition of refuse" not in out
