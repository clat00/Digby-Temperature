"""
Interactive chart comparing the current year's daily temperature
against the historical average (computed from all prior years).

A shaded band shows the historical min–max range for each day.
"""

import pandas as pd
import plotly.graph_objects as go
import os
from datetime import datetime

INPUT_FILE = "digby_temperature_2020-2025.csv"
OUTPUT_HTML = "digby_temperature_vs_average_interactive.html"

if not os.path.exists(INPUT_FILE):
    print(f"Error: {INPUT_FILE} not found!")
    print("Please run fetch_digby_temperature.py first to download the data.")
    exit(1)

print(f"Reading data from {INPUT_FILE}...")
df = pd.read_csv(INPUT_FILE)
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year
df['day_of_year'] = df['date'].dt.dayofyear

current_year = df['year'].max()
prior_years = sorted([y for y in df['year'].unique() if y != current_year])

print(f"Current year: {current_year}")
print(f"Historical years: {prior_years[0]}–{prior_years[-1]}")

hist = df[df['year'] != current_year]
curr = df[df['year'] == current_year].sort_values('day_of_year')

hist_stats = hist.groupby('day_of_year')['avg_temp_c'].agg(['mean', 'min', 'max']).reset_index()
hist_stats.columns = ['day_of_year', 'avg', 'hist_min', 'hist_max']

# 7-day rolling smooth for the average line to reduce day-to-day noise
hist_stats['avg_smooth'] = hist_stats['avg'].rolling(7, center=True, min_periods=1).mean()
hist_stats['min_smooth'] = hist_stats['hist_min'].rolling(7, center=True, min_periods=1).mean()
hist_stats['max_smooth'] = hist_stats['hist_max'].rolling(7, center=True, min_periods=1).mean()

# Reference dates for hover labels (use a non-leap year)
ref_dates = pd.date_range('2025-01-01', periods=366, freq='D')

fig = go.Figure()

# Min–max range band
fig.add_trace(go.Scatter(
    x=hist_stats['day_of_year'],
    y=hist_stats['max_smooth'],
    mode='lines',
    line=dict(width=0),
    showlegend=False,
    hoverinfo='skip',
))
fig.add_trace(go.Scatter(
    x=hist_stats['day_of_year'],
    y=hist_stats['min_smooth'],
    mode='lines',
    line=dict(width=0),
    fill='tonexty',
    fillcolor='rgba(100, 149, 237, 0.15)',
    name=f'Historical range ({prior_years[0]}–{prior_years[-1]})',
    hoverinfo='skip',
))

# Historical average line
hover_avg = [
    f"{ref_dates[doy - 1].strftime('%b %d')}<br>Historical avg: {t:.1f}°C"
    for doy, t in zip(hist_stats['day_of_year'], hist_stats['avg_smooth'])
]
fig.add_trace(go.Scatter(
    x=hist_stats['day_of_year'],
    y=hist_stats['avg_smooth'],
    mode='lines',
    name=f'Historical average ({prior_years[0]}–{prior_years[-1]})',
    line=dict(color='#6366f1', width=3),
    hovertext=hover_avg,
    hoverinfo='text',
))

# Current year line
hover_curr = [
    f"{d.strftime('%b %d, %Y')}<br>Temp: {t:.1f}°C"
    for d, t in zip(curr['date'], curr['avg_temp_c'])
]
fig.add_trace(go.Scatter(
    x=curr['day_of_year'],
    y=curr['avg_temp_c'],
    mode='lines',
    name=str(current_year),
    line=dict(color='#f97316', width=2.5),
    hovertext=hover_curr,
    hoverinfo='text',
))

fig.update_layout(
    title={
        'text': (
            f'Digby, NS — {current_year} Temperature vs Historical Average'
            f'<br><sub>Shaded area shows the {prior_years[0]}–{prior_years[-1]} daily min–max range</sub>'
        ),
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 18},
    },
    xaxis_title='Month',
    yaxis_title='Average Temperature (°C)',
    hovermode='x unified',
    width=1400,
    height=700,
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.02,
        xanchor='center',
        x=0.5,
        bgcolor='rgba(255,255,255,0.8)',
        bordercolor='gray',
        borderwidth=1,
    ),
    plot_bgcolor='white',
    xaxis=dict(
        showgrid=True,
        gridcolor='lightgray',
        gridwidth=0.5,
        range=[1, 366],
        tickmode='array',
        tickvals=[1, 32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335],
        ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='lightgray',
        gridwidth=0.5,
    ),
)

html_content = fig.to_html(full_html=True, include_plotlyjs=True,
                           div_id='vs-average-chart')

nav_style = '''
<style>
    .nav-bar {
        background: #1a1c2e;
        padding: 10px 20px;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    .nav-bar a {
        color: #c4b5fd;
        text-decoration: none;
        font-size: 14px;
    }
    .nav-bar a:hover { text-decoration: underline; }
</style>
'''
nav_html = '<div class="nav-bar"><a href="index.html">&larr; Back to Dashboard</a></div>'
html_content = html_content.replace('</head>', nav_style + '</head>')
html_content = html_content.replace('<body>', '<body>' + nav_html)

with open(OUTPUT_HTML, 'w') as f:
    f.write(html_content)

print(f"\n✓ Saved to {OUTPUT_HTML}")

# Quick comparison stats
merged = curr.merge(hist_stats[['day_of_year', 'avg']], on='day_of_year', how='left')
diff = (merged['avg_temp_c'] - merged['avg']).mean()
direction = 'warmer' if diff > 0 else 'cooler'
print(f"\n{current_year} is running {abs(diff):.1f}°C {direction} than the historical average so far.")
print("✓ Done!")
