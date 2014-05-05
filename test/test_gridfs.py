import os
import sys
import tornado.ioloop
import logging
import time
import unittest
import asyncmongo

app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if app_dir not in sys.path:
    sys.path.insert(0, app_dir)

from asyncgridfs import GridFS

from bson.objectid import ObjectId

class GridfsTest(unittest.TestCase):

    def setUp(self):
        super(GridfsTest, self).setUp()
        self.db = asyncmongo.Client(pool_id='test_query', host='192.168.111.3', port=27017, dbname='gfs', mincached=3)


    def test_get(self):

        def noop_callback(response):
            print response
            logging.info(response)
            loop = tornado.ioloop.IOLoop.instance()
            # delay the stop so kill cursor has time on the ioloop to get pushed through to mongo
            loop.add_timeout(time.time() + .1, loop.stop)

        
        fs = GridFS(self.db,'fs')
        fs.get(ObjectId('53659ad15319b80b7883f03c'),noop_callback)
        tornado.ioloop.IOLoop.instance().start()
        

if __name__ == '__main__':
    unittest.main()
