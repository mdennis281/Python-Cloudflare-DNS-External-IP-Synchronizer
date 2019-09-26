from assets.config import load as config
import time as t

def log(message):
    if config()['general']['loggingEnabled']:
        time = t.strftime('%Y-%m-%d %H:%M:%S',t.localtime())
        f = open(config()['general']['logPath'],'a')
        f.write(time+'\t'+message+'\n')
        f.close()
