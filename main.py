# author: wr786
import os
from re import L
from flask import Flask, session, render_template, request, redirect, send_from_directory
import sqlalchemy

import utils
import db
import config

app = Flask(__name__)

@app.route('/')
def index():
    if 'userName' not in session:
        return redirect("/login")
    return render_template('index.html', userName=session['userName'])

@app.route('/login')
def login_static():
    return app.send_static_file('login.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    userName = request.form["username"].strip()
    passWord = request.form["password"]
    user = db.get_user(userName)
    utils.Dprint(user)
    if user == None:
        statusMsg = "用户名不存在！"
    elif utils.encrypt(passWord) != user.password:
        statusMsg = "密码错误！"
    else:
        session['userName'] = userName
        statusMsg = "登陆成功，正在跳转到首页…"
    return render_template('loginStatus.html', loginMsg=statusMsg)

@app.route('/register')
def register_static():
    return app.send_static_file('register.html')

@app.route('/register', methods=["POST", "GET"])
def register():
    userName = request.form["username"].strip()
    passWord = request.form["password"]
    passWord = utils.encrypt(passWord)
    user = db.get_user(userName)
    if user != None:
        statusMsg = "非常抱歉！您的用户名已经被注册！请换一个用户名注册。"
    else:
        db.add_user(userName, passWord)
        statusMsg = "恭喜您！注册成功！"
    return render_template('registerStatus.html', registerMsg=statusMsg)


if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(port=config.FLASK_PORT, debug=config.DEBUG)