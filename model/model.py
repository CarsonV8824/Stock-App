from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import joblib
import csv
import os

class Model:
    def __init__(self):
        self.model = MLPClassifier(hidden_layer_sizes=(100,), max_iter=500, random_state=42)
        self.scaler = StandardScaler()

    def train(self, X_train, y_train):
        X_train_scaled = self.scaler.fit_transform(X_train)
        self.model.fit(X_train_scaled, y_train)

    def predict(self, X_test):
        X_test = np.array(X_test, dtype=np.float32)
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
    def convert_date_to_posix(date_str):
        temp_df = pd.DataFrame([date_str], columns=["date"])
        temp_df["date"] = pd.to_datetime(
            temp_df["date"],
            utc=True,
            format="%Y-%m-%d %H:%M:%S%z"
        )
        temp_df["date"] = temp_df["date"].astype("int64") // 10**9
        return int(temp_df["date"].iloc[0])

    @staticmethod
    def get_data_for_model():
        """2020-02-10 00:00:00-05:00"""
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
                    yield date, Open, high, low, close, volume
                else:
                    continue

model = Model()
lines = list(model.get_data_for_model())
X = np.array([[line[0], line[1], line[2], line[3], line[4], line[5]] for line in lines], dtype=np.float32)
y = np.array([1 if line[4] > line[1] else 0 for line in lines]) 
model.train(X, y)
print(model.predict(X))
print(model.test_model(X, y))
print(model.predict([[model.convert_date_to_posix("2020-02-10 00:00:00-05:00"),56.645632456, 76.54835795686193,73.46170617265714,74.53742980957031,200622400]]))