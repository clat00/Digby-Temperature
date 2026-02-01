#!/usr/bin/env python3
"""
Analyze how many days each year the temperature dropped below -10°C in Digby.
"""

import pandas as pd
from datetime import datetime

def analyze_cold_days(csv_file='digby_temperature_2020-2025.csv'):
    """Count days below -10°C for each year."""
    
    # Read the CSV file
    df = pd.read_csv(csv_file)
    
    # Convert date column to datetime
    df['date'] = pd.to_datetime(df['date'])
    
    # Extract year from date
    df['year'] = df['date'].dt.year
    
    # Count days where minimum temperature dropped below -10°C
    cold_days = df[df['min_temp_c'] < -10].copy()
    
    # Group by year and count
    cold_days_by_year = cold_days.groupby('year').size()
    
    # Get all years in dataset
    all_years = sorted(df['year'].unique())
    
    # Print results
    print("=" * 60)
    print("ANALYSIS: Days with Temperature Below -10°C in Digby")
    print("=" * 60)
    print()
    
    total_cold_days = 0
    for year in all_years:
        count = cold_days_by_year.get(year, 0)
        total_cold_days += count
        print(f"  {year}: {count:3d} days")
    
    print()
    print("-" * 60)
    print(f"  Total: {total_cold_days:3d} days across all years")
    print("=" * 60)
    print()
    
    # Additional statistics
    if len(cold_days) > 0:
        print("Coldest recorded temperature: {:.1f}°C on {}".format(
            cold_days['min_temp_c'].min(),
            cold_days.loc[cold_days['min_temp_c'].idxmin(), 'date'].strftime('%Y-%m-%d')
        ))
        print()
        
        # Show breakdown by month for cold days
        cold_days['month'] = cold_days['date'].dt.month
        cold_days_by_month = cold_days.groupby('month').size()
        
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        print("Breakdown by month:")
        for month in sorted(cold_days_by_month.index):
            count = cold_days_by_month[month]
            print(f"  {month_names[month-1]}: {count:3d} days")
    
    return cold_days_by_year

if __name__ == '__main__':
    analyze_cold_days()
