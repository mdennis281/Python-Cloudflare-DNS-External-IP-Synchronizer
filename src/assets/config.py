# Author: Michael Dennis (https://github.com/mdennis281)
# Created: 09-26-2019
# Project Repository: https://github.com/mdennis281/Python-Cloudflare-DNS-External-IP-Synchronizer
# License: MIT (https://en.wikipedia.org/wiki/MIT_License)

from configparser import ConfigParser

def load():
    config = ConfigParser()
    config.read('config.ini')

    config = {
        'general': {
            'logPath': config.get('general','logPath'),
            'loggingEnabled': config.getboolean('general','loggingEnabled')
        },
        'API': {
            'token': config.get('CloudFlare-API','token'),
            'siteName': config.get('CloudFlare-API','siteName')
        },
        'DNS': {
            'name': config.get('DNS','name'),
            'recordType': config.get('DNS','recordType'),
            'proxied': config.getboolean('DNS','proxied'),
            'createRecord': config.getboolean('DNS','createRecord')
        }
    }
    return config
