
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
INVOICE TEST
"""

__author__ = "Davide Pellegrino"
__date__ = "2020-06-01"

import logging

from sapgw.invoice.core import Invoice


def main(args):
    """ start testing """
    logging.basicConfig(level=logging.WARNING)
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    logging.debug(f'Init {__file__}')
    m = Invoice(args.profile)
    logging.debug(f'Get invoice ...')
    print(m.getInvoice(args.number))
    logging.debug(f'Init {__file__}')
    print(m.getInvoiceHeader(args.number))
    logging.debug(f'Init {__file__}')
    print(m.getInvoiceBody(args.number))

    return True


def parse_args():
    """Parse the args from main."""
    import argparse
    parser = argparse.ArgumentParser(description='Testing support')
    parser.add_argument("--number", type=str,
                        help='Invoice number', required=True)
    parser.add_argument("--profile", type=str, help='Use specific profile env')
    parser.add_argument("-opt", "--option", help='Test option')
    parser.add_argument("-v", "--verbose",
                        help="increase output verbosity", action="store_true")
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(args)
