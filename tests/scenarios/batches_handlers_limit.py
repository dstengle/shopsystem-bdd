"""The review limit in batches' pick (r93, r94, b483): an item ranked after the world's own ready item (`i92`, which
`work batch start` picks first whatever its estimate), so the pick took one item before it. It exceeds the review
limit when `.shop/delivery.toml` sets the review's size (`[review] size`) to 1, which the first item's estimate alone
passes; it does not under the default limit, whose 1000 lines hold both items' estimates. Its line has a trigger of its
own (`OWN`), so v15n never leaves it out beside the world's item and the limit alone decides; an item an earlier Given
gave lines (one that does not meet the bar, r130) keeps them."""
import sys

W, B, T, F = (sys.modules[n] for n in ("shop_work_queue_world", "shop_backlog_world", "shop_batches_world",
                                       "shop_world_four"))
four, parts = F.four, F.parts
LOW = {"value": "low-value", "urgency": "low-urgency"}      # a score below the world's own item's
OWN = "When the person runs `work check`, `work` shall exit successfully."     # no trigger of the world's own item


@four("GivenDoes", "exceed", "batches")
@four("GivenDoesNot", "exceed", "batches")
def exceeds(step):
    (k1, n1), = parts(step)[:1]
    if k1 != "item" or step.nps != ["the review limit"]:
        return False
    B.write_item(step, n1, **LOW)
    if "Requirements" not in step.context["item_fields"][n1].get("sections", {}):   # lines a Given gave kept (r130)
        sys.modules["shop_readiness_world"].give_lines(step, n1, OWN)
    if step.template == "GivenDoes":
        step.context["delivery"] = step.context.get("delivery", T.DELIVERY) + "\n[review]\nsize = 1\n"
