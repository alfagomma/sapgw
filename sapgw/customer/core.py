
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
    SAPGW Customer functions.
    """
    cache = False
    
    def __init__(self, profile_name, use_cache=False):
        """
        Init Material class.
        """
        logger.info(f'Init Material SDK use cache {use_cache}...')
        self.s = Session(profile_name)
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
        rq = f"{self.s.host}/ZCUSTOMER_GETDETAIL_SU_SRV/zcustomer_general_dataSet('{customer_id}')"
        if self.cache:
            cachekey = rq+str(json.dumps(payload))
            data = self.cache.read(cachekey)
            if data:
                return data
        r = self.s.agent.get(rq, params=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        customer_ana = r.text
        if self.cache:
            self.cache.create(cachekey, customer_ana)
        return customer_ana

    def createCustomerAna(self, payload):
        """
        Create new customer.
        """
        logger.info(f'Creating new customer...')
        rq = f"{self.s.host}/ZCUSTOMER_MAINTAIN_SRV/zcustomer_maintain_entity_set')"
        token = self.s.getCsrfToken()
        headers = {'X-CSRF-Token': token}
        r = self.s.agent.post(rq, json=payload, headers=headers)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        customer_ana = r.text
        return customer_ana        
