
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CUSTOMER
"""

__author__ = "Davide Pellegrino"
__date__ = "2020-06-01"

import json
import logging
import time

from sapgw.session import Session, parseApiError

logger = logging.getLogger(__name__)

class Customer(object):
    """
    SAPGW Customers.
    """
   
    def __init__(self, profile_name=None):
        """
        Init Customer class.
        """
        logger.info('Init SAP Customer...')
        s = Session(profile_name)
        host = s.config.get('sapgw_host')
        self.host = host
        self.s = s            

    def getCustomerAna(self, customer_id:str):
        """
        Anagrafica cliente.
        """
        logger.info(f'Reading customer {customer_id} ana...')
        payload = {
            '$format' : 'json',
        }
        rq = f"{self.host}/ZCUSTOMER_GETDETAIL_SU_SRV/zcustomer_general_dataSet('{customer_id}')"
        agent=self.s.getAgent()
        r = agent.get(rq, params=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        customer_ana = r.text
        return customer_ana

    def createCustomerAna(self, payload):
        """
        Create new customer.
        """
        logger.info(f'Creating new customer...')
        rq = f"{self.host}/ZCUSTOMER_MAINTAIN_SRV/zcustomer_maintain_entity_set')"
        agent=self.s.getAgent()
        r = agent.post(rq, json=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        customer_ana = r.text
        return customer_ana        
