import pandas as pd

def create_features(df: pd.DataFrame, feature_config: dict) -> pd.DataFrame:

    # --- 1. Ensure datetime safely
    date_cols = [
        'order_purchase_timestamp',
        'order_delivered_customer_date',
        'order_estimated_delivery_date'
    ]

    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    # --- 2. Core feature (always useful)
    if all(col in df.columns for col in ['price', 'freight_value']):
        df['total_value'] = df['price'] + df['freight_value']

    # --- 3. Delivery features
    if feature_config.get("create_delivery_features", True):

        if all(col in df.columns for col in [
            'order_delivered_customer_date',
            'order_purchase_timestamp'
        ]):
            df['delivery_time'] = (
                df['order_delivered_customer_date'] - df['order_purchase_timestamp']
            ).dt.days

            df['delivery_time'].fillna(df['delivery_time'].median(), inplace=True)

        if all(col in df.columns for col in [
            'order_delivered_customer_date',
            'order_estimated_delivery_date'
        ]):
            df['delivery_delay'] = (
                df['order_delivered_customer_date'] - df['order_estimated_delivery_date']
            ).dt.days

            df['delivery_delay'].fillna(0, inplace=True)

            df['is_late'] = (df['delivery_delay'] > 0).astype(int)

    # --- 4. Time features
    if feature_config.get("create_time_features", True):

        if 'order_purchase_timestamp' in df.columns:
            df['order_year'] = df['order_purchase_timestamp'].dt.year
            df['order_month'] = df['order_purchase_timestamp'].dt.month
            df['order_weekday'] = df['order_purchase_timestamp'].dt.weekday
            df['order_hour'] = df['order_purchase_timestamp'].dt.hour

    return df