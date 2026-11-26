"""feature_file_tools_uses' prepare (b734): a Given that no frame takes `thing` reaches a b298 world, or prepare fails
naming the fact, so that scenarios#r22 and #r25 never pass on the plain catalogue example."""
import importlib.util
from pathlib import Path
from types import SimpleNamespace

import pytest

SOURCE = Path(__file__).resolve().parents[1] / "scenarios" / "feature_file_tools_uses.py"


def _module():
    spec = importlib.util.spec_from_file_location("ffu_under_test", SOURCE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def _world(subject, code="`order-by`"):
    return {"kinds": {"v1": "verb", "r1": "requirement"}, "values": {},
            "facts": [("use", "r1", code, True), ("take", ("no", subject), "`thing`", True),
                      ("use", "r1", "v1", True)]}


def test_a_fact_unthinged_does_not_read_fails_prepare(tmp_path):
    uses = _module()
    with pytest.raises(AssertionError, match="frame for the verb v1"):
        uses.prepare(SimpleNamespace(repo=tmp_path), _world("frame for the verb v1"), _write, "c1", "ex.com/p/c")


@pytest.mark.parametrize("code, line", [("`order-by`", "ORDERED_RETURN"), ("`order-by-every`", "ORDERED_GIVE")])
def test_a_fact_unthinged_reads_writes_the_b298_line(tmp_path, code, line):
    uses = _module()
    assert uses.prepare(SimpleNamespace(repo=tmp_path), _world("frame of the verb v1", code), _write, "c1",
                        "ex.com/p/c")
    assert getattr(uses, line) in (tmp_path / "spec" / "capabilities" / "c1.md").read_text()
