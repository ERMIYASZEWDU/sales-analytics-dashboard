# 📊 Sales Analytics Dashboard

A comprehensive, interactive sales data analytics dashboard built with Streamlit and Plotly. This dashboard provides deep insights into sales performance, customer behavior, product analytics, and regional trends through beautiful visualizations and advanced analytics.

![Dashboard Preview](https://img.shields.io/badge/Built%20with-Streamlit-red?style=for-the-badge&logo=streamlit)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![Plotly](https://img.shields.io/badge/Plotly-Interactive-brightgreen?style=for-the-badge&logo=plotly)

## 🚀 Features

### 📈 KPI Overview
- **Real-time Metrics**: Total revenue, orders, customers, and average order value
- **Growth Analysis**: Period-over-period growth rates with visual indicators
- **Revenue Trends**: Monthly and quarterly revenue visualization
- **Channel & Category Performance**: Interactive charts showing sales distribution
- **Business Insights**: Automated insights and key performance highlights

### 📊 Sales Trends Analysis
- **Time-series Analysis**: Daily, weekly, monthly, and quarterly trend analysis
- **Seasonal Patterns**: Monthly seasonality and day-of-week performance patterns
- **Growth Metrics**: Period-over-period growth rates and volatility analysis
- **Trend Decomposition**: Trend and seasonal component analysis
- **Moving Averages**: Smoothed trend lines for better pattern recognition

### 🌍 Regional Sales Analysis
- **Geographic Performance**: Regional revenue and market share analysis
- **City-level Insights**: Top performing cities and customer distribution
- **Regional Trends**: Time-series analysis by geographic regions
- **Comparison Matrix**: Normalized performance heatmap across regions
- **Product Preferences**: Regional product category preferences analysis

### 🛍️ Product Performance
- **Category Analysis**: Performance metrics across product categories
- **Top Products**: Best-performing products by various metrics
- **Price vs Volume**: Scatter plot analysis of pricing effectiveness
- **Discount Impact**: Analysis of discount strategies and effectiveness
- **Product Lifecycle**: Automated lifecycle stage classification
- **Revenue Distribution**: Statistical analysis of product performance

### 👥 Customer Analytics
- **RFM Segmentation**: Advanced customer segmentation using Recency, Frequency, Monetary analysis
- **Customer Segments**: Automated classification into actionable segments (Champions, At Risk, etc.)
- **Cohort Analysis**: Customer retention analysis with interactive heatmaps
- **Purchase Behavior**: Analysis of buying patterns and customer lifetime value
- **Preference Analysis**: Product and channel preferences by customer segment

### 🎯 Advanced Filtering System
- **Quick Date Presets**: Last 30/90 days, 6 months, year, etc.
- **Custom Date Ranges**: Flexible date range selection
- **Multi-dimensional Filters**: Region, category, channel, customer segment filtering
- **Revenue Range**: Slider-based revenue filtering
- **Real-time Updates**: Instant dashboard updates with filter changes
- **Filter Summary**: Clear overview of applied filters and data scope

## 🛠️ Technical Stack

- **Framework**: Streamlit 1.29.0
- **Data Processing**: Pandas 2.1.4, NumPy 1.24.3
- **Visualization**: Plotly 5.17.0, Seaborn 0.13.0, Matplotlib 3.8.2
- **Analytics**: SciPy 1.11.4 for statistical analysis
- **Data Generation**: Faker 20.1.0 for realistic synthetic data

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## ⚡ Quick Start

### 1. Clone or Download
```bash
# If using git
git clone <repository-url>
cd sales-analytics-dashboard

# Or download and extract the files to a folder
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Dashboard
```bash
streamlit run app.py
```

### 4. Access the Dashboard
Open your browser and navigate to: `http://localhost:8501`

## 📊 Data Overview

The dashboard uses a comprehensive synthetic dataset with:

- **10,000+ transactions** across 2 years
- **3,000 unique customers** with realistic behavior patterns
- **5 product categories** with 30+ individual products
- **4 global regions** with 24 cities
- **5 sales channels** including online, retail, and mobile
- **5 customer segments** from budget to premium

### Data Features:
- Seasonal sales patterns (holiday spikes, summer trends)
- Realistic pricing with category-appropriate ranges
- Customer lifecycle simulation with acquisition dates
- Geographic distribution with regional preferences
- Discount strategies and promotional effects
- Multiple sales channels with different conversion rates

## 🎨 Dashboard Structure

```
sales-analytics-dashboard/
│
├── app.py                 # Main dashboard application
├── data_generator.py      # Synthetic data generation
├── utils.py              # Data processing utilities
├── requirements.txt      # Python dependencies
├── README.md            # This documentation
│
└── pages/               # Individual dashboard pages
    ├── __init__.py
    ├── kpi_overview.py     # KPI and overview metrics
    ├── sales_trends.py     # Time-series analysis
    ├── regional_analysis.py # Geographic insights
    ├── product_analysis.py  # Product performance
    └── customer_analysis.py # Customer segmentation
```

## 🔧 Customization

### Adding New Metrics
1. Modify `utils.py` to add new calculation functions
2. Update relevant page files in the `pages/` directory
3. Add new visualizations using Plotly

### Modifying Data
1. Edit `data_generator.py` to change data generation parameters
2. Adjust categories, regions, or date ranges as needed
3. Regenerate data by running: `python data_generator.py`

### Styling Changes
1. Modify the CSS in `app.py` for visual customizations
2. Adjust Plotly chart themes in individual page files
3. Update color schemes and layout preferences

## 📈 Key Metrics Explained

### RFM Analysis
- **Recency**: Days since last purchase
- **Frequency**: Number of purchases made
- **Monetary**: Total amount spent

### Customer Segments
- **Champions**: Best customers with recent, frequent, high-value purchases
- **Loyal Customers**: Regular buyers with good purchase history
- **Potential Loyalists**: Recent customers with good spending potential
- **At Risk**: Previous good customers who haven't purchased recently
- **New Customers**: Recent first-time buyers

### Growth Metrics
- **Period-over-Period Growth**: Percentage change from previous period
- **Revenue Velocity**: Revenue generated per day a product is in market
- **Customer Lifetime Value**: Total revenue generated by a customer
- **Average Order Value**: Mean transaction value

## 🚀 Advanced Features

### Interactive Filtering
- Real-time data filtering across all visualizations
- Multi-select options for regions, categories, and channels
- Date range presets for quick analysis
- Revenue range filtering with sliders

### Automated Insights
- Top performer identification across all dimensions
- Growth opportunity detection
- Risk factor highlighting (churn risk, declining products)
- Market concentration analysis

### Export Capabilities
- Chart download options (PNG, PDF, SVG)
- Data table export functionality
- Filtered dataset download

## 🐛 Troubleshooting

### Common Issues

1. **Module Not Found Error**
   ```bash
   pip install -r requirements.txt
   ```

2. **Port Already in Use**
   ```bash
   streamlit run app.py --server.port 8502
   ```

3. **Memory Issues with Large Datasets**
   - Reduce the number of records in `data_generator.py`
   - Use more selective filtering
   - Consider data sampling for very large datasets

4. **Slow Performance**
   - The dashboard uses caching for improved performance
   - Clear cache if data is updated: Press 'C' in the browser
   - Reduce the date range for faster loading

## 📝 License

This project is provided as-is for educational and commercial use. Feel free to modify and adapt according to your needs.

## 🤝 Contributing

Contributions are welcome! Please feel free to:
- Report bugs and issues
- Suggest new features
- Submit pull requests
- Improve documentation

## 📞 Support

For questions and support:
- Check the troubleshooting section above
- Review the code comments for implementation details
- Create an issue for bugs or feature requests

---

**Built with ❤️ using Streamlit, Plotly, and Python**

*This dashboard demonstrates advanced analytics capabilities and can be adapted for real-world sales data with minimal modifications.*