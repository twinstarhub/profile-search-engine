# -*- encoding: utf-8 -*-
"""
Patterns Model

"""
from apps import db

class Patterns(db.Model):

    __tablename__ = 'tb_patterns'

    id            = db.Column(db.Integer, primary_key=True)
    type          = db.Column(db.Integer)
    pattern       = db.Column(db.String(64))
    rank          = db.Column(db.Integer)
    description   = db.Column(db.String(255))
    
    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            setattr(self, property, value)

    def __repr__(self):
        return str(self.pattern)

class BirthPattern(db.Model):

    __tablename__ = 'tb_birthpattern'

    id            = db.Column(db.Integer, primary_key=True)
    pattern       = db.Column(db.String(64), unique=True)
    description   = db.Column(db.String(255))
    
    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            setattr(self, property, value)

    def __repr__(self):
        return str(self.pattern)
