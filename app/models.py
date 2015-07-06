#coding:utf-8
from app import app,db
import os
import qrcode
class User(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(16),index = True,unique = True)
    password = db.Column(db.String(32),index = True)
    friendship = db.relationship('Friend_Ship',backref='user',lazy = 'dynamic')
    contact = db.relationship('Contact',backref='user',lazy = 'dynamic')
    shipAddress = db.relationship('Ship_Address',backref='user',lazy = 'dynamic')
    position = db.Column(db.String(32),index = True)
    corp = db.Column(db.String(32),index = True)
    name = db.Column(db.String(32),index = True)
    qrcode = db.Column(db.String(128),index = True)
    headpic = db.Column(db.String(128),index = True)
    logo = db.Column(db.String(128),index = True)

    def is_authenticated():
        return True

    @classmethod
    def getUser(cls,id):
        user = cls.query.filter(db.or_(User.id==id)).first()
        return user
    @classmethod
    def clear(cls,user):
        contacts =Contact.query.filter(Contact.user_id==user.id).all()
        for c in contacts:
            db.session.delete(c)
        db.session.commit()

    def makeQrcode(self,user):
        qr = qrcode.QRCode(
            version=5,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data("http://weibo.com/smilingly1989?wvr=3.6&lf=reg")
        qr.make(fit=True)
        img = qr.make_image()
        path = app.config["QRCODES_FOLDER"]+"/"+str(user.id)+".png"

        img.save(path)
        self.qrcode = path
        db.session.commit()

        return True

class Friend_Ship(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    friend_id = db.Column(db.Integer,unique = True)

class Contact(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(32))
    text = db.Column(db.String(128))
    _type = db.Column(db.String(32))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    index = db.Column(db.Integer)

class Ship_Address(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(32))
    phone = db.Column(db.String(128))
    address = db.Column(db.String(32))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

