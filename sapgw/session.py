
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SAPGW for AGCLOUD - Session Boot
"""

import configparser
import logging
import os
import time
from sys import exit

import requests
from requests.adapters import HTTPAdapter

logger = logging.getLogger()

class Session(object):
    """
    SAPGW SESSION Boot
    """
    configPath='~/.agcloud/config'
    credentialPath='~/.agcloud/credentials'

    host=False
    agent = False
    csrf = {}

    def __init__(self, profile_name='default'):
        """
        Session Init
        """
        logger.debug(f'Init sapgw session with {profile_name} profile..')
        config_path = os.path.expanduser(self.configPath)
        ## Config
        config = configparser.ConfigParser()
        config.read(config_path)
        if not config.has_section(profile_name):
            logger.error(f'Unknow {profile_name} configs!')
            exit(1)
        #host
        self.host = config.get(profile_name, 'sapgw_host')
        ## Credentials
        credentials_path = os.path.expanduser(self.credentialPath)
        credentials = configparser.ConfigParser()
        credentials.read(credentials_path)
        if not credentials.has_section(profile_name):
            logger.error(f'Unknow {profile_name} credentials!')
            exit(1)
        #agent
        sap_username = credentials.get(profile_name, 'sap_username')
        sap_password = credentials.get(profile_name, 'sap_password')
        agent = requests.Session()
        agent.auth=(sap_username, sap_password)
        self.agent = agent
        return

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
    """ stampa errori response SAPGW """
    status = response.status_code
    try:
        problem = response.text
    except Exception:
        problem = response.text
    msg = f'status {status} [{problem}]'
    logger.warning(msg)
