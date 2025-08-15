# Author: Michael Dennis (https://github.com/mdennis281)
# Created: 09-26-2019
# Project Repository: https://github.com/mdennis281/Python-Cloudflare-DNS-External-IP-Synchronizer
# License: MIT (https://en.wikipedia.org/wiki/MIT_License)
"""Entry point for syncing the current IP with Cloudflare DNS."""

from assets.cloudflare import CloudFlare


def main():
    """Execute the DNS update process."""
    CloudFlare().update_record()


if __name__ == "__main__":
    main()

