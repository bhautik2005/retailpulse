import os
import pandas as pd
import logging

def run_inventory_model(config):

    logging.info("🚀 Running Inventory Model")

    processed_path = config["data"]["processed_path"]
    ml_path = config["data"]["ml_output_path"]

    # --- Ensure folder exists
    os.makedirs(ml_path, exist_ok=True)

    # --- Load data
    df = pd.read_csv(processed_path + "products.csv")

    # --- Create demand score
    df['demand_score'] = df['total_orders'] * df['total_revenue']

    # --- Handle edge case (important)
    if df['demand_score'].nunique() > 1:
        try:
            df['category'] = pd.qcut(
                df['demand_score'],
                q=[0, 0.6, 0.9, 1.0],
                labels=['Low Demand', 'Medium Demand', 'High Demand']
            )
        except ValueError:
            # If there are too many identical values (e.g. lots of 0s), qcut fails.
            # Using rank(method='first') forces unique values so we get expected buckets.
            df['category'] = pd.qcut(
                df['demand_score'].rank(method='first'),
                q=[0, 0.6, 0.9, 1.0],
                labels=['Low Demand', 'Medium Demand', 'High Demand']
            )
    else:
        df['category'] = 'Medium Demand'

    # --- Save to ML OUTPUT folder ✅
    df.to_csv(
        ml_path + "inventory_analysis.csv",
        index=False
    )

    logging.info("✅ Inventory model completed")
