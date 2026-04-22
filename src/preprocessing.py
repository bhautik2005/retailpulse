import pandas as pd

def clean_data(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    df = df.copy()

    cleaning_config = config.get("cleaning", {})

    # 1. Drop duplicates
    if cleaning_config.get("drop_duplicates", True):
        df = df.drop_duplicates()

    # 2. Remove negative prices
    if cleaning_config.get("remove_negative_price", True):
        if "price" in df.columns:
            df = df[df["price"] > 0]

    # 3. Fill payment type
    if "payment_type" in df.columns:
        fill_val = cleaning_config.get("fill_payment_type", "unknown")
        df["payment_type"] = df["payment_type"].fillna(fill_val)

    # 4. Convert date columns
    date_cols = config.get("columns", {}).get("date_columns", [])
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    return df