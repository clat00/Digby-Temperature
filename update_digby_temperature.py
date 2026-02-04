"""
Digby, NS Temperature Data - Incremental Update Script

This script updates the existing CSV file by only fetching new data
since the last recorded date, avoiding redundant API calls.

Requirements:
- API key stored in .env file
- Run: pip install -r requirements.txt
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import time
from calendar import monthrange
import matplotlib.pyplot as plt

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv('WEATHER_API_KEY')

if not API_KEY or API_KEY == 'your_api_key_here':
    raise ValueError("Please set your API key in the .env file")

# Configuration
BASE_URL = "https://api.worldweatheronline.com/premium/v1/past-weather.ashx"
LOCATION = "Digby,Nova Scotia,Canada"
CSV_FILE = "digby_temperature_2020-2025.csv"
PLOT_FILE = "digby_temperature_plot.png"

print("="*60)
print("Digby Temperature Data - Incremental Update")
print("="*60)

# Check if CSV exists
if not os.path.exists(CSV_FILE):
    print(f"\n❌ Error: {CSV_FILE} not found!")
    print("Please run fetch_digby_temperature.py first to create the initial dataset.")
    exit(1)

# Read existing data
print(f"\n📂 Reading existing data from {CSV_FILE}...")
df_existing = pd.read_csv(CSV_FILE)
df_existing['date'] = pd.to_datetime(df_existing['date'])

# Find the last date in the dataset
last_date = df_existing['date'].max()
print(f"Last recorded date: {last_date.date()}")

# Calculate the date to start fetching from (day after last date)
start_date = last_date + timedelta(days=1)
today = datetime.now().date()

print(f"Today's date: {today}")
print(f"Need to fetch: {start_date.date()} to {today}")

# Check if there's new data to fetch
if start_date.date() > today:
    print("\n✓ Data is already up to date! No new data to fetch.")
    exit(0)

# Calculate months to fetch
months_to_fetch = []
current = start_date
while current.date() <= today:
    months_to_fetch.append((current.year, current.month))
    # Move to next month
    if current.month == 12:
        current = datetime(current.year + 1, 1, 1)
    else:
        current = datetime(current.year, current.month + 1, 1)

# Remove duplicates while preserving order
months_to_fetch = list(dict.fromkeys(months_to_fetch))

print(f"\nMonths to fetch: {len(months_to_fetch)}")
for year, month in months_to_fetch:
    print(f"  - {year}-{month:02d}")


def fetch_month_data(year, month, api_key):
    """
    Fetch weather data for a specific month.
    """
    # Get first and last day of month
    first_day = f"{year}-{month:02d}-01"
    last_day_num = monthrange(year, month)[1]
    last_day = f"{year}-{month:02d}-{last_day_num:02d}"
    
    params = {
        'q': LOCATION,
        'date': first_day,
        'enddate': last_day,
        'tp': '24',  # Daily intervals
        'format': 'json',
        'key': api_key
    }
    
    try:
        print(f"  Fetching {year}-{month:02d}...", end=' ')
        response = requests.get(BASE_URL, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # Check for API errors
        if 'data' not in data:
            print(f"ERROR: {data.get('error', 'Unknown error')}")
            return None
        
        weather_data = data['data'].get('weather', [])
        print(f"✓ ({len(weather_data)} days)")
        
        return weather_data
        
    except requests.exceptions.RequestException as e:
        print(f"ERROR: {e}")
        return None


# Fetch new data
print("\n" + "="*60)
print("Fetching new data from API...")
print("="*60)

new_records = []
for year, month in months_to_fetch:
    month_data = fetch_month_data(year, month, API_KEY)
    
    if month_data:
        # Extract daily records
        for day in month_data:
            day_date = datetime.strptime(day['date'], '%Y-%m-%d').date()
            
            # Only include dates after our last recorded date and up to today
            if day_date >= start_date.date() and day_date <= today:
                # Get hourly data for wind averages (if available)
                hourly = day.get('hourly', [{}])
                
                # Calculate average wind speed from hourly data
                wind_speeds = [float(h.get('windspeedKmph', 0)) for h in hourly if h.get('windspeedKmph')]
                avg_wind_speed = sum(wind_speeds) / len(wind_speeds) if wind_speeds else 0
                
                record = {
                    'date': day['date'],
                    'max_temp_c': int(day['maxtempC']),
                    'min_temp_c': int(day['mintempC']),
                    'max_temp_f': int(day['maxtempF']),
                    'min_temp_f': int(day['mintempF']),
                    'avg_temp_c': (int(day['maxtempC']) + int(day['mintempC'])) / 2,
                    'avg_temp_f': (int(day['maxtempF']) + int(day['mintempF'])) / 2,
                    'uv_index': day.get('uvIndex', ''),
                    'sun_hour': day.get('sunHour', ''),
                    'wind_speed_kmph': round(avg_wind_speed, 1),
                    'wind_direction': hourly[0].get('winddir16Point', '') if hourly else '',
                    'wind_gust_kmph': float(hourly[0].get('WindGustKmph', 0)) if hourly and hourly[0].get('WindGustKmph') else 0
                }
                new_records.append(record)
    
    # Be nice to the API - small delay between requests
    time.sleep(0.5)

print(f"\n{'='*60}")
print(f"New days retrieved: {len(new_records)}")

if len(new_records) == 0:
    print("✓ No new data to add. File is up to date!")
    exit(0)

# Convert new data to DataFrame
df_new = pd.DataFrame(new_records)
df_new['date'] = pd.to_datetime(df_new['date'])

# Combine with existing data
df_combined = pd.concat([df_existing, df_new], ignore_index=True)

# Sort by date and remove any potential duplicates
df_combined = df_combined.sort_values('date')
df_combined = df_combined.drop_duplicates(subset=['date'], keep='last')

# Display summary
print("\n" + "="*60)
print("Updated Dataset Summary:")
print("="*60)
print(f"Date range: {df_combined['date'].min().date()} to {df_combined['date'].max().date()}")
print(f"Total days: {len(df_combined)}")
print(f"New days added: {len(df_new)}")

print(f"\nNew data preview:")
print(df_new[['date', 'max_temp_c', 'min_temp_c', 'avg_temp_c']].head(10))

# Save updated CSV
df_combined.to_csv(CSV_FILE, index=False)
print(f"\n{'='*60}")
print(f"✓ Updated data saved to {CSV_FILE}")
print(f"File size: {os.path.getsize(CSV_FILE) / 1024:.1f} KB")
print("="*60)

# Regenerate the plot with updated data
print("\nRegenerating temperature visualization...")
plt.figure(figsize=(15, 6))
plt.plot(df_combined['date'], df_combined['max_temp_c'], label='Max Temp', alpha=0.7, color='red')
plt.plot(df_combined['date'], df_combined['min_temp_c'], label='Min Temp', alpha=0.7, color='blue')
plt.fill_between(df_combined['date'], df_combined['min_temp_c'], df_combined['max_temp_c'], alpha=0.2, color='gray')
plt.xlabel('Date')
plt.ylabel('Temperature (°C)')
plt.title(f'Digby, NS Daily Temperature ({df_combined["date"].min().year}-{df_combined["date"].max().year})')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(PLOT_FILE, dpi=300, bbox_inches='tight')
print(f"✓ Updated plot saved to {PLOT_FILE}")
plt.close()

print("\n✓ All done!")
print("\nNext time you want to update, just run this script again!")

