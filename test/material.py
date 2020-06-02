
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MATERIALS TEST
"""

__author__ = "Davide Pellegrino"
__date__ = "2020-06-01"

import logging

from sapgw.material.core import Material

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)

class testMaterial():
    """ test class """
    def __init__(self, profile_name=None):
        self.m = Material(profile_name)

    def fullMaterial(self, material_id:str):
        """ test ana + class """
        mana = self.m.getMaterialAna(material_id)
        print(mana)
        mcls = self.m.getMaterialClass(material_id)
        print(mcls)
        return
    
    def stock(self, material_id):
        """ test stock """
        mstock = self.m.getMaterialStock(material_id)
        print(mstock)
        return

def main(args):
    """ main test """
    material_id=args.material
    logger.info(f'Init main test {material_id}')

    ts=testMaterial(args.profile_name)
    ts.fullMaterial(material_id)
    ts.stock(material_id)
    return

def parse_args():
    """Parse the args from main."""
    import argparse
    parser = argparse.ArgumentParser(description='Test SAP GW Material')
    parser.add_argument('--material',type=int, help='SAP Material ID', required=True)
    parser.add_argument('--profile', type=str, help='Use specific profile env')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    main(args)
