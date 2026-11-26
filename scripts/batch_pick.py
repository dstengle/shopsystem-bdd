"""The pick of `work batch start` (capability batches r1-r3; workflow simplification plan 4, D7, D8): the `ready` items
in rank order, up to `batch_size` of `.shop/delivery.toml` (default 4), each checked again by the readiness bar,
alone and then laid over the items picked before it, its ids renumbered past its capability's and theirs; the first
item taken, laid over no item, checked once (b588).

An item is blocked unless each item it depends on is `delivered` or picked earlier in this pick; the pick goes over
the table again until a pass picks nothing more, so a dependency ranked lower is still picked first. An item that no
longer passes alone goes back to `shaped`, its reasons under `## Notes`; one that passes alone but not laid with the
picked is left out and stays `ready`, as is one that exceeds the review limit (batch_estimate, b483: checked before
the bar, so an item past it is left out with no run of the bar and stays `ready` whether it would pass or not, b640;
the pick goes on to the items after it, the first item taken whatever its estimate). Nothing is written: `batch_start` commits what the pick gives."""
import copy
from collections import namedtuple

import backlog_items
import backlog_lifecycle
import backlog_lines
import backlog_moves
import backlog_view
import batch_estimate
import readiness_bar
from batch_git import delivery

SIZE = 4
Pick = namedtuple("Pick", "picked returned left_out renumbered superseded", defaults=({}, ()))     # superseded: batch_start's (b741)


def batch_size(root):
    size = delivery(root).get("batch_size", SIZE)
    if not isinstance(size, int) or isinstance(size, bool) or size < 1:
        raise backlog_items.Refused(".shop/delivery.toml: batch_size %r is not a whole number above 0" % (size,))
    return size


def _blocked(item, by_name, picked):
    chosen = {i.name for i in picked}
    return any(d not in chosen and (by_name[d].status if d in by_name else "missing") != "delivered"
               for d in item.depends_on)


def _alone(root, item):
    """(the bar's reasons for the item alone, the copy checked, its renumbered pairs, the ids it took): its ids moved
    past the spec's only (a copy is checked, so an item whose ids a delivered batch took is not returned for them).
    With nothing picked before it, this is the check laid over the picked too, and the pick takes the copy (b588)."""
    alone, taken = copy.deepcopy(item), {}
    pairs = backlog_lines.renumber(root, alone, taken)
    return readiness_bar.check(root, alone)[0], alone, pairs, taken


def pick(root, size=None):
    """The Pick (D7): `picked` in pick order, renumbered (each with its `## Notes` line, and the pairs of this pick
    under its name in `renumbered`, plan 4 review M1); `returned` and `left_out` as (item, reasons), the returned set
    `shaped` with the note."""
    size = batch_size(root) if size is None else size
    everything = backlog_items.items(root)
    by_name = {i.name: i for i in everything}
    ready = next((its for state, its in backlog_view.ordered(everything) if state == "ready"), [])
    picked, returned, left_out, taken, done, renumbered = [], [], [], {}, set(), {}
    review_limit, spent = batch_estimate.limit(root), 0
    while len(picked) < size:
        before = len(done)
        for item in ready:
            if len(picked) >= size:
                break
            if item.name in done or _blocked(item, by_name, picked):
                continue
            done.add(item.name)
            if batch_estimate.exceeds(spent, item, len(picked), review_limit):   # before the bar (b640)
                left_out.append((item, [batch_estimate.reason(spent, item, review_limit)]))
                continue
            reasons, alone, alone_pairs, alone_taken = _alone(root, item)
            if reasons:
                backlog_lifecycle.reopen(item, "returned by work batch start: %s" % "; ".join(reasons))
                returned.append((item, reasons))
                continue
            if picked:
                trial, trial_taken = copy.deepcopy(item), copy.deepcopy(taken)
                pairs = backlog_lines.renumber(root, trial, trial_taken)
                reasons = readiness_bar.check(root, trial, picked)[0]
            else:           # laid over no item: the check alone, done once (b588)
                trial, trial_taken, pairs = alone, alone_taken, alone_pairs
            if reasons:
                left_out.append((item, reasons))
                continue
            if pairs:
                renumbered[trial.name] = pairs
                backlog_moves.add_note(trial, "renumbered by work batch start: %s" % ", ".join(
                    "%s -> %s" % pair for pair in pairs))
            taken = trial_taken
            picked.append(trial)
            spent += batch_estimate.estimate(trial)
        if len(done) == before:
            break
    return Pick(picked, returned, left_out, renumbered)
