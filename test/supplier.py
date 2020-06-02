
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SUPPLIER TEST
"""

__author__ = "Davide Pellegrino"
__date__ = "2020-06-01"

import logging

from sapgw.supplier.core import Supplier

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)

class testSupplier():
    """ test class """
    def __init__(self, profile_name=None):
        self.s = Supplier(profile_name)

    def ana(self, supplier_id:str):
        """ test ana """
        sana = self.s.getSupplier(supplier_id)
        print(sana)
        return
        

def main(args):
    """ main test """
    supplier_id=args.supplier
    logger.info(f'Init main test {supplier_id}')

    ts=testSupplier(args.profile_name)
    ts.ana(supplier_id)
    return

def parse_args():
    """Parse the args from main."""
    import argparse
    parser = argparse.ArgumentParser(description='Test SAP GW')
    parser.add_argument('--material',type=int, help='SAP Supplier ID', required=True)
    parser.add_argument('--profile', type=str, help='Use specific profile env')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    main(args)
