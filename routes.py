from __main__ import app, get_random_account_no
import os, io
import flask
import cv2
from flask import render_template, redirect, render_template, request, session, flash, url_for
from werkzeug.utils import secure_filename
from database import mysql
import MySQLdb.cursors 
from model.data_extraction import DataExtraction
from model.signature_verification import VerifySignature

# from google.cloud import vision
# from google.cloud import vision_v1
# from google.cloud.vision_v1 import types

# setting up google cloud vision credentials
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'GoogleCloudVisionToken.json'

ALLOWED_IMAGE_EXTENSIONS = set(['png','jpg','jpeg','gif'])

# validate image types
def allowed_images(imagename):
    return '.' in imagename and imagename.rsplit('.',1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS
    

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
    if request.method == 'POST' and 'email' in request.form and 'name' in request.form and 'password' in request.form and request.files['signature'].filename != '':
        email = request.form['email']
        name = request.form['name']
        password = request.form['password']
        random_account_number = get_random_account_no()
        print(secure_filename(request.files['signature'].filename))
        signaturename = secure_filename(request.files['signature'].filename)
        request.files['signature'].save(os.path.join(app.config['UPLOAD_SIGNATURE_FOLDER'],signaturename))
        print(signaturename)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email=%s',[email])
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
        else:
            cursor.execute('INSERT INTO `user` (`name`, `email`, `password`,`account_no`,`signature`) VALUES (%s, %s, %s, %s, %s)',[name,email,password,random_account_number,signaturename])
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
        return render_template('dashboard.html',email=session['email'])
    else:
        return redirect('/',)


@app.route('/dashboard/profile')
def profile():
    if 'email' in session:
        return render_template('profile.html',name=session['name'],email=session['email'],role=session['role'])
    else:
        return redirect('/',)



# get the profile information
@app.route('/profile/update_user_details',methods=['POST'])
def update_user_details():
    msg = ''
    if request.method == 'POST':
        if request.files['userimage'].filename != '':
            if allowed_images(request.files['userimage'].filename):
                filename = secure_filename(request.files['userimage'].filename)
                request.files['userimage'].save(os.path.join(app.config['UPLOAD_USER_IMAGE_FOLDER'],filename))
            else:
                flash('Only png, jpg, jpeg image formats are allowed')
        email = request.form['email']
        role = request.form['role']
        name = request.form['name']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query_with_image = 'UPDATE user SET  email =%s, name =%s, role=%s, user_image=%s WHERE email=%s'
        query_without_image = 'UPDATE user SET  email =%s, name =%s, role=%s WHERE email=%s'
        if request.files['userimage'].filename != '':
            cursor.execute(query_with_image,(email,name,role,secure_filename(request.files['userimage'].filename),email))
        else:
            cursor.execute(query_without_image,(email,name,role,email))
        mysql.connection.commit()
        flash('User data updated successfully')
        return redirect(flask.request.url_root+'dashboard/profile',)
    else:
        msg = 'Something went wrong'
    return msg


@app.route('/get_userimage/<email>/')
def display_userimage(email):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT user_image FROM user WHERE email=%s ',[email])
        account = cursor.fetchone()
        if account and account['user_image'] != '':
           return redirect(url_for('static',filename='uploads/user_images/'+account['user_image']))
        else:
            flash('Cannot upload file')


@app.route('/dashboard/history',methods=['GET'])
def history():
    if request.method == 'GET':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM history')
        account = cursor.fetchall()
        return render_template('history.html',chequeDetails=account,email=session['email'])


@app.route('/add_cheque_data',methods=['POST'])
def add_cheque_data():
    if request.method == 'POST':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO `history` (`bank_name`, `bearer`, `amount`, `isvalid`, `cheque_no`) VALUES (%s, %s, %s, %s, %s)',[request.json['bankName'],request.json['bearer'],request.json['amount'],request.json['isValid'],request.json['chequeNo']])
        mysql.connection.commit()
        return 'Cheque details added'


@app.route('/dashboard/extract',methods=['POST','GET'])
def extract():
    if request.method == 'POST':
        if request.files['cheque'].filename != '':
            # vision_client = vision.ImageAnnotatorClient()
            # cheque_content = request.files['cheque'].read()
            # # print(cheque_content)
            # cheque_image = vision_v1.types.Image(content=cheque_content)
            # vision_response = vision_client.text_detection(image=cheque_image)
            # extracted_text = vision_response.text_annotations
            # print(extracted_text)

            # store cheque and send for processing
            filename = secure_filename(request.files['cheque'].filename)
            chequepath = os.path.join(app.config['UPLOAD_CHEQUE_FOLDER'],filename)
            request.files['cheque'].save(chequepath)
            de = DataExtraction(chequepath)
            extracted_data = de.getDetails()
            print(extracted_data)
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO `history` ( `bearer`, `amount`, `amount_in_words`,`account_no`,`date`) VALUES (%s, %s, %s, %s, %s)',[extracted_data[0],extracted_data[3],extracted_data[2],extracted_data[1],extracted_data[5]])
            mysql.connection.commit()
            return render_template('extract-cheque-info.html',email=session['email'],chequedata=extracted_data)
        else:
            return render_template('extract-cheque-info.html',email=session['email'])


    elif request.method == 'GET':
        return render_template('extract-cheque-info.html',email=session['email'])


@app.route('/dashboard/validate-cheque',methods=['POST','GET'])
def validate_cheque():
    if request.method == 'POST':
        if request.files['cheque'].filename != '':
            chequepath = os.path.join(app.config['UPLOAD_CHEQUE_FOLDER'],request.files['cheque'].filename)
            data_extraction_instance = DataExtraction(chequepath)
            extracted_account_no = data_extraction_instance.getDetails()
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT signature FROM customer WHERE account_no=%s ',[extracted_account_no[1]])
            customer_signature_name = cursor.fetchone()
            if customer_signature_name:
                customer_signature_path = os.path.join(app.config['UPLOAD_SIGNATURE_FOLDER'],customer_signature_name['signature'])
                print(customer_signature_path)
                customer_img_instance = cv2.imread(customer_signature_path)
                cheque_signature = extracted_account_no[-1]
                signature_verification_instance = VerifySignature(customer_img_instance,cheque_signature)
                print(signature_verification_instance.find())
            else:
               print('not getting ')

            return render_template('validate-cheque.html',email=session['email'])

        else:
            flash('Cheque not provided')
            return render_template('validate-cheque.html',email=session['email'])


    elif request.method == 'GET':
        return render_template('validate-cheque.html',email=session['email'])


