
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CUSTOMER TEST
"""

__author__ = "Davide Pellegrino"
__version__ = "1.1.1"
__date__ = "2019-12-13"

import logging
from sapgw.customer.core import Customer

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)

def main(args):
    """ main test """
    logger.info(f'Init main')
    m = Customer(profile_name=args.profile)
    cust_ana = m.getCustomerAna(args.customer)
    logger.info(cust_ana)
    return

def parse_args():
    """Parse the args from main."""
    import argparse
    parser = argparse.ArgumentParser(description='Test SAP GW Customer')
    parser.add_argument('--customer',type=int, help='SAP Customer ID', required=True)
    parser.add_argument('--cache', help='Use cached data', action='store_true')
    parser.add_argument('--profile', type=str, help='Use specific profile env')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    main(args)