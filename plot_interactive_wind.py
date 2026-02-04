"""
Interactive Wind Visualizations for Digby, NS

Creates interactive HTML charts for:
1. Monthly average wind speed by year
2. Peak wind gusts by year
"""

import pandas as pd
import plotly.graph_objects as go
import os

# Configuration
INPUT_FILE = "digby_temperature_2020-2025.csv"
OUTPUT_WIND_SPEED = "digby_wind_speed_interactive.html"
OUTPUT_WIND_GUSTS = "digby_wind_gusts_interactive.html"

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

# Extract year and month
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month

print(f"Loaded {len(df)} days of data")
print(f"Years: {sorted(df['year'].unique())}")

# Color palette for years
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']

# ===== CHART 1: MONTHLY AVERAGE WIND SPEED =====
print("\nGenerating monthly average wind speed chart...")

# Calculate monthly averages
monthly_avg = df.groupby(['year', 'month'])['wind_speed_kmph'].mean().reset_index()

fig1 = go.Figure()

for idx, year in enumerate(sorted(df['year'].unique())):
    year_data = monthly_avg[monthly_avg['year'] == year].sort_values('month')
    
    # Create hover text
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    hover_text = [
        f"{month_names[m-1]} {year}<br>Avg: {speed:.1f} km/h"
        for m, speed in zip(year_data['month'], year_data['wind_speed_kmph'])
    ]
    
    fig1.add_trace(go.Scatter(
        x=year_data['month'],
        y=year_data['wind_speed_kmph'],
        name=str(year),
        mode='lines+markers',
        line=dict(color=colors[idx % len(colors)], width=2),
        marker=dict(size=8),
        hovertext=hover_text,
        hoverinfo='text'
    ))

fig1.update_layout(
    title={
        'text': 'Digby, NS Monthly Average Wind Speed by Year',
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 18}
    },
    xaxis_title='Month',
    yaxis_title='Average Wind Speed (km/h)',
    hovermode='closest',
    width=1200,
    height=600,
    legend=dict(
        orientation="v",
        yanchor="top",
        y=0.99,
        xanchor="right",
        x=0.99,
        bgcolor="rgba(255, 255, 255, 0.8)",
        bordercolor="gray",
        borderwidth=1
    ),
    plot_bgcolor='white',
    xaxis=dict(
        showgrid=True,
        gridcolor='lightgray',
        tickmode='array',
        tickvals=list(range(1, 13)),
        ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='lightgray'
    )
)

fig1.write_html(OUTPUT_WIND_SPEED)
print(f"✓ Monthly wind speed chart saved to {OUTPUT_WIND_SPEED}")

# ===== CHART 2: PEAK WIND GUSTS =====
print("\nGenerating peak wind gusts chart...")

# Get daily data with day of year for alignment
df['day_of_year'] = df['date'].dt.dayofyear

fig2 = go.Figure()

for idx, year in enumerate(sorted(df['year'].unique())):
    year_data = df[df['year'] == year].sort_values('day_of_year')
    
    # Filter out zero gusts
    year_data = year_data[year_data['wind_gust_kmph'] > 0]
    
    if len(year_data) == 0:
        continue
    
    # Create hover text
    hover_text = [
        f"Date: {date.strftime('%b %d, %Y')}<br>Gust: {gust:.0f} km/h"
        for date, gust in zip(year_data['date'], year_data['wind_gust_kmph'])
    ]
    
    fig2.add_trace(go.Scatter(
        x=year_data['day_of_year'],
        y=year_data['wind_gust_kmph'],
        name=str(year),
        mode='lines',
        line=dict(color=colors[idx % len(colors)], width=1.5),
        hovertext=hover_text,
        hoverinfo='text',
        opacity=0.7
    ))

fig2.update_layout(
    title={
        'text': 'Digby, NS Daily Peak Wind Gusts by Year',
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 18}
    },
    xaxis_title='Month',
    yaxis_title='Wind Gust Speed (km/h)',
    hovermode='closest',
    width=1200,
    height=600,
    legend=dict(
        orientation="v",
        yanchor="top",
        y=0.99,
        xanchor="right",
        x=0.99,
        bgcolor="rgba(255, 255, 255, 0.8)",
        bordercolor="gray",
        borderwidth=1
    ),
    plot_bgcolor='white',
    xaxis=dict(
        showgrid=True,
        gridcolor='lightgray',
        range=[1, 366],
        tickmode='array',
        tickvals=[1, 32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335],
        ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='lightgray'
    )
)

fig2.write_html(OUTPUT_WIND_GUSTS)
print(f"✓ Peak wind gusts chart saved to {OUTPUT_WIND_GUSTS}")

# Print summary statistics
print("\n" + "="*50)
print("Wind Statistics Summary:")
print("="*50)
print(f"\nMonthly Average Wind Speed (km/h) by Year:")
yearly_monthly_avg = monthly_avg.groupby('year')['wind_speed_kmph'].mean()
for year, avg in yearly_monthly_avg.items():
    print(f"  {year}: {avg:.1f} km/h")

print(f"\nPeak Wind Gusts by Year:")
yearly_max_gust = df.groupby('year')['wind_gust_kmph'].max()
for year, gust in yearly_max_gust.items():
    print(f"  {year}: {gust:.0f} km/h")

print("\n✓ Done!")
