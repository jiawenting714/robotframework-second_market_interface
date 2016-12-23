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


__version__ = '0.1'
class MyMongodbLibrary(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
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

        try:
            if port is not None:
                port = int(port)
            self._connect = pymongo.MongoClient(host,port)
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
            cursor_one = self._collection.find_one(filter_,**kwargs)
            result.append(cursor_one)
            return result
        elif str(one_or_multi).lower() == "m" or str(one_or_multi).lower() == "multi":
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
            delete_one = self._collection.delete_one(filter_)
            return (delete_one.acknowledged,delete_one.raw_result)
        elif str(one_or_multi).lower() == "m" or str(one_or_multi).lower() == "multi":
            delete_multi = self._collection.delete_many(filter_)
            return (delete_multi.acknowledged,delete_multi.raw_result)
        else:
            raise AssertionError("delete parameter error:must be 'o' or 'one' and 'm' or 'multi'")


if __name__ == '__main__':

    mongo = MyMongodbLibrary()
    #mongo.connect_mongodb("10.2.130.194",database="gfwealth")
    mongo.connect_mongodb("localhost",database="gfwealth")
    mongo.select_collection("push")

    #result = mongo.find({"shopId":"559205e644721a2c26d11084","deleted":0},{"stats":1,"title":1},'o')
    #print result

    strs = ObjectId("573a8e75d24d401800cc4a20")
    result = eval('strs')
    print result.__repr__()
    result_del = mongo.delete({"_id":"ObjectId('573a8e75d24d401800cc4a20')"})
    print result_del

    dt = mongo.create_datetime("2016","07","01")
    print dt
    #10.2.130.194


    #client = pymongo.MongoClient("10.2.130.194")
    client = pymongo.MongoClient("localhost")
    db = client.get_database("gfwealth")
    collect = db.get_collection("push")
    cur = collect.find({"shopId":"559205e644721a2c26d11084","deleted":0})
    print cur.count()


    cur2 = collect.find_one({"shopId":"559205e644721a2c26d11084","deleted":0,"createAt":{"$gt":datetime.datetime(2016,06,14)}})
    print cur2

    cur3 = collect.find({'_id': ObjectId('575fd550170ce01100ce533f'), 'createAt': '{"$gt":}'})

    delete = collect.delete_one({"_id":result})
    print delete.acknowledged,delete.raw_result
    delete2 = collect.delete_many({"_id":123})
    print (delete2.acknowledged,delete2.raw_result)



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







































