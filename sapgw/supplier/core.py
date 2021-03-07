
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SUPPLIER
"""

__author__ = "Davide Pellegrino"
__date__ = "2021-03-05"

import logging

from sapgw.session import Session


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

    def getSupplier(self, supplier_id: str):
        """
        Read supplier data.
        """
        logging.info(f'Reading supplier {supplier_id}...')
        params = {
            '$format': 'json'
        }
        rq = f"{self.host}/ZVENDOR_GETDETAIL_SU_SRV/zvendor_general_dataSet('{supplier_id}')"
        try:
            agent = self.s.getAgent()
            r = agent.get(rq, params=params)
        except Exception:
            logging.error(f'Failed request {rq}')
            return False
        return self.s.response(r)

    # def createSupplier(self, payload):
    #     """
    #     Create new supplier.
    #     """
    #     logging.info(f'Creating new supplier...')
    #     rq = f"{self.host}/xxx"
    #     try:
    #         agent = self.s.getAgent()
    #         r = agent.post(rq, json=payload)
    #     except Exception:
    #         logging.error(f'Failed request {rq}')
    #         return False
    #     return self.s.response(r)
