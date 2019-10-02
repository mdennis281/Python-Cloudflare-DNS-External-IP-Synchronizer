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
            'logPath': config.get('general','logPath',fallback="..\\CF-DNS.log"),
            'loggingEnabled': config.getboolean('general','loggingEnabled',fallback=False),
            'logLevel': config.getint('general','logLevel',fallback=2)
        },
        'API': {
            'token': config.get('CloudFlare-API','token',fallback=""),
            'siteName': config.get('CloudFlare-API','siteName',fallback="")
        },
        'DNS': {
            'name': config.get('DNS','name',fallback=""),
            'recordType': config.get('DNS','recordType',fallback="A"),
            'proxied': config.getboolean('DNS','proxied',fallback=False),
            'createRecord': config.getboolean('DNS','createRecord',fallback=True)
        }
    }
    return config
