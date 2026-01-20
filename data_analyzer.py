"""
Agri-Tech Data Analyzer
A Python script for analyzing daily rainfall and crop growth data.
Features: Data validation, error handling, and visualization.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import sys


def load_data(filepath):
    """
    Load CSV file with error handling for missing/corrupt data.
    
    Args:
        filepath (str): Path to the CSV file
        
    Returns:
        pd.DataFrame: Loaded and validated dataframe
    """
    try:
        print(f"Loading data from {filepath}...")
        df = pd.read_csv(filepath)
        print(f"✓ Successfully loaded {len(df)} records")
        return df
    except FileNotFoundError:
        print(f"✗ Error: File '{filepath}' not found.")
        sys.exit(1)
    except pd.errors.EmptyDataError:
        print("✗ Error: CSV file is empty.")
        sys.exit(1)
    except pd.errors.ParserError as e:
        print(f"✗ Error: Failed to parse CSV file: {e}")
        sys.exit(1)


def validate_data(df):
    """
    Validate data integrity and handle missing values.
    
    Args:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        pd.DataFrame: Cleaned dataframe
    """
    print("\nValidating data...")
    
    # Check required columns
    required_columns = ['Date', 'Rainfall_mm', 'Crop_Growth_cm']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        print(f"✗ Error: Missing required columns: {missing_columns}")
        sys.exit(1)
    
    # Check for missing values
    missing_values = df.isnull().sum()
    if missing_values.any():
        print(f"⚠ Found missing values, filling with forward fill method:")
        print(missing_values[missing_values > 0])
        df = df.fillna(method='ffill').fillna(method='bfill')
    
    # Check for invalid data types and convert
    try:
        df['Date'] = pd.to_datetime(df['Date'])
        df['Rainfall_mm'] = pd.to_numeric(df['Rainfall_mm'])
        df['Crop_Growth_cm'] = pd.to_numeric(df['Crop_Growth_cm'])
        
        # Check for negative values (which don't make sense)
        if (df['Rainfall_mm'] < 0).any():
            print("⚠ Found negative rainfall values, setting to 0")
            df.loc[df['Rainfall_mm'] < 0, 'Rainfall_mm'] = 0
        
        if (df['Crop_Growth_cm'] < 0).any():
            print("⚠ Found negative growth values, removing those rows")
            df = df[df['Crop_Growth_cm'] >= 0]
            
    except ValueError as e:
        print(f"✗ Error: Invalid data format - {e}")
        sys.exit(1)
    
    # Sort by date
    df = df.sort_values('Date').reset_index(drop=True)
    print(f"✓ Data validation complete. {len(df)} valid records")
    return df


def calculate_weekly_statistics(df):
    """
    Calculate weekly rainfall and crop growth statistics.
    
    Args:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        pd.DataFrame: Weekly statistics
    """
    print("\nCalculating weekly statistics...")
    
    # Set Date as index for resampling
    df_weekly = df.set_index('Date')
    
    # Calculate weekly aggregates
    weekly_stats = pd.DataFrame({
        'Weekly_Rainfall_mm': df_weekly['Rainfall_mm'].resample('W').sum(),
        'Avg_Growth_cm': df_weekly['Crop_Growth_cm'].resample('W').mean(),
        'Avg_Temperature_C': df_weekly['Temperature_C'].resample('W').mean()
    })
    
    print("\nWeekly Rainfall Summary:")
    print(weekly_stats['Weekly_Rainfall_mm'].describe())
    
    return weekly_stats


def calculate_correlation(df):
    """
    Calculate correlation between rainfall and crop growth.
    
    Args:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        float: Correlation coefficient
    """
    correlation = df['Rainfall_mm'].corr(df['Crop_Growth_cm'])
    print(f"\nCorrelation between Rainfall and Crop Growth: {correlation:.4f}")
    
    if correlation > 0.7:
        print("→ Strong positive correlation: More rain leads to more growth")
    elif correlation > 0.4:
        print("→ Moderate positive correlation")
    elif correlation > 0:
        print("→ Weak positive correlation")
    else:
        print("→ Negative or no correlation")
    
    return correlation


def plot_analysis(df, weekly_stats, correlation):
    """
    Create comprehensive visualizations of the data.
    
    Args:
        df (pd.DataFrame): Daily data
        weekly_stats (pd.DataFrame): Weekly aggregated data
        correlation (float): Correlation coefficient
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Agri-Tech Data Analysis: Rainfall & Crop Growth', 
                 fontsize=16, fontweight='bold')
    
    # Plot 1: Daily Rainfall
    axes[0, 0].bar(df['Date'], df['Rainfall_mm'], color='steelblue', alpha=0.7)
    axes[0, 0].set_title('Daily Rainfall', fontweight='bold')
    axes[0, 0].set_ylabel('Rainfall (mm)')
    axes[0, 0].tick_params(axis='x', rotation=45)
    axes[0, 0].grid(axis='y', alpha=0.3)
    
    # Plot 2: Daily Crop Growth
    axes[0, 1].plot(df['Date'], df['Crop_Growth_cm'], 
                    marker='o', color='green', linewidth=2, markersize=4)
    axes[0, 1].fill_between(df['Date'], df['Crop_Growth_cm'], alpha=0.3, color='green')
    axes[0, 1].set_title('Daily Crop Growth', fontweight='bold')
    axes[0, 1].set_ylabel('Growth (cm)')
    axes[0, 1].tick_params(axis='x', rotation=45)
    axes[0, 1].grid(alpha=0.3)
    
    # Plot 3: Correlation Scatter Plot
    axes[1, 0].scatter(df['Rainfall_mm'], df['Crop_Growth_cm'], 
                       alpha=0.6, s=50, color='darkgreen')
    z = np.polyfit(df['Rainfall_mm'], df['Crop_Growth_cm'], 1)
    p = np.poly1d(z)
    axes[1, 0].plot(df['Rainfall_mm'], p(df['Rainfall_mm']), 
                    "r--", linewidth=2, label=f'Trend (R={correlation:.2f})')
    axes[1, 0].set_title('Rainfall vs Crop Growth', fontweight='bold')
    axes[1, 0].set_xlabel('Rainfall (mm)')
    axes[1, 0].set_ylabel('Growth (cm)')
    axes[1, 0].legend()
    axes[1, 0].grid(alpha=0.3)
    
    # Plot 4: Weekly Rainfall Trend
    axes[1, 1].bar(range(len(weekly_stats)), weekly_stats['Weekly_Rainfall_mm'], 
                   color='lightblue', alpha=0.7, label='Weekly Rainfall')
    axes[1, 1].plot(range(len(weekly_stats)), weekly_stats['Avg_Growth_cm'] * 10, 
                    marker='o', color='red', linewidth=2, markersize=6, label='Growth (×10 for scale)')
    axes[1, 1].set_title('Weekly Rainfall vs Growth Trend', fontweight='bold')
    axes[1, 1].set_xlabel('Week')
    axes[1, 1].set_ylabel('Rainfall (mm) / Growth (cm × 10)')
    axes[1, 1].legend()
    axes[1, 1].grid(alpha=0.3)
    
    plt.tight_layout()
    
    # Save and show
    output_file = 'agri_tech_analysis.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\n✓ Graph saved as '{output_file}'")
    
    plt.show()


def main():
    """Main execution function."""
    print("=" * 60)
    print("AGRI-TECH DATA ANALYZER")
    print("=" * 60)
    
    # Load and validate data
    df = load_data('daily_crop_data.csv')
    df = validate_data(df)
    
    # Calculate statistics
    weekly_stats = calculate_weekly_statistics(df)
    correlation = calculate_correlation(df)
    
    # Generate visualizations
    plot_analysis(df, weekly_stats, correlation)
    
    print("\n" + "=" * 60)
    print("Analysis complete!")
    print("=" * 60)


if __name__ == '__main__':
    main()
