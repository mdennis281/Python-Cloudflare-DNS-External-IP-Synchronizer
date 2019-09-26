import requests, re

def get():
    try:
        page = requests.get('http://checkip.dyndns.com')
        regex = '\\b\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\b'
        ip = re.search(regex,page.text).group(0)
        return ip
    except Exception as err:
        log(repr(err))
        raise err
