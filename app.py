from flask import Flask
import yfinance as yf
from flask import Response, request, jsonify
from markupsafe import escape
from utils import (
    bb,
    get_beta,
    get_beta_info,
    get_ibov_tickers,
    position_relative_to_bands,
    rsi,
    strategy_points,
    strategy_test,
    backtest_algorithm,
    stochastic,
    get_data,
    get_interval,
    get_rsi_info,
    get_stochastic_info,
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
    start, end = get_interval(50)
    df = get_data(
        tickers=yf_ticker, columns=["Open", "High", "Adj Close"], start=start, end=end
    )
    ifr2_df = rsi(df, "Adj Close", 2)
    return {"ifr2": int(round(ifr2_df[-1]))}


@app.route("/backtest/ifr2/<ticker>")
def backtest_ifr2(ticker):
    yf_ticker = escape(ticker) + ".SA"
    start, end = get_interval(500)
    df = get_data(
        tickers=yf_ticker,
        columns=["Open", "High", "Close", "Adj Close"],
        start=start,
        end=end,
    )
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
    start, end = get_interval(365)
    df = get_data(
        tickers=tickers, columns=["Open", "High", "Adj Close"], start=start, end=end
    )

    all_rsi = get_rsi_info(df, tickers)

    return jsonify(all_rsi)


@app.route("/bb/<ticker>")
def bollinger_bands(ticker):
    yf_ticker = escape(ticker) + ".SA"
    start, end = get_interval(50)
    df = get_data(tickers=yf_ticker, columns=["Adj Close"], start=start, end=end)

    k = 2 if request.args.get("k") is None else float(request.args.get("k"))
    n = 20 if request.args.get("n") is None else int(request.args.get("n"))

    bb_df = bb(df, k, n)
    return jsonify(
        {
            "middle_band": bb_df["Middle Band"][-1].round(2),
            "upper_band": bb_df["Upper Band"][-1].round(2),
            "lower_band": bb_df["Lower Band"][-1].round(2),
            "current_price": bb_df["Adj Close"][-1].round(2),
            "text": position_relative_to_bands(ticker, bb_df["Adj Close"], k, n),
        }
    )


@app.route("/beta/<ticker>")
def beta(ticker):
    yf_ticker = escape(ticker) + ".SA"
    interval = (
        365
        if request.args.get("interval") is None
        else int(request.args.get("interval"))
    )
    start, end = get_interval(interval)
    benchmark = "^BVSP"
    tickers = [yf_ticker, benchmark]
    df = get_data(tickers=tickers, columns=["Adj Close"], start=start, end=end)[
        "Adj Close"
    ]
    df.dropna(inplace=True)
    beta, corr, std_asset, std_bench = get_beta(df[yf_ticker], df[benchmark])
    return jsonify(
        {
            "beta": round(beta, 2),
            "corr": round(corr, 2),
            "std_asset": round(std_asset, 4),
            "std_bench": round(std_bench, 4),
        }
    )


@app.route("/stochastic/<ticker>")
def stochastic_calculation(ticker):
    yf_ticker = escape(ticker) + ".SA"
    start, end = get_interval(365)
    df = get_data(
        tickers=yf_ticker, columns=["High", "Low", "Adj Close"], start=start, end=end
    )
    df = stochastic(df)
    return {
        "fast_k": int(round(df["%K"][-1])),
        "fast_d": int(round(df["%D"][-1])),
        "k": int(round(df["Slow %K"][-1])),
        "d": int(round(df["Slow %D"][-1])),
    }


@app.route("/stochastic")
def all_stochastic():

    tickers = get_ibov_tickers()
    start, end = get_interval(120)
    df = get_data(
        tickers=tickers, columns=["High", "Low", "Adj Close"], start=start, end=end
    )

    all_stochastic = get_stochastic_info(df, tickers)

    return jsonify(all_stochastic)


@app.route("/static")
def indicators():
    tickers = get_ibov_tickers()

    start, end = get_interval(365)
    df = get_data(
        tickers=tickers,
        columns=["Open", "High", "Low", "Adj Close"],
        start=start,
        end=end,
    )

    ibov = get_data(tickers="^BVSP", columns=["Adj Close"], start=start, end=end)

    all_rsi = get_rsi_info(df.copy(), tickers)
    all_stochastic = get_stochastic_info(df.copy(), tickers)
    all_beta = get_beta_info(df.copy(), tickers, ibov["Adj Close"])

    indicators = {}
    for ticker in tickers:
        ticker = ticker.replace(".SA", "")

        # Get nested data
        price = all_rsi[ticker]["price"]
        variation = all_rsi[ticker]["variation"]
        mme80_is_up = all_stochastic[ticker]["mme80_is_up"]
        mm50_is_up = all_rsi[ticker]["mm50_is_up"]
        beta = all_beta[ticker]["beta"]
        corr = all_beta[ticker]["corr"]
        std_asset = all_beta[ticker]["std_asset"]
        std_bench = all_beta[ticker]["std_bench"]

        # Delete unnecessary data
        del all_rsi[ticker]["price"]
        del all_rsi[ticker]["variation"]
        del all_rsi[ticker]["mm50_is_up"]
        del all_stochastic[ticker]["mme80_is_up"]
        del all_stochastic[ticker]["price"]
        del all_stochastic[ticker]["variation"]

        indicators[ticker] = {
            "price": price,
            "variation": variation,
            "mme80_is_up": mme80_is_up,
            "mm50_is_up": mm50_is_up,
            "beta": beta,
            "corr": corr,
            "std_asset": std_asset,
            "std_bench": std_bench,
            "rsi": all_rsi[ticker],
            "stochastic": all_stochastic[ticker],
        }
    return jsonify(indicators)
