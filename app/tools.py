#coding:utf-8
from flask import render_template,request,redirect,url_for,jsonify
from models import User,Groups,Contact
from app import app,db
import os

upload_path = app.config["UPLOAD_FOLDER"]

class Tools(object):

    @classmethod
    def getcarddetail(cls,user_id):
        user = User.getUser(user_id)
        # c = Contact.query.filter(db.or_(user_id==user_id)).all()
        info=[]
        intro=[]
        custom=[]
        for item in user.contact.all():
            if item._type == "intro":
                temp={"title":item.title,"text":item.text,"type":item._type}
                intro.append(temp)
            elif item._type == "custom":
                temp={"title":item.title,"text":item.text,"type":item._type}
                custom.append(temp)
            else:
                temp={"title":item.title,"text":item.text,"type":item._type,"index":item.index}
                info.append(temp)

        dic = {
        "name":user.name,
        "corp":user.corp,
        "position":user.position,
        "info":info,
        "intro":intro,
        "custom":custom,
        "logoText":user.logoText if user.logoText else "",
        "headpic":os.path.basename(user.headpic) if user.headpic  else "default_headpic.png",
        "logo":os.path.basename(user.logo) if user.logo  else "default_logo.png",
        "qrcode":os.path.basename(user.qrcode) if user.qrcode  else None
        }
        return jsonify(dic)

    @classmethod
    def getAddressList(cls,user_id):
        user = User.getUser(user_id)
        data={
        "type":"data",
        "datalist":[]
        }
        for item in user.shipAddress.all():
            temp={"name":item.name,"phone":item.phone,"address":item.address,"index":item.id}
            data["datalist"].append(temp)
        return jsonify(data)

    @classmethod
    def getCards_Group(cls,user_id):
        dic={}
        groups=User.getGroups(user_id)
        for g in groups:
            cardlist=[getBrife(card.user_id) for card in Groups.getCards(g)]
            dic[g.groupname]=cardlist
        return dic

    @classmethod
    def makeFakeUser(cls):
        username="testuser"
        u=User(username=username,
                name=u"杨宝玲",
                corp=u"东南大学",
                position=u"学生"
        )
        db.session.add(u)
        db.session.flush()
        user_id=u.id
        db.session.commit()
        return user_id

    @classmethod
    def makeFakeInfo(cls,user_id):

        info=[
        {
        "type":"phone",
        "title":u"手机",
        "text":"15250411234",
        "index":"0"
        },
        {
        "type":"phone",
        "title":u"电话",
        "text":"6656123",
        "index":"1"
        },
        {
        "type":"mail",
        "title":u"邮箱",
        "text":"yang.bl@qq.com",
        "index":"2"
        },
        {
        "type":"link",
        "title":u"网址",
        "text":"http://oriental13.lofter.com",
        "index":"3"
        },
        {
        "type":"address",
        "title":u"地址",
        "text":"上海",
        "index":"4"
        },
        {
        "type":"social",
        "title":u"微信",
        "text":"abao",
        "index":"5"
        }
        ]
        intro={
        "type":"intro",
        "title":u"个人简介",
        "text":"热爱互联网的设计师"
        }
        user = User.getUser(user_id)
        user.headpic = os.path.join(upload_path, "fake_headpic.png")
        user.logo = os.path.join(upload_path,"fake_logo.png")
        user.qrcode = os.path.join(upload_path,"fake_qrcode.png")


        # c = Contact(_type = intro["type"] ,title = intro["title"] , text = intro["text"],user_id=user_id )
        # db.session.add(c)
        # print "@@@"
        # for i in info:
        #     c = Contact(_type = i["type"] ,title = i["title"] , text = i["text"],index = i["index"] ,user_id=user_id )
        #     db.session.add(c)
        print "22"
        db.session.commit()
        print "####"



def getBrife(user_id):
    user = User.getUser(user_id)
    dic = {
    "name":user.name,
    "corp":user.corp,
    "position":user.position,
    "headpic":os.path.basename(user.headpic) if user.headpic  else "default_headpic.png",
    }
    return dic
