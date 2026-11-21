"""The estimate of an item's change and the review limit (batches r93, r94, b483): `work batch start`'s pick stops
before the estimates of the items it took pass the number of changed lines a pull request review reads in one
batch's change (`[review] size` of `.shop/delivery.toml`, else batch_brief's 1000).

An item's estimate is in changed lines: a share for its size rating, and one for each requirement line, universal
condition and model line or vocabulary entry it holds (the code, tests and spec each brings). An item exceeds the
review limit when its estimate, added to those of the items the pick took before it, is more than the limit and the
pick took one item or more before it: the first item is taken whatever its estimate, so a pick is never empty."""
import backlog_items
import backlog_lines
from batch_brief import SIZE as REVIEW
from batch_git import delivery

RATING = {"small": 150, "medium": 300, "large": 600}
UNRATED = RATING["medium"]
LINE = 50           # a requirement line or a universal condition: its handler, its code and its scenario
MODEL = 5           # a model line or a vocabulary entry


def limit(root):
    """The review limit: `[review] size` of `.shop/delivery.toml`, else REVIEW."""
    return delivery(root).get("review", {}).get("size", REVIEW)


def estimate(item):
    """The estimate of the item's change, in changed lines."""
    blocks = backlog_lines.read(item, backlog_items.rel_of(item.name))
    lines = sum(len(g.requirements) for b in blocks for g in b.groups) + len(blocks.universal)
    model = sum(len(m.lines) + len(m.terms) for m in blocks.models)
    return RATING.get(item.size, UNRATED) + LINE * lines + MODEL * model


def exceeds(spent, item, taken, review_limit):
    """Whether the item exceeds the review limit after the pick took `taken` items estimated at `spent` in all."""
    return taken > 0 and spent + estimate(item) > review_limit


def reason(spent, item, review_limit):
    return "exceeds the review limit: an estimate of %d changed lines after the %d taken passes %d" % (
        estimate(item), spent, review_limit)
