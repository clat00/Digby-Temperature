"""
Digby, NS Historical Temperature Data Fetcher

This script fetches daily temperature data for Digby, Nova Scotia 
from 2023-2025 using the WorldWeatherOnline API.

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

print("API key loaded successfully!")

# Configuration
BASE_URL = "https://api.worldweatheronline.com/premium/v1/past-weather.ashx"
LOCATION = "Digby,Nova Scotia,Canada"
START_YEAR = 2023
END_YEAR = 2025
OUTPUT_FILE = "digby_temperature_2023-2025.csv"

print(f"Location: {LOCATION}")
print(f"Time range: {START_YEAR} - {END_YEAR}")
print(f"Output file: {OUTPUT_FILE}")


def fetch_month_data(year, month, api_key):
    """
    Fetch weather data for a specific month.
    
    Args:
        year: Year (e.g., 2023)
        month: Month (1-12)
        api_key: WorldWeatherOnline API key
    
    Returns:
        List of daily weather records or None if error
    """
    # Get first and last day of month
    first_day = f"{year}-{month:02d}-01"
    last_day_num = monthrange(year, month)[1]
    last_day = f"{year}-{month:02d}-{last_day_num:02d}"
    
    # Skip future dates
    today = datetime.now().date()
    if datetime.strptime(first_day, "%Y-%m-%d").date() > today:
        print(f"  Skipping {year}-{month:02d} (future date)")
        return None
    
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


# Fetch data for all months
print("\n" + "="*50)
print("Starting data fetch...")
print("="*50)

all_records = []
total_requests = 0

for year in range(START_YEAR, END_YEAR + 1):
    print(f"\nFetching {year}:")
    for month in range(1, 13):
        month_data = fetch_month_data(year, month, API_KEY)
        
        if month_data:
            # Extract daily records
            for day in month_data:
                record = {
                    'date': day['date'],
                    'max_temp_c': int(day['maxtempC']),
                    'min_temp_c': int(day['mintempC']),
                    'max_temp_f': int(day['maxtempF']),
                    'min_temp_f': int(day['mintempF']),
                    'avg_temp_c': (int(day['maxtempC']) + int(day['mintempC'])) / 2,
                    'avg_temp_f': (int(day['maxtempF']) + int(day['mintempF'])) / 2,
                    'uv_index': day.get('uvIndex', ''),
                    'sun_hour': day.get('sunHour', '')
                }
                all_records.append(record)
        
        total_requests += 1
        
        # Be nice to the API - small delay between requests
        time.sleep(0.5)

print(f"\n{'='*50}")
print(f"Total API requests made: {total_requests}")
print(f"Total days retrieved: {len(all_records)}")

# Convert to DataFrame
df = pd.DataFrame(all_records)

# Sort by date
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date')

# Display summary statistics
print("\n" + "="*50)
print("Data Summary:")
print("="*50)
print(f"Date range: {df['date'].min().date()} to {df['date'].max().date()}")
print(f"Total days: {len(df)}")
print(f"\nTemperature Statistics (Celsius):")
print(df[['max_temp_c', 'min_temp_c', 'avg_temp_c']].describe())

# Display first few rows
print("\nFirst 10 rows:")
print(df.head(10))

# Save to CSV
df.to_csv(OUTPUT_FILE, index=False)
print(f"\n{'='*50}")
print(f"✓ Data saved to {OUTPUT_FILE}")
print(f"File size: {os.path.getsize(OUTPUT_FILE) / 1024:.1f} KB")
print("="*50)

# Quick visualization (optional - comment out if you don't want the plot to display)
print("\nGenerating temperature visualization...")
plt.figure(figsize=(15, 6))
plt.plot(df['date'], df['max_temp_c'], label='Max Temp', alpha=0.7, color='red')
plt.plot(df['date'], df['min_temp_c'], label='Min Temp', alpha=0.7, color='blue')
plt.fill_between(df['date'], df['min_temp_c'], df['max_temp_c'], alpha=0.2, color='gray')
plt.xlabel('Date')
plt.ylabel('Temperature (°C)')
plt.title('Digby, NS Daily Temperature (2023-2025)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

# Save the plot instead of showing it
plot_filename = "digby_temperature_plot.png"
plt.savefig(plot_filename, dpi=300, bbox_inches='tight')
print(f"✓ Plot saved to {plot_filename}")
plt.close()

print("\n✓ All done!")

