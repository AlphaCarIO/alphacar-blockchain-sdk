# -*- coding: utf-8 -*-
import pymongo
import sys
import traceback

class Singleton(object):
    
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kwargs)
        return cls._instance

class MongoWrapper(object):

    DEFAULT_CONF = {
        'host': '127.0.0.1',
        'port': 27017,
        'db_name': 'alphacar',
        'max_pool_size': 10,
        'timeout': 10,
        'username': None,
        'password': None,
        'reCreated': False,
    }

    def __init__(self, conf = DEFAULT_CONF):
        new_conf = self.DEFAULT_CONF.copy()
        new_conf.update(conf)
        self.host = new_conf['host']
        self.port = new_conf['port']
        self.max_pool_size = new_conf['max_pool_size']
        self.timeout = new_conf['timeout']
        self.conn = pymongo.MongoClient(self.host, self.port, 
            maxPoolSize = self.max_pool_size, connectTimeoutMS = 60 * 60 * self.timeout)

    def connect_db(self, db_name, username = '', password = '') :
        try:
            self.db = self.conn[db_name]
            self.username = username
            self.password = password
            if self.username and self.username != '' and self.password and self.password != '' :
                self.connected = self.db.authenticate(self.username, self.password)
            else:
                self.connected = True
            return True
        except Exception:
            print(traceback.format_exc())
            print('Connect Statics Database Fail.')
        return False

    def close(self):
        if self.conn:
            self.conn.close()

    def drop_database(self, db_name):

        if self.connected:
            self.conn.drop_database(db_name)
            return True

        return False

    def create_index(self, collection_name, inds = [], unique = True):

        if self.connected and len(inds) > 0:
            self.db[collection_name].create_index(inds, unique = unique)
            self.close()
            return True

        return False

    def insert_data(self, collection_name, datas):

        try:
            if self.connected and datas != None:
                self.db[collection_name].insert(datas)
                self.close()
                return True
        except Exception:
            #print(traceback.format_exc())
            print('insert_data got ex!')

        return False
            