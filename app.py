from flask import Flask
import yfinance as yf
from flask import Response, request, jsonify
from markupsafe import escape
from datetime import date, datetime, timedelta
import numpy as np
import math
import pandas as pd

# Create a function to round any number to the smallest multiple of 100
def round_down(x):
    return int(math.floor(x / 100.0)) * 100


def rsi(data, column, window=2):

    data = data.copy()

    # Establish gains and losses for each day
    data["Variation"] = data[column].diff()
    data = data[1:]
    data["Gain"] = np.where(data["Variation"] > 0, data["Variation"], 0)
    data["Loss"] = np.where(data["Variation"] < 0, data["Variation"], 0)

    # Calculate simple averages so we can initialize the classic averages
    simple_avg_gain = data["Gain"].rolling(window).mean()
    simple_avg_loss = data["Loss"].abs().rolling(window).mean()
    classic_avg_gain = simple_avg_gain.copy()
    classic_avg_loss = simple_avg_loss.copy()

    for i in range(window, len(classic_avg_gain)):
        classic_avg_gain[i] = (
            classic_avg_gain[i - 1] * (window - 1) + data["Gain"].iloc[i]
        ) / window
        classic_avg_loss[i] = (
            classic_avg_loss[i - 1] * (window - 1) + data["Loss"].abs().iloc[i]
        ) / window

    # Calculate the RSI
    RS = classic_avg_gain / classic_avg_loss
    RSI = 100 - (100 / (1 + RS))
    return RSI


def strategy_points(data, rsi_parameter=None):
    rsi_parameter = 30 if rsi_parameter is None else rsi_parameter

    data["Target1"] = data["High"].shift(1)
    data["Target2"] = data["High"].shift(2)
    data["Target"] = data[["Target1", "Target2"]].max(axis=1)

    # We don't need them anymore
    data.drop(columns=["Target1", "Target2"], inplace=True)

    # Define exact buy price
    data["Buy Price"] = np.where(data["IFR2"] <= rsi_parameter, data["Close"], np.nan)

    # Define exact sell price
    data["Sell Price"] = np.where(
        data["High"] > data["Target"],
        np.where(data["Open"] > data["Target"], data["Open"], data["Target"]),
        np.nan,
    )
    return data


def backtest_algorithm(data, initial_capital=10000):

    # List with the total capital after every operation
    total_capital = [initial_capital]

    # List with profits for every operation. We initialize with 0 so
    # both lists have the same size
    all_profits = [0]

    ongoing = False

    for i in range(0, len(data)):
        if ongoing == True:
            if ~(np.isnan(data["Sell Price"][i])):

                # Define exit point and total profit
                exit = data["Sell Price"][i]
                profit = shares * (exit - entry)

                # Append profit to list and create a new entry with the capital
                # after the operation is complete
                all_profits += [profit]
                current_capital = total_capital[
                    -1
                ]  # current capital is the last entry in the list
                total_capital += [current_capital + profit]
                ongoing = False

        else:
            if ~(np.isnan(data["Buy Price"][i])):
                entry = data["Buy Price"][i]
                shares = round_down(initial_capital / entry)
                ongoing = True

    return all_profits, total_capital


def get_drawdown(data, column="Adj Close"):
    data["Max"] = data[column].cummax()
    data["Delta"] = data["Max"] - data[column]
    data["Drawdown"] = 100 * (data["Delta"] / data["Max"])
    max_drawdown = data["Drawdown"].max()
    return max_drawdown


def strategy_test(all_profits, total_capital):
    num_operations = len(all_profits) - 1
    gains = sum(x >= 0 for x in all_profits)
    pct_gains = 100 * (gains / num_operations)
    losses = num_operations - gains
    pct_losses = 100 - pct_gains
    total_profit = sum(all_profits)

    # The first value entry in total_capital is the initial capital
    pct_profit = (total_profit / total_capital[0]) * 100

    # Compute drawdown
    total_capital = pd.DataFrame(data=total_capital, columns=["total_capital"])
    drawdown = get_drawdown(data=total_capital, column="total_capital")

    return {
        "num_operations": num_operations,
        "gains": int(gains),
        "pct_gains": pct_gains.round(),
        "losses": int(losses),
        "pct_losses": pct_losses.round(),
        "total_profit": total_profit,
        "pct_profit": pct_profit,
        "drawdown": drawdown,
    }


app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello, World!!"


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
