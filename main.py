# author: wr786
from re import L
from flask import Flask, session, render_template, request, redirect, send_from_directory
import sqlalchemy

from . import utils
from . import db

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
    user = list(dbConn.execute(f"select username, password from users where username='{userName}'"))
    if len(user) == 0:
        statusMsg = "用户名不存在！"
    elif encrypt(passWord) != user[0][1]:
        statusMsg = "密码错误！"
    else:
        session['userName'] = userName
        statusMsg = "登陆成功，正在跳转到首页…"
    return render_template('loginStatus.html', loginMsg=statusMsg)