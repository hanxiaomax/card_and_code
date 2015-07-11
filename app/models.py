#coding:utf-8
from app import app,db
import os
import qrcode
from PIL import Image
from datetime import datetime
qrcode_folder = app.config["QRCODES_FOLDER"]
class User(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(32),index = True,unique = True)
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
    logoText = db.Column(db.String(128),index = True)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.name)


    @classmethod
    def addUser(cls,username):
        u=User(username=username)
        db.session.add(u)
        db.session.flush()
        user_id=u.id
        db.session.commit()
        return user_id

    @classmethod
    def deleteUser(cls,username):
        print "1"
        u=cls.isExist(username)
        print "2"
        if u :
            for i in u.contact.all():
                db.session.delete(i)
            for i in u.friendship.all():
                db.session.delete(i)
            for i in u.shipAddress.all():
                db.session.delete(i)
            db.session.delete(u)
            db.session.commit()
            return True
        else:
            return False


    @classmethod
    def isExist(cls,username):
        user = cls.query.filter(db.or_(User.username==username)).first()
        print user
        return user if user else False


    @classmethod
    def getUser(cls,id):
        user = cls.query.filter(db.or_(User.id==id)).first()
        return user
    @classmethod
    def clear(cls,user):
        user.corp = None
        user.position = None
        user.name = None
        if user.logo and os.path.exists(user.logo):
            os.remove(user.logo)
            user.logo = None
        if user.headpic and os.path.exists(user.headpic):
            os.remove(user.headpic)
            user.headpic = None
        if user.qrcode and os.path.exists(user.qrcode):
            os.remove(user.qrcode)
            user.qrcode = None
        contacts =Contact.query.filter(Contact.user_id==user.id).all()

        for c in contacts:
            db.session.delete(c)
        db.session.commit()

    def makeQrcode(self,user,qrlogo=None):


        qr = qrcode.QRCode(
            version=5,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data("http://weibo.com/smilingly1989?wvr=3.6&lf=reg")
        qr.make(fit=True)
        img = qr.make_image()
        time = str(datetime.today()).replace(" ","_").replace(":","_").replace(".","_")
        path = app.config["QRCODES_FOLDER"]+"/"+str(user.id)+time+".png"

        if  qrlogo and os.path.exists(qrlogo) :
            img = img.convert("RGBA")
            icon = Image.open(qrlogo)
            # icon = img.convert('RGBA')
            img_w, img_h = img.size
            factor = 4
            size_w = int(img_w / factor)
            size_h = int(img_h / factor)
            icon_w, icon_h = icon.size
            if icon_w > size_w:
                icon_w = size_w
            if icon_h > size_h:
                icon_h = size_h
            icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)
            icon = icon.convert("RGBA")
            w = int((img_w - icon_w) / 2)
            h = int((img_h - icon_h) / 2)
            img.paste(icon, (w, h), icon)
            img.save(path)
        else:
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

    @classmethod
    def getAdd(cls,index):
        print "22"
        return Ship_Address.query.filter(db.or_(cls.id==int(index))).first()
