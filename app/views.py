#coding:utf-8
from flask import render_template,request,redirect,url_for,jsonify,make_response,g,session
from flask.ext.login import login_user, logout_user, current_user, login_required
from models import Contact,Friend_Ship,User,Ship_Address
from app import app,db
import os
import json
import sqlalchemy.exc
from tools import Tools
from werkzeug import secure_filename
from datetime import datetime
import hashlib
from xml.etree import ElementTree
import requests
import time



upload_path = app.config["UPLOAD_FOLDER"]
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config["ALLOWED_EXTENSIONS"]

#PC端演示页面
@app.route("/demo/")
def demo():
    username="testuser"
    User.deleteUser(username)
    user_id=User.addUser(username)

    return redirect(url_for('electronic_edit',user_id=user_id))


#微信公共平台服务器地址
@app.route('/',methods=['GET', 'POST'])
@app.route('/index/', methods=['GET', 'POST'])
def index():
    if request.method =="GET":
        return redirect(url_for('demo'))


@app.route('/server/',methods=['GET','POST'])
def server():
    if request.method == "GET":
        token = 'youwillneverknowwhoiamlingfeng'
        query = request.args
        signature = query.get('signature')
        timestamp = query.get('timestamp')
        nonce = query.get('nonce')
        echostr = query.get('echostr')
        s = [timestamp, nonce, token]
        s.sort()
        s = ''.join(s)
        if ( hashlib.sha1(s).hexdigest() == signature ):
          return make_response(echostr)

    xml_recv = ElementTree.fromstring(request.data)
    ToUserName = xml_recv.find("ToUserName").text
    FromUserName = xml_recv.find("FromUserName").text
    Content = xml_recv.find("Content").text
    reply= "<xml>\
                <ToUserName><![CDATA[%s]]></ToUserName>\
                <FromUserName><![CDATA[%s]]></FromUserName>\
                <CreateTime>12345678</CreateTime>\
                <MsgType><![CDATA[text]]></MsgType>\
                <Content><![CDATA[%s]]></Content>\
            </xml>"

    response=make_response(reply%("ToUserName",FromUserName,Content))
    response.content_type = 'application/xml'
    return response

#授权后重定向到本页面，参数为code和state
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        query = request.args
        if query.has_key('code'):
            code = query.get("code")#获取用户授权code
            appid="wx7e4cf550df5e7653"
            AppSecret="1ddbff16c17736c5b419f5205aebf869"
            access_token_url="https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code"
            r = requests.get(access_token_url%(appid,AppSecret,code))#请求获取access_token
            j=json.loads(r.text)#从相应对象中获取json字符串并转换为json
            openid=j['openid']
            username=openid
            u=User.isExist(str(openid))
            if not u :
                user_id=User.addUser(openid)
                return redirect(url_for('electronic_edit',user_id=user_id))
            else:
                return redirect(url_for('electronic_edit',user_id=u.id))
        else:
            return "请从微信进入或访问http://microbots.club/demo/"

    if request.method == "POST":
        return render_template("login.html",id="22")


@app.route('/user<int:user_id>_edit/',methods=['GET', 'POST'])
def electronic_edit(user_id):
    if request.method == 'POST':

        user = User.getUser(user_id)
        if user.logo and os.path.exists(user.logo):
            os.remove(user.logo)
            user.logo = None
        if user.headpic and os.path.exists(user.headpic):
            os.remove(user.headpic)
            user.headpic  = None
        file = request.files['file']
        logo = request.files["logo"]
        time = str(datetime.today()).replace(" ","_").replace(":","_").replace(".","_")#防止从缓存加载
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(upload_path, "user_id_"+str(user_id)+"_"+time+filename)
            user.headpic = file_path
            file.save(file_path)
            db.session.commit()
        if logo and allowed_file(logo.filename):
            filename = secure_filename(logo.filename)
            logo_path = os.path.join(upload_path, "user_id_"+str(user_id)+"_"+time+filename.split(".")[0]+".png")
            user.logo = logo_path
            logo.save(logo_path)
            db.session.commit()
        # user.makeQrcode(user,user.headpic)#生成二维码
        user.makeQrcode(user)
        return redirect(url_for("electronic_finish",user_id=user_id))

    return render_template("electronic_edit.html",user_id=user_id)

