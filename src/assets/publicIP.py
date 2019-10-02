# Author: Michael Dennis (https://github.com/mdennis281)
# Created: 09-26-2019
# Project Repository: https://github.com/mdennis281/Python-Cloudflare-DNS-External-IP-Synchronizer
# License: MIT (https://en.wikipedia.org/wiki/MIT_License)
from assets.logger import log
import requests, re, random

#Uses regex to parse webpage for the external IP address
#Has multiple hosts to check ip against, if all hosts fail to return an IP
#it will then raise an exception.
def get():
    def makeCall(source):
        r = requests.get(source)
        r.raise_for_status()
        return r.text

    sources = [
        'http://checkip.dyndns.com',
        'https://api.ipify.org',
        'https://ip.seeip.org/'
    ]

    ip = ''

    # While IP address has not been found and there
    # are still sources that have not been used.
    while (not ip) and sources:
        url = sources.pop(random.randint(0,len(sources)-1))
        try:
            page = makeCall(url)
            regex = '\\b\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\b' #regex matching IP address
            ip = re.search(regex,page).group(0)
            return ip
        except Exception as err:
            log('Unable to parse IP from: ' + url +' | '+repr(err))

    e = 'NETWORK ERROR: Could not determine public IP.'
    log(e)
    raise Exception(e)
