"""
Interactive Visualization of Digby Temperature Data by Year

This script creates an interactive chart with one line per year,
allowing easy comparison of temperature patterns across years.
Click on legend items to show/hide individual years.
"""

import pandas as pd
import plotly.graph_objects as go
import os

# Configuration
INPUT_FILE = "digby_temperature_2020-2025.csv"
OUTPUT_HTML = "digby_temperature_by_year_interactive.html"

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

# Create the interactive visualization
print("\nGenerating interactive year comparison visualization...")

# Color palette for years - distinct colors with good contrast
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']

# Create figure
fig = go.Figure()

# Add a trace for each year
for idx, year in enumerate(sorted(df['year'].unique())):
    year_data = df[df['year'] == year].sort_values('day_of_year')
    
    # Create custom hover text
    hover_text = [
        f"Date: {date.strftime('%b %d, %Y')}<br>Temp: {temp:.1f}°C"
        for date, temp in zip(year_data['date'], year_data['avg_temp_c'])
    ]
    
    fig.add_trace(go.Scatter(
        x=year_data['day_of_year'],
        y=year_data['avg_temp_c'],
        name=str(year),
        mode='lines',
        line=dict(
            color=colors[idx % len(colors)],
            width=2
        ),
        hovertext=hover_text,
        hoverinfo='text',
        opacity=0.8
    ))

# Update layout
fig.update_layout(
    title={
        'text': 'Digby, NS Daily Temperature by Year (2020-2026)<br><sub>Click legend items to show/hide years</sub>',
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 18}
    },
    xaxis_title='Month',
    yaxis_title='Average Temperature (°C)',
    hovermode='closest',
    width=1400,
    height=700,
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
        gridwidth=0.5,
        range=[1, 366],
        tickmode='array',
        tickvals=[1, 32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335],
        ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='lightgray',
        gridwidth=0.5
    )
)

# Save as HTML
fig.write_html(OUTPUT_HTML)
print(f"✓ Interactive plot saved to {OUTPUT_HTML}")
print(f"✓ Open the HTML file in your browser to interact with the chart")
print(f"   - Click legend items to show/hide years")
print(f"   - Double-click a legend item to isolate that year")
print(f"   - Hover over lines to see exact dates and temperatures")

# Show statistics by year
print("\nAverage Temperature by Year (°C):")
yearly_avg = df.groupby('year')['avg_temp_c'].agg(['mean', 'min', 'max'])
print(yearly_avg.round(1))

print("\n✓ Done!")
