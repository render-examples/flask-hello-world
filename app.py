import yfinance as yf
from flask import Flask, request, jsonify
import redis

cache = redis.Redis(host='redis://red-ci9i4g59aq02iht9og6g', port=6379)
redis_timeout = 900

app = Flask(__name__)

@app.route('/')
def info():
    ticker = request.args.get('ticker')
    stock = yf.Ticker(ticker)
    info = stock.info
    return jsonify(info)

@app.route('/news')
def news():
    ticker = request.args.get('ticker')
    stock = yf.Ticker(ticker)
    news = stock.news
    return jsonify(news)

@app.route('/cache')
def info():
    ticker = request.args.get('ticker')
    cached_info = cache.get(ticker)
    if cached_info is not None:
        cached_info['source'] = 'cached'
        return jsonify(cached_info)
    else:
        stock = yf.Ticker(ticker)
        info = stock.info
        info['source'] = 'live'
        cache.set(ticker, jsonify(info))
        cache.expire(ticker, redis_timeout)
        return jsonify(info)
