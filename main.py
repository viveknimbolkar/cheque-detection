from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('header.html')

@app.route('/auth')
def auth():
    return render_template('auth.html')


if __name__ == "__main__":
    app.run(debug=True)