import pandas as pd
import joblib

def load_data():
    orders = pd.read_csv("data/processed/orders.csv")
    customers = pd.read_csv("data/processed/customers.csv")
    products = pd.read_csv("data/processed/products.csv")
    time_series = pd.read_csv("data/processed/time_series.csv")

    churn = pd.read_csv("data/ml_outputs/customer_predictions.csv")
    forecast = pd.read_csv("data/ml_outputs/forecast.csv")

    return orders, customers, products, time_series, churn, forecast

def load_churn_model():
    return joblib.load("models/churn_model2.pkl")
