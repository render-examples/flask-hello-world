from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'giác hơi trăm hủ,giác hơi ở bụng,ngực,cởi hết qaql'
