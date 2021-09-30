
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
INVOICE
"""

__author__ = "Davide Pellegrino"
__date__ = "2021-08-09"

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
        logger.info('Init sap gw invoice...')
        s = Session(profile_name)
        host = s.config.get('sapgw_host')
        self.host = host
        self.s = s

    def getInvoiceHeader(self, invoice_id: str):
        """
        Invoice Header.
        """
        logger.info(f'Reading invoice {invoice_id} head...')
        payload = {
            '$format': 'json'
        }
        rq = f"{self.host}/ZBILL_GET_DETAIL_SRV/BillingHeaderSet('{invoice_id}')"
        try:
            agent = self.s.getAgent()
            r = agent.get(rq, params=payload)
        except Exception:
            logger.error(f'Failed request {rq}')
            return False
        return self.s.response(r)

    def getInvoiceBody(self, invoice_id: str):
        """
        Invoice body.
        """
        logger.info(f'Reading invoice {invoice_id} body...')
        payload = {
            '$format': 'json'
        }
        rq = f"{self.host}/ZBILL_GET_DETAIL_SRV/BillingHeaderSet('{invoice_id}')/To_BillingPosition"
        try:
            agent = self.s.getAgent()
            r = agent.get(rq, params=payload)
        except Exception:
            logger.error(f'Failed request {rq}')
            return False
        return self.s.response(r)

    def getInvoice(self, invoice_id: str):
        """
        Invoice head+body.
        """
        logger.info(f'Reading invoice {invoice_id}...')
        payload = {
            '$format': 'json',
            '$expand': 'To_BillingPosition'
        }
        rq = f"{self.host}/ZBILL_GET_DETAIL_SRV/BillingHeaderSet('{invoice_id}')"
        try:
            agent = self.s.getAgent()
            r = agent.get(rq, params=payload)
        except Exception:
            logger.error(f'Failed request {rq}')
            return False
        return self.s.response(r)
