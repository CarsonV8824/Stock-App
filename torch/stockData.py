import yfinance as yf

# Download historical data for a ticker
data = yf.download("AAPL", start="2023-01-01", end="2024-01-01")
print(data.head())