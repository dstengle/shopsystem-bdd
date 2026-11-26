"""readiness_bound (b721): the bound check's violations an item owns, by the operations its model lines declare or its
lines request, named with the operation or the outcome and the rule."""
import readiness_bound

LABELS = {"v_pb1": "an operation no core line requests", "v_pb2": "an outcome no line handles"}
FOUND = {("v_pb2", ("stock.reserve done",)), ("v_pb1", ("stock.count",)), ("v_pb2", ("other.do done",)),
         ("v_m4", ("stock.reserve",))}


def test_operations_declared_and_requested():
    facts = [("requester", ("capability/x/y/stock-port#r1", "stock.count", "the notes service")),
             ("asks", ("capability/x/y/notebook#r9", "other.do", "the notes service"))]
    ops = readiness_bound.operations({"stock": "service stock", "stock.reserve": "operation stock.reserve"}, facts,
                                     {"stock-port#r1"})
    assert ops == {"stock.reserve", "stock.count"}


def test_reasons_name_the_outcome_and_the_rule_of_owned_operations():
    reasons = readiness_bound.reasons(FOUND, {"stock.reserve", "stock.count"}, LABELS)
    assert reasons == ["the operation stock.count: v_pb1 an operation no core line requests",
                       "the operation outcome stock.reserve done: v_pb2 an outcome no line handles"]


def test_no_reason_of_an_operation_the_item_does_not_own():
    assert readiness_bound.reasons(FOUND, {"notes.add"}, LABELS) == []


def test_before_reads_the_readiness_bars_kept_result(tmp_path, monkeypatch):
    import readiness_before
    (tmp_path / "spec").mkdir()
    monkeypatch.setattr(readiness_before, "get", lambda copy, digest: (set(), FOUND))
    assert readiness_bound.before(tmp_path) == {v for v in FOUND if v[0] != "v_m4"}


def test_before_solves_the_tree_when_nothing_is_kept(tmp_path, monkeypatch):
    import model_check
    import model_facts
    import readiness_before
    (tmp_path / "spec").mkdir()
    monkeypatch.setattr(readiness_before, "get", lambda copy, digest: None)
    monkeypatch.setattr(model_facts.Model, "read", lambda self: self)
    monkeypatch.setattr(model_check, "solve", lambda model: ([("v_pb2", ["stock.reserve done"]), ("v_m4", ["x"])], {}))
    assert readiness_bound.before(tmp_path) == {("v_pb2", ("stock.reserve done",))}
