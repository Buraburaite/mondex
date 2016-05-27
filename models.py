# -*- coding: utf-8 -*-

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.mutable import Mutable

class MutableList(Mutable, list):
        
    @classmethod
    def coerce(cls, key, value):
        if not isinstance(value, MutableList):
            if isinstance(value, list):
                return MutableList(value)
            value = Mutable.coerce(key, value)

        return value   
        
    def __getitem__(self, key):
        value = list.__getitem__(self, key)

        for obj, key in self._parents.items():
            value._parents[obj] = key

        return value

    def __setitem__(self, key, value):
        old_value = list.__getitem__(self, key)
        for obj, key in self._parents.items():
            old_value._parents.pop(obj, None)

        list.__setitem__(self, key, value)
        for obj, key in self._parents.items():
            value._parents[obj] = key

        self.changed()

    def __getstate__(self):
        return list(self)

    def __setstate__(self, state):
        self[:] = state

class MutableDict(Mutable, dict):
    @classmethod
    def coerce(cls, key, value):

        if not isinstance(value, MutableDict):
            if isinstance(value, dict):
                return MutableDict(value)

            return Mutable.coerce(key, value)
        else:
            return value

    def __setitem__(self, key, value):

        dict.__setitem__(self, key, value)
        self.changed()

    def __delitem__(self, key):

        dict.__delitem__(self, key)
        self.changed()
    
    def __getstate__(self):
        return dict(self)

    def __setstate__(self, state):
        self.update(state)

db=SQLAlchemy()

class User(db.Model):
    
    __tablename__="users"
    
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String, unique=True, nullable=False)
    password=db.Column(db.String, nullable=False)
    monNames=db.Column(MutableList.as_mutable(db.PickleType))
    
    def __init__(self, username, password, monNames=MutableList()):
        self.username=username
        self.password=password
        self.monNames=monNames
        
    def __repr__(self):
        return '<username is: "{}"'.format(self.username)

class DEXmon(db.Model):
    
    __tablename__="mons"
    
    id=db.Column(db.Integer, primary_key=True)
    mon=db.Column(db.String(25), nullable=False)
    indexNumber=db.Column(db.String(5), nullable=False)
    fullName=db.Column(db.String(25), nullable=False)
    status=db.Column(MutableDict.as_mutable(db.PickleType))
    
    
    def __init__(self, mon, indexNumber):
        self.mon=mon.lower()
        self.indexNumber=indexNumber
        self.fullName=mon
        self.status=MutableDict()
        
    def __repr__(self):
        return self.fullName