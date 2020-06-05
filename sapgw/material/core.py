
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MATERIAL
"""

__author__ = "Davide Pellegrino"
__date__ = "2020-06-01"

import json
import logging
import time

from sapgw.session import Session, parseApiError

class Material(object):
    """
    SAPGW Materials.
    """
    
    def __init__(self, profile_name=None):
        """
        Init Material class.
        """
        logging.info('Init Material...')
        s = Session(profile_name)
        host = s.config.get('sapgw_host')
        self.host = host
        self.s = s   

    def getMaterialAna(self, material_id:str):
        """
        Anagrafica materiale.
        """
        logging.info(f'Reading material {material_id} ana...')
        payload = {
            '$format' : 'json',
            '$expand' : 'ToDescriptions'
        }
        rq = f"{self.host}/ZMATERIAL_GET_ALL_SU_SRV/zmaterial_client_dataSet(Material='{material_id}')"
        agent=self.s.getAgent()
        r = agent.get(rq, params=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        material_ana = r.text
        return material_ana

    def getMaterialClass(self, material_id:str):
        """
        Classificazione materiale.
        """
        logging.info(f'Reading material {material_id} class...')
        payload = {
            '$format' : 'json'
        }
        rq = f"{self.host}/ZMATERIAL_CLASSIFICATION_SU_SRV/z_material_classSet(Material='{material_id}')/ToClassification"
        agent=self.s.getAgent()
        r = agent.get(rq, params=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        material_class = r.text
        return material_class

    def getMaterialStock(self, material_id:str, plant=None):
        """
        Stock disponibile.
        """
        logging.info(f'Reading material {material_id} stock...')
        payload = {
            '$format' : 'json'
        }
        if plant:payload['$filter']=f"Plant eq '{plant}'"
        rq=f"{self.host}/ZMATERIAL_GET_STOCK_SRV/zmaterial_stockSet('{material_id}')/To_Get_Stock"
        agent=self.s.getAgent()
        r = agent.get(rq, params=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        material_stock = r.text
        return material_stock
