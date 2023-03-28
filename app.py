from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<img src="https://media.cnn.com/api/v1/images/stellar/prod/161004160803-05-sex-is-good-for-you-shutterstock-348997928.jpg?q=w_4148,h_2333,x_0,y_0,c_fill/w_1280" alt="Italian Trulli">
'
