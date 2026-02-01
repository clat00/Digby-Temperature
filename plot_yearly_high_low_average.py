"""
Plot Average High and Low Temperature by Day of Year

This script creates a plot showing the average high and low temperatures
for each day of the year across all years in the dataset.
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

# Configuration
INPUT_FILE = "digby_temperature_2020-2025.csv"
OUTPUT_PLOT = "yearly_high_low_average.png"

# Check if data file exists
if not os.path.exists(INPUT_FILE):
    print(f"Error: {INPUT_FILE} not found!")
    print("Please run fetch_digby_temperature.py first to download the data.")
    exit(1)

# Read the CSV
print(f"Reading data from {INPUT_FILE}...")
df = pd.read_csv(INPUT_FILE)
df['date'] = pd.to_datetime(df['date'])

print(f"Loaded {len(df)} days of temperature data")
print(f"Date range: {df['date'].min().date()} to {df['date'].max().date()}")

# Extract day of year from date
df['day_of_year'] = df['date'].dt.dayofyear

# Calculate average high and low temperature for each day of year across all years
daily_stats = df.groupby('day_of_year').agg({
    'max_temp_c': 'mean',
    'min_temp_c': 'mean'
}).reset_index()

# Create month names for better x-axis labels
month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# Calculate the first day of each month for x-axis ticks
month_starts = [1, 32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335]

# Create the visualization
print("\nGenerating average high/low temperature plot...")

plt.figure(figsize=(15, 6))
plt.plot(daily_stats['day_of_year'], daily_stats['max_temp_c'], 
         label='Average High', alpha=0.7, color='red', linewidth=1.5)
plt.plot(daily_stats['day_of_year'], daily_stats['min_temp_c'], 
         label='Average Low', alpha=0.7, color='blue', linewidth=1.5)
plt.fill_between(daily_stats['day_of_year'], daily_stats['min_temp_c'], 
                 daily_stats['max_temp_c'], alpha=0.2, color='gray')

plt.xlabel('Month', fontsize=12)
plt.ylabel('Temperature (°C)', fontsize=12)
plt.title('Average Daily High and Low Temperature by Day of Year - Digby, NS (2020-2025)', 
          fontsize=14, fontweight='bold')
plt.legend(loc='best', fontsize=11)
plt.xticks(month_starts, month_names)
plt.xlim(1, 365)
plt.grid(True, alpha=0.3, linestyle='--')
plt.tight_layout()

# Save the plot
plt.savefig(OUTPUT_PLOT, dpi=300, bbox_inches='tight')
print(f"✓ Plot saved to {OUTPUT_PLOT}")

# Show summary statistics
print("\nTemperature Statistics (°C):")
print(f"  Coldest average low: {daily_stats['min_temp_c'].min():.2f}°C (day {daily_stats.loc[daily_stats['min_temp_c'].idxmin(), 'day_of_year']:.0f})")
print(f"  Warmest average low: {daily_stats['min_temp_c'].max():.2f}°C (day {daily_stats.loc[daily_stats['min_temp_c'].idxmax(), 'day_of_year']:.0f})")
print(f"  Coldest average high: {daily_stats['max_temp_c'].min():.2f}°C (day {daily_stats.loc[daily_stats['max_temp_c'].idxmin(), 'day_of_year']:.0f})")
print(f"  Warmest average high: {daily_stats['max_temp_c'].max():.2f}°C (day {daily_stats.loc[daily_stats['max_temp_c'].idxmax(), 'day_of_year']:.0f})")
print(f"  Overall temperature range: {daily_stats['max_temp_c'].max() - daily_stats['min_temp_c'].min():.2f}°C")

plt.close()
print("\n✓ Done!")
