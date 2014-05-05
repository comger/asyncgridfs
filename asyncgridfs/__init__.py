# -*- coding:utf-8 -*- 
#!/usr/bin/env python
"""
    author comger@gmail.com
    async mongodb gridfs with tornado IOLoop
"""
import asyncmongo
from tornado import gen
from functools import partial
from bson.py3compat import StringIO
from bson.binary import Binary

chunks_coll = lambda coll: '%s.chunks' % coll
files_coll = lambda coll: '%s.files' % coll


def initcallback(callback, res, error):
    if error:raise error
    callback(res)

class GridFS(object):
    def __init__(self, client, root_collection='fs'):
        assert isinstance(client, asyncmongo.Client)
        assert isinstance(root_collection,(str,unicode))
        self.client = client
        self.root_collectin = root_collection
    

    def get(self, fid, callback=None):
        out = GridOut(self.client,self.root_collectin,fid)
        out.read(callback=callback)


class GridOut(object):

    def __init__(self, client, root_collection, fid):
        self.client = client
        self.root_collection = root_collection
        self.fid = fid
        
    
    def get_file(self, callback):
        """　read fid's file infomation """
        self.__files_coll = self.client.connection(files_coll(self.root_collection))
        func = partial(initcallback,callback)
        self.__files_coll.find_one({"_id": self.fid}, callback=func)

    def read(self,fileobj=None, callback=None):
        """ read a file from gfs include file's infomation and data"""
        if not fileobj:
            func = partial(self.read,callback=callback)
            return self.get_file(callback=func)

        self.__chunks_coll = self.client.connection(chunks_coll(self.root_collection))
        cond = dict(files_id = self.fid)
        def surcor_callback(res,error):
            data = StringIO()
            for item in res:
                data.write(item['data'])
            
            fileobj['data'] = data.read(fileobj['chunkSize'])
            fileobj['data'] = 'xxx' 
            callback(fileobj)

        self.__chunks_coll.find(cond,callback=surcor_callback)


    def list(self, callback=None):
        """ list all filename in gfs db """
        self.client.command('distinct',files_coll(self.root_collection), key='filename', callback=callback)

    def find(self,*args, **kwargs):
        pass

