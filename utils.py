import numpy as np
import math
import pandas as pd
from datetime import date, datetime, timedelta
import yfinance as yf
from db import connect_to_db

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

    shares, entry = 0, 0

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


def get_beta(asset, benchmark):
    asset_change = asset.pct_change()[1:]
    bench_change = benchmark.pct_change()[1:]
    corr = asset_change.corr(bench_change)
    std_asset = asset_change.std()
    std_bench = bench_change.std()
    beta = corr * (std_asset / std_bench)
    return beta, corr, std_asset, std_bench


def strategy_test(all_profits, total_capital):
    gains = sum(x > 0 for x in all_profits)
    losses = sum(x < 0 for x in all_profits)
    num_operations = gains + losses
    pct_gains = 100 * (gains / num_operations)
    pct_losses = 100 - pct_gains
    total_profit = sum(all_profits)

    # The first value entry in total_capital is the initial capital
    pct_profit = (total_profit / total_capital[0]) * 100

    # Compute drawdown
    total_capital = pd.DataFrame(data=total_capital, columns=["total_capital"])
    drawdown = get_drawdown(data=total_capital, column="total_capital")

    return {
        "num_operations": int(num_operations),
        "gains": int(gains),
        "pct_gains": pct_gains.round(),
        "losses": int(losses),
        "pct_losses": pct_losses.round(),
        "total_profit": total_profit,
        "pct_profit": pct_profit,
        "drawdown": drawdown,
    }


def get_ibov_tickers():
    engine = connect_to_db()
    tickers = pd.read_sql("asset", engine, columns=["yf_symbol"])
    tickers = list(tickers["yf_symbol"])
    return tickers

def below_bands(data, k=2, n=20):
    std = data.rolling(n).std()
    middle_band = data.rolling(n).mean()
    lower_band = middle_band - k * std
    return data < lower_band


def above_bands(data, k=2, n=20):
    std = data.rolling(n).std()
    middle_band = data.rolling(n).mean()
    upper_band = middle_band + k * std
    return data > upper_band


def bb(data, k=2, n=20):
    std = data["Adj Close"].rolling(n).std()
    data["Middle Band"] = data["Adj Close"].rolling(n).mean()
    data["Upper Band"] = data["Middle Band"] + std * k
    data["Lower Band"] = data["Middle Band"] - std * k
    return data


def position_relative_to_bands(asset_name, data, k=2, n=20):
    if below_bands(data, k, n)[-1]:
        return f"{asset_name} está abaixo das Bandas de Bollinger"
    elif above_bands(data, k, n)[-1]:
        return f"{asset_name} está acima das Bandas de Bollinger"
    else:
        return f"{asset_name} está dentro das Bandas de Bollinger"


def stochastic(df, k_window=8, mma_window=3):

    df = df.copy()

    n_highest_high = df["High"].rolling(k_window).max()
    n_lowest_low = df["Low"].rolling(k_window).min()

    df["%K"] = (
        (df["Adj Close"] - n_lowest_low) / (n_highest_high - n_lowest_low)
    ) * 100
    df["%D"] = df["%K"].rolling(mma_window).mean()

    df["Slow %K"] = df["%D"]
    df["Slow %D"] = df["Slow %K"].rolling(mma_window).mean()

    return df


def get_data(tickers, columns, start, end):
    df = yf.download(tickers, start=start, end=end).copy()[columns]
    return df


def get_interval(start_delta, end_delta=1):
    start = (datetime.today() - timedelta(days=start_delta)).strftime("%Y-%m-%d")
    end = (date.today() + timedelta(days=end_delta)).strftime("%Y-%m-%d")
    return start, end


