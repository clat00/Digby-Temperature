"""
Wind Data Visualization for Digby, NS

Creates visualizations of wind patterns including:
- Wind speed over time
- Wind direction frequency
- Seasonal wind patterns
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Configuration
INPUT_FILE = "digby_temperature_2020-2025.csv"
OUTPUT_FILE_SPEED = "digby_wind_speed.png"
OUTPUT_FILE_ROSE = "digby_wind_rose.png"

# Check if data file exists
if not os.path.exists(INPUT_FILE):
    print(f"Error: {INPUT_FILE} not found!")
    print("Please run fetch_digby_temperature.py first to download the data.")
    exit(1)

# Read the CSV
print(f"Reading data from {INPUT_FILE}...")
df = pd.read_csv(INPUT_FILE)
df['date'] = pd.to_datetime(df['date'])

# Check if wind data exists
if 'wind_speed_kmph' not in df.columns:
    print("Error: No wind data in CSV file!")
    print("Please re-run fetch_digby_temperature.py to collect wind data.")
    exit(1)

print(f"Loaded {len(df)} days of data")

# Filter out rows with no wind data
df_wind = df[df['wind_speed_kmph'] > 0].copy()
print(f"Days with wind data: {len(df_wind)}")

if len(df_wind) == 0:
    print("No wind data available to visualize.")
    exit(1)

# ===== WIND SPEED OVER TIME =====
print("\nGenerating wind speed visualization...")

fig, axes = plt.subplots(2, 1, figsize=(15, 10))

# Plot 1: Daily wind speed
ax1 = axes[0]
ax1.plot(df_wind['date'], df_wind['wind_speed_kmph'], alpha=0.6, linewidth=0.8, color='steelblue')
ax1.set_xlabel('Date')
ax1.set_ylabel('Wind Speed (km/h)')
ax1.set_title('Digby, NS Daily Average Wind Speed (2020-2026)', fontsize=14, fontweight='bold')
ax1.grid(True, alpha=0.3)

# Add a rolling average
if len(df_wind) > 30:
    df_wind['wind_ma30'] = df_wind['wind_speed_kmph'].rolling(window=30, center=True).mean()
    ax1.plot(df_wind['date'], df_wind['wind_ma30'], color='darkred', linewidth=2, label='30-day average')
    ax1.legend()

# Plot 2: Monthly average wind speed by year
df_wind['year'] = df_wind['date'].dt.year
df_wind['month'] = df_wind['date'].dt.month

monthly_avg = df_wind.groupby(['year', 'month'])['wind_speed_kmph'].mean().reset_index()

ax2 = axes[1]
for year in sorted(df_wind['year'].unique()):
    year_data = monthly_avg[monthly_avg['year'] == year]
    ax2.plot(year_data['month'], year_data['wind_speed_kmph'], marker='o', label=str(year), linewidth=2)

ax2.set_xlabel('Month')
ax2.set_ylabel('Average Wind Speed (km/h)')
ax2.set_title('Monthly Average Wind Speed by Year', fontsize=12, fontweight='bold')
ax2.set_xticks(range(1, 13))
ax2.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
ax2.grid(True, alpha=0.3)
ax2.legend()

plt.tight_layout()
plt.savefig(OUTPUT_FILE_SPEED, dpi=300, bbox_inches='tight')
print(f"✓ Wind speed plot saved to {OUTPUT_FILE_SPEED}")
plt.close()

# ===== WIND DIRECTION ROSE =====
print("\nGenerating wind rose visualization...")

# Map wind directions to angles
direction_map = {
    'N': 0, 'NNE': 22.5, 'NE': 45, 'ENE': 67.5,
    'E': 90, 'ESE': 112.5, 'SE': 135, 'SSE': 157.5,
    'S': 180, 'SSW': 202.5, 'SW': 225, 'WSW': 247.5,
    'W': 270, 'WNW': 292.5, 'NW': 315, 'NNW': 337.5
}

# Filter data with valid wind direction
df_direction = df_wind[df_wind['wind_direction'].isin(direction_map.keys())].copy()

if len(df_direction) > 0:
    # Count frequency of each direction
    direction_counts = df_direction['wind_direction'].value_counts()
    
    # Create polar plot
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='polar')
    
    # Convert directions to angles and counts to radii
    angles = [np.radians(direction_map[d]) for d in direction_counts.index]
    counts = direction_counts.values
    
    # Create bar chart
    bars = ax.bar(angles, counts, width=np.radians(22.5), bottom=0.0, alpha=0.7, edgecolor='black')
    
    # Color bars by frequency
    colors = plt.cm.viridis(counts / counts.max())
    for bar, color in zip(bars, colors):
        bar.set_facecolor(color)
    
    # Set direction labels
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_xticks(np.radians([0, 45, 90, 135, 180, 225, 270, 315]))
    ax.set_xticklabels(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'])
    
    ax.set_title('Wind Direction Frequency\nDigby, NS (2020-2026)', 
                 fontsize=14, fontweight='bold', pad=20)
    
    # Add legend showing average wind speed by direction
    direction_avg_speed = df_direction.groupby('wind_direction')['wind_speed_kmph'].mean()
    legend_text = f"Total observations: {len(df_direction)}\n"
    legend_text += f"Most common: {direction_counts.index[0]} ({direction_counts.values[0]} days)"
    ax.text(0.02, 0.98, legend_text, transform=fig.transFigure, 
            fontsize=10, verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig(OUTPUT_FILE_ROSE, dpi=300, bbox_inches='tight')
    print(f"✓ Wind rose plot saved to {OUTPUT_FILE_ROSE}")
    plt.close()
else:
    print("⚠ No valid wind direction data to create wind rose")

# ===== STATISTICS =====
print("\n" + "="*50)
print("Wind Statistics:")
print("="*50)
print(f"Average wind speed: {df_wind['wind_speed_kmph'].mean():.1f} km/h")
print(f"Maximum wind speed: {df_wind['wind_speed_kmph'].max():.1f} km/h")
print(f"Minimum wind speed: {df_wind['wind_speed_kmph'].min():.1f} km/h")

if 'wind_gust_kmph' in df.columns and df['wind_gust_kmph'].max() > 0:
    print(f"Maximum wind gust: {df['wind_gust_kmph'].max():.1f} km/h")

if len(df_direction) > 0:
    print(f"\nMost common wind direction: {direction_counts.index[0]}")
    print(f"Least common wind direction: {direction_counts.index[-1]}")
    
    print("\nWind direction frequency:")
    for direction, count in direction_counts.head(5).items():
        pct = (count / len(df_direction)) * 100
        print(f"  {direction:4s}: {count:4d} days ({pct:.1f}%)")

print("\n✓ Done!")
