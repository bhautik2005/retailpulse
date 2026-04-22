import streamlit as st
import pandas as pd
from utils import load_data

def show_sales():
    orders, _, _, _, _, forecast = load_data()

    st.header("📊 Sales Dashboard")

    # --- Convert date
    orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])

    # --- Filters (INDUSTRY STANDARD 🔥)
    min_date = orders['order_purchase_timestamp'].min()
    max_date = orders['order_purchase_timestamp'].max()

    date_range = st.date_input(
        "Select Date Range",
        [min_date, max_date]
    )

    filtered = orders[
        (orders['order_purchase_timestamp'] >= pd.to_datetime(date_range[0])) &
        (orders['order_purchase_timestamp'] <= pd.to_datetime(date_range[1]))
    ]

    # --- KPIs (REAL BUSINESS METRICS 🔥)
    total_revenue = filtered['payment_value'].sum()
    total_orders = filtered['order_id'].nunique()
    avg_order_value = total_revenue / total_orders

    late_delivery_rate = filtered['is_late'].mean() * 100

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("💰 Revenue", f"${int(total_revenue):,}")
    col2.metric("📦 Orders", total_orders)
    col3.metric("🧾 Avg Order Value", f"${avg_order_value:.2f}")
    col4.metric("🚚 Late Delivery %", f"{late_delivery_rate:.1f}%")

    # --- Sales Trend
    st.divider()
    st.subheader("📈 Sales Trend")
    
    # Granularity selector
    granularity = st.radio(
        "Time Granularity",
        ["Daily", "Weekly", "Monthly", "Yearly"],
        horizontal=True
    )
    
    if granularity == "Daily":
        trend = filtered.groupby(filtered['order_purchase_timestamp'].dt.date)['payment_value'].sum()
        trend.index = pd.to_datetime(trend.index)
    elif granularity == "Weekly":
        trend = filtered.set_index('order_purchase_timestamp').resample('W')['payment_value'].sum()
    elif granularity == "Yearly":
        trend = filtered.groupby(filtered['order_purchase_timestamp'].dt.year)['payment_value'].sum()
        trend.index = trend.index.astype(str)
    else: # Monthly
        trend = filtered.groupby(['order_year', 'order_month'])['payment_value'].sum()
        trend.index = [f"{y}-{m:02d}" for y, m in trend.index]
        
    st.area_chart(trend)

    # --- Extra Visualizations
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("💳 Top Payment Methods")
        if 'payment_type' in filtered.columns:
            payment_dist = filtered.groupby('payment_type')['payment_value'].sum().sort_values(ascending=False)
            st.bar_chart(payment_dist)
        else:
            st.info("Payment type data not available in this view.")
            
    with col2:
        st.subheader("📍 Orders by Status")
        if 'order_status' in filtered.columns:
            status_dist = filtered['order_status'].value_counts()
            st.bar_chart(status_dist)
        else:
            st.info("Order status data not available in this view.")

    # --- Forecast Overlay
    st.subheader("🔮 Forecast vs Actual")
    forecast['date'] = pd.to_datetime(forecast['date'])
    st.line_chart(forecast.set_index('date')['forecast'])
