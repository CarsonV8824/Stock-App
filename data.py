import yfinance as yf
import pandas as pd
import sqlite3
import sys

STOCKS = [
    # Tech
    "AAPL",   # Apple
    "MSFT",   # Microsoft
    "NVDA",   # NVIDIA
    "AMZN",   # Amazon
    "META",   # Meta Platforms

    # Finance
    "JPM",    # JPMorgan Chase
    "GS",     # Goldman Sachs
    "V",      # Visa

    # Consumer / Retail
    "WMT",    # Walmart
    "COST",   # Costco
    "KO",     # Coca-Cola

    # Energy
    "XOM",    # ExxonMobil
    "CVX",    # Chevron

    # Healthcare
    "JNJ",    # Johnson & Johnson
    "PFE",    # Pfizer

    # Market ETFs / Index Tracking
    "SPY",    # S&P 500 ETF
    "QQQ",    # Nasdaq ETF
    "VIXY"    # Volatility ETF proxy for VIX
]
TICKER_TO_CODE = {ticker: index for index, ticker in enumerate(STOCKS)}
CODE_TO_TICKER = {index: ticker for ticker, index in TICKER_TO_CODE.items()}

def load_data(to_database:bool|None=True) -> tuple[list[list], list] | None:
    """loads data from yfinance to the database or to make predictions from the model"""
    stock = yf.download(STOCKS, start="2020-01-01", end="2026-01-01")
    stock = (
        stock.stack(level="Ticker")
        .reset_index()
        .rename(columns={"level_0": "Date"})
    )
    stock.columns = stock.columns.str.lower()
    next_close = stock.groupby("ticker")["close"].shift(-1)
    stock["predicted_return"] = (next_close - stock["close"]) / stock["close"]
    stock['close_yesterday'] = stock.groupby('ticker')['close'].shift(1)
    stock['close_two_days_ago'] = stock.groupby('ticker')['close'].shift(2)
    stock["volume_yesterday"] = stock.groupby('ticker')['volume'].shift(1)
    stock['ma_5'] = (
    stock.groupby('ticker')['close']
        .rolling(5)
        .mean()
        .reset_index(0, drop=True)
    )
    stock["date"] = pd.to_datetime(stock["date"])
    stock["date"] = stock["date"].astype("int64")
    stock["ticker"] = stock["ticker"].map(TICKER_TO_CODE)

    if to_database:
        stock = stock.dropna()
        connection = sqlite3.connect("data.db")
        stock.to_sql("stockData", connection, if_exists="replace", index=False)
        connection.close()
        return
    else:
        columns = stock.columns.to_list()
        columns.remove("date")
        y_value = columns.pop(columns.index("predicted_return"))
        return stock[columns].to_numpy().tolist(), stock[y_value].to_list()

def get_training_dataframe() -> pd.DataFrame:
    """fetches the training dataframe from sqlite in the same order used for training"""
    connection = sqlite3.connect("data.db")
    data = pd.read_sql_query(
        sql="SELECT * FROM stockData ORDER BY ticker ASC, date ASC",
        con=connection,
    )
    connection.close()
    return data

def get_feature_columns() -> list[str]:
    """returns the feature columns used by the model"""
    data = get_training_dataframe()
    columns = data.columns.to_list()
    columns.remove("date")
    columns.remove("predicted_return")
    return columns

def get_data_from_db() -> tuple[list[list], list]:
    """fetches the data from the sqlite database. Used for training"""
    data = get_training_dataframe()
    columns = data.columns.to_list()
    columns.remove("date")
    y_value = columns.pop(columns.index("predicted_return"))
    return data[columns].to_numpy().tolist(), data[y_value].to_list()

if __name__ == "__main__":
    load_data()
    print(get_data_from_db()[1])
