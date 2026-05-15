import os

import pandas as pd
import torch

from data import CODE_TO_TICKER, STOCKS, TICKER_TO_CODE
from model import StockMLP
from tensors import training_frame_and_scaler
from train import MODEL_PATH, VALIDATION_SPLIT


def get_device() -> torch.device:
    """uses xpu when available, otherwise falls back to cpu"""
    if hasattr(torch, "xpu") and torch.xpu.is_available():
        return torch.device("xpu")
    return torch.device("cpu")


def load_model(input_size: int, device: torch.device) -> StockMLP:
    """loads the trained model from disk"""
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Could not find {MODEL_PATH}. Train the model first so test.py has weights to load."
        )

    model = StockMLP(input_size=input_size).to(device)
    state_dict = torch.load(MODEL_PATH, map_location=device)
    model.load_state_dict(state_dict)
    model.eval()
    return model


def prepare_lookup_dataframe() -> tuple[pd.DataFrame, list[str], object]:
    """reuses the training pipeline to get the dataframe, feature order, and scaler"""
    training_data = training_frame_and_scaler(VALIDATION_SPLIT)
    dataframe = training_data["dataframe"].copy()
    dataframe["date"] = pd.to_datetime(dataframe["date"])
    return dataframe, training_data["feature_columns"], training_data["scaler"]


def find_stock_row(dataframe: pd.DataFrame, ticker: str, target_date: pd.Timestamp) -> pd.Series | None:
    """finds the latest trading row for a ticker on or before the requested date"""
    ticker_code = TICKER_TO_CODE.get(ticker)
    if ticker_code is None:
        return None

    filtered = dataframe[
        (dataframe["ticker"] == ticker_code) &
        (dataframe["date"] <= target_date)
    ].sort_values("date")

    if filtered.empty:
        return None
    return filtered.iloc[-1]


def predict_for_row(model: StockMLP, scaler, feature_columns: list[str], row: pd.Series, device: torch.device) -> float:
    """runs a single-row prediction using the same feature order and scaler as training"""
    features = row[feature_columns].to_frame().T
    scaled_features = scaler.transform(features)
    tensor = torch.tensor(scaled_features, dtype=torch.float32, device=device)

    with torch.no_grad():
        prediction = model(tensor).squeeze().item()
    return prediction


def print_prediction(row: pd.Series, predicted_return: float) -> None:
    """prints a prediction summary for the selected stock/date"""
    current_close = float(row["close"])
    predicted_next_close = current_close * (1 + predicted_return)
    actual_return = row.get("predicted_return")
    actual_next_close = current_close * (1 + float(actual_return)) if pd.notna(actual_return) else None
    ticker = CODE_TO_TICKER.get(int(row["ticker"]), str(row["ticker"]))

    print()
    print(f"Ticker: {ticker}")
    print(f"Trading date used: {row['date'].date()}")
    print(f"Current close: {current_close:.2f}")
    print(f"Predicted next-day return: {predicted_return:.4%}")
    print(f"Predicted next-day close: {predicted_next_close:.2f}")

    if actual_next_close is not None:
        print(f"Actual next-day return in dataset: {float(actual_return):.4%}")
        print(f"Actual next-day close in dataset: {actual_next_close:.2f}")
    print()


def run_tui() -> None:
    """simple terminal UI for picking a ticker/date and getting a model prediction"""
    dataframe, feature_columns, scaler = prepare_lookup_dataframe()
    device = get_device()
    model = load_model(len(feature_columns), device)

    print("Stock prediction TUI")
    print(f"Available tickers: {', '.join(STOCKS)}")
    print("Enter a ticker and a date in YYYY-MM-DD format. Type q to quit.")
    print()

    while True:
        ticker_input = input("Ticker: ").strip().upper()
        if ticker_input.lower() in {"q", "quit", "exit"}:
            break

        if ticker_input not in TICKER_TO_CODE:
            print("That ticker is not in the trained dataset.")
            print()
            continue

        date_input = input("Date (YYYY-MM-DD): ").strip()
        if date_input.lower() in {"q", "quit", "exit"}:
            break

        try:
            requested_date = pd.Timestamp(date_input)
        except ValueError:
            print("Could not parse that date. Use YYYY-MM-DD.")
            print()
            continue

        row = find_stock_row(dataframe, ticker_input, requested_date)
        if row is None:
            print("No trading data was found for that ticker on or before that date.")
            print()
            continue

        predicted_return = predict_for_row(model, scaler, feature_columns, row, device)
        print_prediction(row, predicted_return)


if __name__ == "__main__":
    run_tui()
