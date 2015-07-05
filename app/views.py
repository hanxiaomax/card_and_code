#coding:utf-8
from flask import render_template,request,redirect,url_for,jsonify
from models import Contact,Friend_Ship,User
from app import app,db
import os
import json
import sqlalchemy.exc
from tools import Tools

upload_path = app.config["UPLOAD_FOLDER"]

@app.route('/index/')
@app.route('/')
def login():
    return "11"

@app.route('/user<int:user_id>_edit/')
def electronic_edit(user_id):
    return render_template("electronic_edit.html",user_id=user_id)

#保存名片信息到数据库
@app.route('/_saveContact/',methods=["GET","POST"])
def saveContact():
    user_id = int(request.form['id'])
    info = json.loads(request.form["info"])
    intro = json.loads(request.form["intro"])
    custom = json.loads(request.form["custom"])
    user = User.getUser(user_id)
    User.clear(user)#清空该用户的信息
    user.name = request.form['name']
    user.corp = request.form['corp']
    user.position = request.form['position']
    c = Contact(_type = intro["type"] ,title = intro["title"] , text = intro["text"],user_id=user_id )
    db.session.add(c)
    for i in info:
        c = Contact(_type = i["type"] ,title = i["title"] , text = i["text"],index = i["index"] ,user_id=user_id )
        db.session.add(c)
    for i in custom:
        c = Contact(_type = i["type"] ,title = i["customTitle"] , text = i["customText"],user_id=user_id )
        db.session.add(c)
    user.makeQrcode(user)
    db.session.commit()
    return redirect(url_for("electronic_finish",user_id=user_id))

@app.route('/user<int:user_id>_finish/')
def electronic_finish(user_id):
    return render_template("electronic_finish.html",user_id=user_id)

@app.route('/user<int:user_id>_card/')
def card(user_id):
    return render_template("card.html",user_id=user_id)

@app.route('/_getCardDetail')
def _getCardDetail():
    user_id = request.args.get("user_id")
    return Tools.getcarddetail(user_id)
