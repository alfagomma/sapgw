
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MATERIALS TEST
"""

__author__ = "Davide Pellegrino"
__version__ = "2.1.12"
__date__ = "2019-11-07"

import logging
from sapgw.material.core import Material

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)

def main(args):
    """ main test """
    logger.info(f'Init main')
    m = Material(material_id=args.material, profile_name=args.profile)
    ma = m.getMaterialAna()
    logger.info(ma)
    mc = m.getMaterialClass()
    logger.info(mc)
    mc = m.getMaterialStock()
    logger.info(mc)    
    return

def parse_args():
    """Parse the args from main."""
    import argparse
    parser = argparse.ArgumentParser(description='Test SAP GW Material')
    parser.add_argument('--material',type=int, help='SAP Material ID', required=True)
    parser.add_argument('--cache', help='Use cached data', action='store_true')
    parser.add_argument('--profile', type=str, help='Use specific profile env')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    main(args)