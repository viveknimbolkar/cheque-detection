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
            session['email'] = account['email']
            session['name'] = account['name']
            session['role'] = account['role']
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
    if 'email' in session:
        print('defined')
        return render_template('dashboard.html',)
    else:
        print('not defined')
        return redirect('/',)


@app.route('/dashboard/profile')
def profile():
    if 'email' in session:
        print('defined')
        return render_template('profile.html',name=session['name'],email=session['email'],role=session['role'])
    else:
        print('not defined')
        return redirect('/',)




# get the profile information
@app.route('/profile/update_user_details',methods=['POST'])
def update_user_details():
     msg = ''
     if request.method == 'POST':
        email = request.form['email']
        role = request.form['role']
        name = request.form['name']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE user SET  email =%s, name =%s, role=%s WHERE email=%s',(email,name,role,email))
        mysql.connection.commit()
        msg = 'User data updated successfully'
        return msg
     else:
        msg = 'Something went wrong'
            
     return msg



@app.route('/dashboard/history')
def history():
    return render_template('history.html')


@app.route('/dashboard/extract')
def extract():
    return 'hisstory'




@app.route('/dashboard/upload-cheque')
def upload_cheque():
    return render_template('upload-cheque.html')

