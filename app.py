from flask import Flask
import yfinance as yf
from flask import Response, request, jsonify
from markupsafe import escape
from datetime import date, datetime, timedelta
from utils import (
    get_ibov_tickers,
    rsi,
    strategy_points,
    strategy_test,
    backtest_algorithm,
)

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/price/<ticker>")
def me_api(ticker):
    yf_ticker = escape(ticker) + ".SA"
    start = request.args.get("start")
    end = request.args.get("end")
    df = yf.download(yf_ticker, start=start, end=end).copy()[["Open", "High", "Close"]]
    return Response(df.to_json(orient="table"), mimetype="application/json")


@app.route("/ifr2/<ticker>")
def ifr2(ticker):
    yf_ticker = escape(ticker) + ".SA"
    start = (datetime.today() - timedelta(days=50)).strftime("%Y-%m-%d")
    end = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    df = yf.download(yf_ticker, start=start, end=end).copy()[
        ["Open", "High", "Adj Close"]
    ]
    ifr2_df = rsi(df, "Adj Close", 2)
    return {"ifr2": int(round(ifr2_df[-1]))}


@app.route("/backtest/ifr2/<ticker>")
def backtest_ifr2(ticker):
    yf_ticker = escape(ticker) + ".SA"
    start = (datetime.today() - timedelta(days=500)).strftime("%Y-%m-%d")
    end = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    df = yf.download(yf_ticker, start=start, end=end).copy()[
        ["Open", "High", "Close", "Adj Close"]
    ]
    df["IFR2"] = rsi(df, column="Adj Close")
    entry = (
        None if request.args.get("entry") is None else int(request.args.get("entry"))
    )
    df = strategy_points(data=df, rsi_parameter=entry)
    all_profits, total_capital = backtest_algorithm(df)
    statistics = strategy_test(all_profits, total_capital)

    return jsonify(statistics)


@app.route("/ifr2")
def api():
    tickers = get_ibov_tickers()

    start = (datetime.today() - timedelta(days=50)).strftime("%Y-%m-%d")
    end = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    df = yf.download(tickers, start=start, end=end).copy()[
        ["Open", "High", "Adj Close"]
    ]

    df.columns = [" ".join(col).strip() for col in df.columns.values]

    all_rsi = {}
    for ticker in tickers:
        new_df = df[["Open " + ticker, "High " + ticker, "Adj Close " + ticker]].rename(
            columns={
                "Open " + ticker: "Open",
                "High " + ticker: "High",
                "Adj Close " + ticker: "Adj Close",
            }
        )

        rsi_value = int(round(rsi(new_df, "Adj Close", 2)[-1]))
        target = new_df["High"].shift(2)[-1]
        price = new_df["Adj Close"][-1]
        upside = ((target - price) / price) * 100

        all_rsi[ticker.replace(".SA", "")] = {
            "rsi": rsi_value,
            "target": target.round(2),
            "price": price.round(2),
            "upside": upside.round(2),
        }

    return jsonify(all_rsi)
