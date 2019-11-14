#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Cache utility.
"""

import os, hashlib, json, logging

logger = logging.getLogger()

class Cache(object):
    """ Cache utilities."""

    cachePath= '.cache/sapgw'    

    def __init__(self):
        """Init new Cache utility."""
        logger.info(f'Init cache path {self.cachePath}..')
        if not os.path.exists(self.cachePath):
            logger.debug(f'Creating cache path {self.cachePath}')
            os.makedirs(self.cachePath)
        return

    def read(self, name):
        """ Recupero il dato in cache. """
        logger.info(f'Init read cache {name}...')        
        cachekey = self.__createCacheKey(name)
        if not self.__isCache(cachekey):
            logger.debug(f'{cachekey} is not cached!')
            return False
        try:
            cachefile = f'{self.cachePath}/{cachekey}'
            f = open(cachefile, 'r')
            fromcache = f.read()
            f.close()           
        except IOError:
            logger.exception("Exception occurred")
            return False
        logger.debug(f'Complete reading {cachefile} content: {fromcache}')
        return fromcache

    def create(self, name, data=None):
        """
        Salva il dato in cache.
        """
        logger.info(f'Creating {name} cache..')
        cachekey = self.__createCacheKey(name)
        try:
            f = open(f'{self.cachePath}/{cachekey}', 'w')
            f.write(data)
            f.close()
        except Exception:
            logger.error("Exception occurred", exc_info=True)
            return False
        logger.debug(f'Saved {cachekey} in cache')
        return True

    @staticmethod
    def clearCache(self):
        """
        Elimino tutti i file di cache.
        """
        logger.info('Init cleaning cache dir ...')
        filelist = [ f for f in os.listdir(self.cachePath) ]
        for f in filelist:
            cachefile = os.path.join(self.cachePath, f)
            os.remove(cachefile)
            logger.debug(f'Removed cache {cachefile}!')
        return True

    def __createCacheKey(self, name):
        """Genera una chiave cache """
        logger.info(f'Creating cache key {name}')
        __tmp = f'{json.dumps(name)}'
        cachekey = f'{hashlib.md5(__tmp.encode()).hexdigest()}.tmp'            
        return cachekey
    
    def __isCache(self, cachekey):
        """ verifica esistenza file in cache. """
        logger.info(f'Checking {cachekey} key..')
        return os.path.isfile(f'{self.cachePath}/{cachekey}')        