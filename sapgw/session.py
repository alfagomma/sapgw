
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


class Session(object):
    """
    SAPGW session
    tts 25minutes (csrf 30 min)
    """

    config = False
    __agent = False
    __credentials = False
    __cacheKey = 'ag:sapgw'
    __ttl = 1500

    def __init__(self, profile_name=None):
        """
        Init SAPGW session.
        """
        if not profile_name:
            profile_name = 'default'
        logging.debug(f'Init sapgw session with {profile_name} profile.')
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
        # cache
        self.__setCache()

    def __setCache(self):
        """ set cache """
        logging.debug('Setting redis cache...')
        redis_host = self.config.get('redis_host', '127.0.0.1')
        redis_pass = self.__credentials.get('redis_password', None)
        self.cache = Redis(
            host=redis_host, password=redis_pass, decode_responses=True)
        return True

    def __saveTokenCache(self, payload):
        """save token """
        logging.debug(f'Init set token {payload}')
        expire_in = payload['expires_in']
        uid = payload['access_token']
        csrf = payload['csrf']
        token = {
            'uid': uid,
            'csrf': csrf
        }
        tokenExpireAt = int(time.time()) + expire_in
        self.cache.hmset(self.__cacheKey, token)
        self.cache.expireat(self.__cacheKey, int(tokenExpireAt))
        return token

    def __getCsrfToken(self, agent):
        """ Get csrf token. """
        logging.debug(f'Reading new csrf token from sap...')
        # sap_username = self.__credentials.get('sap_username')
        # sap_password = self.__credentials.get('sap_password')
        host = self.config.get('sapgw_host')
        rq = f'{host}/ZCUSTOMER_MAINTAIN_SRV'
        headers = {'x-csrf-token': 'Fetch'}
        r = agent.get(rq, headers=headers)
        if 200 != r.status_code:
            return False
        csrf = r.headers['x-csrf-token']
        logging.debug(f'OK, new sap csrf is {csrf}')
        return csrf

    def __createToken(self, agent):
        """ Create a dummy token for SAP."""
        logging.debug(f'Creating new session token ...')
        # workaround - simula body response object
        csrf = self.__getCsrfToken(agent)
        body = {
            'access_token': time.time(),
            'csrf': csrf,
            'expires_in': self.__ttl
        }
        token = self.__saveTokenCache(body)
        return token

    def __refreshToken(self, agent):
        """ Refresh current token. """
        logging.debug(f'Init refresh token ...')
        csrf = self.__getCsrfToken(agent)
        body = {
            'csrf': csrf,
            'expires_in': self.__ttl
        }
        token = self.__saveTokenCache(body)
        return token

    def __getToken(self, agent):
        """ Read session token. If not exists, it creates it. """
        logging.debug('Init reading token..')
        token = False
        # NON PUOI USARE CACHE, CREA SEMPRE UNO NUOVO
        # token = self.cache.hgetall(self.__cacheKey)
        if not token:
            logging.debug('Token is not in cache! Creating new...')
            token = self.__createToken(agent)
        return token

    def __createSessionAgent(self, token=None):
        """ Create requests session. """
        logging.debug('Creating new requests session')
        sap_username = self.__credentials.get('sap_username')
        sap_password = self.__credentials.get('sap_password')
        agent = requests.Session()
        agent.auth = (sap_username, sap_password)
        logging.debug(f'Agent with auth {sap_username} - {sap_password}')
        if not token:
            logging.debug('Unknow token. Getting new one!')
            token = self.__getToken(agent)
            logging.debug(
                f'Creatingsessionagent: generatated token is {token}')
            if not token:
                return False
        logging.debug(f"Add csrf {token['csrf']} to agent header")
        try:
            agent.headers.update({
                'X-CSRF-Token': token['csrf'],
                'user-agent': 'SAPGW-Session',
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            })
        except Exception:
            logging.error("Invalid token keys", exc_info=True)
        self.__agent = agent
        return agent

    def getAgent(self, csrf=None):
        """Retrive API request session."""
        logging.debug('Get request agent')
        agent = self.__agent
        if not agent:
            agent = self.__createSessionAgent()
            if not agent:
                logging.error('Unable to create agent!')
                exit(1)
        # NON PUOI SALVARLO, OGNI VOLTA CHE LANCI requests.session(), CAMBI I COOKIE
        # QUINDI CAMBI ANCHE I TOKEN SAP
        # if not agent:
        #     agent=self.__createSessionAgent()
        # else:
        #     ttl = self.cache.ttl(self.__cacheKey)
        #     if ttl < 1:
        #         agent=self.__createSessionAgent()
        #     elif 1 <= ttl <= 120:
        #         refreshedToken=self.__refreshToken(agent)
        #         agent = self.__createSessionAgent(refreshedToken)
        #     if not agent:
        #         logging.error('Unable to create agent!')
        #         exit(1)
        return agent

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
                print(error)
            fr['error'] = error
            if r.status_code >= 400 and r.status_code < 500:
                logging.warning(error)
            else:
                logging.error(error)
        return json.dumps(fr)

#  DEPRECATED
#  def parseApiError(response):
#     """ stampa errori api """
#     logging.debug('Parsing error')
#     status = response.status_code
#     try:
#         problem = json.loads(response.text)
#     except Exception:
#         # Add handlers to the logger
#         logging.error('Not jsonable %s' % response.text, exc_info=True)
#         return False
#     logging.debug(problem)
#     msg = f'status {status}'
#     if 'title' in problem:
#         msg += f" / {problem['title']}"
#     if 'errors' in problem:
#         for k, v in problem['errors'].items():
#             msg += f'\n\t -{k}:{v}'
#     if status >= 400 and status < 500:
#         logging.warning(msg)
#     else:
#         logging.error(msg)
#     return msg
