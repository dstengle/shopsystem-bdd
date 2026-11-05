"""The price of a request (capability telemetry; workflow simplification plan 7, D5): a dated table of each model's
input, output and cache-read price in dollars per million tokens, `.shop/delivery.toml`'s `[prices."<model>"]` over
it, cache writes priced by their time to live. A transcript carries tokens and the model, never dollars: a request of
a model with no price costs None and is named, never guessed (0018). Standard library only."""
import batch_git
from measure_read import Refused, number
from workqueue import Refused as WorkRefused

AS_OF = "2026-10-06"
PRICES = {
    "claude-opus-5-5": (4.0, 20.0, 0.20), "claude-opus-5": (5.0, 25.0, 0.50), "claude-opus-4": (5.0, 25.0, 0.50),
    "claude-sonnet-5-5": (2.0, 10.0, 0.20), "claude-sonnet-5": (2.0, 10.0, 0.20), "claude-sonnet-4": (3.0, 15.0, 0.30),
    "claude-haiku-5-5": (0.10, 0.50, 0.01), "claude-haiku-4": (1.0, 5.0, 0.10),
    "claude-fable-5-1": (10.0, 50.0, 0.25), "claude-fable-5": (10.0, 50.0, 1.00),
}
WRITE_5M = 1.25
WRITE_1H = 2.0
FIELDS = ("input", "output", "cache_read")
TOKENS = ("input_tokens", "cache_write_5m_tokens", "cache_write_1h_tokens", "cache_read_tokens", "output_tokens")


def prices(root):
    """PRICES with `.shop/delivery.toml`'s `[prices."<model>"]` over it: each a table of `input`, `output` and
    `cache_read`, numbers of 0 or more, all three and nothing else; anything else is refused, naming the key."""
    try:
        given = batch_git.delivery(root).get("prices", {})
    except WorkRefused as why:
        raise Refused(str(why)) from None
    if not isinstance(given, dict):
        raise Refused(".shop/delivery.toml: prices is not a table of models")
    table = dict(PRICES)
    for model, entry in given.items():
        where = ".shop/delivery.toml: prices.%s" % model
        if not isinstance(entry, dict) or set(entry) != set(FIELDS):
            raise Refused("%s is not a table of exactly %s" % (where, ", ".join(FIELDS)))
        for key in FIELDS:
            if not number(entry[key]) or entry[key] < 0:
                raise Refused("%s.%s %r is not a number of 0 or more" % (where, key, entry[key]))
        table[model] = tuple(float(entry[k]) for k in FIELDS)
    return table


def price_of(model, table):
    """The price of `model`: that of the longest key it starts with (a dated id still matches), or None."""
    keys = [k for k in table if model and model.startswith(k)]
    return table[max(keys, key=len)] if keys else None


def cost(request, table):
    """The request's cost in dollars, unrounded: 0 for a request with no tokens, whatever its model; None for one of a
    model with no price."""
    if not any(getattr(request, k) for k in TOKENS):
        return 0.0
    price = price_of(request.model, table)
    if price is None:
        return None
    given, out, read = price
    return (request.input_tokens * given + request.cache_write_5m_tokens * given * WRITE_5M
            + request.cache_write_1h_tokens * given * WRITE_1H + request.cache_read_tokens * read
            + request.output_tokens * out) / 1_000_000
