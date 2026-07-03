"""
Product Performance Analysis Page
Detailed product and category performance tracking
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from utils import get_top_products, format_currency, format_number

def show(df):
    """Display product performance analysis"""
    
    st.header("🛍️ Product Performance Analysis")
    
    # Product filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_categories = st.multiselect(
            "Select Categories",
            options=df['product_category'].unique(),
            default=df['product_category'].unique()
        )
    
    with col2:
        metric_choice = st.selectbox(
            "Primary Metric",
            ["Revenue", "Quantity Sold", "Orders", "Avg Price"]
        )
    
    with col3:
        top_n = st.slider(
            "Top N Products",
            min_value=5,
            max_value=20,
            value=10
        )
    
    # Filter data
    filtered_df = df[df['product_category'].isin(selected_categories)]
    
    # Category overview
    st.subheader("📊 Category Performance Overview")
    
    category_metrics = filtered_df.groupby('product_category').agg({
        'revenue': 'sum',
        'quantity': 'sum',
        'transaction_id': 'count',
        'unit_price': 'mean',
        'discount_rate': 'mean'
    }).round(2)
    
    category_metrics.columns = ['Total Revenue', 'Total Quantity', 'Total Orders', 'Avg Unit Price', 'Avg Discount Rate']
    category_metrics = category_metrics.reset_index()
    
    # Category performance chart
    metric_mapping = {
        "Revenue": 'Total Revenue',
        "Quantity Sold": 'Total Quantity', 
        "Orders": 'Total Orders',
        "Avg Price": 'Avg Unit Price'
    }
    
    chart_metric = metric_mapping[metric_choice]
    
    fig_category = px.bar(
        category_metrics,
        x='product_category',
        y=chart_metric,
        title=f'{metric_choice} by Product Category',
        labels={'product_category': 'Category', chart_metric: metric_choice},
        color=chart_metric,
        color_continuous_scale='Viridis'
    )
    fig_category.update_layout(height=400)
    st.plotly_chart(fig_category, use_container_width=True)
    
    # Top products analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"🏆 Top {top_n} Products by Revenue")
        
        top_products = filtered_df.groupby('product_name').agg({
            'revenue': 'sum',
            'quantity': 'sum',
            'transaction_id': 'count',
            'unit_price': 'mean'
        }).round(2)
        
        top_products = top_products.sort_values('revenue', ascending=False).head(top_n)
        top_products = top_products.reset_index()
        
        fig_top_products = px.bar(
            top_products,
            x='revenue',
            y='product_name',
            orientation='h',
            title=f'Top {top_n} Products by Revenue',
            labels={'revenue': 'Revenue ($)', 'product_name': 'Product'}
        )
        fig_top_products.update_layout(height=500)
        st.plotly_chart(fig_top_products, use_container_width=True)
    
    with col2:
        st.subheader("📈 Product Revenue Distribution")
        
        # Revenue distribution by product
        product_revenue = filtered_df.groupby('product_name')['revenue'].sum().reset_index()
        
        fig_dist = px.histogram(
            product_revenue,
            x='revenue',
            nbins=20,
            title='Product Revenue Distribution',
            labels={'revenue': 'Revenue ($)', 'count': 'Number of Products'}
        )
        fig_dist.update_layout(height=500)
        st.plotly_chart(fig_dist, use_container_width=True)
    
    # Product performance metrics table
    st.subheader("📋 Product Performance Metrics")
    
    # Enhanced product metrics
    product_performance = filtered_df.groupby(['product_category', 'product_name']).agg({
        'revenue': 'sum',
        'quantity': 'sum',
        'transaction_id': 'count',
        'unit_price': 'mean',
        'discount_rate': 'mean',
        'customer_id': 'nunique'
    }).round(2)
    
    # Add calculated metrics
    product_performance['revenue_per_customer'] = (
        product_performance['revenue'] / product_performance['customer_id']
    ).round(2)
    
    product_performance['avg_quantity_per_order'] = (
        product_performance['quantity'] / product_performance['transaction_id']
    ).round(2)
    
    # Reset index for display
    product_performance = product_performance.reset_index()
    
    # Format currency columns
    display_performance = product_performance.copy()
    display_performance['revenue'] = display_performance['revenue'].apply(format_currency)
    display_performance['unit_price'] = display_performance['unit_price'].apply(format_currency)
    display_performance['revenue_per_customer'] = display_performance['revenue_per_customer'].apply(format_currency)
    
    # Format percentage
    display_performance['discount_rate'] = (display_performance['discount_rate'] * 100).round(1).astype(str) + '%'
    
    # Rename columns
    display_performance.columns = [
        'Category', 'Product', 'Revenue', 'Quantity Sold', 'Orders', 
        'Avg Unit Price', 'Avg Discount Rate', 'Unique Customers',
        'Revenue per Customer', 'Avg Qty per Order'
    ]
    
    # Sort by revenue
    display_performance = display_performance.sort_values('Revenue', key=lambda x: x.str.replace('$', '').str.replace(',', '').astype(float), ascending=False)
    
    st.dataframe(display_performance, use_container_width=True, hide_index=True)
    
    # Product trends over time
    st.subheader("📅 Product Category Trends")
    
    # Monthly trends by category
    monthly_category = filtered_df.groupby([
        filtered_df['date'].dt.to_period('M'), 'product_category'
    ])['revenue'].sum().reset_index()
    monthly_category['date'] = monthly_category['date'].dt.to_timestamp()
    
    fig_trends = px.line(
        monthly_category,
        x='date',
        y='revenue',
        color='product_category',
        title='Monthly Revenue Trends by Category',
        labels={'revenue': 'Revenue ($)', 'date': 'Date', 'product_category': 'Category'}
    )
    fig_trends.update_layout(height=500)
    fig_trends.update_traces(line=dict(width=3))
    st.plotly_chart(fig_trends, use_container_width=True)
    
    # Price vs Performance Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💰 Price vs Volume Analysis")
        
        # Scatter plot of price vs quantity sold
        price_volume = filtered_df.groupby('product_name').agg({
            'unit_price': 'mean',
            'quantity': 'sum',
            'revenue': 'sum',
            'product_category': 'first'
        }).reset_index()
        
        fig_scatter = px.scatter(
            price_volume,
            x='unit_price',
            y='quantity',
            size='revenue',
            color='product_category',
            title='Price vs Quantity Sold (Size = Revenue)',
            labels={'unit_price': 'Average Unit Price ($)', 'quantity': 'Total Quantity Sold'},
            hover_data=['product_name']
        )
        fig_scatter.update_layout(height=500)
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Discount Impact Analysis")
        
        # Analyze discount effectiveness
        discount_analysis = filtered_df.copy()
        discount_analysis['discount_bucket'] = pd.cut(
            discount_analysis['discount_rate'],
            bins=[0, 0.05, 0.15, 0.25, 1.0],
            labels=['0-5%', '5-15%', '15-25%', '25%+'],
            include_lowest=True
        )
        
        discount_impact = discount_analysis.groupby('discount_bucket').agg({
            'revenue': 'sum',
            'quantity': 'sum',
            'transaction_id': 'count'
        }).reset_index()
        
        fig_discount = px.bar(
            discount_impact,
            x='discount_bucket',
            y='revenue',
            title='Revenue by Discount Range',
            labels={'discount_bucket': 'Discount Range', 'revenue': 'Revenue ($)'}
        )
        fig_discount.update_layout(height=500)
        st.plotly_chart(fig_discount, use_container_width=True)
    
    # Product lifecycle analysis
    st.subheader("🔄 Product Lifecycle Analysis")
    
    # Calculate product metrics for lifecycle staging
    lifecycle_metrics = filtered_df.groupby('product_name').agg({
        'date': ['min', 'max'],
        'revenue': 'sum',
        'quantity': 'sum',
        'transaction_id': 'count'
    }).round(2)
    
    lifecycle_metrics.columns = ['first_sale', 'last_sale', 'total_revenue', 'total_quantity', 'total_orders']
    lifecycle_metrics = lifecycle_metrics.reset_index()
    
    # Calculate days in market
    lifecycle_metrics['days_in_market'] = (
        lifecycle_metrics['last_sale'] - lifecycle_metrics['first_sale']
    ).dt.days + 1
    
    # Calculate velocity (revenue per day)
    lifecycle_metrics['revenue_velocity'] = lifecycle_metrics['total_revenue'] / lifecycle_metrics['days_in_market']
    
    # Classify products into lifecycle stages
    def classify_lifecycle(row):
        days = row['days_in_market']
        velocity = row['revenue_velocity']
        
        if days < 90:
            return 'New Product'
        elif velocity > lifecycle_metrics['revenue_velocity'].quantile(0.75):
            return 'Growth'
        elif velocity > lifecycle_metrics['revenue_velocity'].quantile(0.25):
            return 'Mature'
        else:
            return 'Decline'
    
    lifecycle_metrics['lifecycle_stage'] = lifecycle_metrics.apply(classify_lifecycle, axis=1)
    
    # Lifecycle distribution
    lifecycle_dist = lifecycle_metrics['lifecycle_stage'].value_counts().reset_index()
    lifecycle_dist.columns = ['lifecycle_stage', 'product_count']
    
    fig_lifecycle = px.pie(
        lifecycle_dist,
        values='product_count',
        names='lifecycle_stage',
        title='Product Lifecycle Distribution'
    )
    fig_lifecycle.update_layout(height=400)
    st.plotly_chart(fig_lifecycle, use_container_width=True)
    
    # Product insights
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💡 Product Insights")
        
        # Top performing product
        top_product = top_products.iloc[0]['product_name']
        top_revenue = top_products.iloc[0]['revenue']
        
        # Best category
        best_category = category_metrics.loc[category_metrics['Total Revenue'].idxmax(), 'product_category']
        
        # Most discounted category
        most_discounted = category_metrics.loc[category_metrics['Avg Discount Rate'].idxmax(), 'product_category']
        
        st.info(f"""
        **Top Performers:**
        - Best Product: {top_product}
        - Revenue: {format_currency(top_revenue)}
        - Best Category: {best_category}
        - Most Discounted: {most_discounted}
        """)
    
    with col2:
        st.subheader("🚀 Growth Opportunities")
        
        # Products with high discount rates but low revenue
        high_discount_low_revenue = product_performance[
            (product_performance['discount_rate'] > 0.15) & 
            (product_performance['revenue'] < product_performance['revenue'].median())
        ]
        
        if len(high_discount_low_revenue) > 0:
            opportunity_product = high_discount_low_revenue.iloc[0]['product_name']
            st.warning(f"""
            **Action Items:**
            - Review pricing for: {opportunity_product}
            - High discounts, low revenue
            - Consider product positioning
            """)
        else:
            st.success("""
            **Portfolio Health:**
            - Discount strategy aligned
            - No major pricing concerns
            - Good revenue distribution
            """)