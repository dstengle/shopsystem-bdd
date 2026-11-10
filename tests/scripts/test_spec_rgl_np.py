"""Grammar 4's noun phrases (the CNL 4 design, I8; spec_rgl_np): of, its, no, has, holds, lists, only and compounds
over the rows and attributes of the codified-2 fixture."""
import pathlib
import sys

import pytest
import spec_grammar4

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

