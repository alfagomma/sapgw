
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

from sapgw.session import Session


class Customer(object):
    """
    SAPGW Customers.
    """

    def __init__(self, profile_name=None):
        """
        Init Customer class.
        """
        logging.info('Init SAP Customer...')
        s = Session(profile_name)
        host = s.config.get('sapgw_host')
        self.host = host
        self.s = s

    def getCustomerAna(self, customer_id: str):
        """
        Anagrafica cliente.
        """
        logging.info(f'Reading customer {customer_id} ana...')
        payload = {
            '$format': 'json',
        }
        rq = f"{self.host}/ZCUSTOMER_GETDETAIL_SU_SRV/zcustomer_general_dataSet('{customer_id}')"
        try:
            agent = self.s.getAgent()
            r = agent.get(rq, params=payload)
        except Exception:
            logging.error(f'Failed request {rq}')
            return False
        return self.s.response(r)

    def createCustomerAna(self, payload):
        """
        Create new customer.
        agent.headers.update({
            'X-CSRF-Token': csrf,
            'user-agent': 'SAPGW-Session',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        self.__currentAgent = agent
        """
        logging.info(f'Creating new customer...')
        rq = f"{self.host}/ZCUSTOMER_MAINTAIN_SRV/zcustomer_maintain_entity_set"
        # recupero xcsrf
        xcsrf = self.s.getXcsrf()
        if not xcsrf:
            logging.error(f'Failed to read xcsfr')
            return False
        try:
            agent = self.s.getAgent()
            agent.headers.update({
                'X-CSRF-Token': xcsrf
            })            
            r = agent.post(rq, json=payload)
        except Exception:
            logging.error(f'Failed request {rq}')
            return False
        return self.s.response(r)
