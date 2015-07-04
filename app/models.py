#coding:utf-8
from app import db
import os

class User(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(16),index = True,unique = True)
    password = db.Column(db.String(32),index = True)
    friendship = db.relationship('Friend_Ship',backref='user',lazy = 'dynamic')
    contact = db.relationship('Contact',backref='user',lazy = 'dynamic')

    def is_authenticated():
        return True

class Friend_Ship(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    friend_id = db.Column(db.Integer,unique = True)

class Contact(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    catagory = db.Column(db.String(32))
    value = db.Column(db.String(128))


