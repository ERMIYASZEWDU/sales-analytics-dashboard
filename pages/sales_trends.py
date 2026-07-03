"""
Sales Trends Analysis Page
Detailed time-series analysis and trend visualization
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from utils import format_currency, format_number

def show(df):
    """Display sales trends analysis"""
    
    st.header("📊 Sales Trends Analysis")
    
    # Time granularity selector
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        time_granularity = st.selectbox(
            "Time Granularity",
            ["Daily", "Weekly", "Monthly", "Quarterly"]
        )
    
    with col2:
        metric = st.selectbox(
            "Metric",
            ["Revenue", "Orders", "Customers", "Average Order Value"]
        )
    
    # Prepare data based on granularity
    if time_granularity == "Daily":
        time_df = df.groupby(df['date'].dt.date).agg({
            'revenue': 'sum',
            'transaction_id': 'count',
            'customer_id': 'nunique'
        }).reset_index()
        time_df['avg_order_value'] = time_df['revenue'] / time_df['transaction_id']
        
    elif time_granularity == "Weekly":
        time_df = df.groupby(df['date'].dt.to_period('W')).agg({
            'revenue': 'sum',
            'transaction_id': 'count',
            'customer_id': 'nunique'
        }).reset_index()
        time_df['date'] = time_df['date'].dt.to_timestamp()
        time_df['avg_order_value'] = time_df['revenue'] / time_df['transaction_id']
        
    elif time_granularity == "Monthly":
        time_df = df.groupby(df['date'].dt.to_period('M')).agg({
            'revenue': 'sum',
            'transaction_id': 'count',
            'customer_id': 'nunique'
        }).reset_index()
        time_df['date'] = time_df['date'].dt.to_timestamp()
        time_df['avg_order_value'] = time_df['revenue'] / time_df['transaction_id']
        
    else:  # Quarterly
        time_df = df.groupby([df['date'].dt.year, df['date'].dt.quarter]).agg({
            'revenue': 'sum',
            'transaction_id': 'count',
            'customer_id': 'nunique'
        }).reset_index()
        time_df['date'] = pd.to_datetime(time_df[['date', 'quarter']].assign(month=time_df['quarter']*3, day=1))
        time_df['avg_order_value'] = time_df['revenue'] / time_df['transaction_id']
    
    # Select y-axis based on metric choice
    metric_mapping = {
        "Revenue": 'revenue',
        "Orders": 'transaction_id',
        "Customers": 'customer_id',
        "Average Order Value": 'avg_order_value'
    }
    
    y_column = metric_mapping[metric]
    
    # Main trend chart
    st.subheader(f"{metric} Trend - {time_granularity}")
    
    fig_trend = px.line(
        time_df,
        x='date',
        y=y_column,
        title=f'{metric} Over Time ({time_granularity})',
        labels={y_column: metric, 'date': 'Date'}
    )
    
    # Add moving average for daily/weekly data
    if time_granularity in ["Daily", "Weekly"]:
        window = 7 if time_granularity == "Daily" else 4
        time_df[f'{y_column}_ma'] = time_df[y_column].rolling(window=window).mean()
        
        fig_trend.add_trace(
            go.Scatter(
                x=time_df['date'],
                y=time_df[f'{y_column}_ma'],
                mode='lines',
                name=f'{window}-Period Moving Average',
                line=dict(dash='dash', color='red')
            )
        )
    
    fig_trend.update_layout(height=500)
    fig_trend.update_traces(line=dict(width=3))
    st.plotly_chart(fig_trend, use_container_width=True)
    
    # Seasonal analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📅 Seasonal Patterns")
        
        # Monthly seasonality
        monthly_pattern = df.groupby(df['date'].dt.month)[y_column.replace('transaction_id', 'revenue')].sum().reset_index()
        monthly_pattern['month_name'] = pd.to_datetime(monthly_pattern['date'], format='%m').dt.strftime('%B')
        
        fig_seasonal = px.bar(
            monthly_pattern,
            x='month_name',
            y=y_column.replace('transaction_id', 'revenue'),
            title='Monthly Seasonality Pattern',
            labels={'month_name': 'Month', y_column.replace('transaction_id', 'revenue'): 'Revenue'}
        )
        fig_seasonal.update_layout(height=400)
        st.plotly_chart(fig_seasonal, use_container_width=True)
    
    with col2:
        st.subheader("📊 Day-of-Week Analysis")
        
        # Day of week pattern
        dow_pattern = df.groupby(df['day_of_week'])[y_column.replace('transaction_id', 'revenue')].sum().reset_index()
        
        # Reorder days
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        dow_pattern['day_of_week'] = pd.Categorical(dow_pattern['day_of_week'], categories=day_order, ordered=True)
        dow_pattern = dow_pattern.sort_values('day_of_week')
        
        fig_dow = px.bar(
            dow_pattern,
            x='day_of_week',
            y=y_column.replace('transaction_id', 'revenue'),
            title='Day of Week Performance',
            labels={'day_of_week': 'Day of Week', y_column.replace('transaction_id', 'revenue'): 'Revenue'}
        )
        fig_dow.update_layout(height=400)
        st.plotly_chart(fig_dow, use_container_width=True)
    
    # Growth analysis
    st.subheader("📈 Growth Analysis")
    
    # Calculate period-over-period growth
    if len(time_df) > 1:
        time_df_sorted = time_df.sort_values('date')
        time_df_sorted['pct_change'] = time_df_sorted[y_column].pct_change() * 100
        
        # Growth chart
        fig_growth = px.bar(
            time_df_sorted.dropna(),
            x='date',
            y='pct_change',
            title=f'{metric} Growth Rate (%)',
            labels={'pct_change': 'Growth Rate (%)', 'date': 'Period'},
            color='pct_change',
            color_continuous_scale=['red', 'white', 'green']
        )
        fig_growth.update_layout(height=400)
        st.plotly_chart(fig_growth, use_container_width=True)
        
        # Growth statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_growth = time_df_sorted['pct_change'].mean()
            st.metric("Average Growth", f"{avg_growth:.1f}%")
        
        with col2:
            max_growth = time_df_sorted['pct_change'].max()
            st.metric("Max Growth", f"{max_growth:.1f}%")
        
        with col3:
            min_growth = time_df_sorted['pct_change'].min()
            st.metric("Min Growth", f"{min_growth:.1f}%")
        
        with col4:
            volatility = time_df_sorted['pct_change'].std()
            st.metric("Volatility (σ)", f"{volatility:.1f}%")
    
    # Trend decomposition (simple)
    st.subheader("🔍 Trend Components")
    
    if len(time_df) >= 12:  # Need sufficient data points
        # Simple trend and seasonality extraction
        from scipy import signal
        
        # Detrend
        values = time_df[y_column].values
        trend = signal.detrend(values, type='linear') + np.mean(values)
        seasonal = values - trend
        
        # Create subplot
        fig_decomp = make_subplots(
            rows=3, cols=1,
            subplot_titles=['Original', 'Trend', 'Seasonal'],
            vertical_spacing=0.05
        )
        
        # Original
        fig_decomp.add_trace(
            go.Scatter(x=time_df['date'], y=values, name='Original', line=dict(color='blue')),
            row=1, col=1
        )
        
        # Trend
        fig_decomp.add_trace(
            go.Scatter(x=time_df['date'], y=trend, name='Trend', line=dict(color='red')),
            row=2, col=1
        )
        
        # Seasonal
        fig_decomp.add_trace(
            go.Scatter(x=time_df['date'], y=seasonal, name='Seasonal', line=dict(color='green')),
            row=3, col=1
        )
        
        fig_decomp.update_layout(height=600, showlegend=False)
        st.plotly_chart(fig_decomp, use_container_width=True)
    
    # Data table
    st.subheader("📋 Detailed Data")
    
    # Format the display dataframe
    display_df = time_df.copy()
    if 'revenue' in display_df.columns:
        display_df['revenue'] = display_df['revenue'].apply(format_currency)
    if 'avg_order_value' in display_df.columns:
        display_df['avg_order_value'] = display_df['avg_order_value'].apply(format_currency)
    
    # Rename columns for better display
    column_renames = {
        'date': 'Date',
        'revenue': 'Revenue',
        'transaction_id': 'Orders',
        'customer_id': 'Customers',
        'avg_order_value': 'Avg Order Value'
    }
    display_df = display_df.rename(columns=column_renames)
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)