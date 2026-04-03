# Update Checklist

Steps to pull the latest weather data, regenerate all charts, and publish to GitHub Pages.

## 1. Fetch new data

```bash
python3 update_digby_temperature.py
```

This downloads any new days since the last update and regenerates the static temperature plot.

## 2. Regenerate interactive charts

```bash
python3 plot_interactive_by_year.py
python3 plot_interactive_wind.py
```

These rebuild the three interactive HTML files served on GitHub Pages:
- `digby_temperature_by_year_interactive.html`
- `digby_wind_speed_interactive.html`
- `digby_wind_gusts_interactive.html`

## 3. Push to GitHub Pages

```bash
git add -A
git commit -m "Add <month> <year> data and regenerate charts"
git push
```
