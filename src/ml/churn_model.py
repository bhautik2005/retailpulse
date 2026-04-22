import os
import pandas as pd
import joblib
import logging

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


def run_churn_model(config):

    logging.info("🚀 Running Churn Model")

    processed_path = config["data"]["processed_path"]
    ml_path = config["data"]["ml_output_path"]

    # --- Ensure folders exist
    os.makedirs("models", exist_ok=True)
    os.makedirs(ml_path, exist_ok=True)

    # --- Load data
    df = pd.read_csv(processed_path + "customers.csv")

    # --- Create target
    df['churn'] = (df['recency'] > 90).astype(int)

    # --- (NEW) Segmentation feature
    df['segment'] = pd.qcut(
        df['monetary'].rank(method='first'),
        q=[0, 0.5, 0.8, 0.95, 1.0],
        labels=['low', 'mid', 'high', 'vip']
    )

    # --- Features
    feature_cols = ['recency', 'frequency', 'monetary', 'avg_review']
    X = df[feature_cols]
    y = df['churn']

    # --- Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # --- Train
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    # --- Evaluate
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    logging.info(f"📊 Churn Model Accuracy: {acc:.4f}")

    # --- Save model
    joblib.dump(model, "models/churn_model.pkl")

    # --- Save predictions (to ML OUTPUT folder ✅)
    df['churn_pred'] = model.predict(X)

    df.to_csv(
        ml_path + "customer_predictions.csv",
        index=False
    )

    logging.info("✅ Churn model completed")
 
    st.header("🤖 Customer Churn Analysis")
    st.markdown("Predict customer status based on purchase frequency, spending, and satisfaction.")
    st.divider()

    # 1. Load the model
    model = load_churn_model()

    # 2. Input Section
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Transaction Data")
        # Recency is collected but not passed to the model as per your requirements
        recency = st.number_input("Recency (Days)", 0, 365, 30, help="Days since last purchase")
        frequency = st.number_input("Frequency", 1, 100, 5, help="Total number of orders")
        
    with col2:
        st.subheader("⭐ Customer Value")
        monetary = st.number_input("Monetary ($)", 0.0, 10000.0, 500.0, step=10.0)
        avg_review = st.slider("Avg Review Score", 1.0, 5.0, 4.0, step=0.1)

    st.markdown("---")

    # 3. Prediction Logic
    if st.button("🔍 Generate Risk Report", use_container_width=True):
        # Create the dataframe for the model (Frequency, Monetary, Review)
        input_df = pd.DataFrame([[frequency, monetary, avg_review]],
                                columns=['frequency', 'monetary', 'avg_review'])

        # Calculate Probabilities
        # probs[0] = Churn (0), probs[1] = Active (1)
        probs = model.predict_proba(input_df)[0]
        churn_prob = probs[0]
        active_prob = probs[1]

        # Apply your Custom 40% Threshold Logic
        if churn_prob > 0.40:
            status = "CHURN RISK"
            alert_type = st.error
        else:
            status = "Active"
            alert_type = st.success

        # 4. Display the Output exactly as requested
        result_string = f"Status: {status:10} | Risk Score: {churn_prob:.2%} | Active Confidence: {active_prob:.2%}"
        
        st.subheader("Prediction Result")
        alert_type(f"### {result_string}")

        # 5. Visual Breakdown
        st.write("---")
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Risk Probability", f"{churn_prob:.2%}")
        with c2:
            st.metric("Loyalty Confidence", f"{active_prob:.2%}")
            
        # Optional: Add a risk progress bar
        st.write("**Risk Intensity:**")
        st.progress(churn_prob)
        
        if status == "CHURN RISK":
            st.warning("🚨 **Retention Action Required:** This customer's risk profile exceeds the 40% safety threshold.")