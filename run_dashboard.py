#!/usr/bin/env python3
"""
Simple script to run the Sales Analytics Dashboard
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    packages = [
        "streamlit",
        "pandas", 
        "numpy",
        "plotly",
        "scipy",
        "seaborn",
        "matplotlib"
    ]
    
    for package in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        except subprocess.CalledProcessError:
            print(f"Warning: Failed to install {package}")
    
    print("Package installation complete!")

def generate_data():
    """Generate sample data if it doesn't exist"""
    if not os.path.exists('sales_data.csv'):
        print("Generating sample sales data...")
        try:
            import data_generator
            data_generator.save_sample_data()
            print("Sample data generated successfully!")
        except Exception as e:
            print(f"Error generating data: {e}")

def run_dashboard():
    """Run the Streamlit dashboard"""
    print("\nStarting Sales Analytics Dashboard...")
    print("The dashboard will open in your browser at: http://localhost:8501")
    print("Press Ctrl+C to stop the dashboard")
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\nDashboard stopped by user")
    except Exception as e:
        print(f"Error running dashboard: {e}")

if __name__ == "__main__":
    print("🚀 Sales Analytics Dashboard Setup")
    print("=" * 50)
    
    # Step 1: Install requirements
    install_requirements()
    
    # Step 2: Generate data
    generate_data()
    
    # Step 3: Run dashboard
    run_dashboard()