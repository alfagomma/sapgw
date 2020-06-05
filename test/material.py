
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MATERIALS TEST
"""

__author__ = "Davide Pellegrino"
__date__ = "2020-06-01"

import logging

from sapgw.material.core import Material

class test():
    """ test class """
    def __init__(self, profile_name=None):
        logging.debug('Init test')
        self.m = Material(profile_name)

    def fullMaterial(self, material_id:str):
        """ test ana + class """
        logging.debug(f'test full material {material_id}')
        mana = self.m.getMaterialAna(material_id)
        logging.info(mana)
        mcls = self.m.getMaterialClass(material_id)
        logging.info(mcls)
        return True
    
    def stock(self, material_id):
        """ test stock """
        logging.debug(f'test stock {material_id}')
        mstock = self.m.getMaterialStock(material_id)
        logging.info(mstock)
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