# -*- coding: utf-8 -*-
import pymongo
import sys
import traceback

DEFAULT_CONF = {
    'host': '127.0.0.1',
    'port': 27017,
    'db_name': 'alphacar',
    'username': None,
    'password': None,
    'reCreated': False,
}

class Singleton(object):
    
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kwargs)
        return cls._instance

class MongoWrapper(object):

    def __init__(self, conf = DEFAULT_CONF):
        
        try:
            self.conn = pymongo.MongoClient(conf['host'], conf['port'])
            if reCreated:
                self.conn.drop_database(conf['db_name'])
            self.db = self.conn[conf['db_name']]
            self.username=conf['username']
            self.password=conf['password']
            if self.username and self.password:
                self.connected = self.db.authenticate(self.username, self.password)
            else:
                self.connected = True
        except Exception:
            print(traceback.format_exc())
            print('Connect Statics Database Fail.')
            sys.exit(1)
