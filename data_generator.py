"""
Sales Data Generator
Creates realistic synthetic sales data for the dashboard
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)

def generate_sales_data(num_records=10000):
    """Generate comprehensive synthetic sales data"""
    
    # Date range: Last 2 years
    start_date = datetime.now() - timedelta(days=730)
    end_date = datetime.now()
    
    # Product categories and items
    categories = {
        'Electronics': ['Smartphone', 'Laptop', 'Tablet', 'Headphones', 'Smart Watch', 'Camera'],
        'Clothing': ['T-Shirt', 'Jeans', 'Dress', 'Jacket', 'Sneakers', 'Sweater'],
        'Home & Garden': ['Furniture', 'Kitchen Appliance', 'Bedding', 'Decorative Item', 'Tools', 'Plants'],
        'Sports': ['Fitness Equipment', 'Sports Shoes', 'Outdoor Gear', 'Team Jersey', 'Exercise Bike', 'Yoga Mat'],
        'Books': ['Fiction', 'Non-Fiction', 'Educational', 'Biography', 'Self-Help', 'Children\'s Book']
    }
    
    # Regions and cities
    regions = {
        'North America': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Toronto', 'Vancouver'],
        'Europe': ['London', 'Paris', 'Berlin', 'Madrid', 'Rome', 'Amsterdam'],
        'Asia Pacific': ['Tokyo', 'Singapore', 'Sydney', 'Mumbai', 'Seoul', 'Bangkok'],
        'Latin America': ['São Paulo', 'Mexico City', 'Buenos Aires', 'Bogotá', 'Lima', 'Santiago']
    }
    
    # Sales channels
    channels = ['Online', 'Retail Store', 'Mobile App', 'Phone Order', 'Partner Store']
    
    # Customer segments
    segments = ['Premium', 'Standard', 'Budget', 'Corporate', 'Student']
    
    # Generate simple names
    first_names = ['John', 'Jane', 'Mike', 'Sarah', 'David', 'Lisa', 'Chris', 'Emma', 'Alex', 'Kate',
                  'Tom', 'Anna', 'Mark', 'Lucy', 'Paul', 'Nina', 'Steve', 'Amy', 'Jack', 'Eva']
    last_names = ['Smith', 'Johnson', 'Brown', 'Davis', 'Wilson', 'Moore', 'Taylor', 'Anderson', 
                 'Thomas', 'Jackson', 'White', 'Harris', 'Martin', 'Garcia', 'Rodriguez', 'Lewis',
                 'Lee', 'Walker', 'Hall', 'Allen']
    
    # Generate data
    records = []
    customer_ids = [f"CUST_{i:06d}" for i in range(1, 3001)]  # 3000 unique customers
    
    for i in range(num_records):
        # Random date with seasonal trends
        random_days = np.random.randint(0, 730)
        date = start_date + timedelta(days=random_days)
        
        # Seasonal multiplier (higher sales in Q4)
        seasonal_multiplier = 1.0
        if date.month in [11, 12]:  # Holiday season
            seasonal_multiplier = 1.4
        elif date.month in [6, 7, 8]:  # Summer
            seasonal_multiplier = 1.2
        
        # Day of week effect (weekends slightly lower for B2B)
        day_multiplier = 0.9 if date.weekday() >= 5 else 1.0
        
        # Select random category and product
        category = np.random.choice(list(categories.keys()))
        product = np.random.choice(categories[category])
        
        # Select region and city
        region = np.random.choice(list(regions.keys()))
        city = np.random.choice(regions[region])
        
        # Product pricing based on category
        base_prices = {
            'Electronics': (200, 2000),
            'Clothing': (20, 300),
            'Home & Garden': (50, 1000),
            'Sports': (30, 500),
            'Books': (10, 80)
        }
        
        min_price, max_price = base_prices[category]
        unit_price = np.random.uniform(min_price, max_price)
        
        # Quantity (most orders are 1-3 items, some bulk orders)
        if np.random.random() < 0.1:  # 10% bulk orders
            quantity = np.random.randint(10, 50)
        else:
            quantity = np.random.randint(1, 4)
        
        # Calculate revenue
        revenue = unit_price * quantity * seasonal_multiplier * day_multiplier
        
        # Add some noise to make it more realistic
        revenue *= np.random.uniform(0.95, 1.05)
        
        # Customer info
        customer_id = np.random.choice(customer_ids)
        customer_segment = np.random.choice(segments)
        
        # Sales channel (online more popular)
        channel_weights = [0.4, 0.25, 0.2, 0.1, 0.05]
        channel = np.random.choice(channels, p=channel_weights)
        
        # Salesperson (simple name generation)
        salesperson = f"{np.random.choice(first_names)} {np.random.choice(last_names)}"
        
        # Discount (occasionally applied)
        discount_rate = 0
        if np.random.random() < 0.15:  # 15% chance of discount
            discount_rate = np.random.uniform(0.05, 0.25)
        
        discount_amount = revenue * discount_rate
        final_revenue = revenue - discount_amount
        
        # Customer acquisition date (for cohort analysis)
        customer_since = date - timedelta(days=np.random.randint(0, 730))
        
        # Build record
        record = {
            'transaction_id': f"TXN_{i+1:08d}",
            'date': date,
            'customer_id': customer_id,
            'customer_segment': customer_segment,
            'customer_since': customer_since,
            'product_category': category,
            'product_name': product,
            'quantity': quantity,
            'unit_price': round(unit_price, 2),
            'discount_rate': round(discount_rate, 4),
            'discount_amount': round(discount_amount, 2),
            'revenue': round(final_revenue, 2),
            'region': region,
            'city': city,
            'sales_channel': channel,
            'salesperson': salesperson
        }
        
        records.append(record)
    
    # Create DataFrame
    df = pd.DataFrame(records)
    
    # Add derived columns
    df['month'] = df['date'].dt.month
    df['quarter'] = df['date'].dt.quarter
    df['year'] = df['date'].dt.year
    df['day_of_week'] = df['date'].dt.day_name()
    df['is_weekend'] = df['date'].dt.weekday >= 5
    
    # Customer tenure (days since first purchase)
    df['customer_tenure_days'] = (df['date'] - df['customer_since']).dt.days
    
    # Sort by date
    df = df.sort_values('date').reset_index(drop=True)
    
    return df

def save_sample_data():
    """Generate and save sample data to CSV"""
    print("Generating sales data...")
    df = generate_sales_data(10000)
    
    # Save to CSV
    df.to_csv('sales_data.csv', index=False)
    print(f"Generated {len(df)} records and saved to sales_data.csv")
    
    # Print summary stats
    print("\nDataset Summary:")
    print(f"Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"Total revenue: ${df['revenue'].sum():,.2f}")
    print(f"Average order value: ${df['revenue'].mean():.2f}")
    print(f"Unique customers: {df['customer_id'].nunique()}")
    print(f"Product categories: {df['product_category'].nunique()}")
    print(f"Regions: {df['region'].nunique()}")
    
    return df

if __name__ == "__main__":
    save_sample_data()