import yfinance as yf
import pandas as pd
import sqlite3
import sys

def load_data():
    
    stocks = [
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
    stock = yf.download(stocks, start="2020-01-01", end="2026-01-01")
    ml_df = (
        stock.stack(level="Ticker")
        .reset_index()
        .rename(columns={"level_0": "Date"})
    )
    connection = sqlite3.connect("data.db")
    ml_df.to_sql("stockData", connection, if_exists="replace", index=False)
    connection.close()
    print(stock.columns)

def get_data():
    connection = sqlite3.connect("data.db")
    data = pd.read_sql_query(sql="SELECT * FROM stockData ORDER BY Ticker ASC;", con=connection)
    print(data.describe())

if __name__ == "__main__":
    get_data()