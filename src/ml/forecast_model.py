import os
import pandas as pd
import joblib
import logging

from statsmodels.tsa.arima.model import ARIMA


def run_forecast_model(config):

    logging.info("🚀 Running Forecast Model")

    processed_path = config["data"]["processed_path"]
    ml_path = config["data"]["ml_output_path"]

    # --- Ensure folders exist
    os.makedirs("models", exist_ok=True)
    os.makedirs(ml_path, exist_ok=True)

    # --- Load data
    df = pd.read_csv(processed_path + "time_series.csv")

    # --- Safety: ensure correct format
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])

    # --- Sort (important for time series)
    df = df.sort_values('date')

    # --- Train ARIMA
    model = ARIMA(df['daily_sales'], order=(5,1,0))
    model_fit = model.fit()

    # --- Calculate and log accuracy metrics
    from sklearn.metrics import mean_absolute_error
    train_preds = model_fit.predict()
    mae = mean_absolute_error(df['daily_sales'], train_preds)
    
    logging.info(f"📊 Forecast Model Training MAE: {mae:.2f}")
    logging.info(f"📊 Forecast Model AIC: {model_fit.aic:.2f}")

    # --- Forecast next 30 days
    forecast = model_fit.forecast(steps=30)

    # --- Create proper forecast dataframe (IMPORTANT FIX ✅)
    forecast_df = pd.DataFrame({
        "date": pd.date_range(
            start=df['date'].max(),
            periods=30,
            freq='D'
        ),
        "forecast": forecast.values
    })

    # --- Save model
    joblib.dump(model_fit, "models/forecast_model.pkl")

    # --- Save forecast to ML OUTPUT folder ✅
    forecast_df.to_csv(
        ml_path + "forecast.csv",
        index=False
    )

    logging.info("✅ Forecast model completed")
