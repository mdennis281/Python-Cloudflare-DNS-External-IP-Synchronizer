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
