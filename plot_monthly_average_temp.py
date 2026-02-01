"""
Plot Monthly Average Temperature

This script creates a plot showing the average temperature for each month
across all years in the dataset.
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

# Configuration
INPUT_FILE = "digby_temperature_2020-2025.csv"
OUTPUT_PLOT = "monthly_average_temperature.png"

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

# Extract month and day of year from date
df['month'] = df['date'].dt.month
df['day_of_year'] = df['date'].dt.dayofyear

# Calculate average temperature for each day of year across all years
daily_avg = df.groupby('day_of_year')['avg_temp_c'].mean()

# Create month names for better x-axis labels
month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# Calculate the first day of each month for x-axis ticks
month_starts = [1, 32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335]

# Create the visualization
print("\nGenerating daily average temperature plot...")

plt.figure(figsize=(14, 6))
plt.plot(daily_avg.index, daily_avg.values, linewidth=1.5, color='#2E86AB')
plt.fill_between(daily_avg.index, daily_avg.values, alpha=0.3, color='#2E86AB')

plt.xlabel('Month', fontsize=12, fontweight='bold')
plt.ylabel('Average Temperature (°C)', fontsize=12, fontweight='bold')
plt.title('Average Temperature by Day of Year - Digby, NS (2020-2025)', 
          fontsize=14, fontweight='bold')
plt.xticks(month_starts, month_names)
plt.xlim(1, 365)
plt.grid(True, alpha=0.3, linestyle='--', linewidth=0.8)
plt.tight_layout()

# Save the plot
plt.savefig(OUTPUT_PLOT, dpi=300, bbox_inches='tight')
print(f"✓ Plot saved to {OUTPUT_PLOT}")

# Show summary statistics
print("\nDaily Temperature Statistics (°C):")
print(f"  Minimum daily average: {daily_avg.min():.2f}°C (day {daily_avg.idxmin()} of year)")
print(f"  Maximum daily average: {daily_avg.max():.2f}°C (day {daily_avg.idxmax()} of year)")
print(f"  Temperature range: {daily_avg.max() - daily_avg.min():.2f}°C")
print(f"  Overall mean: {daily_avg.mean():.2f}°C")

plt.close()
print("\n✓ Done!")
