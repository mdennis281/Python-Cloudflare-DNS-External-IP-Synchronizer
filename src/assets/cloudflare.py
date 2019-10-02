# Author: Michael Dennis (https://github.com/mdennis281)
# Created: 09-26-2019
# Project Repository: https://github.com/mdennis281/Python-Cloudflare-DNS-External-IP-Synchronizer
# License: MIT (https://en.wikipedia.org/wiki/MIT_License)

from assets.config import load as config
from assets.logger import log
from assets import publicIP
import requests


class CloudFlare:
    def __init__(self):
        self.settings = config()
        self.headers = headers = {
            'Authorization': 'Bearer ' + self.settings['API']['token'],
            'Content-Type': 'application/json'
        }
        self.apiurl = 'https://api.cloudflare.com/client/v4/'
        self.getZoneID()
        self.getDNSRecord()

    #Gets the ID of zone specified in the config file
    #Returns: zoneID
    #Defines: self.getZoneID
    #This runs on instanciation of the class.
    def getZoneID(self):
        params = {
            'name': self.settings['API']['siteName']
        }
        response = requests.get(
            self.apiurl+'zones',
            params=params,
            headers=self.headers
        )
        zones = response.json().get('result',[])

        if zones:
            for zone in zones:
                if zone['name'] == self.settings['API']['siteName']:
                    self.zoneID = zone['id']
                    return zone['id']

        if not response.json()['success']:
            err='CLOUDFLARE ERROR: '+response.json()['errors'][0]['message']
            log(err,1)
            raise Exception(err)

        err = (
            'ZONE ERROR: The zone: "'+
            self.settings['API']['siteName']+
            '" Does not exist!'
        )
        log(err,1)
        raise Exception(err)

    #Gets the ID of a DNS record specified in the config file
    #Returns: recordID || None
    #Defines: self.recordID, self.recordIP
    #Defines both of the above to none if no record exists
    #This runs on instanciation of the class.
    def getDNSRecord(self):
        params = {
            'name': self.settings['DNS']['name']
        }
        response = requests.get(
            self.apiurl+'zones/'+self.zoneID+'/dns_records',
            params=params,
            headers=self.headers
        )
        records = response.json().get('result',[])

        if records:
            for record in records:
                if record['name'] == self.settings['DNS']['name']:
                    self.recordID = record['id']
                    self.recordIP = record['content']
                    return record['id']

        if not response.json()['success']:
            err = 'CLOUDFLARE ERROR: '+response.json()['errors'][0]['message']
            log(err,1)
            raise Exception(err)

        self.recordID = None
        self.recordIP = None
        return None


    #Updates a DNS Record in CloudFlare
    #Will automatically call "create" if no record exists.
    #Returns: True (will raise exception otherwise)
    #relies on data from the config.ini file
    def updateRecord(self):
        IP = publicIP.get()

        if self.recordID and self.recordIP != IP:
            payload = {
                'type': self.settings['DNS']['recordType'],
                'name': self.settings['DNS']['name'],
                'content': IP,
                'proxied': self.settings['DNS']['proxied'],
            }
            response = requests.put(
                self.apiurl+'zones/'+self.zoneID+'/dns_records/'+self.recordID,
                json=payload,
                headers=self.headers
            )
            if response.json()['success']:
                log('DNS Record IP Updated to: '+IP+' (old: '+self.recordIP+')',2)
                return True
            else:
                err= 'CLOUDFLARE ERROR: '+response.json()['errors'][0]['message']
                log(err,1)
                raise Exception(err)
        elif not self.recordID: #no existing record
            if self.settings['DNS']['createRecord']:
                return self.createRecord()
            log(
                'No DNS record exists. set createRecord to True in the config '+
                'file to automatically create a new record'
            ,2)
        else:
            log('Current public IP matches DNS Record',3)

    #Creates a DNS Record in CloudFlare
    #Returns: True (will raise exception otherwise)
    #relies on data from the config.ini file
    def createRecord(self):
        IP = publicIP.get()
        payload = {
            'type': self.settings['DNS']['recordType'],
            'name': self.settings['DNS']['name'],
            'content': IP,
            'proxied': self.settings['DNS']['proxied'],
        }

        response = requests.post(
            self.apiurl+'zones/'+self.zoneID+'/dns_records/',
            json=payload,
            headers=self.headers
        )

        if response.json()['success']:
            log('DNS Record created to: '+IP,2)
            return True
        else:
            err= 'CLOUDFLARE ERROR: '+response.json()['errors'][0]['message']
            log(err,1)
            raise Exception(err)
