from __main__ import app
from flask import render_template, redirect, render_template, request, session
from database import mysql
import MySQLdb.cursors

    
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/auth')
def auth():
    return render_template('auth.html')


@app.route('/login',methods=['POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email=%s AND password=%s',[email,password])
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['email'] = account['email']
            session['name'] = account['name']
            msg = 'Logged in successfully!'
            return redirect('/dashboard')
        else:
            msg = 'Incorrect username or password!'
    elif request.method == 'POST':
        msg = 'Empty fields are not allowed!'
        
    return msg



@app.route('/register',methods=['POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'name' in request.form and 'password' in request.form:
        email = request.form['email']
        name = request.form['name']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email=%s',[email])
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
        else:
            cursor.execute('INSERT INTO `user` (`name`, `email`, `password`) VALUES (%s, %s, %s)',[name,email,password])
            mysql.connection.commit()
            msg = 'User registered successfully!'
    else:
         msg = 'Empty fields are not allowed!'
    return msg


@app.route('/logout')
def logout():
    session.pop('loggedin',None)
    session.pop('email',None)
    session.pop('name',None)
    return redirect('/')
    

@app.route('/dashboard')
def dashboard():
    return 'dashboard'    


@app.route('/dashboard/history')
def history():
    return 'history'


@app.route('/dashboard/verify')
def verify():
    return 'verify'