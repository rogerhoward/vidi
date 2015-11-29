#!/usr/bin/env python
import requests, os, sys
url_base = ''
from PIL import Image
import StringIO
# from config import *
import config
from db import Picture, getmd5

class Server(object):
    """A pastec server object:

    Attributes:
        image: a Pillow Image object.
        info: a dictionary providing image metadata
    """

    commands = ['add','search','ping', 'save', 'load', 'clear', 'bulk']


    def __init__(self, host='locahost', port=8001):
        """Return a Server object."""
        self.host = host
        self.port = port
        self.url = 'http://%s:%s' % (self.host, self.port)

    def ping(self):
        url = '%s/' % (self.url)
        print(url)
        r = requests.post(url, data={'type': 'PING'})
        return r.json()

    def add(self, path, id):
        url = '%s/index/images/%s' % (self.url, id)
        print(url)
        file_path_md5 = getmd5(path)
        this_image = Image.open(path)
        tmp_filename = '%s.%s' % (file_path_md5, 'jpg')
        tmp_path = os.path.join(config.tmp_root, tmp_filename)

        if (this_image.width > config.max_dim) or (this_image.height > config.max_dim):
            this_image.thumbnail((config.max_dim, config.max_dim), Image.ANTIALIAS)
            this_image.save(tmp_path, 'JPEG', quality=70)

        with open(tmp_path,'rb') as this_file:
            r = requests.put(url, data=this_file, headers={'content-type': 'image/jpeg'})
        return r.json()

    def clear(self):
        url = '%s/index/io' % (self.url)
        print(url)
        body_data = {"type": "CLEAR"}
        r = requests.post(url, json=body_data)
        return r.json()

    def bulk(self, path):
        url = '%s/index/io' % (self.url)
        print('url: %s' % url)

        session = config.DBSession()

        for directory, directories, files in os.walk(path):
            for filename in files:
                file_path = os.path.join(directory, filename)
                if filename.endswith('.jpg'):
                    file_path_md5 = getmd5(file_path)
                    if session.query(Picture).filter(Picture.path_md5 == file_path_md5).count() == 0:
                        new_picture = Picture( path=file_path )
                        session.add(new_picture)
                        session.commit()
                        self.add(file_path, new_picture.id)
                    else:
                        print('skipping, record already exists: %s' % (file_path_md5))

        session.commit()

        # body_data = {"type": "WRITE", "index_path": path}
        # r = requests.post(url, json=body_data)
        return {'status':'success'}

    def save(self, path):
        url = '%s/index/io' % (self.url)
        print(url, path)
        body_data = {"type": "WRITE", "index_path": path}
        r = requests.post(url, json=body_data)
        return r.json()

    def load(self, path):
        url = '%s/index/io' % (self.url)
        print(url, path)
        body_data = {"type": "LOAD", "index_path": path}
        r = requests.post(url, json=body_data)
        return r.json()

    def find(self, path):
        url = '%s/index/searcher' % (self.url)

        with open(path, 'rb') as this_file:
            body_data = this_file.read()
        
        r = requests.post(url, data=body_data, headers={'content-type': 'image/jpeg'})
        return r.json()