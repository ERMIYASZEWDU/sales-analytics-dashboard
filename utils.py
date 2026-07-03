"""
Utility functions for data processing and analysis
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import streamlit as st
import os
from data_generator import generate_sales_data

@st.cache_data
def load_and_process_data():
    """Load and process sales data with caching"""
    
    # Check if data file exists, if not generate it
    if not os.path.exists('sales_data.csv'):
        st.info("Generating sample data for the first time...")
        df = generate_sales_data(10000)
        df.to_csv('sales_data.csv', index=False)
    else:
        df = pd.read_csv('sales_data.csv')
        df['date'] = pd.to_datetime(df['date'])
        df['customer_since'] = pd.to_datetime(df['customer_since'])
    
    return df

def calculate_kpis(df):
    """Calculate key performance indicators"""
    
    total_revenue = df['revenue'].sum()
    total_orders = len(df)
    unique_customers = df['customer_id'].nunique()
    avg_order_value = df['revenue'].mean()
    
    # Calculate period-over-period growth
    df_sorted = df.sort_values('date')
    current_month = df_sorted['date'].max().month
    current_year = df_sorted['date'].max().year
    
    # Current month data
    current_month_data = df[
        (df['date'].dt.month == current_month) & 
        (df['date'].dt.year == current_year)
    ]
    
    # Previous month data
    if current_month == 1:
        prev_month, prev_year = 12, current_year - 1
    else:
        prev_month, prev_year = current_month - 1, current_year
    
    prev_month_data = df[
        (df['date'].dt.month == prev_month) & 
        (df['date'].dt.year == prev_year)
    ]
    
    # Calculate growth rates
    current_revenue = current_month_data['revenue'].sum()
    prev_revenue = prev_month_data['revenue'].sum()
    
    revenue_growth = ((current_revenue - prev_revenue) / prev_revenue * 100) if prev_revenue > 0 else 0
    
    current_orders = len(current_month_data)
    prev_orders = len(prev_month_data)
    
    order_growth = ((current_orders - prev_orders) / prev_orders * 100) if prev_orders > 0 else 0
    
    return {
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'unique_customers': unique_customers,
        'avg_order_value': avg_order_value,
        'revenue_growth': revenue_growth,
        'order_growth': order_growth,
        'current_month_revenue': current_revenue,
        'prev_month_revenue': prev_revenue
    }

def get_top_products(df, n=10):
    """Get top N products by revenue"""
    return df.groupby('product_name')['revenue'].sum().nlargest(n).reset_index()

def get_regional_performance(df):
    """Calculate regional sales performance"""
    regional_stats = df.groupby('region').agg({
        'revenue': ['sum', 'mean', 'count'],
        'customer_id': 'nunique'
    }).round(2)
    
    regional_stats.columns = ['total_revenue', 'avg_order_value', 'total_orders', 'unique_customers']
    regional_stats = regional_stats.reset_index()
    
    return regional_stats

def calculate_customer_segments(df):
    """Perform RFM analysis for customer segmentation"""
    
    # Calculate RFM metrics
    current_date = df['date'].max()
    
    rfm = df.groupby('customer_id').agg({
        'date': lambda x: (current_date - x.max()).days,  # Recency
        'transaction_id': 'count',  # Frequency
        'revenue': 'sum'  # Monetary
    }).reset_index()
    
    rfm.columns = ['customer_id', 'recency', 'frequency', 'monetary']
    
    # Create RFM scores (1-5 scale)
    rfm['r_score'] = pd.qcut(rfm['recency'].rank(method='first'), 5, labels=[5,4,3,2,1])
    rfm['f_score'] = pd.qcut(rfm['frequency'].rank(method='first'), 5, labels=[1,2,3,4,5])
    rfm['m_score'] = pd.qcut(rfm['monetary'].rank(method='first'), 5, labels=[1,2,3,4,5])
    
    # Combine RFM scores
    rfm['rfm_score'] = rfm['r_score'].astype(str) + rfm['f_score'].astype(str) + rfm['m_score'].astype(str)
    
    # Create customer segments
    def segment_customers(row):
        if row['rfm_score'] in ['555', '554', '544', '545', '454', '455', '445']:
            return 'Champions'
        elif row['rfm_score'] in ['543', '444', '435', '355', '354', '345', '344', '335']:
            return 'Loyal Customers'
        elif row['rfm_score'] in ['553', '551', '552', '541', '542', '533', '532', '531', '452', '451']:
            return 'Potential Loyalists'
        elif row['rfm_score'] in ['512', '511', '422', '421', '412', '411', '311']:
            return 'New Customers'
        elif row['rfm_score'] in ['155', '154', '144', '214', '215', '115', '114']:
            return 'At Risk'
        elif row['rfm_score'] in ['155', '154', '144', '214', '215', '115']:
            return 'Cannot Lose Them'
        else:
            return 'Others'
    
    rfm['segment'] = rfm.apply(segment_customers, axis=1)
    
    return rfm

def format_currency(value):
    """Format value as currency"""
    return f"${value:,.2f}"

def format_number(value):
    """Format number with commas"""
    return f"{value:,}"

def calculate_seasonal_trends(df):
    """Calculate seasonal sales trends"""
    monthly_sales = df.groupby(df['date'].dt.to_period('M'))['revenue'].sum().reset_index()
    monthly_sales['date'] = monthly_sales['date'].dt.to_timestamp()
    
    quarterly_sales = df.groupby(['year', 'quarter'])['revenue'].sum().reset_index()
    quarterly_sales['period'] = quarterly_sales['year'].astype(str) + ' Q' + quarterly_sales['quarter'].astype(str)
    
    return monthly_sales, quarterly_sales

def get_channel_performance(df):
    """Analyze sales channel performance"""
    channel_stats = df.groupby('sales_channel').agg({
        'revenue': ['sum', 'mean'],
        'transaction_id': 'count',
        'customer_id': 'nunique'
    }).round(2)
    
    channel_stats.columns = ['total_revenue', 'avg_order_value', 'total_orders', 'unique_customers']
    channel_stats = channel_stats.reset_index()
    
    # Calculate conversion rate (assuming total visitors is 10x unique customers)
    channel_stats['estimated_visitors'] = channel_stats['unique_customers'] * 10
    channel_stats['conversion_rate'] = (channel_stats['unique_customers'] / channel_stats['estimated_visitors'] * 100).round(2)
    
    return channel_stats