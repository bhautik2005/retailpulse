import streamlit as st
import pandas as pd
from utils import load_data

def show_products():
    orders, _, _, _, _, _ = load_data()

    st.header("📦 Product Insights")
    st.divider()

    # --- Date Filters
    orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
    min_date = orders['order_purchase_timestamp'].min()
    max_date = orders['order_purchase_timestamp'].max()

    date_range = st.date_input(
        "Select Time Period",
        [min_date, max_date],
        key="product_date"
    )

    filtered = orders[
        (orders['order_purchase_timestamp'] >= pd.to_datetime(date_range[0])) &
        (orders['order_purchase_timestamp'] <= pd.to_datetime(date_range[1]))
    ]
    
    # Dynamically calculate product stats for the selected time period
    product_stats = filtered.groupby('product_id').agg(
        total_revenue=('payment_value', 'sum'),
        total_orders=('order_id', 'nunique')
    ).reset_index()

    # --- KPIs
    total_products = product_stats['product_id'].nunique()
    total_revenue = product_stats['total_revenue'].sum()
    
    col1, col2 = st.columns(2)
    col1.metric("Total Unique Products Sold", f"{total_products:,}")
    col2.metric("Total Catalog Revenue", f"${int(total_revenue):,}")

    st.divider()

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader(f"🏆 Top 10 Products by Revenue")
        top = product_stats.sort_values(by='total_revenue', ascending=False).head(10)
        if len(top) > 0:
            top['short_id'] = top['product_id'].astype(str).apply(lambda x: x[:8] + "...")
            st.bar_chart(top.set_index('short_id')['total_revenue'])
        else:
            st.info("No data for this period.")

    with col2:
        st.subheader("Data Overview")
        if len(top) > 0:
            st.dataframe(
                top[['short_id', 'total_revenue', 'total_orders']].set_index('short_id'),
                use_container_width=True
            )
        else:
            st.info("No data.")
