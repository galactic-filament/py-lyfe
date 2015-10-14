from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/login')
def login():
    pass


@app.route('/five-oh-oh')
def five_oh_oh():
    raise 'ayy lmao'
