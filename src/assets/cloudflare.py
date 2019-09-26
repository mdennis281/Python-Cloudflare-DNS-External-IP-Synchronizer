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
            log(err)
            raise Exception(err)

        err = (
            'ZONE ERROR: The zone: "'+
            self.settings['API']['siteName']+
            '" Does not exist!'
        )
        log(err)
        raise Exception(err)

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
            log(err)
            raise Exception(err)

        self.recordID = None
        self.recordIP = None

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
                log('DNS Record IP Updated to: '+IP+' (old: '+self.recordIP+')')
                return True
            else:
                err= 'CLOUDFLARE ERROR: '+response.json()['errors'][0]['message']
                log(err)
                raise Exception(err)
        elif self.recordIP != IP:
            self.createRecord()
        else:
            log('Current public IP matches DNS Record')

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
            log('DNS Record created to: '+IP)
            return True
        else:
            err= 'CLOUDFLARE ERROR: '+response.json()['errors'][0]['message']
            log(err)
            raise Exception(err)
