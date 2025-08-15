# Author: Michael Dennis (https://github.com/mdennis281)
# Created: 09-26-2019
# Project Repository: https://github.com/mdennis281/Python-Cloudflare-DNS-External-IP-Synchronizer
# License: MIT (https://en.wikipedia.org/wiki/MIT_License)

"""Interface for Cloudflare API operations."""

import requests

from assets.config import load_config
from assets.logger import log
from assets.public_ip import get_public_ip


class CloudFlare:
    """Cloudflare client for managing DNS records."""

    def __init__(self):
        self.settings = load_config()
        self.headers = {
            "Authorization": f"Bearer {self.settings['API']['token']}",
            "Content-Type": "application/json",
        }
        self.api_url = "https://api.cloudflare.com/client/v4/"
        self.get_zone_id()
        self.get_dns_record()

    def get_zone_id(self):
        """Retrieve the zone ID from Cloudflare based on configuration."""

        params = {"name": self.settings["API"]["siteName"]}
        response = requests.get(
            f"{self.api_url}zones", params=params, headers=self.headers, timeout=10
        )
        zones = response.json().get("result", [])

        if zones:
            for zone in zones:
                if zone["name"] == self.settings["API"]["siteName"]:
                    self.zone_id = zone["id"]
                    return zone["id"]

        if not response.json().get("success"):
            err = (
                "CLOUDFLARE ERROR: " + response.json()["errors"][0]["message"]
            )
            log(err, 1)
            raise Exception(err)

        err = (
            "ZONE ERROR: The zone: "
            + self.settings["API"]["siteName"]
            + " Does not exist!"
        )
        log(err, 1)
        raise Exception(err)

    def get_dns_record(self):
        """Get the DNS record ID and existing IP, if any."""

        params = {"name": self.settings["DNS"]["name"]}
        response = requests.get(
            f"{self.api_url}zones/{self.zone_id}/dns_records",
            params=params,
            headers=self.headers,
            timeout=10,
        )
        records = response.json().get("result", [])

        if records:
            for record in records:
                if record["name"] == self.settings["DNS"]["name"]:
                    self.record_id = record["id"]
                    self.record_ip = record["content"]
                    return record["id"]

        if not response.json().get("success"):
            err = (
                "CLOUDFLARE ERROR: " + response.json()["errors"][0]["message"]
            )
            log(err, 1)
            raise Exception(err)

        self.record_id = None
        self.record_ip = None
        return None


    def update_record(self):
        """Update the Cloudflare DNS record or create it if missing."""

        ip_address = get_public_ip()

        if self.record_id and self.record_ip != ip_address:
            payload = {
                "type": self.settings["DNS"]["recordType"],
                "name": self.settings["DNS"]["name"],
                "content": ip_address,
                "proxied": self.settings["DNS"]["proxied"],
            }
            response = requests.put(
                f"{self.api_url}zones/{self.zone_id}/dns_records/{self.record_id}",
                json=payload,
                headers=self.headers,
                timeout=10,
            )
            if response.json().get("success"):
                log(
                    f"DNS Record IP Updated to: {ip_address} "
                    f"(old: {self.record_ip})",
                    2,
                )
                return True

            err = (
                "CLOUDFLARE ERROR: " + response.json()["errors"][0]["message"]
            )
            log(err, 1)
            raise Exception(err)
        elif not self.record_id:  # no existing record
            if self.settings["DNS"]["createRecord"]:
                return self.create_record()
            log(
                "No DNS record exists. set createRecord to True in the config "
                "file to automatically create a new record",
                2,
            )
        else:
            log("Current public IP matches DNS Record", 3)

    def create_record(self):
        """Create a new DNS record in Cloudflare."""

        ip_address = get_public_ip()
        payload = {
            "type": self.settings["DNS"]["recordType"],
            "name": self.settings["DNS"]["name"],
            "content": ip_address,
            "proxied": self.settings["DNS"]["proxied"],
        }

        response = requests.post(
            f"{self.api_url}zones/{self.zone_id}/dns_records/",
            json=payload,
            headers=self.headers,
            timeout=10,
        )

        if response.json().get("success"):
            log(f"DNS Record created to: {ip_address}", 2)
            return True

        err = (
            "CLOUDFLARE ERROR: " + response.json()["errors"][0]["message"]
        )
        log(err, 1)
        raise Exception(err)
