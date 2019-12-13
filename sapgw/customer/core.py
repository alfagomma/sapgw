
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CUSTOMER SDK
"""

__author__ = "Davide Pellegrino"
__date__ = "2019-12-04"

import json
import logging
import time

from sapgw.session import Session, parseApiError
from sapgw.utility.cache import Cache as cachemodule

logger = logging.getLogger()
class Customer(object):
    """
    SAPGW Customers.
    """
    cache = False
    
    def __init__(self, profile_name=False, use_cache=False):
        """
        Init Material class.
        """
        logger.info(f'Init Material SDK use cache {use_cache}...')
        s = Session(profile_name)
        self.sapHost = s.getSapHost()
        self.sapAgent = s.create()
        if use_cache:
            self.cache = cachemodule()

    def getCustomerAna(self, customer_id):
        """
        Anagrafica cliente.
        """
        logger.info(f'Reading customer {customer_id} ana...')
        payload = {
            '$format' : 'json',
        }
        rq = f"{self.sapHost}/ZCUSTOMER_GETDETAIL_SU_SRV/zcustomer_general_dataSet('{customer_id}')"
        if self.cache:
            cachekey = rq+str(json.dumps(payload))
            data = self.cache.read(cachekey)
            if data:
                return data
        r = self.sapAgent.get(rq, params=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        customer_ana = r.text
        if self.cache:
            self.cache.create(cachekey, customer_ana)
        return customer_ana
