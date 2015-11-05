#!/usr/bin/env python
import requests, os, sys

# path to the parent directory of the iiify.py application
project_root = os.path.dirname(os.path.abspath(__file__))

if False:
    # path to where media is stored - make it if it doesn't exist
    media_root = os.path.join(project_root, 'media')
    if not os.path.exists(media_root):
        os.makedirs(media_root)

if False:
    # path to where the disk cache is stored - make it if it doesn't exist
    cache_root = os.path.join(project_root, 'cache')
    if not os.path.exists(cache_root):
        os.makedirs(cache_root)

# path to where the disk cache is stored - make it if it doesn't exist
static_root = os.path.join(project_root, 'static')
if not os.path.exists(static_root):
    os.makedirs(static_root)