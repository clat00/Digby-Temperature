# Digby, NS Temperature Data Project

This project fetches historical daily temperature data for Digby, Nova Scotia from 2020-2025 using the WorldWeatherOnline API.

## Setup

1. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

2. **Configure API key:**
   - Open the `.env` file
   - Replace `your_api_key_here` with your actual WorldWeatherOnline API key

## Usage

### Initial Setup: Fetch All Historical Data

Run this **once** to download the complete historical dataset:

```bash
python3 fetch_digby_temperature.py
```

This will:
- Make ~72 API calls (one per month from Jan 2020 - Dec 2025)
- Fetch daily max/min temperatures for Digby, NS
- Save data to `digby_temperature_2020-2025.csv`
- Generate a temperature visualization as `digby_temperature_plot.png`
- Display summary statistics

### Monthly Updates: Add New Data Only

After the initial setup, use this script to add only new months of data:

```bash
python3 update_digby_temperature.py
```

This will:
- Read your existing CSV file
- Find the last recorded date
- **Only fetch data from that date forward** (saves API calls!)
- Append new data to the CSV
- Regenerate the updated plot
- Display what was added

**Run this monthly** to keep your dataset current without re-downloading everything.

### Regenerate Visualizations

To create visualizations from existing data without re-fetching:

```bash
python3 visualize_temperature.py
```

#### Additional Visualizations

Generate a plot showing average temperature by month across all years:

```bash
python3 plot_monthly_average_temp.py
```

Generate a plot showing average high/low temperatures for each day of the year:

```bash
python3 plot_yearly_high_low_average.py
```

Generate wind speed and wind direction visualizations:

```bash
python3 visualize_wind.py
```

This creates:
- Wind speed over time with 30-day rolling average
- Monthly average wind speed by year
- Wind rose diagram showing prevailing wind directions

#### Interactive Visualizations

Generate an interactive HTML chart for year-by-year temperature comparison:

```bash
python3 plot_interactive_by_year.py
```

This creates an interactive chart where you can:
- Click legend items to show/hide individual years
- Double-click a legend item to isolate that year
- Hover over lines to see exact dates and temperatures
- Zoom, pan, and export the chart

Generate interactive wind charts (monthly average speed and peak gusts):

```bash
python3 plot_interactive_wind.py
```

Open the generated HTML files in any web browser to interact with them.

## Output Files

- `digby_temperature_2020-2025.csv` - Daily temperature and wind data
- `digby_temperature_plot.png` - Temperature visualization (all years)
- `digby_temperature_by_year.png` - Year-by-year comparison (static)
- `digby_temperature_by_year_interactive.html` - Year-by-year comparison (interactive)
- `march_vs_november_comparison.png` - Seasonal comparison (March vs November)
- `monthly_average_temperature.png` - Average temperature by day of year
- `yearly_high_low_average.png` - Average high/low temperatures across the year
- `digby_wind_speed.png` - Wind speed over time and monthly averages
- `digby_wind_rose.png` - Wind direction frequency (wind rose diagram)
- `digby_wind_speed_interactive.html` - Monthly average wind speed by year (interactive)
- `digby_wind_gusts_interactive.html` - Peak wind gusts by year (interactive)

## Data Included

Each day includes:
- Date
- Maximum temperature (°C and °F)
- Minimum temperature (°C and °F)  
- Average temperature (°C and °F)
- UV index
- Sun hours
- Wind speed (km/h)
- Wind direction (16-point compass)
- Wind gust speed (km/h)

## Project Files

- `.env` - API key configuration (never commit this!)
- `fetch_digby_temperature.py` - **Initial full dataset fetch** (run once)
- `update_digby_temperature.py` - **Incremental updates** (run monthly)
- `visualize_temperature.py` - Generate visualizations from existing data
- `visualize_by_year.py` - Create year-by-year comparison plots (static PNG)
- `plot_interactive_by_year.py` - Create interactive year-by-year chart (HTML)
- `compare_march_november.py` - Compare March vs November temperatures
- `plot_monthly_average_temp.py` - Plot average temperature by day of year
- `plot_yearly_high_low_average.py` - Plot average high/low temperatures across the year
- `analyze_cold_days.py` - Analyze cold temperature patterns
- `analyze_extreme_cold_days.py` - Analyze extreme cold events
- `analyze_january_patterns.py` - Analyze January temperature patterns
- `requirements.txt` - Python dependencies
- `.gitignore` - Protects sensitive files

## Workflow Recommendation

1. **First time:** Run `fetch_digby_temperature.py` to get all historical data (2020-2025)
2. **Monthly:** Run `update_digby_temperature.py` to add only new data since last update
3. **Anytime:** Run visualization scripts to explore the data

This approach minimizes API calls and keeps your data current!

## API Usage

- Uses WorldWeatherOnline Historical Weather API
- Free tier supports 500 calls/month
- Initial fetch: ~72 calls for 6 years of data (2020-2025)
- Monthly updates: ~1 call per update
- Data available from July 2008 onwards

## API Documentation

https://www.worldweatheronline.com/weather-api/api/docs/historical-weather-api.aspx

