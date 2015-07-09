#coding:utf-8
from flask import render_template,request,redirect,url_for,jsonify
from models import User
from app import app,db
import os
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
        "logoText":user.logoText if user.logoText else u"Logo字幕（选填）",
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

