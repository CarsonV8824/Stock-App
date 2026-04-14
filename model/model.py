from pyparsing import line
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import joblib
import csv
import os
from typing import Generator 

class Model:
    def __init__(self):
        self.model = MLPRegressor(hidden_layer_sizes=(100,), max_iter=2000, random_state=42)
        self.scaler = StandardScaler()

    def train(self, X_train, y_train):
        X_train_scaled = self.scaler.fit_transform(X_train)
        self.model.fit(X_train_scaled, y_train)

    def predict(self, X_test: list) -> np.ndarray:
        if type(X_test) == list:
            X_test = np.array(X_test, dtype=np.float32)
        elif type(X_test) == np.ndarray:
            pass
        else:
            raise ValueError("X_test must be a list or numpy array")
        X_test_scaled = self.scaler.transform(X_test)
        return self.model.predict(X_test_scaled)

    def save_model(self, file_path):
        joblib.dump(self.model, file_path)

    def load_model(self, file_path):
        self.model = joblib.load(file_path)

    def test_model(self, X_test, y_test):
        X_test_scaled = self.scaler.transform(X_test)
        return self.model.score(X_test_scaled, y_test)

    @staticmethod
    def convert_date_to_posix(date_str:str) -> int:
        temp_df = pd.DataFrame([date_str], columns=["date"])
        temp_df["date"] = pd.to_datetime(
            temp_df["date"],
            utc=True,
            format="%Y-%m-%d %H:%M:%S%z"
        )
        temp_df["date"] = temp_df["date"].astype("int64") // 10**9
        return int(temp_df["date"].iloc[0])
    
    @staticmethod
    def convert_all_times_in_history_to_posix(data_frame: pd.DataFrame) -> pd.DataFrame:
        data_frame["date"] = pd.to_datetime(
            data_frame["date"],
            utc=True,
            format="%Y-%m-%d %H:%M:%S%z"
        )
        data_frame["date"] = data_frame["date"].astype("int64") // 10**9
        return data_frame

    @staticmethod
    def get_data_for_model() ->  Generator[tuple[int, float, float, float, float, int], None, None]:
        """Generator that yields date, Open, high, low, close, volume from the data.csv file. Extra columns are ignored and return None. The date is converted to POSIX seconds and returned as an integer. Open, high, low, close are returned as floats and volume is returned as an integer."""
        file_path_data = os.path.join(os.path.dirname(__file__), "..", "data", "data.csv")
        with open(file_path_data, "r") as f:
            for index, line in enumerate(csv.reader(f)):
                if index != 0:
                    temp_data_frame = pd.DataFrame(
                        [line],
                        columns=["date", "Open", "high", "low", "close", "volume", "Dividends", "Stock Splits"]
                    )

                    temp_data_frame["date"] = pd.to_datetime(
                        temp_data_frame["date"],
                        utc=True,
                        format="%Y-%m-%d %H:%M:%S%z"
                    )

                    # Convert to POSIX seconds
                    temp_data_frame["date"] = temp_data_frame["date"].astype("int64") // 10**9

                    # Extract scalar
                    date = int(temp_data_frame["date"].iloc[0])

                    Open = float(line[1])
                    high = float(line[2])
                    low = float(line[3])
                    close = float(line[4])
                    volume = int(line[5])
                    print(date, Open, high, low, close, volume)
                    yield date, Open, high, low, close, volume
                else:
                    continue

model = Model()
lines = list(model.get_data_for_model())
X = np.array([[line[0]] for line in lines], dtype=np.float32)
y = np.array([[line[1], line[2], line[3], line[4]] for line in lines], dtype=np.float32)
model.train(X, y)
print(model.predict(X))
print(model.test_model(X, y))
print(model.predict([[model.convert_date_to_posix("2026-02-27 00:00:00-05:00")]]))
