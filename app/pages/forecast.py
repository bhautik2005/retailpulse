import streamlit as st
import pandas as pd
import joblib
from utils import load_data

def show_forecast():
    _, _, _, ts, _, forecast_default = load_data()

    st.header("📈 Demand Forecast")

    # Load the trained model dynamically
    try:
        model_fit = joblib.load("models/forecast_model.pkl")
        model_loaded = True
    except Exception as e:
        st.warning("Could not load dynamic forecast_model.pkl, falling back to static forecast.")
        model_loaded = False
        forecast = forecast_default

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        # Granularity selector
        granularity = st.radio(
            "Forecast View",
            ["Daily", "Weekly", "Monthly"],
            horizontal=True
        )
    
    with col2:
        # Forecast Horizon customization
        if model_loaded:
            horizon = st.slider("Forecast Horizon (Days)", min_value=7, max_value=365, value=30, step=1)
        else:
            horizon = 30
            st.info("Dynamic forecasting unavailable. Showing default 30 days.")

    ts['date'] = pd.to_datetime(ts['date'])
    
    if model_loaded:
        # Generate dynamic forecast
        forecast_values = model_fit.forecast(steps=horizon)
        last_date = ts['date'].max()
        forecast = pd.DataFrame({
            "date": pd.date_range(start=last_date + pd.Timedelta(days=1), periods=horizon, freq='D'),
            "forecast": forecast_values.values
        })
    else:
        forecast['date'] = pd.to_datetime(forecast['date'])

    # KPI - Expected Revenue
    expected_revenue = forecast['forecast'].sum()
    st.metric(f"📊 Expected Revenue (Next {horizon} days)", f"${int(expected_revenue):,}")
    
    st.divider()

    st.subheader("Historical Sales & Future Forecast")
    
    if granularity == "Daily":
        hist_trend = ts.set_index('date')['daily_sales']
        fut_trend = forecast.set_index('date')['forecast']
    elif granularity == "Weekly":
        hist_trend = ts.set_index('date').resample('W')['daily_sales'].sum()
        fut_trend = forecast.set_index('date').resample('W')['forecast'].sum()
    else: # Monthly
        hist_trend = ts.set_index('date').resample('M')['daily_sales'].sum()
        fut_trend = forecast.set_index('date').resample('M')['forecast'].sum()
        
    st.line_chart(hist_trend)
    st.subheader("Predicted Revenue Path")
    st.area_chart(fut_trend)