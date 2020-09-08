
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SUPPLIER
"""

__author__ = "Davide Pellegrino"
__date__ = "2020-06-01"

import json
import logging
import time

from sapgw.session import Session, parseApiError

class Supplier(object):
    """
    SAPGW Suppliers.
    """
    
    def __init__(self, profile_name=None):
        """
        Init Supplier class.
        """
        logging.info('Init Supplier...')
        s = Session(profile_name)
        host = s.config.get('sapgw_host')
        self.host = host
        self.s = s   

    def getSupplier(self, supplier_id:str):
        """
        Anagrafica fornitore.
        """
        logging.info(f'Reading supplier {supplier_id}...')
        params = {
            '$format' : 'json'
        }
        rq = f"{self.host}/ZVENDOR_GETDETAIL_SU_SRV/zvendor_general_dataSet('{supplier_id}')"
        agent=self.s.getAgent()
        r = agent.get(rq, params=params)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        supplier_data = r.text
        return supplier_data

    def createSupplier(self, payload):
        """
        Create new supplier.
        """
        logging.info(f'Creating new supplier...')
        rq = f"{self.host}/xxx"
        agent=self.s.getAgent()
        r = agent.post(rq, json=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        supplier_data = r.text
        return supplier_data   