
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
INVOICE
"""

__author__ = "Davide Pellegrino"
__date__ = "2022-02-02"

import logging

from sapgw.session import Session

logger = logging.getLogger(__name__)


class Invoice(object):
    """
    SAPGW Invoices.
    """

    def __init__(self, profile_name=None):
        """
        Init Invoice class.
        """
        logger.debug('Init sap gw invoice...')
        s = Session(profile_name)
        host = s.config.get('sapgw_host')
        self.host = host
        self.s = s

    def getInvoiceHeader(self, invoice_id: str):
        """
        Invoice Header.
        """
        logger.debug(f'Reading invoice {invoice_id} head...')
        payload = {
            '$format': 'json'
        }
        rq = f"{self.host}/ZBILL_GET_DETAIL_SRV/BillingHeaderSet('{invoice_id}')"
        agent = self.s.getAgent()
        r = agent.get(rq, params=payload)
        return self.s.response(r)

    def getInvoiceBody(self, invoice_id: str):
        """
        Invoice body.
        """
        logger.debug(f'Reading invoice {invoice_id} body...')
        payload = {
            '$format': 'json'
        }
        rq = f"{self.host}/ZBILL_GET_DETAIL_SRV/BillingHeaderSet('{invoice_id}')/To_BillingPosition"

        agent = self.s.getAgent()
        r = agent.get(rq, params=payload)
        return self.s.response(r)

    def getInvoice(self, invoice_id: str):
        """
        Invoice head+body.
        """
        logger.debug(f'Reading invoice {invoice_id}...')
        payload = {
            '$format': 'json',
            '$expand': 'To_BillingPosition'
        }
        rq = f"{self.host}/ZBILL_GET_DETAIL_SRV/BillingHeaderSet('{invoice_id}')"
        agent = self.s.getAgent()
        r = agent.get(rq, params=payload)
        return self.s.response(r)
