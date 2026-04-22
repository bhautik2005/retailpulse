import streamlit as st

# Configure page with custom icon and layout
st.set_page_config(
    page_title="RetailPulse Dashboard", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a modern UI feel
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {display: none;}
        
        .stButton>button {
            border-radius: 8px;
            font-weight: bold;
            border: 1px solid #1E88E5;
            color: #1E88E5;
        }
        .stButton>button:hover {
            background-color: #1E88E5;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar styling
with st.sidebar:
    st.title("⚡ RetailPulse")
    st.markdown("---")
    st.subheader("Navigation")
    
    # Modern selection box with icons
    page = st.radio(
        "Select a module",
        ["📊 Sales", "👥 Customer", "🤖 Churn Prediction", "📈 Forecast", "📦 Products", "🏭 Inventory"],
        key="main_nav_radio",
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.caption("Powered by ML & Advanced Analytics\n\n© 2026 RetailPulse")

# Router logic
if page == "📊 Sales":
    from pages.sales import show_sales
    show_sales()

elif page == "👥 Customer":
    from pages.customer import show_customer
    show_customer()

elif page == "🤖 Churn Prediction":
    from pages.churn_predict import show_churn_predict
    show_churn_predict()

elif page == "📈 Forecast":
    from pages.forecast import show_forecast
    show_forecast()

elif page == "📦 Products":
    from pages.products import show_products
    show_products()

elif page == "🏭 Inventory":
    from pages.inventory import show_inventory
    show_inventory()