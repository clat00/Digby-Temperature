"""
Visualize Digby Temperature Data by Year

This script creates a chart with one line per year,
allowing easy comparison of temperature patterns across years.
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

# Configuration
INPUT_FILE = "digby_temperature_2020-2025.csv"
OUTPUT_PLOT = "digby_temperature_by_year.png"

# Check if data file exists
if not os.path.exists(INPUT_FILE):
    print(f"Error: {INPUT_FILE} not found!")
    print("Please run fetch_digby_temperature.py first to download the data.")
    exit(1)

# Read the CSV
print(f"Reading data from {INPUT_FILE}...")
df = pd.read_csv(INPUT_FILE)
df['date'] = pd.to_datetime(df['date'])

# Extract year and day of year for alignment
df['year'] = df['date'].dt.year
df['day_of_year'] = df['date'].dt.dayofyear

print(f"Loaded {len(df)} days of temperature data")
print(f"Years: {sorted(df['year'].unique())}")

# Create the visualization
print("\nGenerating year comparison visualization...")

plt.figure(figsize=(15, 8))

# Color palette for years - distinct colors with good contrast
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']

# Plot each year
for idx, year in enumerate(sorted(df['year'].unique())):
    year_data = df[df['year'] == year].sort_values('day_of_year')
    
    # Use average temperature for cleaner comparison
    plt.plot(year_data['day_of_year'], 
             year_data['avg_temp_c'], 
             label=str(year), 
             alpha=0.8, 
             linewidth=2,
             color=colors[idx % len(colors)])

plt.xlabel('Day of Year', fontsize=12)
plt.ylabel('Average Temperature (°C)', fontsize=12)
plt.title('Digby, NS Daily Temperature by Year (2020-2025)', fontsize=14, fontweight='bold')
plt.legend(loc='best', fontsize=11)
plt.grid(True, alpha=0.3, linestyle='--')
plt.xlim(1, 366)  # Show full year range

# Add month labels on x-axis
month_days = [1, 32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335]
month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
plt.xticks(month_days, month_labels)

plt.tight_layout()

# Save the plot
plt.savefig(OUTPUT_PLOT, dpi=300, bbox_inches='tight')
print(f"✓ Plot saved to {OUTPUT_PLOT}")

# Show statistics by year
print("\nAverage Temperature by Year (°C):")
yearly_avg = df.groupby('year')['avg_temp_c'].agg(['mean', 'min', 'max'])
print(yearly_avg.round(1))

plt.close()
print("\n✓ Done!")

