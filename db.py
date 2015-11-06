#!/usr/bin/env python

import os, sys
import hashlib, shutil

#sql alchemy imports
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String , Text
from sqlalchemy import event

engine = create_engine('sqlite:///demo.db', echo=False)
Base = declarative_base()

def getmd5(message):    
    return hashlib.md5(message.encode('utf-8')).hexdigest()
    

def getfilemd5(path):
    md5 = hashlib.md5()
    with open(path,'rb') as f: 
        for chunk in iter(lambda: f.read(8192), b''): 
             md5.update(chunk)
    return md5.hexdigest()


class Picture(Base):
    '''
    A model representing an image saved into the pastec index
    '''
    __tablename__ = 'picture'

    id = Column(Integer, primary_key=True)
    path = Column(Text())
    path_md5 = Column(String(32), index=True)

    def __repr__(self):
        return "<Trainable(content = %s , score = %s)>" % (self.content, self.score)


def before_insert_listener(mapper, connection, target):
    # 'target' is the inserted object
    print('input file: %s' % (target.path))
    if target.path and target.path_md5 is None:
        target.path_md5 = getmd5(target.path)

event.listen(Picture, 'before_insert', before_insert_listener)



Base.metadata.create_all(engine)

if __name__ == '__main__':
    print 'db.py is initializing...'

