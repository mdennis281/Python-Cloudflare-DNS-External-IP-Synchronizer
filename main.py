# Author: Michael Dennis (https://github.com/mdennis281)
# Created: 09-26-2019
# Project Repository: https://github.com/mdennis281/Python-Cloudflare-DNS-External-IP-Synchronizer
# License: MIT (https://en.wikipedia.org/wiki/MIT_License)

import logging
import sys
import configparser
import os
from src.cloudflare import CloudFlare

# Configure logging
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '../config.ini'))
log_enabled = config.getboolean('general', 'loggingEnabled', fallback=True)
log_level = config.getint('general', 'logLevel', fallback=3)
log_path = config.get('general', 'logPath', fallback='./../CF-DNS.log')

LEVEL_MAP = {3: logging.DEBUG, 2: logging.INFO, 1: logging.ERROR}

if log_enabled:
	os.makedirs(os.path.dirname(log_path) or '.', exist_ok=True)
	logging.basicConfig(
		level=LEVEL_MAP.get(log_level, logging.DEBUG),
		format='%(asctime)s\t%(levelname)s\t%(message)s',
		datefmt='%Y-%m-%d %H:%M:%S',
		handlers=[logging.FileHandler(log_path, encoding='utf-8'), logging.StreamHandler(sys.stdout)]
	)
else:
	logging.basicConfig(handlers=[logging.NullHandler()])

CloudFlare().update_record()