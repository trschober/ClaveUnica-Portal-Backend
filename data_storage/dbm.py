# -*- coding: utf-8 -*-
from pymongo import MongoClient
import datetime


class DBM_Repository:

    def __init__(self, host_port, replicaset_name, user, password, db):
        __conn = MongoClient(host=host_port, replicaset=replicaset_name)
        self.__handle = __conn[db]
        self.__handle.authenticate(user, password)

    def delete_session(self, token):
        try:
            self.__handle.front_token_sessions_blacklisted.insert({"token": token, "deleted_datetime": datetime.datetime.now()})
            return True
        except:
            return False

    def find_exist_db_storage(self, collection, field, value):
        try:
            result_object = self.__handle[collection].find_one({field: value})
        except:
            return False
        if result_object is not None:
            del result_object["_id"]
            return result_object
        else:
            return False
