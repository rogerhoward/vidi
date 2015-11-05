#!/usr/bin/env python
import requests, os, sys
url_base = ''

from config import *


class Server(object):
    """A subclass of GenericDynamicImage which implements IIIF 2.0-compliant
    behavior:

    Attributes:
        image: a Pillow Image object.
        info: a dictionary providing image metadata
    """

    commands = ['add', 'search']

    def __init__(self, host='locahost', port=8001 ):
        """Return a IIIFImage object minimally initiated by *identifier*
        with additional parameters required to generate dynamic derivatives."""

        self.host = host
        self.port = port
        self.url = 'http://%s:%s' % (self.host, self.port)


    def __unicode__(self):
        """Return image info dictionary based on identifier."""
        return self.url


    def ping(self):
        url = '%s/' % (self.url)

        r = requests.post(url, json={'type':'PING'})

        return r.json()

    def add(self, path, id):
        url = '%s/index/images/%s' % (self.url, id)

        with open(path) as this_file:
            body_data = this_file.read()
            r = requests.put(url, data=body_data, headers={'content-type':'image/jpeg'})

        return r.json()


    def find(self, path):
        url = '%s/index/searcher' % (self.url)

        with open(path) as this_file:
            body_data = this_file.read()
            r = requests.post(url, data=body_data, headers={'content-type':'image/jpeg'})

        return r.json()
