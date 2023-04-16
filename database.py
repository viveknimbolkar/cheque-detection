#database configurations
from __main__ import app
from flask_mysqldb import MySQL

app.secret_key = 'secretkey'
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'Cheque'
 
mysql = MySQL(app)