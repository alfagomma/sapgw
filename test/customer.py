
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CUSTOMER TEST
"""

__author__ = "Davide Pellegrino"
__date__ = "2019-12-13"

import logging
from sapgw.customer.core import Customer


def testCreatenew(profile_name):
    logging.debug('Creating new customer')
    c = Customer(profile_name)
    data = {
        "cid": "15",
        "account_group": "CUST",
        "name": "DAPE S.R.L.",
        "channel": "MIS",
        "tax_code": "00716950670",
        "tax_code_2": "",
        "phone": "",
        "phone2": "",
        "website": "dape.it",
        "area1": "",
        "area3": "",
        "postalcode": "64022",
        "region": "TE",
        "address": "VIA FILETTO",
        "street_number": "55/A",
        "locality": "GIULIANOVA",
        "country": "IT",
        "short_address": ""
    }
    newcust = c.createCustomerAna(data)
    logging.info(newcust)
    return True


def testCustomer(profile_name, customer_id: str):
    logging.debug(f'test ana {customer_id}')
    c = Customer(profile_name)
    cana = c.getCustomerAna(customer_id)
    logging.info(cana)
    return True


def main(args):
    """ start testing """
    logging.basicConfig(level=logging.INFO)
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    logging.debug(f'Init {__file__}')
    testCustomer(args.profile, args.customer)

    return


def parse_args():
    """Parse the args from main."""
    import argparse
    parser = argparse.ArgumentParser(description='Testing support')
    parser.add_argument("--profile", type=str, help='Use specific profile env')
    parser.add_argument("-c", "--customer", type=str,
                        help='Customer id', required=True)
    parser.add_argument("-v", "--verbose",
                        help="increase output verbosity", action="store_true")
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(args)
