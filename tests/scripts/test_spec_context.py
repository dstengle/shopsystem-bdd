"""spec_context: a context read once per state of its files, on the logic check's cluster (grammar 4, codified-2),
never the live spec."""
import os
import pathlib
import shutil
import sys

import spec_context
import spec_logic_vocab

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import toolchain

CLUSTER = pathlib.Path(__file__).resolve().parent / "fixtures" / "logic" / "cluster"


def test_the_context_is_read_once_per_state_of_its_files(tmp_path):
    toolchain.require()
    shutil.copytree(CLUSTER, tmp_path / "c")
    root = tmp_path / "c"
    ctx = spec_context.load(root)
    assert spec_context.load(root) is ctx
    assert [s.id for s in ctx.statements][:2] == ["supervision#r1", "supervision#r2"]
    assert ctx.statements[-1] == spec_context.Statement("U1", None, None, ctx.statements[-1].tree)
    assert ctx.statements[0].group == "supervision#g1" and ctx.statements[0].capability == "supervision"
    assert ctx.facts["supervision#r11"][0] == 'form("supervision#r11",when).'
    assert ctx.refused == {} and ctx.domain[:len(spec_logic_vocab.domain(ctx.vocab))] == spec_logic_vocab.domain(
        ctx.vocab)
    cap = root / "spec" / "capabilities" / "supervision.md"
    cap.write_text(cap.read_text().replace("- [r12] When", "- [r12] Whenever"))
    os.utime(cap, ns=(cap.stat().st_mtime_ns + 10**9,) * 2)
    again = spec_context.load(root)
    assert again is not ctx and "supervision#r12" in again.refused and "supervision#r12" not in again.facts
    draft = tmp_path / "supervision.md"
    draft.write_text(cap.read_text().replace("- [r12] Whenever", "- [r12] When").replace(
        "shall not set the status of the initiative to `started`.",
        "shall set the status of the initiative to `done`."))
    drafted = spec_context.load(root, [draft])
    assert drafted.refused == {} and drafted.caps["supervision"].path == draft
    assert 'set("supervision#r12",1,x3,t_status,v_done).' in drafted.facts["supervision#r12"]
    assert spec_context.load(root, [draft]) is drafted
