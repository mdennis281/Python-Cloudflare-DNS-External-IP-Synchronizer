# Author: Michael Dennis (https://github.com/mdennis281)
# Created: 09-26-2019
# Project Repository: https://github.com/mdennis281/Python-Cloudflare-DNS-External-IP-Synchronizer
# License: MIT (https://en.wikipedia.org/wiki/MIT_License)

"""Simple logging utility."""

import time

from assets.config import load_config


def log(message, log_level=3):
    """Write a message to the log file if enabled and level permits."""

    settings = load_config()
    if settings["general"]["loggingEnabled"]:
        if settings["general"]["logLevel"] >= log_level:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            with open(
                settings["general"]["logPath"], "a", encoding="utf-8"
            ) as log_file:
                log_file.write(f"{timestamp}\t{message}\n")
