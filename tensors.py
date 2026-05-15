import torch
from sklearn.preprocessing import StandardScaler

from data import get_training_dataframe, get_feature_columns

def training_tensors(validation_split: float = 0.2):
    training_data = training_frame_and_scaler(validation_split)

    X_train = torch.tensor(training_data["X_train"], dtype=torch.float32)
    y_train = torch.tensor(training_data["y_train"], dtype=torch.float32)
    X_val = torch.tensor(training_data["X_val"], dtype=torch.float32)
    y_val = torch.tensor(training_data["y_val"], dtype=torch.float32)
    return X_train, y_train, X_val, y_val

def training_frame_and_scaler(validation_split: float = 0.2) -> dict:
    """returns train/validation arrays along with the fitted feature scaler"""
    data = get_training_dataframe()
    feature_columns = get_feature_columns()

    X = data[feature_columns].to_numpy()
    y = data["predicted_return"].to_numpy()

    scaler_x = StandardScaler()
    split_index = int(len(X) * (1 - validation_split))

    X_train = scaler_x.fit_transform(X[:split_index])
    X_val = scaler_x.transform(X[split_index:])

    return {
        "dataframe": data,
        "feature_columns": feature_columns,
        "scaler": scaler_x,
        "split_index": split_index,
        "X_train": X_train,
        "y_train": y[:split_index],
        "X_val": X_val,
        "y_val": y[split_index:],
    }

if __name__ == "__main__":
    training_tensors()