def get_rsi_info(df, tickers):
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
        new_df.dropna(inplace=True)

        rsi_value = int(round(rsi(new_df, "Adj Close", 2)[-1]))
        max_today = new_df["High"][-1]
        max_1_day_ago = new_df["High"][-2]

        # Target is the max value of today and yesterday. This is because the operation
        # starts at the end of the current day, and all possible sells are in the next day
        # Therefore, tomorrow the last two days will be today and yesterday
        target = max(max_today, max_1_day_ago)
        price = new_df["Adj Close"][-1]
        upside = ((target - price) / price) * 100

        # Variation of the last 100 days
        interval = 100
        start_date = (datetime.today() - timedelta(days=interval)).strftime("%Y-%m-%d")
        first_date = new_df.index[new_df.index >= start_date][0]
        index = new_df.index.get_loc(first_date)
        initial_price = new_df.iloc[index]["Adj Close"]
        variation = ((price - initial_price) / initial_price) * 100

        # Figure out if MM50 is up
        mm50 = new_df["Adj Close"].rolling(50).mean()
        mm50_today = mm50[-1]
        mm50_prev = mm50[-2]
        mm50_is_up = 1 if mm50_today > mm50_prev else 0

        all_rsi[ticker.replace(".SA", "")] = {
            "rsi": rsi_value,
            "target": target.round(2),
            "price": price.round(2),
            "upside": upside.round(2),
            "mm50_is_up": mm50_is_up,
            "variation": variation.round(2),
        }

    return all_rsi


def get_stochastic_info(df, tickers):
    df.columns = [" ".join(col).strip() for col in df.columns.values]

    all_stochastic = {}
    for ticker in tickers:
        new_df = df[["High " + ticker, "Low " + ticker, "Adj Close " + ticker]].rename(
            columns={
                "High " + ticker: "High",
                "Low " + ticker: "Low",
                "Adj Close " + ticker: "Adj Close",
            }
        )

        new_df.dropna(inplace=True)

        new_df = stochastic(new_df)

        # current price
        price = new_df["Adj Close"][-1]

        # Variation of the last 100 days
        interval = 100
        start_date = (datetime.today() - timedelta(days=interval)).strftime("%Y-%m-%d")
        first_date = new_df.index[new_df.index >= start_date][0]
        index = new_df.index.get_loc(first_date)
        initial_price = new_df.iloc[index]["Adj Close"]
        variation = ((price - initial_price) / initial_price) * 100

        # Figure out if slow K is up
        k_today = new_df["Slow %K"][-1]
        k_prev = new_df["Slow %K"][-2]
        k_is_up = 1 if k_today > k_prev else 0

        # Figure out if slow K crossed above or under D
        d_today = new_df["Slow %D"][-1]
        d_prev = new_df["Slow %D"][-2]
        k_crossed_above = 1 if (k_prev < d_prev) & (k_today > d_today) else 0
        k_crossed_below = 1 if (k_prev > d_prev) & (k_today < d_today) else 0

        # Figure out if MME80 is up
        mme80 = new_df["Adj Close"].ewm(span=80).mean()
        mme80_today = mme80[-1]
        mme80_prev = mme80[-2]
        mme80_is_up = 1 if mme80_today > mme80_prev else 0

        all_stochastic[ticker.replace(".SA", "")] = {
            "k": int(round(k_today)),
            "d": int(round(d_today)),
            "price": price.round(2),
            "variation": variation.round(2),
            "k_is_up": k_is_up,
            "k_crossed_above": k_crossed_above,
            "k_crossed_below": k_crossed_below,
            "mme80_is_up": mme80_is_up,
        }
    return all_stochastic


def get_beta_info(df, tickers, ibov):
    df.columns = [" ".join(col).strip() for col in df.columns.values]

    all_beta = {}
    for ticker in tickers:
        new_df = df["Adj Close " + ticker]
        new_df.dropna(inplace=True)

        beta, corr, std_asset, std_bench = get_beta(new_df, ibov)

        all_beta[ticker.replace(".SA", "")] = {
            "beta": round(beta, 2),
            "corr": round(corr, 2),
            "std_asset": round(std_asset, 4),
            "std_bench": round(std_bench, 4),
        }

    return all_beta
