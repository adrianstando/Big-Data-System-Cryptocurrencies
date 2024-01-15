from fastapi import FastAPI, HTTPException, Query
from river import metrics
from river.forest import ARFRegressor
from sklearn.linear_model import LinearRegression
from typing import List
import numpy as np
import os

app = FastAPI()

N_LAG_VALUES = os.getenv('N_LAG_VALUES', default=10)
N_PER_ROLLING_METRIC = os.getenv('N_PER_ROLLING_METRIC', default=10)

models = {}
rolling_mse_arf_dict = {}
rolling_mse_lr_dict = {}


class RollingRMSE:
    def __init__(self, window_size):
        self.window_size = window_size
        self.y_true_list = []
        self.y_pred_list = []

    def update(self, y_true, y_pred):
        self.y_true_list.append(y_true)
        self.y_pred_list.append(y_pred)

        # Keep only the last `window_size` observations
        if len(self.y_true_list) > self.window_size:
            self.y_true_list.pop(0)
            self.y_pred_list.pop(0)

    def get(self):
        if len(self.y_true_list) == 0:
            raise Warning("No observations available to calculate RMSE.")

        # Calculate RMSE for the last `window_size` observations
        squared_errors = [(true - pred) ** 2 for true, pred in zip(self.y_true_list, self.y_pred_list)]
        mean_squared_error = sum(squared_errors) / len(squared_errors)
        root_mean_squared_error = mean_squared_error ** 0.5

        return root_mean_squared_error


def create_model():
    return ARFRegressor(
        n_models=50,  # number of trees
        grace_period=20,  # number of observations before the model starts to update itself
        max_size=100,  # maximum size of the model in MB
        metric=metrics.RMSE(),  # metric to track the performance of the model
        seed=42  # random seed for reproducibility
    )


def create_rolling_metric():
    return RollingRMSE(window_size=N_PER_ROLLING_METRIC)


def extract_features(lag_values):
    # extract features from lag values for the format that the model expects
    lag_values_dict = {f"lag_{i}": lag for i, lag in enumerate(lag_values, start=1)}
    sample = {
        **lag_values_dict
    }

    return sample


@app.get("/")
async def root():
    return {"message": "Hello World"}


# Route to predict future value
@app.get("/predict")
async def predict(
        lag_values: List[float] = Query(None),
        crypto_name: str = 'BTC'
):
    try:
        original_lag_values = lag_values.copy()

        if len(lag_values) < N_LAG_VALUES:
            mean_value = sum(lag_values) / len(lag_values)
            std_value = np.std(lag_values)
            missing_values = list(np.random.normal(mean_value, std_value, N_LAG_VALUES - len(lag_values)))
            lag_values = missing_values + lag_values

        if crypto_name not in models:
            models[crypto_name] = create_model()
            rolling_mse_arf_dict[crypto_name] = create_rolling_metric()
            rolling_mse_lr_dict[crypto_name] = create_rolling_metric()

        model = models[crypto_name]
        rolling_mse_arf = rolling_mse_arf_dict[crypto_name]
        rolling_mse_lr = rolling_mse_lr_dict[crypto_name]

        # FIRST MODEL
        # Adaptive Random Forest model

        previous_window_for_prediction = lag_values[:-1]
        true_value = original_lag_values[-1]
        newest_window_for_prediction = lag_values[1:]

        # update the model with the previous value
        previous_features = extract_features(previous_window_for_prediction)
        prediction = model.predict_one(previous_features)
        rolling_mse_arf.update(true_value, prediction)
        model.learn_one(previous_features, true_value)
        current_rolling_mse = rolling_mse_arf.get()
        prediction_arf_previous = prediction

        # predict the future value
        newest_features = extract_features(newest_window_for_prediction)
        prediction_arf = model.predict_one(newest_features)

        # SECOND MODEL
        # curve fitting with LinearRegression
        if len(original_lag_values) < 2:
            original_lag_values = [
                original_lag_values[0],
                original_lag_values[0] + np.random.normal(0, 0.1, 1)[0]
            ]

        y_values_previous = original_lag_values[:-1]
        y_values = original_lag_values[1:]

        # create once more the previous model
        true_value = original_lag_values[-1]
        X_values = np.arange(1, len(y_values_previous) + 1).reshape(-1, 1)
        lr = LinearRegression().fit(X_values, y_values_previous)
        prediction_lr = float(lr.predict([[len(y_values_previous) + 1]])[0])
        rolling_mse_lr.update(true_value, prediction_lr)
        current_rolling_mse_lr = rolling_mse_lr.get()
        prediction_lr_previous = prediction_lr

        # predict the future value
        X_values = np.arange(1, len(y_values) + 1).reshape(-1, 1)
        lr = LinearRegression().fit(X_values, y_values)
        prediction_lr = float(lr.predict([[len(y_values_previous) + 1]])[0])

        return {
            "prediction_arf": prediction_arf,
            "rolling_rmse_arf": current_rolling_mse,
            "prediction_lr": prediction_lr,
            "rolling_rmse_lr": current_rolling_mse_lr,
            "real_previous_value": true_value,
            "prediction_previous_value_lr": prediction_lr_previous,
            "prediction_previous_value_arf": prediction_arf_previous
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
