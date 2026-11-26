"""`spec unassign <job> --from <bounded context>` and `spec drop job|actor|subdomain|context <it>` (b795, product
r45-r57): the product service's operations unassign, drop job, drop actor, drop subdomain and drop context requested
on the command line, product_drop's over the product product_store keeps, committed, and what was taken back printed; a drop that changes nothing commits nothing.
A refusal names the parameter, which the CLI adapter spells as its option or positional (the dests are the
parameters' names), or the job, the subdomain or the bounded context that still refers to what is dropped."""
import product_drop
import product_store

# `spec drop <what>`: the operation, its parameter's dest, and the words of what it drops
DROPS = {"job": (product_drop.drop_job, "job", "the job"),
         "actor": (product_drop.drop_actor, "product_actor", "the product actor"),
         "subdomain": (product_drop.drop_subdomain, "subdomain", "the subdomain"),
         "context": (product_drop.drop_context, "bounded_context", "the bounded context")}


def cmd_unassign(args):
    product = product_drop.unassign(product_store.read(args.root), args.job, args.bounded_context)
    product_store.kept(args.root, product, "spec unassign: %s from %s" % (args.job, args.bounded_context))
    print("unassigned the job %s from the bounded context %s" % (args.job, args.bounded_context))
    return 0


def cmd_drop(args):
    drop, dest, words = DROPS[args.what]
    ident = getattr(args, dest)
    product = product_store.read(args.root)
    dropped = drop(product, ident)
    if dropped != product:
        product_store.kept(args.root, dropped, "spec drop %s: %s" % (args.what, ident))
    print("dropped %s %s" % (words, ident))
    return 0


def add_parsers(sub):
    u = sub.add_parser("unassign", help="take a job back from the bounded context it is assigned to")
    u.add_argument("job", help="the job's id")
    u.add_argument("--from", dest="bounded_context", required=True, help="the bounded context's id")
    d = sub.add_parser("drop", help="take a job, a product actor, a subdomain or a bounded context out of the product")
    what = d.add_subparsers(dest="what", required=True)
    what.add_parser("job", help="drop a job no job needs, no bounded context holds and no subdomain serves") \
        .add_argument("job", help="the job's id")
    what.add_parser("actor", help="drop a product actor no job has and no bounded context maps") \
        .add_argument("product_actor", metavar="product_actor", help="the product actor, as 'the developer'")
    what.add_parser("subdomain", help="drop a subdomain no bounded context addresses") \
        .add_argument("subdomain", help="the subdomain's id")
    what.add_parser("context", help="drop a bounded context that holds no job") \
        .add_argument("bounded_context", metavar="bounded_context", help="the bounded context's id")


COMMANDS = {"unassign": cmd_unassign, "drop": cmd_drop}
