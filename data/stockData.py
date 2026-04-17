import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def getStockData(stock_name:str, current_date:str="2026-04-01", past_date:str="2020-01-01") -> pd.DataFrame | None:
    """Returns a dict with DataFrame key with pd.DataFrame of stock data and an Index key with the incriments of the years. Returns None if an error"""
    try:
        stock = yf.Ticker(stock_name)
        hist = stock.history(start=past_date, end=current_date)
        return hist
    except Exception as e:
        print(f"Eror in stockData.py line 30: {e}")
        return None