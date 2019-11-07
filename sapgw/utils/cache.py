#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Cache utility.
"""
import os, hashlib, json, logging

logger = logging.getLogger(__name__)

class Cache(object):
    """ Cache utilities."""

    cachePath= '~/.cache/sapgw'    

    def __init__(self):
        """Init new Cache utility."""
        if not os.path.exists(self.cachePath):
            os.makedirs(self.cachePath)

    def read(self, name):
        """ Recupero il dato in cache. """
        logger.debug(f'Init read cache {name}...')        
        cachekey = self.__createCacheKey(name)
        if not self.__isCache(cachekey):
            return False
        try:
            f = open(f'{self.cachePath}/{cachekey}', 'r')
            fromcache = f.read()
            f.close()            
        except IOError:
            logging.exception("Exception occurred")
            return False
        return fromcache

    def create(self, name, data):
        """
        Salva il dato in cache.
        """
        cachekey = self.__createCacheKey(name)
        try:
            f = open(f'{self.cachePath}/{cachekey}', 'w')
            f.write(data)
            f.close()
        except IOError:
            logging.exception("Exception occurred")
            return False
        logger.debug(f'Saved {cachekey} in cache')
        return True

    @staticmethod
    def clearCache(self):
        """
        Elimino tutti i file di cache.
        """
        logger.debug('Init cleaning cache dir ...')
        filelist = [ f for f in os.listdir(self.cachePath) ]
        for f in filelist:
            os.remove(os.path.join(self.cachePath, f))
        return True

    def __createCacheKey(self, name):
        """Genera una chiave cache """
        __tmp = f'{json.dumps(name)}'
        cachekey = f'{hashlib.md5(__tmp.encode()).hexdigest()}.tmp'            
        return cachekey
    
    def __isCache(self, cachekey):
        """ verifica esistenza file in cache. """
        logger.debug(f'Checking {cachekey} key..')
        return os.path.isfile(f'{self.cachePath}/{cachekey}')        