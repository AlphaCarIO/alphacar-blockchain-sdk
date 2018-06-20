# -*- coding: utf-8 -*-
import ipfsapi

DEFAULT_CONF = {
    'host' : '127.0.0.1',
    'port': 5001,
}

class IPFSWrapper(object):

    def __init__(self, conf = DEFAULT_CONF):
        self.client = ipfsapi.Client(conf['host'], conf['port'])

    def id(self):
        return self.client.id()

    def addJsonData(self, jsonObj):
        return self.client.add_json(jsonObj)

if __name__ == "__main__":

    api = IPFSWrapper()
    
    print(api.id())
