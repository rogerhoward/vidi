#!/usr/bin/env python
import requests, os, sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import Base

max_dim = 600

# path to the parent directory of the iiify.py application
project_root = os.path.dirname(os.path.abspath(__file__))

photo_root = '/Users/rogerhoward/Dropbox/Personal_Photos'

# # path to where media is stored - make it if it doesn't exist
# media_root = os.path.join(project_root, 'media')
# if not os.path.exists(media_root):
#     os.makedirs(media_root)

if False:
    # path to where the disk cache is stored - make it if it doesn't exist
    cache_root = os.path.join(project_root, 'cache')
    if not os.path.exists(cache_root):
        os.makedirs(cache_root)

# path to where tmp files are stored
tmp_root = os.path.join(project_root, 'tmp')
if not os.path.exists(tmp_root):
    os.makedirs(tmp_root)

# path to where the disk cache is stored - make it if it doesn't exist
static_root = os.path.join(project_root, 'static')
if not os.path.exists(static_root):
    os.makedirs(static_root)



engine = create_engine('sqlite:///demo.db', echo=True)
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)