
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MATERIALS SKD
"""

__author__ = "Davide Pellegrino"
__version__ = "2.1.12"
__date__ = "2019-11-07"

import json, logging, time
from sapgw.session import Session, parseApiError

logger = logging.getLogger(__name__)

class Material(object):
    """
    SAPGW Materials.
    """

    material_id = None

    def __init__(self, profile_name=None):
        """
        Init Material class.
        """
        logger.debug(f'Init Material SDK {profile_name}')
        session = Session(profile_name)
        self.apibot = session.apibot
        self.endpoint = session.ep_sapgw


    def getMaterialAna(self):
        """
        Anagrafica materiale.
        """
        logger.debug('Reading material ana...')
        payload = {
            '$format' : 'json',
            '$expand' : 'ToDescriptions'
        }
        rq = f"{self.endpoint}/ZMATERIAL_GET_ALL_SU_SRV/zmaterial_client_dataSet(Material='{self.material_id}')"
        cachekey = Cache.createCacheKey(rq, payload)
        if not self.refresh and Cache.isCache(cachekey):
            material_ana = Cache.fromCache(cachekey)
        else:
            r = self.s.get(rq, params=payload)
            if 200 != r.status_code:
                self.parseApiError(r)
                return False
            material_ana = r.text
            Cache.toCache(cachekey, material_ana)
        return material_ana

    def getMaterialClass(self):
        """
        Classificazione materiale.
        """
        logger.debug('Reading material class...')
        payload = {
            '$format' : 'json'
        }
        rq = f"{self.endpoint}/ZMATERIAL_CLASSIFICATION_SU_SRV/z_material_classSet(Material='{self.material_id}')/ToClassification"
        cachekey = Cache.createCacheKey(rq, payload)
        if not self.refresh and Cache.isCache(cachekey):
            material_class = Cache.fromCache(cachekey)
        else:
            r = self.s.get(rq, params=payload)
            if 200 != r.status_code:
                self.parseApiError(r)
                return False
            material_class = r.text
            Cache.toCache(cachekey, material_class)
        return material_class
