from flask import render_template,request,redirect,url_for,jsonify
from models import Contact,Friend_Ship,User
from app import app,db

class Tools(object):
    @classmethod
    def getcarddetail(cls,user_id):
        user = User.getUser(user_id)
        c = Contact.query.filter(db.or_(user_id==user_id)).all()
        info=[]
        intro=[]
        custom=[]
        for item in c:
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
        "custom":custom
        }
        print dic["info"]
        return jsonify(dic)


