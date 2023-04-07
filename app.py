import random
from flask import Flask 
app = Flask(__name__)

app.config['UPLOAD_USER_IMAGE_FOLDER'] = 'static/uploads/user_images'
app.config['MAX_USER_IMAGE_SIZE'] = 2 * 1024 * 1024


app.config['UPLOAD_CHEQUE_FOLDER'] = 'static/uploads/cheques'
app.config['MAX_CHEQUE_SIZE'] = 5 * 1024 * 1024


app.config['UPLOAD_SIGNATURE_FOLDER'] = 'static/uploads/signatures'
app.config['MAX_CSIGNATURE_SIZE'] = 3 * 1024 * 1024

# get 10 digit random account number
def get_random_account_no():
    return random.randint(int('1'+'0'*(10-1)), int('9'*10))

# import external routes
import routes


if __name__ == "__main__":
    app.run(debug=True)