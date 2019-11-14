
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SAPGW for AGCLOUD - Session Boot
"""

import os, logging, requests, configparser
from requests.adapters import HTTPAdapter
from sys import exit

logger = logging.getLogger()

class Session(object):
    """
    SAPGW SESSION Boot
    """

    def __init__(self, profile_name=None):
        """
        Session Init
        """
        if not profile_name:
            profile_name = 'default'
        logger.debug(f'Init session with {profile_name} profile..')
        config_path = os.path.expanduser('~/.agcloud/config')
        ## Config
        config = configparser.ConfigParser()
        config.read(config_path)
        if not config.has_section(profile_name):
            logger.error(f'Unknow {profile_name} configs!')
            exit(1)
        ## Credentials
        credentials_path = os.path.expanduser('~/.agcloud/credentials')
        credentials = configparser.ConfigParser()
        credentials.read(credentials_path)
        if not credentials.has_section(profile_name):
            logger.error(f'Unknow {profile_name} credentials!')
            exit(1)
        self.profile = profile_name
        self.config = config
        self.credentials = credentials
        return
    
    def getSapHost(self):
        """return sap host"""
        logger.debug(f'Return sap host..')
        host = self.config.get(self.profile, 'sapgw_host')
        return host

    def create(self):
        """ create new sap connection """
        logger.debug('Init new sap connection...')
        sap_username = self.credentials.get(self.profile, 'sap_username')
        sap_password = self.credentials.get(self.profile, 'sap_password')
        logger.debug(f'Sap connection: {sap_username}:{sap_password}')
        s = requests.Session()
        s.auth=(sap_username, sap_password)
        return s


def testConnection(self):
    """ Test SAPGW Connection with auth credentials."""
    from requests.exceptions import ConnectionError
    logger.debug('Init test connection...')
    s = Session()
    sapagent = s.create()
    try:
        sapagent.get(s.getSapHost())
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