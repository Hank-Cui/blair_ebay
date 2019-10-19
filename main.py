from flask import Flask, redirect
from flask import request
from flask.templating import render_template
from flask.helpers import url_for
#from Ansible_platform1 import info
import pymysql
import psutil
import datetime
import urllib
import json

db = pymysql.connect(host="", user="", passwd='', db='')
cur = db.cursor()
app = Flask(__name__)

#输入连接后要求用户先登录
@app.route('/', methods=['GET'])
def login():
    return render_template('login.html')

#登录完成后进入主页
@app.route('/login/<number>', methods=['POST'])
def login_post(number):
    if number == "1":
        username = request.form['username']
        password = request.form['password']
        sql = """ select username,password from user where username='%s' and password='%s' """ % (username, password)
        db.ping(reconnect=True)
        cur.execute(sql)
        results = cur.fetchone()
        find_tasks = """ select * from tasks """
        db.ping(reconnect=True)
        cur.execute(find_tasks)
        data = cur.fetchmany(2)
        id, tasks, username = ([], [], [])
        for task in data:
            tasks.append(task)
            for item in task:
                username.append(item)
        if results:
            db.close()
            return render_template('index.html', tasks=tasks, username=username, id=2)
        else:
            db.close()
            return render_template('registration.html')
    if number == "2":
        return render_template('reset-password.html')
    elif number == "3":
        return render_template('registration.html')
    else:
        return render_template('error-500.html')

#允许用户创建新任务
@app.route("/new_task", methods=['Get'])
def new_task_load():
    find_tasks = """ select * from tasks """
    db.ping(reconnect=True)
    cur.execute(find_tasks)
    data = cur.fetchmany(2)
    tasks, username = ([], [])
    for task in data:
        tasks.append(task)
        for item in task:
            username.append(item)
    return render_template("new_task.html")

#允许用户创建新任务并将任务数据提交至数据库
@app.route('/new_task', methods=['POST'])
def new_task():
    nickname = request.form['nickname']
    task_title = request.form['task_title']
    task_description = request.form['task_description']
    get_id = '''select id from tasks'''
    db.ping(reconnect=True)
    id = cur.execute(get_id)
    sql_new_task = '''
        insert into tasks values ('%i','%s','%s','%s')
        '''
    db.ping(reconnect=True)
    cur.execute(sql_new_task % (id, nickname, task_title, task_description))
    db.commit()
    db.close()
    return redirect(url_for("task_detail", id=id))

#提交任务完成后跳转至
@app.route('/task_detail?id=<id>')
def task_detail(id):
    sql_get_detail = '''select * from tasks where id='%i' '''
    db.ping(reconnect=True)
    cur.execute(sql_get_detail % int(id))
    details = cur.fetchone()
    return str(details)

#注册页面
@app.route('/registration', methods=['Get'])
def registration1():
    return render_template('registration.html')

#注册函数
@app.route('/registration', methods=['POST'])
def registration():
    email = request.form['email']
    nickname = request.form['name1']
    password = request.form['password1']
    rename = """
        select * from user where username='%s'
        """
    db.ping(reconnect=True)
    n = cur.execute(rename % nickname)
    db.commit()
    if n <= 0:
        sql_insert = """
             insert into user values('%i','%s','%s','%s')
                                           """
        db.ping(reconnect=True)
        cur.execute(sql_insert % (0, nickname, password, email))
        db.commit()
        return render_template('login.html')
    else:
        return render_template('login.html')
    db.close()


app.run('127.0.0.1', port=6789, debug=True)