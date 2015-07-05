#coding:utf-8
from flask import render_template,request,redirect,url_for,jsonify
from models import Contact,Friend_Ship,User
from app import app,db
import os
import json
import sqlalchemy.exc
from tools import Tools
from werkzeug import secure_filename
upload_path = app.config["UPLOAD_FOLDER"]


@app.route('/index/')
@app.route('/', methods=['GET', 'POST'])
def index():
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>hello</h1>

    '''
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config["ALLOWED_EXTENSIONS"]

@app.route('/user<int:user_id>_edit/',methods=['GET', 'POST'])
def electronic_edit(user_id):
    if request.method == 'POST':
        user = User.getUser(user_id)
        os.remove(user.logo)
        os.remove(user.headpic)
        file = request.files['file']
        logo = request.files["logo"]
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(upload_path, "user_id_"+str(user_id)+"_"+filename)
            user.headpic = file_path
            file.save(file_path)
            db.session.commit()
        if logo and allowed_file(logo.filename):
            filename = secure_filename(logo.filename)
            logo_path = os.path.join(upload_path, "user_id_"+str(user_id)+"_"+filename)
            user.logo = logo_path
            logo.save(logo_path)
            db.session.commit()
        return redirect(url_for("electronic_finish",user_id=user_id))

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
