"""model_work's reading of spec/decisions/ (b735): a requirement id a decision's `enforced_by` names that its
capability's `retired:` lists is history on a decision no longer in force (superseded or rejected), and a reference
that names nothing on an accepted one; a live id resolves on either."""
import sys
import textwrap
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import model_facts

PATH = "example.org/fixture/decided"
INDEX = textwrap.dedent(f"""\
    ---
    id: bounded-context/{PATH}
    language: codified-2
    ---

    # decided

    ## Purpose
    Something.
    """)
CAPABILITY = textwrap.dedent(f"""\
    ---
    id: capability/{PATH}/thing
    narrator: the person
    group: service
    language: codified-2
    retired: [g1, r1]
    ---

    # thing

    ## Purpose
    Something.

    ## Behaviour
    """)
DECISION = textwrap.dedent(f"""\
    ---
    id: design-decision/{PATH}/kept
    summary: "Kept."
    date: 2026-11-26
    status: %s
    tier: requirement
    enforced_by: [thing#r1]
    verified_by: [scenario]
    ---

    # 0001. Kept

    ## Decision

    Kept.
    """)


def dangling(tmp_path, status):
    for rel, text in (("spec/index.md", INDEX), ("spec/capabilities/thing.md", CAPABILITY),
                      ("spec/decisions/0001-kept.md", DECISION % status)):
        (tmp_path / rel).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / rel).write_text(text)
    model = model_facts.Model(tmp_path)
    model.read()
    return [d for d in model.dangling if "thing#r1" in d]


@pytest.mark.parametrize("status", ["superseded", "rejected"])
def test_a_decision_no_longer_in_force_may_name_a_retired_requirement(tmp_path, status):
    assert dangling(tmp_path, status) == []


def test_an_accepted_decision_naming_a_retired_requirement_is_unresolved(tmp_path):
    assert dangling(tmp_path, "accepted") == [
        f"spec/decisions/0001-kept.md: capability/{PATH}/thing#r1 is not a requirement in this repository"]
