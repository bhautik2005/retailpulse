import os
import logging

from src.config_loader import load_config
from src.ml.churn_model import run_churn_model
from src.ml.forecast_model import run_forecast_model
from src.ml.inventory_model import run_inventory_model


logging.basicConfig(
    filename="logs/ml_pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def run_ml_pipeline():

    try:
        config = load_config()

        ml_path = config["data"]["ml_output_path"]

        # --- Ensure folder exists
        os.makedirs(ml_path, exist_ok=True)
        os.makedirs("models", exist_ok=True)

        logging.info("🚀 ML Pipeline Started")

        # --- Run models
        run_churn_model(config)
        run_forecast_model(config)
        run_inventory_model(config)

        logging.info("✅ All models completed")
        print("✅ ML PIPELINE COMPLETED")

    except Exception as e:
        logging.error(f"❌ ML Pipeline failed: {str(e)}", exc_info=True)
        print("❌ ML pipeline failed. Check logs.")


if __name__ == "__main__":
    run_ml_pipeline()
