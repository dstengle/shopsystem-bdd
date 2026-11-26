"""`spec product <id> --purpose <text>`, `spec actor <product actor>` and `spec job <id> [--actor <a> ...] --statement
<text> [--needs <j> ...]` (b602, product r1-r7), `spec subdomain <id> --type <t> [--serves <j> ...]` and `spec context
<id> [--addresses <s> ...] [--shop <shop>]` (b642, product r15-r21): the product service's operations declare,
declare actor, declare job, declare subdomain and declare context requested on the command line, each product_layer's
or product_map's over the product product_store keeps, committed, and what is kept printed. A refusal names the parameter, which the CLI adapter spells as its option (`--statement`, `--actor`,
`--needs`, `--type`, `--serves`, `--addresses`: their dests are the parameters' names)."""
import product_layer
import product_map
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


def cmd_subdomain(args):
    product = product_map.declare_subdomain(product_store.read(args.root), args.id, args.subdomain_type,
                                            args.job or [])
    product_store.kept(args.root, product, "spec subdomain: %s" % args.id)
    print("declared the subdomain %s" % args.id)
    return 0


def cmd_context(args):
    product = product_map.declare_context(product_store.read(args.root), args.id, args.subdomain or [], args.shop)
    product_store.kept(args.root, product, "spec context: %s" % args.id)
    print("declared the bounded context %s%s" % (args.id, " kept by %s" % args.shop if args.shop else
                                                 ", a third-party provider"))
    return 0


def add_parsers(sub):
    p = sub.add_parser("product", help="declare the product this bounded context belongs to: its id and purpose")
    p.add_argument("id", help="the product's id, as missingmass.io/shopsystem")
    p.add_argument("--purpose", required=True, metavar="<text>", help="what the product is for, one sentence")
    a = sub.add_parser("actor", help="declare an actor of the product, one it serves")
    a.add_argument("product_actor", metavar="actor", help="the actor, as 'the developer'")
    j = sub.add_parser("job", help="declare a job to be done of the product, or declare it again")
    j.add_argument("id", help="the job's id")
    j.add_argument("--actor", dest="product_actor", action="append", metavar="<actor>",
                   help="an actor of the product the job is for")
    j.add_argument("--statement", dest="job_statement", required=True, metavar="<text>",
                   help="the job statement: When <situation>, <actor> wants <motivation>, so they can <outcome>.")
    j.add_argument("--needs", dest="need", action="append", metavar="<job>",
                   help="a job of the product this job needs done first")

    s = sub.add_parser("subdomain", help="declare a subdomain of the product with its type and the jobs it serves")
    s.add_argument("id", help="the subdomain's id, as specification")
    s.add_argument("--type", dest="subdomain_type", required=True, metavar="<type>",
                   help="the subdomain type: core, supporting or generic")
    s.add_argument("--serves", dest="job", action="append", metavar="<job>",
                   help="a job of the product the subdomain serves")
    c = sub.add_parser("context", help="declare a bounded context of the product's domain map")
    c.add_argument("id", help="the bounded context's id, under the product's id")
    c.add_argument("--addresses", dest="subdomain", action="append", metavar="<subdomain>",
                   help="a subdomain of the product it addresses")
    c.add_argument("--shop", metavar="<shop>", help="the shop that keeps it; none for a third-party provider")


COMMANDS = {"product": cmd_product, "actor": cmd_actor, "job": cmd_job, "subdomain": cmd_subdomain,
            "context": cmd_context}
