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
            new_conf = DEFAULT_CONF.copy()
            new_conf.update(conf)

            self.conn = pymongo.MongoClient(new_conf['host'], new_conf['port'])
            self.reCreated = new_conf['reCreated']
            if self.reCreated:
                self.conn.drop_database(new_conf['db_name'])
            self.db = self.conn[new_conf['db_name']]
            self.username=new_conf['username']
            self.password=new_conf['password']
            if self.username and self.username != '' and self.password and self.password != '' :
                self.connected = self.db.authenticate(self.username, self.password)
            else:
                self.connected = True
        except Exception:
            print(traceback.format_exc())
            print('Connect Statics Database Fail.')
            sys.exit(1)
