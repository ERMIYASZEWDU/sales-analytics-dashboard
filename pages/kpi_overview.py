"""
KPI Overview Page
Main dashboard with key performance indicators and summary metrics
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils import calculate_kpis, format_currency, format_number, calculate_seasonal_trends

def show(df):
    """Display KPI overview dashboard"""
    
    st.header("📈 Key Performance Indicators")
    
    # Calculate KPIs
    kpis = calculate_kpis(df)
    
    # Top-level metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Revenue",
            value=format_currency(kpis['total_revenue']),
            delta=f"{kpis['revenue_growth']:.1f}% vs last month"
        )
    
    with col2:
        st.metric(
            label="Total Orders",
            value=format_number(kpis['total_orders']),
            delta=f"{kpis['order_growth']:.1f}% vs last month"
        )
    
    with col3:
        st.metric(
            label="Unique Customers",
            value=format_number(kpis['unique_customers'])
        )
    
    with col4:
        st.metric(
            label="Avg Order Value",
            value=format_currency(kpis['avg_order_value'])
        )
    
    st.markdown("---")
    
    # Revenue trends and distribution
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📊 Revenue Trends")
        
        # Monthly revenue trend
        monthly_sales, quarterly_sales = calculate_seasonal_trends(df)
        
        fig_trend = px.line(
            monthly_sales,
            x='date',
            y='revenue',
            title='Monthly Revenue Trend',
            labels={'revenue': 'Revenue ($)', 'date': 'Date'}
        )
        fig_trend.update_layout(height=400)
        fig_trend.update_traces(line=dict(width=3, color='#1f77b4'))
        st.plotly_chart(fig_trend, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Revenue by Quarter")
        
        # Quarterly revenue pie chart
        fig_pie = px.pie(
            quarterly_sales,
            values='revenue',
            names='period',
            title='Quarterly Distribution'
        )
        fig_pie.update_layout(height=400)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Sales channel and category performance
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📱 Sales by Channel")
        
        channel_revenue = df.groupby('sales_channel')['revenue'].sum().reset_index()
        channel_revenue = channel_revenue.sort_values('revenue', ascending=True)
        
        fig_channel = px.bar(
            channel_revenue,
            x='revenue',
            y='sales_channel',
            orientation='h',
            title='Revenue by Sales Channel',
            labels={'revenue': 'Revenue ($)', 'sales_channel': 'Sales Channel'}
        )
        fig_channel.update_layout(height=400)
        st.plotly_chart(fig_channel, use_container_width=True)
    
    with col2:
        st.subheader("🛍️ Sales by Category")
        
        category_revenue = df.groupby('product_category')['revenue'].sum().reset_index()
        category_revenue = category_revenue.sort_values('revenue', ascending=True)
        
        fig_category = px.bar(
            category_revenue,
            x='revenue',
            y='product_category',
            orientation='h',
            title='Revenue by Product Category',
            labels={'revenue': 'Revenue ($)', 'product_category': 'Category'}
        )
        fig_category.update_layout(height=400)
        st.plotly_chart(fig_category, use_container_width=True)
    
    # Performance summary table
    st.subheader("📋 Performance Summary")
    
    # Create summary metrics by different dimensions
    summary_data = []
    
    # By month
    monthly_summary = df.groupby(df['date'].dt.to_period('M')).agg({
        'revenue': 'sum',
        'transaction_id': 'count',
        'customer_id': 'nunique'
    }).reset_index()
    monthly_summary['date'] = monthly_summary['date'].dt.to_timestamp()
    monthly_summary['avg_order_value'] = monthly_summary['revenue'] / monthly_summary['transaction_id']
    
    # Recent months performance
    recent_months = monthly_summary.tail(6)
    recent_months['period'] = recent_months['date'].dt.strftime('%Y-%m')
    recent_months = recent_months[['period', 'revenue', 'transaction_id', 'customer_id', 'avg_order_value']]
    recent_months.columns = ['Period', 'Revenue', 'Orders', 'Customers', 'Avg Order Value']
    
    # Format for display
    recent_months['Revenue'] = recent_months['Revenue'].apply(format_currency)
    recent_months['Avg Order Value'] = recent_months['Avg Order Value'].apply(format_currency)
    
    st.dataframe(recent_months, use_container_width=True, hide_index=True)
    
    # Key insights
    st.subheader("💡 Key Insights")
    
    # Calculate insights
    top_category = df.groupby('product_category')['revenue'].sum().idxmax()
    top_region = df.groupby('region')['revenue'].sum().idxmax()
    top_channel = df.groupby('sales_channel')['revenue'].sum().idxmax()
    
    peak_month = monthly_sales.loc[monthly_sales['revenue'].idxmax(), 'date'].strftime('%B %Y')
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"""
        **Top Performers:**
        - Best Category: {top_category}
        - Best Region: {top_region}
        - Best Channel: {top_channel}
        """)
    
    with col2:
        st.success(f"""
        **Business Highlights:**
        - Peak Month: {peak_month}
        - Total Customers: {kpis['unique_customers']:,}
        - Growth Rate: {kpis['revenue_growth']:.1f}%
        """)