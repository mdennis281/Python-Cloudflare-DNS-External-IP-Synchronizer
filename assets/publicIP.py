# Author: Michael Dennis (https://github.com/mdennis281)
# Created: 09-26-2019
# Project Repository: https://github.com/mdennis281/Python-Cloudflare-DNS-External-IP-Synchronizer
# License: MIT (https://en.wikipedia.org/wiki/MIT_License)

import requests, re

#Uses regex to parse webpage for the external IP address
def get():
    try:
        page = requests.get('http://checkip.dyndns.com')
        regex = '\\b\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\b'
        ip = re.search(regex,page.text).group(0)
        return ip
    except Exception as err:
        log(repr(err))
        raise err
