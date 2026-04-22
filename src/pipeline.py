import logging
# from config_loader import load_config
from src.config_loader import load_config
from src.ingestion import load_data
from src.merge import merge_data
from src.preprocessing import clean_data
from src.validation import validate_data
from src.feature_engineering import create_features
from src.build_datasets import build_datasets


# --- Logging setup
logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def run_pipeline(config_path="config/config.yaml"):

    try:
        # --- Load config
        config = load_config(config_path)
        logging.info("✅ Config loaded")

        raw_path = config["data"]["raw_path"]
        processed_path = config["data"]["processed_path"]

        logging.info("🚀 Pipeline started")

        # --- 1. Ingestion
        data = load_data(config)
        logging.info(f"✅ Data loaded: {list(data.keys())}")

        # --- 2. Merge
        df = merge_data(data, config)
        logging.info(f"✅ Data merged: shape={df.shape}")

        # --- 3. Cleaning
        df = clean_data(df, config)
        logging.info(f"✅ Data cleaned: shape={df.shape}")

        # --- 4. Validation
        validate_data(df, config)
        logging.info("✅ Data validated")

        # --- 5. Feature Engineering
        df = create_features(df, config)
        logging.info("✅ Features created")

        # --- 6. Build datasets
        customer_df, product_df, time_series_df = build_datasets(df)
        logging.info("✅ Derived datasets built")

        # --- 7. Save outputs
        df.to_csv(processed_path + "orders.csv", index=False)
        customer_df.to_csv(processed_path + "customers.csv", index=False)
        product_df.to_csv(processed_path + "products.csv", index=False)
        time_series_df.to_csv(processed_path + "time_series.csv", index=False)

        logging.info("✅ All files saved successfully")

        print("✅ PIPELINE COMPLETED")

    except Exception as e:
        logging.error(f"❌ Pipeline failed: {str(e)}", exc_info=True)
        print("❌ Pipeline failed. Check logs.")


if __name__ == "__main__":
    run_pipeline()