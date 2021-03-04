
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

    __cacheKey = 'ag:sapgw:session'
    __ttl = 1500  # 25minuti

    def __init__(self, profile_name=None):
        """
        Init SAPGW session.
        """
        profile_name = profile_name if profile_name else 'default'
        logging.debug(f'init sapgw session -p {profile_name}')
        self.__initProfileConfig(profile_name)
        self.__initRedisInstance()

        self.__initRedisInstance()

    def __initProfileConfig(self, profile_name):
        """ load profile conf"""
        import configparser
        logging.debug(f'Init {profile_name} profile..')
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
        logging.debug('Setting redis cache instance...')
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
        logging.debug(f'Agent with auth {sap_username} - {sap_password}')
        # chiamo x leggere csrf e ricevo i cookie
        host = self.config.get('sapgw_host')
        rq = f'{host}/ZCUSTOMER_MAINTAIN_SRV'
        r = agent.get(rq, headers={'x-csrf-token': 'Fetch'})
        if 200 != r.status_code:
            logging.error('Fetch csrf token failed!')
            return False
        csrf = r.headers['x-csrf-token']
        logging.debug(f'OK, new sap csrf is {csrf}')
        # salvo cache key ed inizio ttl
        self.redis.set(self.__cacheKey, csrf, ex=self.__ttl)
        # ora che ho la risposta csrf e so che REQUESTS ha con se i cookie,
        # aggiorno headers dell'agent
        try:
            agent.headers.update({
                'X-CSRF-Token': csrf,
                'user-agent': 'SAPGW-Session',
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            })
        except Exception:
            logging.error("Invalid token keys", exc_info=True)
            return False
        self.__agent = agent
        return True

    def getAgent(self, csrf=None):
        """Retrive API request session."""
        logging.debug('Get request agent')
        # ogni volta che viene chiamata un FX, getagent deve verificare se e da quanto tempo cè un a chiave sessione
        # leggo da redis il ttl del cachekey
        # primo controllo: la class python ha gia valorizzato un __agnet ?
        if self.__agent:
            # bene, controllo il ttl
            ttl = self.redis.ttl(self.__cacheKey)
            if ttl < 5:
                logging.debug('Invalid cache key')
                self.__createSessionAgent()
        else:
            self.__createSessionAgent()
        if not self.__agent:
            logging.error('Unable to create SAP sessionagent!')
            exit(1)
        return self.__agent

    def response(self, r):
        """ default response object from requests"""
        fr = {}
        logging.debug(
            f'{r.url} ({r.elapsed}) {r.status_code}')
        # print(r.raise_for_status())
        body = r.json() if r.text else None
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
            if r.status_code >= 400 and r.status_code < 500:
                logging.debug({'400': error})
            else:
                logging.debug({'error': error})
        return json.dumps(fr)
