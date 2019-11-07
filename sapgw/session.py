
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SAPGW for AGCLOUD - Session Boot
"""

import os, json, time, logging
import requests
import configparser
from sys import exit

logger = logging.getLogger()

class Session(object):
    """
    SAPGW SESSION Boot
    """

    sapagent = None

    def __init__(self, profile_name=None):
        """
        Session Init
        """
        logger.debug(f'Init session with {profile_name} profie..')
        config_path = os.path.expanduser('~/.agcloud/config')
        
        ## Config
        config = configparser.ConfigParser()
        config.read(config_path)
        if not config.has_section(profile_name):
            logger.error(f'Unknow {profile_name} configs!')
            exit(1)
        self.ep_sapgw = config.get(profile_name, 'ep_sapgw')
        ## Credentials
        credentials_path = os.path.expanduser('~/.agcloud/credentials')
        credentials = configparser.ConfigParser()
        credentials.read(credentials_path)
        if not credentials.has_section(profile_name):
            logger.error(f'Unknow {profile_name} credentials!')
            exit(1)

        sap_username = credentials.get(profile_name, 'sap_username')
        sap_password = credentials.get(profile_name, 'sap_password')
        
        saprq = requests.Session()
        saprq.auth=(sap_username, sap_password)
        self.sapagent = saprq
        return
    
    def testConnection(self):
        """ Test SAPGW Connection with auth credentials."""
        logger.debug('Init test connection...')
        rUid = self.sapagent.get('/')
        if 200 != rUid.status_code:
            parseApiError(rUid)
            return False
        return True


def parseApiError(response):
    """ stampa errori response SAPGW """
    status = response.status_code
    try:
        problem = response.text
    except Exception:
        # Add handlers to the logger
        logger.error('Not jsonable')
        problem = response.text
    msg = f'status {status} [{problem}]'
    logger.warning(msg)