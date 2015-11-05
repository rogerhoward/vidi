#!/usr/bin/env python
import requests, os, sys
url_base = ''

from config import *


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
        with open(path, 'rb') as this_file:
            body_data = this_file.read()
        r = requests.put(url, data=body_data, headers={'content-type': 'image/jpeg'})
        return r.json()

    def clear(self):
        url = '%s/index/io' % (self.url)
        print(url)
        body_data = {"type": "CLEAR"}
        r = requests.post(url, json=body_data)
        return r.json()

    def bulk(self, path, start=1):
        url = '%s/index/io' % (self.url)
        print('url: %s' % url)

        for directory, directories, files in os.walk(path):
            for filename in files:
                file_path = os.path.join(directory, filename)
                if filename.endswith('.jpg'):
                    self.add(file_path, start)
                    start += 1

        body_data = {"type": "WRITE", "index_path": path}
        r = requests.post(url, json=body_data)
        return r.json()

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