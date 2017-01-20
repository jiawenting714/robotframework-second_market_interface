#  Copyright (c) 2010 Franz Allan Valencia See
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import pymongo
from bson.objectid import ObjectId
import datetime
from time import sleep

__version__ = '0.1'
class MyMongodbLibrary(object):
    ROBOT_LIBRARY_SCOPE = 'TEST CASE'
    ROBOT_LIBRARY_VERSION = '0.1'

    def __init__(self):

        self._connect = None
        self._db = None
        self._collection = None

    def objectid(self,_id):
        '''
        return the ObjectId(_id)

        | objectid | 559205e644721a2c26d11084 |
        '''
        return ObjectId(_id)

    def create_datetime(self,year, month, day, hour=0, minute=0, second=0, microsecond=0, tzinfo=None):
        '''
        return the datetime object

        | create datetime | 2016 | 07 | 01 | 12 | 12 | 12 |
        '''
        try:
            year = int(year)
            month = int(month)
            day = int(day)
            hour = int(hour)
            minute = int(minute)
            second = int(second)
        except:
            pass
        return datetime.datetime(year,month,day,hour,minute,second,microsecond,tzinfo)

    def connect_mongodb(self,host,port=None,database="test",username=None,password=None,**kwargs):

        '''
        connect mongodb with host port,and select database <database>

        | connect mongodb | localhost |
        | connect mongodb | localhost | 27017 | test |
        '''
        #mongodb://gfactivity:gfactivity@10.2.124.15:27017/gfactivity
        #hostUrl:mongodb://[username:password@]hostIp:port/database

        host_url = "mongodb://"
        if username:
            host_url = host_url+username+":"
        if password:
            host_url = host_url+password+"@"
        if host:
            host_url = host_url+host+":"
        if port:
            host_url = host_url+str(port)+"/"
        else:
            host_url = host_url+"27017"+"/"
        if database:
            host_url = host_url+database

        try:
            if port is not None:
                port = int(port)
            self._connect = pymongo.MongoClient(host_url,port,maxPoolSize=200,socketKeepAlive=True)
            self._db = self._connect.get_database(database)
        except:
            raise AssertionError("connect mongodb error,please "
                                 "check host,port database is correct!")

    def select_collection(self,collection):

        '''
        select collection that the name is <collection>

        | select collection | user | #select collection named <user>
        '''
        self._collection = self._db.get_collection(collection)

    def find(self,filter_,projection=None,one_or_multi="m",*args, **kwargs):

        '''
        Query the database
        if one_or_multi == 'o' or 'one' Get a single document from the database that matched the filter
        else one_or_multi == 'm' or 'multi' get all document from the database that matched the filter

        return the list of matched results

        | find | {"name":"zhangsan"} | one |
        | find | {"name":"zhangsan"} | multi|
        '''

        dic_kwargs = {}
        dic_kwargs.setdefault("projection",projection)
        kwargs.update(dic_kwargs)

        result = []

        if str(one_or_multi).lower() == "o" or str(one_or_multi).lower() == "one":
            try:
                cursor_one = self._collection.find_one(filter_,**kwargs)
            except:
                sleep(2)
                cursor_one = self._collection.find_one(filter_,**kwargs)
            result.append(cursor_one)
            return result
        elif str(one_or_multi).lower() == "m" or str(one_or_multi).lower() == "multi":
            try:
                cursor = self._collection.find(filter_,**kwargs)
            except:
                sleep(2)
                cursor = self._collection.find(filter_,**kwargs)
            for c in cursor:
                result.append(c)
            return result
        else:
            raise AssertionError("find parameter error:must be 'o' or 'one' and 'm' or 'multi'")

    def delete(self,filter_,one_or_multi="m"):
        '''
        if one_or_multi == 'one' or 'o' Delete a single document matching the filter
        else if one_or_multi = 'm' or 'multi' Delete one or more documents matching the filter

        | delete | {"name":"zhangsan"} | one |
        | delete | {"name":"zhangsan"} | multi|

        return tuple (acknowledged,raw_result) like (true,{ok:1,n:0})

        '''

        if filter_.has_key("_id") and str(filter_.get("_id")).startswith("ObjectId"):
            value = eval(filter_.get("_id"))
            filter_["_id"] = value

        if str(one_or_multi).lower() == "o" or str(one_or_multi).lower() == "one":
            print filter_
            try:
                delete_one = self._collection.delete_one(filter_)
            except:
                sleep(2)
                delete_one = self._collection.delete_one(filter_)
            return (delete_one.acknowledged,delete_one.raw_result)
        elif str(one_or_multi).lower() == "m" or str(one_or_multi).lower() == "multi":
            try:
                delete_multi = self._collection.delete_many(filter_)
            except:
                sleep(2)
                delete_multi = self._collection.delete_many(filter_)
            return (delete_multi.acknowledged,delete_multi.raw_result)
        else:
            raise AssertionError("delete parameter error:must be 'o' or 'one' and 'm' or 'multi'")

    def update(self,filter_,update,one_or_multi="m"):
        '''
        if one_or_multi == 'one' or 'o' Delete a single document matching the filter
        else if one_or_multi = 'm' or 'multi' Delete one or more documents matching the filter

        | update | {"name":"zhangsan"} | {'$inc': {'x': 3}} | one |
        | update | {"name":"zhangsan"} | {'$inc': {'x': 3}}| multi |

        return tuple (acknowledged,raw_result) like (true,{ok:1,n:0})
        '''
        if filter_.has_key("_id") and str(filter_.get("_id")).startswith("ObjectId"):
            value = eval(filter_.get("_id"))
            filter_["_id"] = value
        if str(one_or_multi).lower() == "o" or str(one_or_multi).lower() == "one":
            print filter_
            try:
                update_one = self._collection.update_one(filter_,update)
            except:
                sleep(2)
                update_one = self._collection.update_one(filter_,update)
            return update_one
        elif str(one_or_multi).lower() == "m" or str(one_or_multi).lower() == "multi":
            try:
                update_many = self._collection.update_many(filter_,update)
            except:
                sleep(2)
                update_many = self._collection.update_many(filter_,update)
            return update_many
        else:
            raise AssertionError("delete parameter error:must be 'o' or 'one' and 'm' or 'multi'")

    def close_connection(self):
        """Disconnect from MongoDB"""
        if self._connect:
            self._connect.close()

if __name__ == '__main__':
    mongo = MyMongodbLibrary()
    # mongo.connect_mongodb("mongodb://gfactivity:gfactivity@10.2.124.15",27017,'gfactivity')
    mongo.connect_mongodb("10.2.124.15",27017,'gfactivity','gfactivity','gfactivity')
    mongo.select_collection("marketing_activity")
    results = mongo.find({"activity_name":"www"})
    print results
    '''

    import paramiko
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("10.2.64.14",22,"gf","gf37888676")
    stdin,stdout,stderr = ssh.exec_command('mongo 10.2.64.14/gfwealth C:\Users\Administrator\Desktop\test.js')
    for o in stdout.readlines():
        print o
    #554efd6d3bf8fc1e00b4376f
    '''
