#!/usr/bin/env python3
"""
Analyze how many days each year the MAX temperature stayed below -10°C in Digby.
This represents days where it never got warmer than -10°C all day.
"""

import pandas as pd
from datetime import datetime

def analyze_extreme_cold_days(csv_file='digby_temperature_2020-2025.csv'):
    """Count days where MAX temperature stayed below -10°C for each year."""
    
    # Read the CSV file
    df = pd.read_csv(csv_file)
    
    # Convert date column to datetime
    df['date'] = pd.to_datetime(df['date'])
    
    # Extract year from date
    df['year'] = df['date'].dt.year
    
    # Count days where MAXIMUM temperature stayed below -10°C
    extreme_cold_days = df[df['max_temp_c'] < -10].copy()
    
    # Group by year and count
    extreme_cold_by_year = extreme_cold_days.groupby('year').size()
    
    # Get all years in dataset
    all_years = sorted(df['year'].unique())
    
    # Print results
    print("=" * 60)
    print("ANALYSIS: Days with MAX Temperature Below -10°C in Digby")
    print("(Days that never got warmer than -10°C)")
    print("=" * 60)
    print()
    
    total_extreme_cold = 0
    for year in all_years:
        count = extreme_cold_by_year.get(year, 0)
        total_extreme_cold += count
        print(f"  {year}: {count:3d} days")
    
    print()
    print("-" * 60)
    print(f"  Total: {total_extreme_cold:3d} days across all years")
    print("=" * 60)
    print()
    
    # Additional statistics
    if len(extreme_cold_days) > 0:
        print("Coldest MAX temperature: {:.1f}°C on {}".format(
            extreme_cold_days['max_temp_c'].min(),
            extreme_cold_days.loc[extreme_cold_days['max_temp_c'].idxmin(), 'date'].strftime('%Y-%m-%d')
        ))
        print()
        
        # Show breakdown by month for extreme cold days
        extreme_cold_days['month'] = extreme_cold_days['date'].dt.month
        extreme_cold_by_month = extreme_cold_days.groupby('month').size()
        
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        print("Breakdown by month:")
        for month in sorted(extreme_cold_by_month.index):
            count = extreme_cold_by_month[month]
            print(f"  {month_names[month-1]}: {count:3d} days")
        
        print()
        print("Most extreme cold days (max temp below -10°C):")
        print("-" * 60)
        extreme_sorted = extreme_cold_days.sort_values('max_temp_c').head(10)
        for _, row in extreme_sorted.iterrows():
            print(f"  {row['date'].strftime('%Y-%m-%d')}: Max {row['max_temp_c']:5.1f}°C, Min {row['min_temp_c']:5.1f}°C")
    else:
        print("No days found where maximum temperature stayed below -10°C")
    
    return extreme_cold_by_year

if __name__ == '__main__':
    analyze_extreme_cold_days()
