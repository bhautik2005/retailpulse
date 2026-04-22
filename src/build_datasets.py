import pandas as pd

def build_datasets(df):

    # --- Customer (RFM base)
    customer_df = df.groupby('customer_unique_id').agg({
        'order_purchase_timestamp': ['max','count'],
        'payment_value': 'sum',
        'review_score': 'mean'
    }).reset_index()

    customer_df.columns = ['customer_id','last_purchase','frequency','monetary','avg_review']

    latest = df['order_purchase_timestamp'].max()
    customer_df['recency'] = (latest - customer_df['last_purchase']).dt.days

    # --- Product
    product_df = df.groupby('product_id').agg({
        'order_id':'count',
        'payment_value':'sum',
        'price':'mean'
    }).reset_index()

    product_df.columns = ['product_id','total_orders','total_revenue','avg_price']

    # --- Time series
    ts = df.groupby(df['order_purchase_timestamp'].dt.date)['payment_value'].sum().reset_index()
    ts.columns = ['date','daily_sales']

    return customer_df, product_df, ts