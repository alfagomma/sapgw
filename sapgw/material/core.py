
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MATERIALS SDK
"""

__author__ = "Davide Pellegrino"
__version__ = "2.1.12"
__date__ = "2019-11-07"

import json, logging, time
from sapgw.utility.cache import Cache as cachemodule
from sapgw.session import Session, parseApiError

logger = logging.getLogger()
class Material(object):
    """
    SAPGW Materials.
    """
    cache = False
    
    def __init__(self, material_id:int, profile_name=None, use_cache=False):
        """
        Init Material class.
        """
        logger.info(f'Init Material SDK: id {material_id} use cache {use_cache}...')
        self.material_id = material_id
        s = Session(profile_name)
        self.sapHost = s.getSapHost()
        self.sapAgent = s.getSapConnecion()
        if use_cache:
            self.cache = cachemodule()

    def getMaterialAna(self):
        """
        Anagrafica materiale.
        """
        logger.info('Reading material ana...')
        payload = {
            '$format' : 'json',
            '$expand' : 'ToDescriptions'
        }
        rq = f"{self.sapHost}/ZMATERIAL_GET_ALL_SU_SRV/zmaterial_client_dataSet(Material='{self.material_id}')"
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

    def getMaterialClass(self):
        """
        Classificazione materiale.
        """
        logger.info('Reading material class...')
        payload = {
            '$format' : 'json'
        }
        rq = f"{self.sapHost}/ZMATERIAL_CLASSIFICATION_SU_SRV/z_material_classSet(Material='{self.material_id}')/ToClassification"
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
