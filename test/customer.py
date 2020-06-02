
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CUSTOMER TEST
"""

__author__ = "Davide Pellegrino"
__date__ = "2019-12-13"

import logging
from sapgw.customer.core import Customer

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)

class testCustomer():
    """ test customer """

    def __init__(self, profile_name=None):
        """ init test """
        self.c=Customer(profile_name)

    def ana(self, customer_id:str):
        """test customer ana"""
        cana=self.c.getCustomerAna(customer_id)
        print(cana)
        return


def main(args):
    """ main test """
    logger.info(f'Init main')
    customer_id=args.customer

    tc = testCustomer(profile_name=args.profile)
    tc.ana(customer_id)
    return

def parse_args():
    """Parse the args from main."""
    import argparse
    parser = argparse.ArgumentParser(description='Test SAP GW Customer')
    parser.add_argument('--customer',type=int, help='SAP Customer ID', required=True)
    parser.add_argument('--profile', type=str, help='Use specific profile env')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    main(args)