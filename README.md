asyncgridfs
===========

async mongo gridfs for tornado


Installation
------------

Installing: `pip install asyncgridfs` or ` easy_install asyncgridfs`


Usage 
-----

    import asyncmongo
    import tornado.web
    from asyncgridfs import GridFS
    
    class Handler(tornado.web.RequestHandler):
        @property
        def db(self):
            if not hasattr(self, '_db'):
                self._db = asyncmongo.Client(pool_id='mydb', host='127.0.0.1', port=27017, maxcached=10, maxconnections=50, dbname='test')
            return self._db
    
        @tornado.web.asynchronous
        def get(self):
            fid = self.get_argument('fid')
            fs = GridFS(self.db)
            fs.get(ObjectId(fid),callback=self._on_get)
            

        @tornado.web.asynchronous
        def post(self):
            f = self.request.files['imgFile'][0]
            content = f.pop('body')
            content_type = f.pop('content_type')
            filename = f.pop('filename')

            fs = GridFS(self.db)
            fs.put(content, contentType=content_type, filename=filename, callback=self._on_post)

    
        def _on_get(self, fileobj):
        	self.set_header('Content-Type', fileobj['contentType'])
        	self.write(fileobj['data'])
        	self.finish()
            
        def _on_put(self, _id):
        	self.write(str(_id))
        	self.finish()

