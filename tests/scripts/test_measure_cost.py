"""The price of a request (telemetry, plan 7 D5): by its model's longest key, cache writes by their time to live, zero
usage free, an unpriced model never guessed, and `.shop/delivery.toml`'s `[prices]` over the table."""
from types import SimpleNamespace

import backlog_testing  # noqa: F401  (the scripts directory on the path)
import measure_cost
import pytest
from measure_read import Refused

M = 1_000_000


def request(model="claude-opus-5-5", **tokens):
    kinds = ("input_tokens", "cache_write_5m_tokens", "cache_write_1h_tokens", "cache_read_tokens", "output_tokens")
    return SimpleNamespace(model=model, **{k: tokens.get(k, 0) for k in kinds})


def test_a_request_is_priced_by_its_model():
    assert measure_cost.cost(request(output_tokens=M), measure_cost.PRICES) == pytest.approx(20.0)
    assert measure_cost.cost(request(input_tokens=M), measure_cost.PRICES) == pytest.approx(4.0)


def test_a_dated_model_takes_the_longest_key():
    table = measure_cost.PRICES
    assert measure_cost.price_of("claude-opus-5-5-20261001", table) == table["claude-opus-5-5"]
    assert measure_cost.price_of("claude-opus-5-1", table) == table["claude-opus-5"]


def test_one_hour_cache_writes_cost_twice_the_input():
    """Review Focus 2."""
    assert measure_cost.cost(request(cache_write_1h_tokens=M), measure_cost.PRICES) == pytest.approx(8.0)
    assert measure_cost.cost(request(cache_write_5m_tokens=M), measure_cost.PRICES) == pytest.approx(5.0)


def test_zero_usage_costs_nothing():
    """Review Focus 2."""
    assert measure_cost.cost(request(model="<synthetic>"), measure_cost.PRICES) == 0.0


def test_an_unpriced_model_is_named_not_guessed():
    """Review Focus 2."""
    assert measure_cost.cost(request(model="claude-new-9", output_tokens=5), measure_cost.PRICES) is None


def test_delivery_overrides_a_price(tmp_path):
    (tmp_path / ".shop").mkdir()
    toml = tmp_path / ".shop" / "delivery.toml"
    toml.write_text('[prices."claude-opus-5-5"]\ninput = 1\noutput = 2\ncache_read = 0.1\n')
    table = measure_cost.prices(tmp_path)
    assert measure_cost.cost(request(output_tokens=M), table) == pytest.approx(2.0)
    toml.write_text('[prices."claude-opus-5-5"]\ninput = "x"\noutput = 2\ncache_read = 0.1\n')
    with pytest.raises(Refused, match=r"prices\.claude-opus-5-5"):
        measure_cost.prices(tmp_path)


@pytest.mark.parametrize("model", ["claude-opus-4-20250514", "claude-opus-4-1-20250805", "claude-opus-4-5-20251101"])
def test_an_opus_4_the_table_states_no_price_for_is_unpriced(model):
    """Plan 7 review M3: the table (the claude-api skill's, 2026-10-06) prices Opus 4.6 to 4.8; an older Opus 4 is
    named, never priced by a guess."""
    assert measure_cost.price_of(model, measure_cost.PRICES) is None


def test_opus_4_6_to_4_8_are_priced():
    for model in ("claude-opus-4-6", "claude-opus-4-7", "claude-opus-4-8"):
        assert measure_cost.price_of(model, measure_cost.PRICES) == (5.0, 25.0, 0.50), model


def test_haiku_5_5_over_a_100k_prompt_takes_its_long_rate():
    """Plan 7 review M3: $0.50 / $2.50 when the prompt (new input, cache writes and reads) is over 100K tokens, cache
    reads 0.1 x input, as the claude-api skill gives it."""
    short = request("claude-haiku-5-5", input_tokens=40_000, cache_read_tokens=60_000, output_tokens=M)
    assert measure_cost.cost(short, measure_cost.PRICES) == pytest.approx((40_000 * 0.10 + 60_000 * 0.01) / M + 0.50)
    long = request("claude-haiku-5-5", input_tokens=40_000, cache_write_5m_tokens=1, cache_read_tokens=60_000,
                   output_tokens=M)
    want = (40_000 * 0.50 + 1 * 0.50 * 1.25 + 60_000 * 0.05) / M + 2.50
    assert measure_cost.cost(long, measure_cost.PRICES) == pytest.approx(want)
