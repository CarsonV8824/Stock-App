import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

apple = yf.Ticker("NVDA")


hist = apple.history(start="2020-01-01", end="2026-04-01")
#print(hist)
#hist.to_csv("data/nvda_stock_data.csv")
#print(apple.info["regularMarketPrice"])

sns.set_style("whitegrid")
sns.lineplot(data=hist, x=hist.index, y="Close")
plt.title("NVIDIA Stock Price (2026)")
plt.xlabel("Date")
plt.ylabel("Closing Price (USD)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
