#!/usr/bin/env python

from flask import Flask, Response, send_file, jsonify, abort, request
import StringIO, os, re, requests, urllib
import simplejson as json

from vidi import Server
import config

app = Flask(__name__)

# # http://127.0.0.1:5000/g9_20090806_0143.jpg/full/600,/!90/80.jpg
# @app.route('/static/<path:asset>')
# def static_asset(asset):
#     static_asset_path = os.path.join()
#     return send_file(static_asset_path)
#     print 'static_asset: %s' % (static_asset_path)


# http://127.0.0.1:5000/g9_20090806_0143.jpg/full/600,/!90/80.jpg
@app.route('/images/')
def images():
    image_list = []
    for directory, directories, files in os.walk(config.photo_root):
        for filename in files:
            file_path = os.path.join(directory, filename)
            if filename.endswith('.jpg'):
                image_list.append(file_path)

    return '<br>\n'.join(image_list)



@app.after_request
def add_header(response):
    # Force upstream caches to refresh at 100 minute intervals
    response.cache_control.max_age = 100
    # Enable CORS to allow cross-domain loading of tilesets from this server
    # Especially useful for SeaDragon viewers running locally
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

if __name__ == '__main__':
    print('launching server...')

    app.debug = True
    app.run(port=9000)
