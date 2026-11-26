"""`spec assign <job> --to <bounded context>` and `spec plays <product actor> --in <bounded context> --as <actor>`
(b675, product r22-r25): the product service's operations assign and map requested on the command line, product_assign's
over the product product_store keeps, committed, and what is kept printed. A refusal names the parameter, which the CLI
adapter spells as its option or positional (the dests are the parameters' names)."""
import product_assign
import product_store


def cmd_assign(args):
    product = product_assign.assign(product_store.read(args.root), args.job, args.bounded_context)
    product_store.kept(args.root, product, "spec assign: %s to %s" % (args.job, args.bounded_context))
    print("assigned the job %s to the bounded context %s" % (args.job, args.bounded_context))
    return 0


def cmd_plays(args):
    product = product_assign.map_actor(product_store.read(args.root), args.product_actor, args.bounded_context,
                                       args.actor)
    product_store.kept(args.root, product, "spec plays: %s in %s" % (args.product_actor, args.bounded_context))
    print("mapped the product actor %s to %s in the bounded context %s" % (args.product_actor, args.actor,
                                                                           args.bounded_context))
    return 0


def add_parsers(sub):
    a = sub.add_parser("assign", help="assign a job of the product to the one bounded context that serves it")
    a.add_argument("job", help="the job's id")
    a.add_argument("--to", dest="bounded_context", required=True, help="the bounded context's id")
    p = sub.add_parser("plays", help="map a product actor to the actor a bounded context's model calls it by")
    p.add_argument("product_actor", metavar="product_actor", help="the product actor, as 'the developer'")
    p.add_argument("--in", dest="bounded_context", required=True, help="the bounded context's id")
    p.add_argument("--as", dest="actor", required=True, help="the actor of the bounded context, as 'the person'")


COMMANDS = {"assign": cmd_assign, "plays": cmd_plays}
