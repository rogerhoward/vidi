#!/usr/bin/env python

import os, sys

#sql alchemy imports
from sqlalchemy import #!/usr/bin/env python
'''
this is where we declare our database
'''
import os
import sys

#sql alchemy imports
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String , Text


engine = create_engine('sqlite:///demo.db', echo=False)
Base = declarative_base()


class SavedImage(Base):
    '''
    A model representing an image saved into the pastec index
    '''
    __tablename__ = 'trainable'

    id = Column(Integer, primary_key=True)
    path = Column(Text())
    score = Column(String(16))

    def __repr__(self):
        return "<Trainable(content = %s , score = %s)>" % (self.content, self.score)


Base.metadata.create_all(engine)


if __name__ == '__main__':
    print 'i am working'

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String , Text


engine = create_engine('sqlite:///sentimentstore.db', echo=False)

Base = declarative_base()


class Trainable(Base):
    '''
    declaring the data base for featueto start buliding cit-corpus for a are diffrent database
    '''
    __tablename__ = 'trainable'

    id = Column(Integer, primary_key=True)
    content = Column(Text())
    score = Column(String(16))

    def __repr__(self):
        return "<Trainable(content = %s , score = %s)>" % (self.content, self.score)


Base.metadata.create_all(engine)


if __name__ == '__main__':
    print 'i am working'
