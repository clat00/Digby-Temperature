"""
Compare March vs November Temperatures by Year

Analyzes which month is typically colder in Digby, NS
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

# Configuration
INPUT_FILE = "digby_temperature_2020-2025.csv"
OUTPUT_PLOT = "march_vs_november_comparison.png"

# Check if data file exists
if not os.path.exists(INPUT_FILE):
    print(f"Error: {INPUT_FILE} not found!")
    print("Please run fetch_digby_temperature.py first to download the data.")
    exit(1)

# Read the CSV
print(f"Reading data from {INPUT_FILE}...")
df = pd.read_csv(INPUT_FILE)
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month

# Filter for March (3) and November (11)
march_data = df[df['month'] == 3].copy()
november_data = df[df['month'] == 11].copy()

print("\nMarch vs November Temperature Comparison")
print("="*60)

# Calculate average temperatures by year
march_avg = march_data.groupby('year')['avg_temp_c'].mean()
november_avg = november_data.groupby('year')['avg_temp_c'].mean()

# Combine into a comparison dataframe
comparison = pd.DataFrame({
    'March': march_avg,
    'November': november_avg
})
comparison['Difference (Mar - Nov)'] = comparison['March'] - comparison['November']
comparison['Colder Month'] = comparison['Difference (Mar - Nov)'].apply(
    lambda x: 'November' if x > 0 else 'March' if x < 0 else 'Same'
)

print("\nAverage Temperature by Year (°C):")
print(comparison.round(2))

# Overall averages
print("\n" + "="*60)
print(f"Overall March Average:    {march_avg.mean():.1f}°C")
print(f"Overall November Average: {november_avg.mean():.1f}°C")
print(f"Difference:               {march_avg.mean() - november_avg.mean():.1f}°C")

if march_avg.mean() > november_avg.mean():
    print(f"\n✓ November is colder on average by {november_avg.mean() - march_avg.mean():.1f}°C")
else:
    print(f"\n✓ March is colder on average by {march_avg.mean() - november_avg.mean():.1f}°C")

# Count which month is colder more often
november_colder_count = (comparison['Colder Month'] == 'November').sum()
march_colder_count = (comparison['Colder Month'] == 'March').sum()

print(f"\nNovember was colder in {november_colder_count} out of {len(comparison)} years")
print(f"March was colder in {march_colder_count} out of {len(comparison)} years")

# Create visualization
print("\nGenerating comparison visualization...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Plot 1: Side-by-side bar chart
years = comparison.index
x = range(len(years))
width = 0.35

ax1.bar([i - width/2 for i in x], comparison['March'], width, 
        label='March', alpha=0.8, color='#2ca02c')
ax1.bar([i + width/2 for i in x], comparison['November'], width, 
        label='November', alpha=0.8, color='#ff7f0e')

ax1.set_xlabel('Year', fontsize=12)
ax1.set_ylabel('Average Temperature (°C)', fontsize=12)
ax1.set_title('March vs November Average Temperature by Year', fontsize=13, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(years)
ax1.legend()
ax1.grid(True, alpha=0.3, axis='y')

# Plot 2: Temperature difference
colors = ['red' if x > 0 else 'blue' for x in comparison['Difference (Mar - Nov)']]
ax2.bar(x, comparison['Difference (Mar - Nov)'], alpha=0.7, color=colors)
ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
ax2.set_xlabel('Year', fontsize=12)
ax2.set_ylabel('Temperature Difference (°C)\nMarch - November', fontsize=12)
ax2.set_title('Temperature Difference (Positive = March Warmer)', fontsize=13, fontweight='bold')
ax2.set_xticks(x)
ax2.set_xticklabels(years)
ax2.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(OUTPUT_PLOT, dpi=300, bbox_inches='tight')
print(f"✓ Plot saved to {OUTPUT_PLOT}")

plt.close()
print("\n✓ Done!")

