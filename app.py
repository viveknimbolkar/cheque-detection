from flask import Flask 
app = Flask(__name__)

# import external routes
import routes


if __name__ == "__main__":
    app.run(debug=True)