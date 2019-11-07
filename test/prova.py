
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MATERIALS SDK
"""

__author__ = "Davide Pellegrino"
__version__ = "2.1.12"
__date__ = "2019-11-07"

import logging
from sapgw.material.core import Material

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

def test():
    """ test Material class."""
    # import argparse
    logger.debug('Init test')
    material = Material(profile_name='default')
    material.material_id = 2305278
    mana = material.getMaterialAna()
    logger.info(mana)
    mclass = material.getMaterialClass()
    logger.info(mclass)

if __name__ == '__main__':
    """ Do Test """  
    test()