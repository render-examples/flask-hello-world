import yfinance as yf
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def hyfproxy():
    ticker = request.args.get('ticker')
    stock = yf.Ticker(ticker)
    info = stock.info
    return jsonify(info)
