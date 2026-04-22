🚀 RetailPulse: AI-Powered E-Commerce Analytics Platform

RetailPulse is a full-stack data analytics + machine learning platform that transforms raw e-commerce data into actionable business insights.
```
It integrates:

📊 Data Pipeline (ETL)
🤖 Machine Learning Models
📈 Interactive Dashboard (Streamlit)
🎯 Project Objectives
Analyze sales, customer behavior, and product performance
Predict customer churn
Forecast future sales demand
Optimize inventory decisions
Build a real-world end-to-end data product
🧠 Key Features
📊 Data Analytics
Sales trend analysis
Customer segmentation (RFM)
Delivery performance insights
Product category performance
🤖 Machine Learning Models
1️⃣ Churn Prediction
Predicts customers likely to stop purchasing
Model: Random Forest
Output: customer_predictions.csv
2️⃣ Demand Forecasting
Predicts future sales (next 30 days)
Model: ARIMA
Output: forecast.csv
3️⃣ Inventory Optimization (Analytics-Based)
Categorizes products:
High Demand
Medium Demand
Low Demand
Output: inventory_analysis.csv

📦 Project Structure

RetailPulse/
│
├── data/
│   ├── raw/
│   ├── processed/
│   ├── ml_outputs/
│
├── models/
│
├── logs/
│
├── src/
│   ├── pipeline.py
│   ├── preprocessing.py
│   ├── validation.py
│   ├── feature_engineering.py
│   ├── build_datasets.py
│   ├── ml/
│       ├── churn_model.py
│       ├── forecast_model.py
│       ├── inventory_model.py
│       ├── run_all_models.py
│
├── app/
│   ├── app.py
│   ├── pages/
│
├── config/
│   ├── config.yaml
│
├── requirements.txt
└── README.md

🔄 Workflow Pipeline
Raw Data → Data Cleaning → Feature Engineering
        → ML Models → Predictions
        → Streamlit Dashboard → Insights


🚀 How to Run the Project
1️⃣ Install Dependencies
pip install -r requirements.txt

2️⃣ Run Data Pipeline
python -m src.pipeline

3️⃣ Run ML Models
python -m src.ml.run_all_models

4️⃣ Run Dashboard
streamlit run app/app.py

📊 Dashboard Pages
  - 📊 Sales Dashboard (KPIs + trends + forecast)
  - 👥 Customer Dashboard (churn + segmentation)
  - 🤖 Churn Prediction (user input → prediction)
  - 📈 Forecast Dashboard (future sales)
  - 📦 Inventory Dashboard (stock insights)

🧠 Business Insights Generated

Late deliveries negatively impact customer reviews
A small segment of customers drives most revenue
Certain product categories dominate sales
High churn customers can be targeted for retention
Inventory can be optimized using demand segmentation


🛠️ Tech Stack
Python
Pandas, NumPy
Scikit-learn
Statsmodels
Streamlit
Matplotlib, Seaborn
 
🎯 Future Improvements
Add real-time data pipeline
Deploy backend using FastAPI
Add model explainability (SHAP)
Integrate cloud storage (AWS S3)
Enhance UI with advanced filters
👨‍💻 Author

Bhautik Gondaliya
