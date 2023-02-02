from flask import Flask, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key = 'secretkey'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'cheque'
 
mysql = MySQL(app)



@app.route('/')
def index():
    return render_template('header.html')


@app.route('/auth')
def auth():
    return render_template('auth.html')


@app.route('/login',methods=['GET'])
def login():
    return render_template('auth.html')


@app.route('/register',methods=['GET'])
def register():
    return render_template('auth.html')


if __name__ == "__main__":
    app.run(debug=True)