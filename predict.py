import joblib
import pandas as pd
# from sklearn.metrics import mean_absolute_error, mean_squared_error
from reestimator.params import STORAGE_LOCATION

# def get_model(path_to_joblib=STORAGE_LOCATION):
#     pipeline = joblib.load(path_to_joblib)
#     return pipeline


# def evaluate_model(y, y_pred):
#     MAE = round(mean_absolute_error(y, y_pred), 2)
#     RMSE = round(sqrt(mean_squared_error(y, y_pred)), 2)
#     res = {'MAE': MAE, 'RMSE': RMSE}
#     return res
