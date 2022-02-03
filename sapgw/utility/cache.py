#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Cache utility.
"""

import hashlib
import json
import logging
import os


class Cache(object):
    """ Cache utilities."""

    cachePath= '.cache/sapgw'    

    def __init__(self):
        """Init new Cache utility."""
        logging.debug(f'Init cache path {self.cachePath}..')
        if not os.path.exists(self.cachePath):
            logging.debug(f'Creating cache path {self.cachePath}')
            os.makedirs(self.cachePath)
        return

    def read(self, name):
        """ Recupero il dato in cache. """
        logging.debug(f'Init read cache {name}...')        
        cachekey = self.__createCacheKey(name)
        if not self.__isCache(cachekey):
            logging.debug(f'{cachekey} is not cached!')
            return False
        try:
            cachefile = f'{self.cachePath}/{cachekey}'
            f = open(cachefile, 'r')
            fromcache = f.read()
            f.close()           
        except IOError:
            logging.exception("Exception occurred")
            return False
        logging.debug(f'Complete reading {cachefile} content: {fromcache}')
        return fromcache

    def create(self, name, data=None):
        """
        Salva il dato in cache.
        """
        logging.debug(f'Creating {name} cache..')
        cachekey = self.__createCacheKey(name)
        try:
            f = open(f'{self.cachePath}/{cachekey}', 'w')
            f.write(data)
            f.close()
        except Exception:
            logging.error("Exception occurred", exc_info=True)
            return False
        logging.debug(f'Saved {cachekey} in cache')
        return True

    @staticmethod
    def clearCache(self):
        """
        Elimino tutti i file di cache.
        """
        logging.debug('Init cleaning cache dir ...')
        filelist = [ f for f in os.listdir(self.cachePath) ]
        for f in filelist:
            cachefile = os.path.join(self.cachePath, f)
            os.remove(cachefile)
            logging.debug(f'Removed cache {cachefile}!')
        return True

    def __createCacheKey(self, name):
        """Genera una chiave cache """
        logging.debug(f'Creating cache key {name}')
        __tmp = f'{json.dumps(name)}'
        cachekey = f'{hashlib.md5(__tmp.encode()).hexdigest()}.tmp'            
        return cachekey
    
    def __isCache(self, cachekey):
        """ verifica esistenza file in cache. """
        logging.debug(f'Checking {cachekey} key..')
        return os.path.isfile(f'{self.cachePath}/{cachekey}')        
