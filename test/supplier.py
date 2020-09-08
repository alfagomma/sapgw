
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SUPPLIER TEST
"""

__author__ = "Davide Pellegrino"
__date__ = "2020-06-01"

import logging

from sapgw.supplier.core import Supplier

class test():
    """ test class """
    def __init__(self, profile_name=None):
        logging.debug('Init test')
        self.s = Supplier(profile_name)

    def ana(self):
        """ test ana """
        sana = self.s.getSupplier(50000003)
        logging.info(sana)
        return True
        

def main(args):
    """ start testing """
    logging.basicConfig(level=logging.INFO)
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    logging.debug(f'Init {__file__}')
    t = test(profile_name=args.profile)
    for atr in args.test:
        if hasattr(t, atr):getattr(t, atr)()
    return
    
def parse_args():
    """Parse the args from main."""
    import argparse
    parser = argparse.ArgumentParser(description='Testing support')
    parser.add_argument("--profile", type=str, help='Use specific profile env')
    parser.add_argument("-t", "--test", nargs='+', help='What can I do for you?', required=True)
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    main(args)