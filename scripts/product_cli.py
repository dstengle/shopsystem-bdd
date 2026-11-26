"""`spec product <id> --purpose <text>`, `spec actor <product actor>` and `spec job <id> [--actor <a> ...] --statement
<text> [--needs <j> ...]` (b602, product r1-r7): the product service's operations declare, declare actor and declare
job requested on the command line, each product_layer's over the product product_store keeps, committed, and what is
kept printed. A refusal names the parameter, which the CLI adapter spells as its option (`--statement`, `--actor`,
`--needs`: their dests are the parameters' names)."""
import product_layer
import product_store


def cmd_product(args):
    product = product_layer.declare(product_store.read(args.root), args.id, args.purpose)
    product_store.kept(args.root, product, "spec product: %s" % args.id)
    print("declared the product %s" % args.id)
    return 0


def cmd_actor(args):
    product = product_layer.declare_actor(product_store.read(args.root), args.product_actor)
    product_store.kept(args.root, product, "spec actor: %s" % args.product_actor)
    print("declared the product actor %s" % args.product_actor)
    return 0


def cmd_job(args):
    product = product_layer.declare_job(product_store.read(args.root), args.id, args.product_actor or [],
                                        args.job_statement, args.need or [])
    product_store.kept(args.root, product, "spec job: %s" % args.id)
    print("declared the job %s" % args.id)
    return 0


def add_parsers(sub):
    p = sub.add_parser("product", help="declare the product this bounded context belongs to: its id and purpose")
    p.add_argument("id", help="the product's id, as missingmass.io/shopsystem")
    p.add_argument("--purpose", required=True, help="what the product is for, one sentence")
    a = sub.add_parser("actor", help="declare an actor of the product, one it serves")
    a.add_argument("product_actor", metavar="actor", help="the actor, as 'the developer'")
    j = sub.add_parser("job", help="declare a job to be done of the product, or declare it again")
    j.add_argument("id", help="the job's id")
    j.add_argument("--actor", dest="product_actor", action="append", help="an actor of the product the job is for")
    j.add_argument("--statement", dest="job_statement", required=True,
                   help="the job statement: When <situation>, <actor> wants <motivation>, so they can <outcome>.")
    j.add_argument("--needs", dest="need", action="append", help="a job of the product this job needs done first")


COMMANDS = {"product": cmd_product, "actor": cmd_actor, "job": cmd_job}
