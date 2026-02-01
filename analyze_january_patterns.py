#!/usr/bin/env python3
"""
Analyze January temperature patterns in Digby to understand if current 2026 conditions are unusual.
"""

import pandas as pd
from datetime import datetime

def analyze_january_patterns(csv_file='digby_temperature_2020-2025.csv'):
    """Analyze January temperature patterns."""
    
    # Read the CSV file
    df = pd.read_csv(csv_file)
    
    # Convert date column to datetime
    df['date'] = pd.to_datetime(df['date'])
    
    # Extract year and month
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    
    # Filter for January only
    jan_df = df[df['month'] == 1].copy()
    
    print("=" * 70)
    print("JANUARY TEMPERATURE ANALYSIS (2020-2025)")
    print("=" * 70)
    print()
    
    # Days with min temp below -12°C in January
    print("Days in January with MIN temperature at or below -12°C:")
    print("-" * 70)
    below_minus_12 = jan_df[jan_df['min_temp_c'] <= -12]
    
    for year in sorted(jan_df['year'].unique()):
        year_data = below_minus_12[below_minus_12['year'] == year]
        count = len(year_data)
        print(f"  January {year}: {count} days")
        if count > 0:
            for _, row in year_data.iterrows():
                print(f"    - {row['date'].strftime('%Y-%m-%d')}: Max {row['max_temp_c']:5.1f}°C, Min {row['min_temp_c']:5.1f}°C")
    
    print()
    total_below_12 = len(below_minus_12)
    print(f"Total: {total_below_12} days across all Januarys")
    print()
    
    # Extended cold periods (consecutive days below -5°C max)
    print("=" * 70)
    print("Extended Cold Periods in January (consecutive days with MAX < -5°C):")
    print("-" * 70)
    
    for year in sorted(jan_df['year'].unique()):
        year_data = jan_df[jan_df['year'] == year].sort_values('date')
        
        print(f"\nJanuary {year}:")
        
        current_streak = 0
        max_streak = 0
        streak_start = None
        streaks = []
        
        for _, row in year_data.iterrows():
            if row['max_temp_c'] < -5:
                if current_streak == 0:
                    streak_start = row['date']
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                if current_streak > 0:
                    streaks.append((streak_start, current_streak))
                current_streak = 0
        
        # Check if streak continues to end of month
        if current_streak > 0:
            streaks.append((streak_start, current_streak))
        
        if streaks:
            for start_date, length in streaks:
                print(f"  - {length} consecutive days starting {start_date.strftime('%Y-%m-%d')}")
        else:
            print(f"  - No periods with max temp below -5°C")
        
        print(f"  Longest cold streak: {max_streak} days")
    
    # Overall January statistics
    print()
    print("=" * 70)
    print("OVERALL JANUARY STATISTICS:")
    print("-" * 70)
    
    for year in sorted(jan_df['year'].unique()):
        year_data = jan_df[jan_df['year'] == year]
        avg_max = year_data['max_temp_c'].mean()
        avg_min = year_data['min_temp_c'].mean()
        coldest_min = year_data['min_temp_c'].min()
        days_below_minus_10 = len(year_data[year_data['min_temp_c'] < -10])
        days_max_below_zero = len(year_data[year_data['max_temp_c'] < 0])
        
        print(f"\nJanuary {year}:")
        print(f"  Average max temp: {avg_max:5.1f}°C")
        print(f"  Average min temp: {avg_min:5.1f}°C")
        print(f"  Coldest min temp: {coldest_min:5.1f}°C")
        print(f"  Days with min below -10°C: {days_below_minus_10}")
        print(f"  Days with max below 0°C: {days_max_below_zero}")
    
    # Grand averages
    print()
    print("JANUARY AVERAGES (2020-2025):")
    avg_max_all = jan_df['max_temp_c'].mean()
    avg_min_all = jan_df['min_temp_c'].mean()
    print(f"  Average max temperature: {avg_max_all:5.1f}°C")
    print(f"  Average min temperature: {avg_min_all:5.1f}°C")
    print()
    print("=" * 70)

if __name__ == '__main__':
    analyze_january_patterns()
