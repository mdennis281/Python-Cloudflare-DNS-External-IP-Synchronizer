# Author: Michael Dennis (https://github.com/mdennis281)
# Created: 09-26-2019
# Project Repository: https://github.com/mdennis281/Python-Cloudflare-DNS-External-IP-Synchronizer
# License: MIT (https://en.wikipedia.org/wiki/MIT_License)

from assets.config import load as config
import time as t

def log(message,logLevel=3):
    if config()['general']['loggingEnabled']:
        if config()['general']['logLevel'] >= logLevel:
            time = t.strftime('%Y-%m-%d %H:%M:%S',t.localtime())
            f = open(config()['general']['logPath'],'a')
            f.write(time+'\t'+message+'\n')
            f.close()