#保存名片信息到数据库
@app.route('/_saveContact/',methods=["GET","POST"])
def saveContact():
    # print "saveContact"
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


    db.session.commit()
    return redirect(url_for("electronic_finish",user_id=user_id))


@app.route('/user<int:user_id>_finish/')
def electronic_finish(user_id):
    user = User.getUser(user_id)
    qrcode = os.path.basename(user.qrcode)
    if user.logo :
        logo = os.path.basename(user.logo)
    else:
        # print "using default logo"
        logo = "default_logo.png"
    if user.headpic :
        headpic = os.path.basename(user.headpic)
    else:
        # print "using default head"
        headpic = "default_headpic.png"

    return render_template("electronic_finish.html",user_id=user_id,qrcode=qrcode,logo=logo,headpic=headpic)

@app.route('/user<int:user_id>_card/')
def card(user_id):
    return render_template("card.html",user_id=user_id)

@app.route('/_getCardDetail')
def _getCardDetail():
    user_id = request.args.get("user_id")
    return Tools.getcarddetail(user_id)

@app.route('/user<int:user_id>_editcard/')
def editcard(user_id):
    return render_template("edit-fang.html",user_id=user_id)


@app.route('/user<int:user_id>_editluxury/')
def editluxury(user_id):
    return render_template("edit-luxury.html",user_id=user_id)

@app.route('/user<int:user_id>_editbusiness/')
def editbusiness(user_id):
    return render_template("edit-business.html",user_id=user_id)

@app.route('/user<int:user_id>_editfashion/')
def editfashion(user_id):
    return render_template("edit-fashion.html",user_id=user_id)


@app.route('/user<int:user_id>_aftercard/')
def afterEditcard(user_id):
    return render_template("after_edit.html",user_id=user_id)

@app.route('/user<int:user_id>_makeOrder/')
def makeOrder(user_id):
    return render_template("makeOrder.html",user_id=user_id)

@app.route('/user<int:user_id>_shipAddress/')
def shipAddress(user_id):
    return render_template("shipAddress.html",user_id=user_id)

@app.route('/user<int:user_id>_enterAddress/')
def enterAddress(user_id):
    return render_template("enterAddress.html",user_id=user_id)


@app.route('/user<int:user_id>_shipway/')
def shipway(user_id):
    return render_template("shipway.html",user_id=user_id)




@app.route('/_saveShipAddress/')
def saveShipAddress():
    query = request.args
    user_id  = query.get('user_id')
    name = query.get('name')
    phone = query.get('phone')
    address = query.get('address')
    index = query.get('index')
    add=Ship_Address.getAdd(index)
    if add:
        add.name=name
        add.phone=phone
        add.address=address
    else:
        s=Ship_Address(name=name,phone=phone,address=address,user_id=user_id)
        db.session.add(s)
    db.session.commit()

    return redirect(url_for('makeOrder',user_id=user_id))

@app.route('/_getShipAddress/')
def getShipAddress():
    user_id  = request.args.get('user_id')
    return Tools.getAddressList(user_id)

@app.route('/user<int:user_id>_cardback/',methods=["GET","POST"])
def cardback(user_id):
    if request.method == "POST":
        user = User.getUser(user_id)
        if user.logo and os.path.exists(user.logo):
            os.remove(user.logo)
            user.logo  = None
        logo = request.files["backlogo"]
        time = str(datetime.today()).replace(" ","_").replace(":","_").replace(".","_")#防止从缓存加载
        logoText = request.form['logo-text']
        user.logoText = logoText
        if logo and allowed_file(logo.filename):
            filename = secure_filename(logo.filename)
            logo_path = os.path.join(upload_path, "user_id_"+str(user_id)+"_"+time+filename.split(".")[0]+".png")
            user.logo = logo_path
            logo.save(logo_path)

        db.session.commit()
        return redirect(url_for("editcard",user_id=user_id))

    return render_template("cardback.html",user_id=user_id)
