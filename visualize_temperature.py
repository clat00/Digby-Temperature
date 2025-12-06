"""
Visualize Digby Temperature Data

This script reads the CSV file and creates temperature visualizations
without needing to re-fetch data from the API.
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

# Configuration
INPUT_FILE = "digby_temperature_2023-2025.csv"
OUTPUT_PLOT = "digby_temperature_plot.png"

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

# Create the visualization
print("\nGenerating temperature visualization...")

plt.figure(figsize=(15, 6))
plt.plot(df['date'], df['max_temp_c'], label='Max Temp', alpha=0.7, color='red', linewidth=1.5)
plt.plot(df['date'], df['min_temp_c'], label='Min Temp', alpha=0.7, color='blue', linewidth=1.5)
plt.fill_between(df['date'], df['min_temp_c'], df['max_temp_c'], alpha=0.2, color='gray')

plt.xlabel('Date', fontsize=12)
plt.ylabel('Temperature (°C)', fontsize=12)
plt.title('Digby, NS Daily Temperature (2023-2025)', fontsize=14, fontweight='bold')
plt.legend(loc='best', fontsize=11)
plt.grid(True, alpha=0.3, linestyle='--')
plt.tight_layout()

# Save the plot
plt.savefig(OUTPUT_PLOT, dpi=300, bbox_inches='tight')
print(f"✓ Plot saved to {OUTPUT_PLOT}")

# Show summary statistics
print("\nTemperature Statistics (Celsius):")
print(df[['max_temp_c', 'min_temp_c', 'avg_temp_c']].describe())

plt.close()
print("\n✓ Done!")

