"""
Regional Analysis Page
Geographic sales performance and regional insights
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import get_regional_performance, format_currency, format_number

def show(df):
    """Display regional sales analysis"""
    
    st.header("🌍 Regional Sales Analysis")
    
    # Regional performance overview
    regional_stats = get_regional_performance(df)
    
    # Top-level regional metrics
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🏆 Regional Performance Ranking")
        
        # Sort by total revenue
        regional_stats_sorted = regional_stats.sort_values('total_revenue', ascending=False)
        
        fig_regional = px.bar(
            regional_stats_sorted,
            x='total_revenue',
            y='region',
            orientation='h',
            title='Total Revenue by Region',
            labels={'total_revenue': 'Revenue ($)', 'region': 'Region'},
            color='total_revenue',
            color_continuous_scale='Viridis'
        )
        fig_regional.update_layout(height=400)
        st.plotly_chart(fig_regional, use_container_width=True)
    
    with col2:
        st.subheader("📊 Market Share")
        
        fig_pie = px.pie(
            regional_stats,
            values='total_revenue',
            names='region',
            title='Revenue Market Share'
        )
        fig_pie.update_layout(height=400)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Detailed regional metrics
    st.subheader("📈 Regional Performance Metrics")
    
    # Format the regional stats for display
    display_stats = regional_stats.copy()
    display_stats['total_revenue'] = display_stats['total_revenue'].apply(format_currency)
    display_stats['avg_order_value'] = display_stats['avg_order_value'].apply(format_currency)
    display_stats['total_orders'] = display_stats['total_orders'].apply(format_number)
    display_stats['unique_customers'] = display_stats['unique_customers'].apply(format_number)
    
    # Add calculated metrics
    regional_stats['revenue_per_customer'] = regional_stats['total_revenue'] / regional_stats['unique_customers']
    regional_stats['orders_per_customer'] = regional_stats['total_orders'] / regional_stats['unique_customers']
    
    display_stats['revenue_per_customer'] = regional_stats['revenue_per_customer'].apply(format_currency)
    display_stats['orders_per_customer'] = regional_stats['orders_per_customer'].round(2)
    
    # Rename columns for better display
    display_stats.columns = [
        'Region', 'Total Revenue', 'Avg Order Value', 'Total Orders', 
        'Unique Customers', 'Revenue per Customer', 'Orders per Customer'
    ]
    
    st.dataframe(display_stats, use_container_width=True, hide_index=True)
    
    # City-level analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏙️ Top Cities by Revenue")
        
        city_revenue = df.groupby(['region', 'city'])['revenue'].sum().reset_index()
        city_revenue = city_revenue.sort_values('revenue', ascending=False).head(10)
        city_revenue['city_region'] = city_revenue['city'] + ' (' + city_revenue['region'] + ')'
        
        fig_cities = px.bar(
            city_revenue,
            x='revenue',
            y='city_region',
            orientation='h',
            title='Top 10 Cities by Revenue',
            labels={'revenue': 'Revenue ($)', 'city_region': 'City (Region)'}
        )
        fig_cities.update_layout(height=500)
        st.plotly_chart(fig_cities, use_container_width=True)
    
    with col2:
        st.subheader("👥 Customer Distribution")
        
        customer_by_city = df.groupby(['region', 'city'])['customer_id'].nunique().reset_index()
        customer_by_city = customer_by_city.sort_values('customer_id', ascending=False).head(10)
        customer_by_city['city_region'] = customer_by_city['city'] + ' (' + customer_by_city['region'] + ')'
        
        fig_customers = px.bar(
            customer_by_city,
            x='customer_id',
            y='city_region',
            orientation='h',
            title='Top 10 Cities by Customer Count',
            labels={'customer_id': 'Unique Customers', 'city_region': 'City (Region)'},
            color='customer_id',
            color_continuous_scale='Blues'
        )
        fig_customers.update_layout(height=500)
        st.plotly_chart(fig_customers, use_container_width=True)
    
    # Regional trends over time
    st.subheader("📅 Regional Trends Over Time")
    
    # Monthly trends by region
    monthly_regional = df.groupby([df['date'].dt.to_period('M'), 'region'])['revenue'].sum().reset_index()
    monthly_regional['date'] = monthly_regional['date'].dt.to_timestamp()
    
    fig_trends = px.line(
        monthly_regional,
        x='date',
        y='revenue',
        color='region',
        title='Monthly Revenue Trends by Region',
        labels={'revenue': 'Revenue ($)', 'date': 'Date', 'region': 'Region'}
    )
    fig_trends.update_layout(height=500)
    fig_trends.update_traces(line=dict(width=3))
    st.plotly_chart(fig_trends, use_container_width=True)
    
    # Regional comparison matrix
    st.subheader("🔍 Regional Comparison Matrix")
    
    # Create comparison metrics
    comparison_metrics = df.groupby('region').agg({
        'revenue': ['sum', 'mean'],
        'quantity': 'sum',
        'discount_rate': 'mean',
        'customer_id': 'nunique'
    }).round(2)
    
    comparison_metrics.columns = ['Total Revenue', 'Avg Revenue', 'Total Quantity', 'Avg Discount Rate', 'Unique Customers']
    comparison_metrics = comparison_metrics.reset_index()
    
    # Normalize for heatmap (0-1 scale)
    heatmap_data = comparison_metrics.copy()
    numeric_cols = heatmap_data.select_dtypes(include=[np.number]).columns
    
    for col in numeric_cols:
        heatmap_data[col] = (heatmap_data[col] - heatmap_data[col].min()) / (heatmap_data[col].max() - heatmap_data[col].min())
    
    # Create heatmap
    fig_heatmap = px.imshow(
        heatmap_data[numeric_cols].T,
        labels=dict(x="Region", y="Metric", color="Normalized Score"),
        x=comparison_metrics['region'],
        y=numeric_cols,
        color_continuous_scale='RdYlBu_r',
        title='Regional Performance Heatmap (Normalized)'
    )
    fig_heatmap.update_layout(height=400)
    st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # Regional insights
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Regional Insights")
        
        # Calculate insights
        top_region = regional_stats.loc[regional_stats['total_revenue'].idxmax(), 'region']
        top_aov_region = regional_stats.loc[regional_stats['avg_order_value'].idxmax(), 'region']
        most_customers_region = regional_stats.loc[regional_stats['unique_customers'].idxmax(), 'region']
        
        st.info(f"""
        **Regional Leaders:**
        - Highest Revenue: {top_region}
        - Highest AOV: {top_aov_region}
        - Most Customers: {most_customers_region}
        """)
        
        # Growth opportunities
        lowest_revenue_region = regional_stats.loc[regional_stats['total_revenue'].idxmin(), 'region']
        lowest_customers_region = regional_stats.loc[regional_stats['unique_customers'].idxmin(), 'region']
        
        st.warning(f"""
        **Growth Opportunities:**
        - Expand in: {lowest_revenue_region}
        - Customer Acquisition: {lowest_customers_region}
        """)
    
    with col2:
        st.subheader("📊 Regional Statistics")
        
        # Key statistics
        total_regions = len(regional_stats)
        revenue_std = regional_stats['total_revenue'].std()
        revenue_mean = regional_stats['total_revenue'].mean()
        cv = (revenue_std / revenue_mean) * 100  # Coefficient of variation
        
        st.success(f"""
        **Market Dynamics:**
        - Active Regions: {total_regions}
        - Revenue Variability: {cv:.1f}%
        - Market Concentration: {'High' if cv > 50 else 'Moderate' if cv > 25 else 'Low'}
        """)
    
    # Product preferences by region
    st.subheader("🛍️ Regional Product Preferences")
    
    regional_products = df.groupby(['region', 'product_category'])['revenue'].sum().reset_index()
    
    # Get top category per region
    top_categories = regional_products.loc[regional_products.groupby('region')['revenue'].idxmax()]
    
    fig_preferences = px.sunburst(
        regional_products,
        path=['region', 'product_category'],
        values='revenue',
        title='Product Category Preferences by Region'
    )
    fig_preferences.update_layout(height=500)
    st.plotly_chart(fig_preferences, use_container_width=True)
    
    # Regional preferences table
    preferences_table = top_categories[['region', 'product_category', 'revenue']].copy()
    preferences_table['revenue'] = preferences_table['revenue'].apply(format_currency)
    preferences_table.columns = ['Region', 'Top Category', 'Category Revenue']
    
    st.dataframe(preferences_table, use_container_width=True, hide_index=True)