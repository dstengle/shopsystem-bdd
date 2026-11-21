"""b445: the readiness bar's copy holds spec/ and no adapter program, so the CLI contract's v_a3 and v_a4 would fire
for every operation before and after every lay. They name an operation or a command, never an item's group or
requirement, and an item's command is unbuilt at `work ready`; the bar checks neither (as v_a5 and v_a6, decision
0112), and `spec check` and `work batch done` keep checking them on the built tree."""
import pathlib
import shutil

import readiness_bar

FIXTURE = pathlib.Path(__file__).parent / "fixtures" / "domain-model"


def test_a_copy_of_spec_with_no_program_has_no_v_a3_or_v_a4(tmp_path):
    import toolchain
    toolchain.require()
    shutil.copytree(FIXTURE / "spec", tmp_path / "spec")       # the program notes_cli.py is left out, as in the copy
    found, _ = readiness_bar._violations(tmp_path)
    assert not {name for name, _ in found} & {"v_a3", "v_a4"}


def test_the_bar_skips_the_adapter_rules():
    assert {"v_a3", "v_a4", "v_a5", "v_a6"} <= readiness_bar.OWN_STAGE
