import streamlit as st
import pandas as pd
from utils import load_data

def show_forecast():
    _, _, _, ts, _, forecast = load_data()

    st.header("📈 Demand Forecast")

    # add KPI
    next_30_days = forecast['forecast'].sum()
    st.metric("📊 Expected Revenue (Next 30 days)", f"${int(next_30_days):,}")
    
    st.divider()

    st.subheader("Historical Sales & Future Forecast")
    
    # Granularity selector
    granularity = st.radio(
        "Forecast View",
        ["Daily", "Weekly", "Monthly"],
        horizontal=True
    )
    
    ts['date'] = pd.to_datetime(ts['date'])
    forecast['date'] = pd.to_datetime(forecast['date'])
    
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