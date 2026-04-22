import streamlit as st
import pandas as pd
from utils import load_churn_model

# def show_churn_predict():

#     st.header("🤖 Customer Churn Prediction")
#     st.markdown("Enter the customer's behavioral metrics below to predict their likelihood of churning.")
#     st.divider()

#     model = load_churn_model()

#     col1, col2 = st.columns(2)
    
#     with col1:
#         st.subheader("Purchase Behavior")
#         recency = st.number_input("Recency (Days Since Last Order)", 0, 365, 30)
#         frequency = st.number_input("Frequency (Total Purchases)", 1, 100, 2)
        
#     with col2:
#         st.subheader("Satisfaction & Experience")
#         monetary = st.number_input("Total Lifetime Spend ($)", 0.0, 100000.0, 500.0, step=50.0)
#         avg_review = st.slider("Average Review Score", 1.0, 5.0, 4.0, step=0.1)

#     st.markdown("---")

#     if st.button("🔍 Predict Churn Risk", use_container_width=True):
#         with st.spinner("Analyzing customer profile using Random Forest..."):
#             data = pd.DataFrame([[recency, frequency, monetary, avg_review]],
#                                 columns=['recency', 'frequency','monetary','avg_review'])

#             pred = model.predict(data)[0]

#             st.divider()
#             if pred == 1:
#                 st.error("⚠️ **High Risk Customer (Churn Detected)**\n\nThis customer's profile matches historical patterns of churn. Consider triggering an automated retention workflow (e.g., personalized discount email).")
#             else:
#                 st.success("✅ **Loyal Customer**\n\nThis customer shows strong retention signals. No immediate action is required.")
 
def show_churn_predict():
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