"""The payments service's command line, a stand-in for the example: its argparse only, which spec check reads."""
import argparse


def main(argv=None):
    top = argparse.ArgumentParser(prog="payments")
    top.add_argument("--root")
    top.add_argument("--json", action="store_true")
    sub = top.add_subparsers(dest="command", required=True)
    p = sub.add_parser("authorise")
    p.add_argument("card")
    p.add_argument("--amount")
    p.add_argument("--currency")
    p.add_argument("--reference")
    p = sub.add_parser("capture")
    p.add_argument("authorisation")
    p = sub.add_parser("void")
    p.add_argument("authorisation")
    p = sub.add_parser("settle")
    p.add_argument("authorisation")
    p = sub.add_parser("reverse")
    p.add_argument("authorisation")
    p = sub.add_parser("disburse")
    p.add_argument("payout")
    p = sub.add_parser("contest")
    p.add_argument("authorisation")
    p = sub.add_parser("resolve")
    p.add_argument("dispute")
    return top.parse_args(argv)


if __name__ == "__main__":
    main()
