"""
Sales Analytics Dashboard
A comprehensive sales data analysis and visualization tool built with Streamlit
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Import custom modules
from data_generator import generate_sales_data
from utils import load_and_process_data, calculate_kpis
from pages import kpi_overview, sales_trends, regional_analysis, product_analysis, customer_analysis

# Page configuration
st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    
    /* Metric containers */
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.2rem;
        border-radius: 10px;
        border: none;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        color: white;
        margin-bottom: 1rem;
    }
    
    /* Enhanced metric styling */
    .stMetric {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin: 0.5rem 0;
    }
    
    .stMetric > label {
        font-size: 14px !important;
        font-weight: 600 !important;
        color: white !important;
    }
    
    .stMetric > div {
        font-size: 28px !important;
        font-weight: 700 !important;
        color: white !important;
    }
    
    /* Chart containers */
    .plotly-graph-div {
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    
    /* Enhanced buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Enhanced selectbox and multiselect */
    .stSelectbox > div > div {
        background-color: #f8f9fa;
        border-radius: 8px;
        border: 2px solid #e9ecef;
    }
    
    .stMultiSelect > div > div {
        background-color: #f8f9fa;
        border-radius: 8px;
        border: 2px solid #e9ecef;
    }
    
    /* Info boxes styling */
    .stAlert > div {
        border-radius: 8px;
        border-left: 4px solid;
    }
    
    /* Headers styling */
    h1 {
        color: #2c3e50;
        font-weight: 700;
        margin-bottom: 2rem;
    }
    
    h2 {
        color: #34495e;
        font-weight: 600;
        margin: 1.5rem 0 1rem 0;
    }
    
    h3 {
        color: #5a6c7d;
        font-weight: 600;
        margin: 1rem 0 0.5rem 0;
    }
    
    /* Enhanced dataframe styling */
    .stDataFrame > div {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Loading spinner */
    .stSpinner > div {
        border-color: #667eea transparent #667eea transparent;
    }
    
    /* Custom gradient background */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Sidebar filters styling */
    .css-1d391kg .stRadio > label {
        font-weight: 600;
        color: #2c3e50;
    }
    
    /* Enhanced tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 8px 8px 0 0;
        font-weight: 600;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #5a6fd8 0%, #6a4490 100%);
    }
    
    /* Animation for page transitions */
    .element-container {
        animation: fadeIn 0.5s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Enhanced sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
        border-right: 3px solid #667eea;
    }
    
    /* Footer styling */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        text-align: center;
        padding: 10px;
        font-size: 12px;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application function"""
    st.title("📊 Sales Analytics Dashboard")
    st.markdown("---")
    
    # Load data first
    with st.spinner("Loading sales data..."):
        df = load_and_process_data()
    
    # Sidebar navigation
    st.sidebar.title("🔍 Navigation & Filters")
    page = st.sidebar.radio(
        "Select Analysis View",
        ["📈 KPI Overview", "📊 Sales Trends", "🌍 Regional Analysis", 
         "🛍️ Product Performance", "👥 Customer Analysis"]
    )
    
    # Enhanced filtering system
    st.sidebar.markdown("### 📅 Date & Time Filters")
    
    # Quick date presets
    date_preset = st.sidebar.selectbox(
        "Quick Date Selection",
        ["Custom Range", "Last 30 Days", "Last 90 Days", "Last 6 Months", 
         "Last Year", "This Year", "All Time"]
    )
    
    # Calculate date range based on preset
    today = df['date'].max()
    if date_preset == "Last 30 Days":
        start_date = today - pd.Timedelta(days=30)
        end_date = today
    elif date_preset == "Last 90 Days":
        start_date = today - pd.Timedelta(days=90)
        end_date = today
    elif date_preset == "Last 6 Months":
        start_date = today - pd.Timedelta(days=180)
        end_date = today
    elif date_preset == "Last Year":
        start_date = today - pd.Timedelta(days=365)
        end_date = today
    elif date_preset == "This Year":
        start_date = pd.Timestamp(today.year, 1, 1)
        end_date = today
    elif date_preset == "All Time":
        start_date = df['date'].min()
        end_date = df['date'].max()
    else:  # Custom Range
        date_range = st.sidebar.date_input(
            "Select Custom Date Range",
            value=(df['date'].min(), df['date'].max()),
            min_value=df['date'].min(),
            max_value=df['date'].max()
        )
        if len(date_range) == 2:
            start_date, end_date = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
        else:
            start_date, end_date = df['date'].min(), df['date'].max()
    
    # Additional filters
    st.sidebar.markdown("### 🎯 Advanced Filters")
    
    # Region filter
    selected_regions = st.sidebar.multiselect(
        "Select Regions",
        options=sorted(df['region'].unique()),
        default=sorted(df['region'].unique())
    )
    
    # Product category filter
    selected_categories = st.sidebar.multiselect(
        "Select Product Categories",
        options=sorted(df['product_category'].unique()),
        default=sorted(df['product_category'].unique())
    )
    
    # Sales channel filter
    selected_channels = st.sidebar.multiselect(
        "Select Sales Channels",
        options=sorted(df['sales_channel'].unique()),
        default=sorted(df['sales_channel'].unique())
    )
    
    # Customer segment filter
    selected_segments = st.sidebar.multiselect(
        "Select Customer Segments",
        options=sorted(df['customer_segment'].unique()),
        default=sorted(df['customer_segment'].unique())
    )
    
    # Revenue range filter
    st.sidebar.markdown("### 💰 Revenue Range")
    min_revenue = float(df['revenue'].min())
    max_revenue = float(df['revenue'].max())
    
    revenue_range = st.sidebar.slider(
        "Revenue Range ($)",
        min_value=min_revenue,
        max_value=max_revenue,
        value=(min_revenue, max_revenue),
        step=10.0
    )
    
    # Apply all filters
    df_filtered = df[
        (df['date'] >= start_date) & 
        (df['date'] <= end_date) &
        (df['region'].isin(selected_regions)) &
        (df['product_category'].isin(selected_categories)) &
        (df['sales_channel'].isin(selected_channels)) &
        (df['customer_segment'].isin(selected_segments)) &
        (df['revenue'] >= revenue_range[0]) &
        (df['revenue'] <= revenue_range[1])
    ]
    
    # Filter summary
    st.sidebar.markdown("### 📊 Filter Summary")
    filter_info = f"""
    **Data Overview:**
    - Records: {len(df_filtered):,} of {len(df):,}
    - Date Range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}
    - Regions: {len(selected_regions)} of {df['region'].nunique()}
    - Categories: {len(selected_categories)} of {df['product_category'].nunique()}
    - Revenue: ${revenue_range[0]:,.0f} - ${revenue_range[1]:,.0f}
    """
    st.sidebar.info(filter_info)
    
    # Reset filters button
    if st.sidebar.button("🔄 Reset All Filters"):
        st.rerun()
    
    # Show data quality warning if too few records
    if len(df_filtered) < 100:
        st.warning("⚠️ Limited data available with current filters. Consider expanding filter criteria for more comprehensive analysis.")
    
    # Route to appropriate page with enhanced styling
    with st.container():
        if page == "📈 KPI Overview":
            kpi_overview.show(df_filtered)
        elif page == "📊 Sales Trends":
            sales_trends.show(df_filtered)
        elif page == "🌍 Regional Analysis":
            regional_analysis.show(df_filtered)
        elif page == "🛍️ Product Performance":
            product_analysis.show(df_filtered)
        elif page == "👥 Customer Analysis":
            customer_analysis.show(df_filtered)
    
    # Add footer
    st.markdown("""
    <div class="footer">
        Sales Analytics Dashboard • Built with Streamlit & Plotly • 
        Data updated: {} • Total Records: {:,}
    </div>
    """.format(
        df['date'].max().strftime('%Y-%m-%d'),
        len(df_filtered)
    ), unsafe_allow_html=True)

if __name__ == "__main__":
    main()