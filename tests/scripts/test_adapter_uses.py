"""adapter_uses (b637): an adapter spec's `uses:` read, the provider operations a held contract declares, and the
port operations it realises; the scenarios of checking r135, r136 drive the failing checks and product r35 the trace,
these the cases that pass."""
import adapter_uses

PROVIDER = "bounded-context/example.org/fixture/inventory"
INDEX = """---
id: bounded-context/example.org/fixture/domain-model/adapter/stock-inventory
kind: adapter
realises: [stock-port#r1]
providers: [%s@1.2.0]
uses:
%s---

# stock over inventory
"""
CONTRACT = """context = "%s"
version = "1.2.0"

[operations."inventory.hold"]
requirements = ["holding#r1: When a client holds an item, the inventory service shall complete the request."]

[operations."inventory.release"]
""" % PROVIDER


def spec(tmp_path, monkeypatch, *uses):
    root = tmp_path / "adapters" / "stock-inventory"
    (root / "spec").mkdir(parents=True)
    (root / "spec" / "index.md").write_text(INDEX % (PROVIDER, "".join("  - %s\n" % u for u in uses)))
    kept = root / "provider" / "example.org" / "fixture" / "inventory" / "1.2.0"
    kept.mkdir(parents=True)
    (kept / "contract.toml").write_text(CONTRACT)
    monkeypatch.setattr(adapter_uses, "realised", lambda *_, **__: {"stock.reserve": ["stock-port#r1"]})
    return root


def test_a_port_operation_that_uses_a_held_provider_operation_passes(tmp_path, monkeypatch):
    root = spec(tmp_path, monkeypatch, "stock.reserve → inventory.hold")
    assert adapter_uses.problems(root) == []


def test_a_port_operation_may_use_several_provider_operations_named_by_their_provider(tmp_path, monkeypatch):
    root = spec(tmp_path, monkeypatch, "stock.reserve → inventory.hold of %s" % PROVIDER,
                "stock.reserve -> inventory.release")
    assert adapter_uses.entries(root) == ([("stock.reserve", "inventory.hold", PROVIDER),
                                           ("stock.reserve", "inventory.release", None)], [])
    assert adapter_uses.problems(root) == []


def test_an_operation_of_another_provider_is_not_declared(tmp_path, monkeypatch):
    root = spec(tmp_path, monkeypatch, "stock.reserve → inventory.hold of bounded-context/example.org/fixture/ledger")
    assert ["inventory.hold" in p for p in adapter_uses.problems(root)] == [True]


def test_an_entry_that_does_not_read_is_a_problem(tmp_path, monkeypatch):
    root = spec(tmp_path, monkeypatch, "stock.reserve → inventory.hold", "reserve with hold")
    assert [p for p in adapter_uses.problems(root) if "reserve with hold" in p]


def test_the_requirements_a_used_operation_s_contract_lists_are_followed(tmp_path, monkeypatch):
    root = spec(tmp_path, monkeypatch, "stock.reserve → inventory.hold", "stock.cancel → inventory.release")
    assert [g[0].split(":")[0] for g in adapter_uses.governed(root, "stock.reserve")] == ["holding#r1"]
    assert adapter_uses.governed(root, "stock.cancel") == []


def test_only_the_operations_a_realised_port_line_governs_are_realised(tmp_path, monkeypatch):
    root = tmp_path / "adapters" / "stock-inventory"
    (root / "spec").mkdir(parents=True)
    text = INDEX % (PROVIDER, "")
    (root / "spec" / "index.md").write_text(text.replace("[stock-port#r1]", "[stock-port#r1, notebook#r1]"))
    monkeypatch.setattr(adapter_uses, "_ported", lambda parent: {"stock-port"})
    governing = {"stock.reserve": [("stock-port#r1", "...")], "notes.add": [("notebook#r1", "...")],
                 "stock.cancel": [("stock-port#r2", "...")]}
    assert adapter_uses.realised(root, governing) == {"stock.reserve": ["stock-port#r1"]}
