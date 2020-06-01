
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SAPGW for AGCLOUD - Session Boot
"""

import configparser
import json
import logging
import os
import time
from sys import exit

import requests
from redis import Redis

logger = logging.getLogger(__name__)

class Session(object):
    """
    SAPGW session
    """
    config=False
    __agent=False
    __credentials=False
    __cacheKey='ag:sapgw'

    def __init__(self, profile_name='default'):
        """
        Init SAPGW session.
        """
        if not profile_name:
            profile_name = 'default'        
        logger.info(f'Init agbot session with {profile_name} profile.')
        ## Config
        config_path = os.path.expanduser('~/.agcloud/config')
        cp = configparser.ConfigParser()
        cp.read(config_path)
        if not cp.has_section(profile_name):
            logger.error(f'Unknow {profile_name} configs!')
            exit(1)
        self.config=cp[profile_name]
        ## Credentials
        credentials_path = os.path.expanduser('~/.agcloud/credentials')
        ccp = configparser.ConfigParser()
        ccp.read(credentials_path)
        if not ccp.has_section(profile_name):
            logger.error(f'Unknow {profile_name} credentials!')
            exit(1)
        self.__credentials=ccp[profile_name]
        #cache
        self.__setCache()

    def __setCache(self):
        """ set cache """
        logger.debug('Setting redis cache...')
        redis_host = self.config.get('redis_host', '127.0.0.1')
        redis_pass = self.__credentials.get('redis_password', None)
        self.cache=Redis(host=redis_host, password=redis_pass, decode_responses=True)
        return True

    def __createToken(self):
        """ Create new session token. """
        logger.info(f'Init new session token ...')
        sap_username = self.__credentials.get('sap_username')
        sap_password = self.__credentials.get('sap_password')
        host = self.config.get('sapgw_host')
        rqToken = f'{host}/ZCUSTOMER_MAINTAIN_SRV'
        rUid = requests.get(rqToken, auth=(sap_username, sap_password))
        if 200 != rUid.status_code:
            parseApiError(rUid)
            return False
        responseUid = json.loads(rUid.text)
        token = self.__setToken(responseUid)
        return token

    def __getToken(self):
        """ Read session token. If not exists, it creates it. """
        logger.info('Init reading token..')
        token = self.cache.hgetall(self.__cacheKey)
        if not token:
            token = self.__createToken()
        return token

    def __createSessionAgent(self, token=None):
        """ Create requests session. """
        logger.debug('Creating new requests session')
        agent=requests.Session()
        agent.headers.update({'user-agent': 'SAPGW-Session'})
        if not token:
            token = self.__getToken()
            if not token:return False
        try:
            agent.headers.update({'x-csrf-token': token['csrf'] })
        except Exception:
            logger.error("Invalid token keys", exc_info=True)
        self.__agent=agent
        return agent

    def getAgent(self):
        """Retrive API request session."""
        logger.info('Get request agent')
        agent=self.__agent
        if not agent:
            agent=self.__createSessionAgent()
        else:
            ttl = self.cache.ttl(self.__cacheKey)
            if ttl < 1:
                agent=self.__createSessionAgent()
            elif 1 <= ttl <= 900:
                refreshedToken=self.__refreshToken()
                agent = self.__createSessionAgent(refreshedToken)
            if not agent:
                logger.error('Unable to create agent!')
                exit(1)
        return agent




    def getCsrfToken(self):
        """Retrive csrf"""
        logger.debug('Reading csrf')
        now=int(time.time())
        created_at = int(self.csrf['created_at']) if 'created_at' in self.csrf else False
        if int(created_at-now)>300:return self.csrf['token']
        rq = f"{self.host}/ZCUSTOMER_MAINTAIN_SRV')"
        headers={'x-csrf-token': 'Fetch'}
        r = self.agent.get(rq, headers=headers)
        if 200 != r.status_code:return False
        token = r.headers['x-csrf-token']
        if not token:return False
        self.csrf={
            'token': token,
            'created_at':int(time.time())
        }
        return token

def testConnection(self):
    """ Test SAPGW Connection with auth credentials."""
    from requests.exceptions import ConnectionError
    logger.debug('Init test connection...')
    s = Session()
    try:
        s.agent.get(s.host)
    except ConnectionError as ce:
        logger.exception(f'{ce}')
        return False
    except Exception:
        logger.error("Exception occurred", exc_info=True)
        return False
    return True

def parseApiError(response):
    """ stampa errori api """
    logger.debug('Parsing error')
    status = response.status_code
    try:
        problem = json.loads(response.text)
    except Exception:
        # Add handlers to the logger
        logger.error('Not jsonable', exc_info=True)
        return False
    msg = f'status {status}'
    if 'title' in problem:
        msg+=f" / {problem['title']}"
    if 'errors' in problem:
        for k,v in problem['errors'].items():
            msg+=f'\n\t -{k}:{v}'
    if status >=400 and status <500:
        logger.warning(msg)
    else:
        logger.error(msg)
    return msg