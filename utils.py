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


def strategy_test(all_profits, total_capital):
    print(all_profits)
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
    url = "http://bvmf.bmfbovespa.com.br/indices/ResumoCarteiraTeorica.aspx?Indice=IBOV&amp;idioma=pt-br"
    html = pd.read_html(url, decimal=",", thousands=".", index_col="Código")[0][:-1]
    tickers = (html.index + ".SA").to_list()
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
        (df["Adj Close"] - n_lowest_low) / 
        (n_highest_high - n_lowest_low)
    ) * 100
    df["%D"] = df['%K'].rolling(mma_window).mean()
    
    df["Slow %K"] = df["%D"]
    df["Slow %D"] = df["Slow %K"].rolling(mma_window).mean()
    
    return df 
