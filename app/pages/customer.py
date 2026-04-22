import streamlit as st
import pandas as pd
from utils import load_data

def show_customer():
    _, _, _, _, churn, _ = load_data()

    st.header("👥 Customer Insights")

    # Handle if customer_id doesn't exist
    total_customers = churn['customer_id'].nunique() if 'customer_id' in churn.columns else len(churn)
    churn_rate = churn['churn_pred'].mean() * 100

    col1, col2 = st.columns(2)
    col1.metric("Total Customers", f"{total_customers:,}")
    col2.metric("Predicted Churn Rate", f"{churn_rate:.1f}%")

    st.divider()

    # Recalculate segment dynamically so it shows the realistic non-even distribution
    churn['dynamic_segment'] = pd.qcut(
        churn['monetary'].rank(method='first'),
        q=[0, 0.5, 0.8, 0.95, 1.0],
        labels=['Low Value', 'Mid Value', 'High Value', 'VIP']
    )

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Churn Distribution")
        st.bar_chart(churn['churn_pred'].value_counts())

    with col2:
        st.subheader("Customer Segments")
        st.bar_chart(churn['dynamic_segment'].value_counts())