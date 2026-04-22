import streamlit as st
import pandas as pd
from utils import load_data

def show_inventory():
    orders, _, _, _, _, _ = load_data()

    st.header("🏭 Inventory & Demand Dashboard")
    st.divider()

    # --- Date Filters
    orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
    min_date = orders['order_purchase_timestamp'].min()
    max_date = orders['order_purchase_timestamp'].max()

    date_range = st.date_input(
        "Select Time Period",
        [min_date, max_date],
        key="inventory_date"
    )

    filtered = orders[
        (orders['order_purchase_timestamp'] >= pd.to_datetime(date_range[0])) &
        (orders['order_purchase_timestamp'] <= pd.to_datetime(date_range[1]))
    ]
    
    # Calculate demand score on the fly for the selected date range
    product_stats = filtered.groupby('product_id').agg(
        total_revenue=('payment_value', 'sum'),
        total_orders=('order_id', 'nunique')
    ).reset_index()
    
    product_stats['demand_score'] = product_stats['total_orders'] * product_stats['total_revenue']
    
    if len(product_stats) > 0:
        try:
            product_stats['category'] = pd.qcut(
                product_stats['demand_score'],
                q=[0, 0.6, 0.9, 1.0],
                labels=['Low Demand', 'Medium Demand', 'High Demand']
            )
        except ValueError:
            product_stats['category'] = pd.qcut(
                product_stats['demand_score'].rank(method='first'),
                q=[0, 0.6, 0.9, 1.0],
                labels=['Low Demand', 'Medium Demand', 'High Demand']
            )
    else:
        product_stats['category'] = pd.Series([], dtype='object')

    # --- KPIs
    total_products = product_stats['product_id'].nunique()
    high_demand = (product_stats['category'] == 'High Demand').sum()
    low_demand = (product_stats['category'] == 'Low Demand').sum()

    col1, col2, col3 = st.columns(3)
    col1.metric("Active Products", total_products)
    col2.metric("🔥 High Demand", high_demand)
    col3.metric("❄️ Low Demand", low_demand)

    st.divider()

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Demand Distribution")
        if len(product_stats) > 0:
            st.bar_chart(product_stats['category'].value_counts())
        else:
            st.info("No data.")

    with col2:
        st.subheader("🔥 Top Products by Demand Score")
        if len(product_stats) > 0:
            top = product_stats.sort_values(by='demand_score', ascending=False).head(10)
            top['short_id'] = top['product_id'].astype(str).apply(lambda x: x[:8] + "...")
            st.dataframe(top[['short_id','demand_score','category']].set_index('short_id'), use_container_width=True)
        else:
            st.info("No data.")

    st.divider()
    st.info("""
    **Business Logic:**
    🔥 **High Demand (Top 10%)** → Priority restocking  
    ⚠️ **Medium Demand (Next 30%)** → Maintain normal inventory  
    ❄️ **Low Demand (Bottom 60%)** → Reduce inventory overhead
    """)
