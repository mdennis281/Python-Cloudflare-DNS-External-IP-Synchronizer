# Author: Michael Dennis (https://github.com/mdennis281)
# Created: 09-26-2019
# Project Repository: https://github.com/mdennis281/Python-Cloudflare-DNS-External-IP-Synchronizer
# License: MIT (https://en.wikipedia.org/wiki/MIT_License)
"""Retrieve the machine's public IP address."""

import random
import re

import requests

from assets.logger import log

def get_public_ip():
    """Fetch the public IP address from a list of providers."""

    def make_call(source):
        response = requests.get(source, timeout=10)
        response.raise_for_status()
        return response.text

    sources = [
        "http://checkip.dyndns.com",
        "https://api.ipify.org",
        "https://ip.seeip.org/",
    ]

    ip_address = ""

    # While IP address has not been found and there
    # are still sources that have not been used.
    while not ip_address and sources:
        url = sources.pop(random.randint(0, len(sources) - 1))
        try:
            page = make_call(url)
            ip_regex = r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"
            ip_address = re.search(ip_regex, page).group(0)
            return ip_address
        except Exception as err:  # pylint: disable=broad-except
            log(f"Unable to parse IP from: {url} | {err!r}")

    error_message = "NETWORK ERROR: Could not determine public IP."
    log(error_message, 1)
    raise Exception(error_message)
