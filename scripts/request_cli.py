"""The commands of `work` for the steps of a request's conversation on its issue (capability requests, r29-r33,
r39, r43, r44, r57, r58): `offer`, `fits`, `propose`, `accept`, `sync` and `watch`, their parsers, dispatch and what they print."""
import request_accept
import request_forward
import request_steps
import request_sync
import request_watch


def add_parsers(sub):
    p = sub.add_parser("offer", help="the upstream: answer an open request with what may serve it, posted")
    p.add_argument("request")
    p.add_argument("--capability", action="append", default=[], help="a capability that may serve it, quoted whole")
    p.add_argument("--note", help="the offer's words, before the capabilities and the glossary")
    p = sub.add_parser("fits", help="the asker: an offered capability serves the request; it is delivered, posted")
    p.add_argument("request")
    p.add_argument("--serves", action="append", default=[], help="a requirement id that serves it")
    p = sub.add_parser("propose", help="the asker: write lines into the request, in the upstream's terms")
    p.add_argument("request")
    p.add_argument("--line", action="append", default=[], dest="lines", help="one line; give it once a line")
    p = sub.add_parser("accept", help="the upstream's person: accept a request whose lines are settled, as an item")
    p.add_argument("request")
    sub.add_parser("sync", help="record what the other side of each request posted, and print every live request")
    p = sub.add_parser("watch", help="poll the requests' issues; print what `work sync` would take in, and exit")
    p.add_argument("--every", type=float, default=60, help="seconds between polls (default: 60)")
    p.add_argument("--polls", type=int, help="end, exit 1, after this many polls that find nothing (default: no end)")
    p.add_argument("--forward", action="store_true",
                   help="wake on GitHub's events (gh webhook forward), polling GitHub's notifications where it cannot;"
                        " --every is then the longest wait, --polls the waits")


def cmd_offer(args):
    request_steps.offer(args.root, args.request, args.capability, args.note)
    return 0


def cmd_fits(args):
    request_steps.fits(args.root, args.request, args.serves)
    return 0


def cmd_propose(args):
    request_steps.propose(args.root, args.request, args.lines)
    return 0


def cmd_accept(args):
    import backlog_items
    item = request_accept.accept(args.root, args.request)
    print("%s shaped" % backlog_items.label(item))
    return 0


def cmd_sync(args):
    return request_sync.sync(args.root)


def cmd_watch(args):
    try:
        if args.forward:
            return request_forward.forward(args.root, args.every, args.polls)
        return request_watch.watch(args.root, args.every, args.polls)
    except KeyboardInterrupt:
        return 130


COMMANDS = {"offer": cmd_offer, "fits": cmd_fits, "propose": cmd_propose, "accept": cmd_accept, "sync": cmd_sync,
            "watch": cmd_watch}
