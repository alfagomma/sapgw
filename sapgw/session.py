
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SAPGW for AGCLOUD - Session Boot
"""
import json
import logging
import os
import time
from sys import exit


class Session(object):
    """
    SAPGW session
    tts 25minutes (csrf 30 min)
    """

    __currentAgent = False
    __cacheKey = 'ag:sapgw:session'
    __ttl = (60*30)  # 30minuti

    def __init__(self, profile_name=None):
        """
        Init SAPGW session.
        """
        profile_name = profile_name if profile_name else 'default'
        logging.info(f'Init SAPGW session -p {profile_name}')
        self.__initProfileConfig(profile_name)
        self.__initRedisInstance()

    def __initProfileConfig(self, profile_name):
        """ load profile conf"""
        import configparser
        logging.info(f'Loading profile {profile_name}..')
        # Config
        config_path = os.path.expanduser('~/.agcloud/config')
        cp = configparser.ConfigParser()
        cp.read(config_path)
        if not cp.has_section(profile_name):
            logging.error(f'Unknow {profile_name} configs!')
            exit(1)
        self.config = cp[profile_name]
        # Credentials
        credentials_path = os.path.expanduser('~/.agcloud/credentials')
        ccp = configparser.ConfigParser()
        ccp.read(credentials_path)
        if not ccp.has_section(profile_name):
            logging.error(f'Unknow {profile_name} credentials!')
            exit(1)
        self.__credentials = ccp[profile_name]
        return

    def __initRedisInstance(self):
        """init redis instance. """
        from redis import Redis
        logging.info('Setting redis cache instance...')
        redis_host = self.config.get('redis_host')
        redis_pass = self.__credentials.get('redis_password')
        try:
            redis_instance = Redis(
                host=redis_host, password=redis_pass, decode_responses=True)
        except:
            logging.error('Unable to create redis instance!!')
            return False
        self.redis = redis_instance
        return True

    def __createSessionAgent(self):
        """ Create requests session. """
        import requests
        logging.info('Creating new sap requests session')
        sap_username = self.__credentials.get('sap_username')
        sap_password = self.__credentials.get('sap_password')
        agent = requests.Session()
        agent.auth = (sap_username, sap_password)
        agent.headers.update({
            'user-agent': 'SAPGW-Session',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        self.__currentAgent = agent
        return agent

    def getAgent(self, csrf=None):
        """Retrive API request session."""
        logging.info('Get request agent')
        if self.__currentAgent:
            return self.__currentAgent
        return self.__createSessionAgent()

    def getXcsrf(self):
        """ Read XCSRF. """
        logging.info('Read my xcsrf')
        if not self.__currentAgent:
            logging.warning('Unable to read XCSRF. Create agent first!')
            return False
        # bene, controllo il ttl  
        if self.redis.ttl(self.__cacheKey) > 3:
            return self.redis.get(self.__cacheKey)
        #######################
        logging.info('Sleeping 3sec waiting expiring...')
        time.sleep(3)
        #######################
        agent = self.__currentAgent
        # chiamo x leggere csrf e ricevo i cookie
        host = self.config.get('sapgw_host')
        rq = f'{host}/ZCUSTOMER_MAINTAIN_SRV'
        try:
            r = agent.get(rq, headers={'x-csrf-token': 'Fetch'})
        except Exception:
            logging.error("Unable to fetch csrf token")
            return False
        if 200 != r.status_code:
            logging.error('Fetch csrf token failed!')
            return False
        csrf = r.headers['x-csrf-token']
        logging.debug(f'OK, new sap csrf is {csrf}')
        # salvo cache key ed inizio ttl
        self.redis.set(self.__cacheKey, csrf, ex=self.__ttl)
        return csrf

    def response(self, r):
        """ default response object from requests"""
        fr = {}
        logging.debug(
            f'{r.url} ({r.elapsed}) {r.status_code}')
        # print(r.raise_for_status())
        try:
            body = r.json() if r.text else None
        except:
            logging.error(f'Unable to json response {r.text}')
            return False
        if r.ok:
            fr['status'] = 'ok'
            if body:
                fr = {**fr, **body}
        else:
            fr['status'] = 'ko'
            error = {}
            if 'error' in body:
                details = body['error']['message'] if 'message' in body['error'] else None
                error['title'] = details['value']
            fr['error'] = error
            if r.status_code >= 400 and r.status_code < 500:
                logging.debug({'400': error})
            else:
                logging.debug({'error': error})
        return json.dumps(fr)
