
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CUSTOMER TEST
"""

__author__ = "Davide Pellegrino"
__date__ = "2019-12-13"

import logging
from sapgw.customer.core import Customer

class test():
    """ test customer """

    def __init__(self, profile_name=None):
        """ init test """
        logging.debug('Init test')
        self.c=Customer(profile_name)

    def ana(self, customer_id:str):
        """test customer ana"""
        logging.debug(f'test ana {customer_id}')
        cana=self.c.getCustomerAna(customer_id)
        logging.info(cana)
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