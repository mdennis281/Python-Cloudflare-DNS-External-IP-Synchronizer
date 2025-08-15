# Author: Michael Dennis (https://github.com/mdennis281)
# Created: 09-26-2019
# Project Repository: https://github.com/mdennis281/Python-Cloudflare-DNS-External-IP-Synchronizer
# License: MIT (https://en.wikipedia.org/wiki/MIT_License)

from configparser import ConfigParser


def load_config():
    """Load configuration values from config.ini into a dictionary."""

    parser = ConfigParser()
    parser.read("config.ini")

    settings = {
        "general": {
            "logPath": parser.get(
                "general", "logPath", fallback="..\\CF-DNS.log"
            ),
            "loggingEnabled": parser.getboolean(
                "general", "loggingEnabled", fallback=False
            ),
            "logLevel": parser.getint("general", "logLevel", fallback=2),
        },
        "API": {
            "token": parser.get("CloudFlare-API", "token", fallback=""),
            "siteName": parser.get("CloudFlare-API", "siteName", fallback=""),
        },
        "DNS": {
            "name": parser.get("DNS", "name", fallback=""),
            "recordType": parser.get("DNS", "recordType", fallback="A"),
            "proxied": parser.getboolean("DNS", "proxied", fallback=False),
            "createRecord": parser.getboolean(
                "DNS", "createRecord", fallback=True
            ),
        },
    }
    return settings
