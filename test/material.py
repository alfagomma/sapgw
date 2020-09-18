
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MATERIALS TEST
"""

__author__ = "Davide Pellegrino"
__date__ = "2020-06-01"

import logging

from sapgw.material.core import Material


def main(args):
    """ start testing """
    logging.basicConfig(level=logging.INFO)
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    logging.debug(f'Init {__file__}')

    m = Material(args.profile)
    mana = m.getMaterialAna(args.material)
    if 200 != mana.status_code:
        print()
    print(type(mana.json()), type(mana.text))
    #
    # mcls = m.getMaterialClass(args.material)
    # print(mcls)
    # mstock = m.getMaterialStock(args.material)
    # print(mstock)
    return


def parse_args():
    """Parse the args from main."""
    import argparse
    parser = argparse.ArgumentParser(description='Testing support')
    parser.add_argument("--material", type=str,
                        help='Material id', required=True)
    parser.add_argument("--profile", type=str, help='Use specific profile env')
    parser.add_argument("-opt", "--option", help='Test option')
    parser.add_argument("-v", "--verbose",
                        help="increase output verbosity", action="store_true")
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(args)
