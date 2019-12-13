
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MATERIAL SDK
"""

__author__ = "Davide Pellegrino"
__date__ = "2019-12-04"

import json, logging, time
from sapgw.utility.cache import Cache as cachemodule
from sapgw.session import Session, parseApiError

logger = logging.getLogger()
class Material(object):
    """
    SAPGW Materials.
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

    def getMaterialAna(self, material_id):
        """
        Anagrafica materiale.
        """
        logger.info(f'Reading material {material_id} ana...')
        payload = {
            '$format' : 'json',
            '$expand' : 'ToDescriptions'
        }
        rq = f"{self.sapHost}/ZMATERIAL_GET_ALL_SU_SRV/zmaterial_client_dataSet(Material='{material_id}')"
        if self.cache:
            cachekey = rq+str(json.dumps(payload))
            data = self.cache.read(cachekey)
            if data:
                return data
        r = self.sapAgent.get(rq, params=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        material_ana = r.text
        if self.cache:
            self.cache.create(cachekey, material_ana)
        return material_ana

    def getMaterialClass(self, material_id):
        """
        Classificazione materiale.
        """
        logger.info(f'Reading material {material_id} class...')
        payload = {
            '$format' : 'json'
        }
        rq = f"{self.sapHost}/ZMATERIAL_CLASSIFICATION_SU_SRV/z_material_classSet(Material='{material_id}')/ToClassification"
        if self.cache:
            cachekey = rq+str(json.dumps(payload))
            data = self.cache.read(cachekey)
            if data:
                return data
        r = self.sapAgent.get(rq, params=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        material_class = r.text
        if self.cache:
            self.cache.create(cachekey, material_class)
        return material_class

    def getMaterialStock(self, material_id, plant=None):
        """
        Stock disponibile
        """
        logger.info(f'Reading material {material_id} stock...')
        payload = {
            '$format' : 'json'
        }
        if plant:
            payload['$filter']=f"Plant eq '{plant}'"
        rq=f"{self.sapHost}/ZMATERIAL_GET_STOCK_SRV/zmaterial_stockSet('{material_id}')/To_Get_Stock"
        if self.cache:
            cachekey = rq+str(json.dumps(payload))
            data = self.cache.read(cachekey)
            if data:
                return data
        r = self.sapAgent.get(rq, params=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        material_stock = r.text
        if self.cache:
            self.cache.create(cachekey, material_stock)
        return material_stock


