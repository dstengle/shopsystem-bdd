"""batch_summary (b580): the batch summary form and the summary of measure batch's figures."""
import batch_summary

FIGURES = {"cost": 12.3456, "tokens": {"output_tokens": 10, "new_input_tokens": 20, "cache_read_tokens": 30},
           "wall_time": "2 h 5 min", "opening_time": "1 min 2 s",
           "window": {"started": "2026-11-25T10:00:00+00:00", "first_review": "2026-11-25T11:30:00+00:00",
                      "built": "2026-11-25T12:00:00+00:00", "closed": "2026-11-25T12:05:00+00:00"},
           "test_runs": [{"kind": "done", "task": "t1", "passed": True, "seconds": 61},
                         {"kind": "review", "task": None, "passed": True, "seconds": 120}]}


def test_the_form_names_each_figure_in_order():
    assert [line.split(":")[0] for line in batch_summary.form()] == ["- %s" % n for n in batch_summary.NAMES]


def test_the_summary_states_cost_tokens_and_times():
    said = dict(batch_summary.values(FIGURES))
    assert said["cost"] == "$12.35"
    assert (said["output tokens"], said["new input tokens"], said["cache-read tokens"]) == (10, 20, 30)
    assert said["wall time"] == "2 h 5 min" and said["opening time"] == "1 min 2 s"
    assert said["building time"] != batch_summary.UNKNOWN and said["review time"] != batch_summary.UNKNOWN
    assert said["test runs"].startswith("2: done t1 ") and ", review " in said["test runs"]


def test_a_figure_no_record_gives_is_unknown():
    said = dict(batch_summary.values({}))
    assert said["cost"] == said["building time"] == said["output tokens"] == batch_summary.UNKNOWN
    assert said["test runs"] == "none"
