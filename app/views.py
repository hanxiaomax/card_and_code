#coding:utf-8
from flask import render_template,request,redirect,url_for,jsonify,make_response,g
from flask.ext.login import login_user, logout_user, current_user, login_required
from models import Contact,Friend_Ship,User
from app import app,db
import os
import json
import sqlalchemy.exc
from tools import Tools
from werkzeug import secure_filename
from datetime import datetime
import time
import hashlib
from xml.etree import ElementTree

upload_path = app.config["UPLOAD_FOLDER"]

# @lm.user_loader
# def load_user(id):
#     return User.query.get(int(id))

# @app.route('/login/', methods=['GET', 'POST'])
# def login():
#     # #已经登录
#     # if g.user is not None and g.user.is_authenticated():
#     #     return redirect(url_for('electronic_edit',user_id=g.user.id))
#     if request.method == "GET":
#     #尚未登录
#         xml_recv = ElementTree.fromstring(request.data)
#         UserName = xml_recv.find("FromUserName").text#openID
#         user = User.isExist("1")
#         # if user:
#         #     g.user = UserName
#         # else:
#         #     u=User(username=UserName)
#         #     g.user = UserName
#         #     db.session.add(u)
#         #     db.session.commit()
#         #     user = User.isExist(UserName)
#         return redirect(url_for('electronic_edit',user_id=user.id))
#     else:
#         return "登录失败"



@app.route('/',methods=['GET', 'POST'])
@app.route('/index/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        return redirect(url_for("message_handler"))
    return render_template("token.html",user_id="1")
    # return "施工中"

@app.route('/message/', methods=['GET', 'POST'])
def message_handler():
    if request.method == "POST":
        xml_recv = ElementTree.fromstring(request.data)
        ToUserName = xml_recv.find("ToUserName").text
        FromUserName = xml_recv.find("FromUserName").text
        CreateTime = xml_recv.find("CreateTime").text
        Event = xml_recv.find("Event").text
        MsgType = xml_recv.find("MsgType").text
        reply = "<xml><ToUserName><![CDATA[%s]]></ToUserName>\
                        <FromUserName><![CDATA[%s]]></FromUserName>\
                        <CreateTime>%s</CreateTime>\
                        <MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]>\
                        </Content><FuncFlag>0</FuncFlag></xml>"

        response = make_response( reply %(ToUserName,FromUserName,CreateTime,"hhhhhhh"))
        response.content_type = 'application/xml'
        return response


@app.route('/login/', methods=['GET', 'POST'])
def wechat_auth():
    """
    加密/校验流程如下：
    1. 将token、timestamp、nonce三个参数进行字典序排序
    2. 将三个参数字符串拼接成一个字符串进行sha1加密
    3. 开发者获得加密后的字符串可与signature对比，标识该请求来源于微信
    4. 原样返回echostr
    """
    if request.method == "GET":
        token = "youwillneverknowwhoiamlingfeng"
        query = request.args
        signature = query.get('signature')#微信加密签名，结合了后三者
        timestamp = query.get('timestamp')
        nonce = query.get('nonce')#随机数
        echostr = query.get('echostr')#随机字符串
        s = [timestamp,nonce,token]
        s.sort()
        s = "".join(s)
        if(hashlib.sha1(s).hexdigest() == signature):
            return echostr

    if request.method == "POST":

        # xml_recv = ElementTree.fromstring(request.data)
        # UserName = xml_recv.find("FromUserName").text#openID
        user = User.isExist("1")
        return redirect(url_for('electronic_edit',user_id=user.id))



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config["ALLOWED_EXTENSIONS"]

@app.route('/user<int:user_id>_edit/',methods=['GET', 'POST'])
def electronic_edit(user_id):
    if request.method == 'POST':
        # print "electronic_edit POST"
        user = User.getUser(user_id)
        if user.logo and os.path.exists(user.logo):
            os.remove(user.logo)
        if user.headpic and os.path.exists(user.headpic):
            os.remove(user.headpic)
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
            logo_path = os.path.join(upload_path, "user_id_"+str(user_id)+"_"+time+filename.split(".")[0]+"png")
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


