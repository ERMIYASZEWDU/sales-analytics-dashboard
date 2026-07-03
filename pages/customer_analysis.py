"""
Customer Analysis Page
Customer segmentation, RFM analysis, and behavioral insights
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from utils import calculate_customer_segments, format_currency, format_number

def show(df):
    """Display customer analysis dashboard"""
    
    st.header("👥 Customer Analysis & Segmentation")
    
    # Calculate RFM segments
    with st.spinner("Calculating customer segments..."):
        rfm_df = calculate_customer_segments(df)
    
    # Customer overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_customers = df['customer_id'].nunique()
    avg_customer_value = df.groupby('customer_id')['revenue'].sum().mean()
    avg_order_frequency = df.groupby('customer_id')['transaction_id'].count().mean()
    customer_retention = len(rfm_df[rfm_df['recency'] <= 90]) / len(rfm_df) * 100
    
    with col1:
        st.metric("Total Customers", format_number(total_customers))
    
    with col2:
        st.metric("Avg Customer Value", format_currency(avg_customer_value))
    
    with col3:
        st.metric("Avg Order Frequency", f"{avg_order_frequency:.1f}")
    
    with col4:
        st.metric("90-Day Retention", f"{customer_retention:.1f}%")
    
    st.markdown("---")
    
    # Customer segmentation overview
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🎯 Customer Segments (RFM Analysis)")
        
        # Segment distribution
        segment_counts = rfm_df['segment'].value_counts().reset_index()
        segment_counts.columns = ['segment', 'customer_count']
        
        # Calculate segment value
        segment_value = df.merge(
            rfm_df[['customer_id', 'segment']], 
            on='customer_id'
        ).groupby('segment')['revenue'].sum().reset_index()
        
        segment_analysis = segment_counts.merge(segment_value, on='segment')
        segment_analysis['avg_value_per_customer'] = segment_analysis['revenue'] / segment_analysis['customer_count']
        
        fig_segments = px.scatter(
            segment_analysis,
            x='customer_count',
            y='avg_value_per_customer',
            size='revenue',
            color='segment',
            title='Customer Segments: Count vs Value',
            labels={
                'customer_count': 'Number of Customers',
                'avg_value_per_customer': 'Average Value per Customer ($)'
            },
            hover_data=['revenue']
        )
        fig_segments.update_layout(height=500)
        st.plotly_chart(fig_segments, use_container_width=True)
    
    with col2:
        st.subheader("📊 Segment Distribution")
        
        fig_pie = px.pie(
            segment_counts,
            values='customer_count',
            names='segment',
            title='Customer Segment Distribution'
        )
        fig_pie.update_layout(height=500)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Detailed segment analysis
    st.subheader("📈 Segment Performance Analysis")
    
    # Format segment analysis for display
    display_segments = segment_analysis.copy()
    display_segments['revenue'] = display_segments['revenue'].apply(format_currency)
    display_segments['avg_value_per_customer'] = display_segments['avg_value_per_customer'].apply(format_currency)
    display_segments['customer_count'] = display_segments['customer_count'].apply(format_number)
    
    display_segments.columns = ['Segment', 'Customer Count', 'Total Revenue', 'Avg Value per Customer']
    
    st.dataframe(display_segments, use_container_width=True, hide_index=True)
    
    # RFM distribution analysis
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("📅 Recency Distribution")
        
        fig_recency = px.histogram(
            rfm_df,
            x='recency',
            nbins=20,
            title='Days Since Last Purchase',
            labels={'recency': 'Days Since Last Purchase', 'count': 'Number of Customers'}
        )
        fig_recency.update_layout(height=400)
        st.plotly_chart(fig_recency, use_container_width=True)
    
    with col2:
        st.subheader("🔄 Frequency Distribution")
        
        fig_frequency = px.histogram(
            rfm_df,
            x='frequency',
            nbins=20,
            title='Purchase Frequency',
            labels={'frequency': 'Number of Orders', 'count': 'Number of Customers'}
        )
        fig_frequency.update_layout(height=400)
        st.plotly_chart(fig_frequency, use_container_width=True)
    
    with col3:
        st.subheader("💰 Monetary Distribution")
        
        fig_monetary = px.histogram(
            rfm_df,
            x='monetary',
            nbins=20,
            title='Customer Lifetime Value',
            labels={'monetary': 'Total Spent ($)', 'count': 'Number of Customers'}
        )
        fig_monetary.update_layout(height=400)
        st.plotly_chart(fig_monetary, use_container_width=True)
    
    # Customer cohort analysis
    st.subheader("📊 Customer Cohort Analysis")
    
    # Prepare cohort data
    df_cohort = df.copy()
    df_cohort['order_period'] = df_cohort['date'].dt.to_period('M')
    df_cohort['cohort_group'] = df_cohort.groupby('customer_id')['date'].transform('min').dt.to_period('M')
    
    # Calculate period number
    df_cohort['period_number'] = (
        df_cohort['order_period'] - df_cohort['cohort_group']
    ).apply(attrgetter('n'))
    
    # Cohort table
    cohort_data = df_cohort.groupby(['cohort_group', 'period_number'])['customer_id'].nunique().reset_index()
    cohort_table = cohort_data.pivot(index='cohort_group', columns='period_number', values='customer_id')
    
    # Calculate cohort sizes
    cohort_sizes = df_cohort.groupby('cohort_group')['customer_id'].nunique()
    
    # Calculate retention rates
    retention_table = cohort_table.divide(cohort_sizes, axis=0)
    
    # Create heatmap (limit to first 12 periods for readability)
    retention_display = retention_table.iloc[:, :12] * 100  # Convert to percentage
    
    fig_cohort = px.imshow(
        retention_display.values,
        labels=dict(x="Period Number", y="Cohort Month", color="Retention Rate (%)"),
        x=[f"Period {i}" for i in retention_display.columns],
        y=[str(idx) for idx in retention_display.index],
        color_continuous_scale='RdYlBu_r',
        title='Customer Retention Cohort Analysis'
    )
    fig_cohort.update_layout(height=500)
    st.plotly_chart(fig_cohort, use_container_width=True)
    
    # Customer behavior analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🛒 Purchase Behavior")
        
        # Average days between purchases
        customer_behavior = df.groupby('customer_id').agg({
            'date': ['min', 'max', 'count'],
            'revenue': 'sum'
        })
        
        customer_behavior.columns = ['first_purchase', 'last_purchase', 'total_orders', 'total_revenue']
        customer_behavior = customer_behavior.reset_index()
        
        # Calculate days between first and last purchase
        customer_behavior['customer_lifespan'] = (
            customer_behavior['last_purchase'] - customer_behavior['first_purchase']
        ).dt.days
        
        # Average days between orders (for customers with more than 1 order)
        multi_order_customers = customer_behavior[customer_behavior['total_orders'] > 1]
        multi_order_customers['avg_days_between_orders'] = (
            multi_order_customers['customer_lifespan'] / (multi_order_customers['total_orders'] - 1)
        )
        
        fig_behavior = px.histogram(
            multi_order_customers,
            x='avg_days_between_orders',
            nbins=20,
            title='Average Days Between Orders',
            labels={'avg_days_between_orders': 'Days Between Orders', 'count': 'Number of Customers'}
        )
        fig_behavior.update_layout(height=400)
        st.plotly_chart(fig_behavior, use_container_width=True)
    
    with col2:
        st.subheader("💳 Spending Patterns")
        
        # Customer value distribution
        fig_value = px.box(
            rfm_df,
            y='monetary',
            title='Customer Value Distribution',
            labels={'monetary': 'Total Customer Value ($)'}
        )
        fig_value.update_layout(height=400)
        st.plotly_chart(fig_value, use_container_width=True)
    
    # Customer preferences analysis
    st.subheader("🎯 Customer Preferences by Segment")
    
    # Merge customer segments with transaction data
    df_with_segments = df.merge(rfm_df[['customer_id', 'segment']], on='customer_id')
    
    # Category preferences by segment
    segment_categories = df_with_segments.groupby(['segment', 'product_category'])['revenue'].sum().reset_index()
    
    # Get top category for each segment
    top_categories_by_segment = segment_categories.loc[
        segment_categories.groupby('segment')['revenue'].idxmax()
    ][['segment', 'product_category', 'revenue']]
    
    fig_preferences = px.sunburst(
        segment_categories,
        path=['segment', 'product_category'],
        values='revenue',
        title='Product Preferences by Customer Segment'
    )
    fig_preferences.update_layout(height=500)
    st.plotly_chart(fig_preferences, use_container_width=True)
    
    # Channel preferences by segment
    segment_channels = df_with_segments.groupby(['segment', 'sales_channel'])['revenue'].sum().reset_index()
    
    fig_channels = px.bar(
        segment_channels,
        x='segment',
        y='revenue',
        color='sales_channel',
        title='Sales Channel Preferences by Segment',
        labels={'revenue': 'Revenue ($)', 'segment': 'Customer Segment'}
    )
    fig_channels.update_layout(height=400)
    st.plotly_chart(fig_channels, use_container_width=True)
    
    # Customer insights and recommendations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💡 Customer Insights")
        
        # Key insights
        top_segment = segment_counts.iloc[0]['segment']
        top_segment_count = segment_counts.iloc[0]['customer_count']
        highest_value_segment = segment_analysis.loc[segment_analysis['avg_value_per_customer'].idxmax(), 'segment']
        
        champions_count = len(rfm_df[rfm_df['segment'] == 'Champions'])
        at_risk_count = len(rfm_df[rfm_df['segment'] == 'At Risk'])
        
        st.info(f"""
        **Key Insights:**
        - Largest Segment: {top_segment} ({top_segment_count:,} customers)
        - Highest Value Segment: {highest_value_segment}
        - Champions: {champions_count:,} customers
        - At Risk: {at_risk_count:,} customers
        """)
    
    with col2:
        st.subheader("🚀 Recommendations")
        
        # Calculate churn risk
        high_recency_customers = len(rfm_df[rfm_df['recency'] > 180])
        churn_risk_pct = (high_recency_customers / len(rfm_df)) * 100
        
        # One-time buyers
        one_time_buyers = len(rfm_df[rfm_df['frequency'] == 1])
        one_time_pct = (one_time_buyers / len(rfm_df)) * 100
        
        st.warning(f"""
        **Action Items:**
        - Re-engage {high_recency_customers:,} inactive customers ({churn_risk_pct:.1f}%)
        - Convert {one_time_buyers:,} one-time buyers ({one_time_pct:.1f}%)
        - Focus on {at_risk_count:,} at-risk customers
        """)

from operator import attrgetter