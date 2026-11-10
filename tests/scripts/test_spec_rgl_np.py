"""Grammar 4's noun phrases (the CNL 4 design, I8; spec_rgl_np): of, its, no, has, holds, lists, only and compounds
over the rows and attributes of the codified-2 fixture, and v_t18, a declared compound that a row or an attribute
also derives."""
import pathlib
import shutil
import subprocess
import sys

import pytest
import spec_grammar4
import spec_lexicon
import spec_rgl_np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import toolchain

REPO = pathlib.Path(__file__).resolve().parents[2]
FIXTURE = REPO / "tests" / "scripts" / "fixtures" / "codified-2"


@pytest.fixture(scope="module")
def root():
    toolchain.require()
    return FIXTURE


def tree(root, line):
    p = spec_grammar4.parse(root, line)
    assert p.tree, p.refusal
    return p.tree


def test_of_and_its_read_a_row_and_an_attribute(root):
    t = tree(root, "When a session ends a stage, `work` shall print the status of the stage and the worktree of the "
                   "session.")
    assert "t_status_1_Of_k_stage" in t and "r1_of_Mod k_worktree_n" in t and "k_thing_And" in t
    assert "k_worktree_Its" in tree(root, "A session shall change only files in its worktree.")
    assert "t_status_1_Its" in tree(root, "When a session ends a stage, `work` shall print its status.")


def test_no_has_and_holds(root):
    t = tree(root, "While a session has no worktree, when the person runs `work start`, `work` shall exit successfully.")
    assert "r1_of_Has" in t and "DetNo" in t
    t = tree(root, "While a worktree holds a file, when a session writes the file, `work` shall print the worktree.")
    assert "r2_in_Holds" in t


def test_a_compound_means_what_its_genitive_means_and_only_takes_an_object(root):
    assert "t_status_1_Cpd_k_stage DetThe" in tree(root, "When a session ends a stage, `work` shall print the stage "
                                                         "status.")
    assert "r1_of_Cpd" in tree(root, "When a session writes a file, `work` shall print the session worktree.")
    assert "k_thing_Only" in tree(root, "A session shall change only files in its worktree.")


def test_a_list_is_never_coerced_to_a_kind_above(root):
    p = spec_grammar4.parse(root, "When the person runs `work start`, `work` shall print the file, the stage and the "
                                  "worktree.")
    assert p.tree and len(p.trees) == 1 and "k_thing_More" in p.tree


def test_a_declared_compound_that_is_derived_is_refused(tmp_path):
    shutil.copytree(FIXTURE / "spec", tmp_path / "spec")
    index = tmp_path / "spec" / "index.md"
    index.write_text(index.read_text().replace("codified-2", "codified-1")
                     + "- **stage status** (noun): how far a stage is.\n"
                     "- **session worktree** (noun): a worktree of a session.\n"
                     "- **pull request** (noun): a change asked for.\n")
    lexicon = spec_lexicon.read(tmp_path)
    assert spec_rgl_np.derived(lexicon) == {"stage status": "the attribute status of stage",
                                            "session worktree": "the row worktree | of | session"}
    # `model check` reads a codified-1 index's lexicon (a codified-2 one is v_p0 until the switch, I19)
    done = subprocess.run([sys.executable, str(REPO / "scripts" / "model"), "--root", str(tmp_path), "check"],
                          capture_output=True, text=True, timeout=300)
    found = [line for line in done.stdout.splitlines() if "v_t18" in line or "/stage-status" in line
             or "/session-worktree" in line or "/pull-request" in line]
    assert found[0].startswith("v_t18") and "(2)" in found[0], done.stdout
    assert all("pull-request" not in line for line in found[:3]), done.stdout
