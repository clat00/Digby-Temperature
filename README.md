# Digby, NS Temperature Data Project

This project fetches historical daily temperature data for Digby, Nova Scotia from 2023-2025 using the WorldWeatherOnline API.

## Setup

1. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

2. **Configure API key:**
   - Open the `.env` file
   - Replace `your_api_key_here` with your actual WorldWeatherOnline API key

## Usage

### Fetch Temperature Data

Run the main script to fetch data from the API:

```bash
python3 fetch_digby_temperature.py
```

This will:
- Make ~36 API calls (one per month from Jan 2023 - Dec 2025)
- Fetch daily max/min temperatures for Digby, NS
- Save data to `digby_temperature_2023-2025.csv`
- Generate a temperature visualization as `digby_temperature_plot.png`
- Display summary statistics

### Regenerate Visualization

To create visualizations from existing data without re-fetching:

```bash
python3 visualize_temperature.py
```

## Output Files

- `digby_temperature_2023-2025.csv` - Daily temperature data
- `digby_temperature_plot.png` - Temperature visualization

## Data Included

Each day includes:
- Date
- Maximum temperature (°C and °F)
- Minimum temperature (°C and °F)  
- Average temperature (°C and °F)
- UV index
- Sun hours

## Project Files

- `.env` - API key configuration (never commit this!)
- `fetch_digby_temperature.py` - Main script to fetch data from API
- `visualize_temperature.py` - Generate visualizations from existing data
- `requirements.txt` - Python dependencies
- `.gitignore` - Protects sensitive files

## API Usage

- Uses WorldWeatherOnline Historical Weather API
- Free tier supports 100+ calls/month
- This project uses ~36 calls total for 3 years of data
- Data available from July 2008 onwards

## API Documentation

https://www.worldweatheronline.com/weather-api/api/docs/historical-weather-api.aspx

