from flask import Flask 
app = Flask(__name__)

app.config['UPLOAD_USER_IMAGE_FOLDER'] = 'static/uploads/'
app.config['MAX_USER_IMAGE_SIZE'] = 2 * 1024 * 1024

# import external routes
import routes


if __name__ == "__main__":
    app.run(debug=True)