# Interactive Visualization Plan

## Goal
Create interactive temperature visualizations where users can click on years in the legend to show/hide them from the chart.

## Current State
- Static PNG images generated using matplotlib
- All visualizations are non-interactive
- Images viewed locally or embedded in documents

## Recommended Approach: Plotly

### Why Plotly?
1. **Python-based** - Integrates seamlessly with existing codebase
2. **Browser-based** - Generates standalone HTML files (no server needed)
3. **Built-in interactivity** - Legend click-to-toggle is native functionality
4. **Easy migration** - Similar API to matplotlib
5. **Rich features** - Hover tooltips, zoom, pan, export options
6. **No hosting required** - HTML files can be opened directly in any browser

### What Would Change?

#### Dependencies
Add to `requirements.txt`:
```
plotly>=5.14.0
```

#### Code Changes
- Create new Python scripts (e.g., `plot_interactive_by_year.py`)
- Replace `matplotlib.pyplot` with `plotly.graph_objects` or `plotly.express`
- Output HTML files instead of PNG images
- Keep existing matplotlib scripts for static images

#### Output Files
- `digby_temperature_by_year_interactive.html` - Interactive year comparison
- `yearly_high_low_average_interactive.html` - Interactive high/low chart
- Can still generate PNG versions for reports/documents

### Implementation Example

**Before (matplotlib):**
```python
import matplotlib.pyplot as plt

plt.figure(figsize=(15, 8))
plt.plot(x, y, label='2020')
plt.savefig('output.png')
```

**After (plotly):**
```python
import plotly.graph_objects as go

fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y, name='2020', mode='lines'))
fig.write_html('output.html')
```

### Key Features Available

1. **Legend Click Behavior**
   - Single click: Hide/show individual year
   - Double click: Isolate single year (hide all others)
   
2. **Built-in Tools**
   - Zoom and pan
   - Hover tooltips showing exact values
   - Export to PNG (via toolbar)
   - Reset axes

3. **Customization**
   - Custom colors (keep existing palette)
   - Responsive layout
   - Dark/light themes
   - Custom hover text

### Workflow

1. **Install Plotly:**
   ```bash
   pip3 install plotly
   ```

2. **Create Interactive Scripts:**
   - `plot_interactive_by_year.py` - Main year comparison
   - `plot_interactive_monthly.py` - Monthly averages
   - `plot_interactive_high_low.py` - High/low averages

3. **View Results:**
   - Double-click HTML file to open in default browser
   - Or right-click → "Open with" → choose browser

4. **Share:**
   - Send HTML files via email
   - Host on GitHub Pages
   - Embed in local documentation

## Alternative Approaches

### Option 2: Bokeh
- Python-based interactive visualizations
- Similar capabilities to Plotly
- Slightly more complex API
- Less commonly used than Plotly

### Option 3: JavaScript (D3.js, Chart.js)
- More control over interactivity
- Requires JavaScript knowledge
- More development time
- Separate from Python workflow

### Option 4: Dash (Plotly)
- Full web application framework
- Requires running a server
- Overkill for simple click-to-toggle
- Better for complex dashboards

## Recommended Implementation Plan

### Phase 1: Single Interactive Chart
1. Install Plotly
2. Create `plot_interactive_by_year.py` (convert year comparison)
3. Test HTML output in browser
4. Verify legend click functionality works

### Phase 2: Additional Charts
5. Convert `plot_yearly_high_low_average.py` to interactive version
6. Convert `plot_monthly_average_temp.py` to interactive version
7. Update README with interactive visualization instructions

### Phase 3: Enhancement (Optional)
8. Add custom hover tooltips (show date, temp, year)
9. Add range selector for date filtering
10. Combine multiple charts into single HTML dashboard

## Pros and Cons

### Pros ✓
- No server or hosting required
- Works offline (HTML files are self-contained)
- Professional, polished appearance
- Easy to share (just send HTML file)
- Maintains all existing static PNG workflows
- Minimal code changes needed

### Cons ✗
- HTML files are larger than PNGs (~1-5 MB vs ~100 KB)
- Requires modern web browser
- One more dependency to install
- Slight learning curve for plotly syntax

## Questions to Consider

1. **Which visualizations to make interactive?**
   - All of them?
   - Just the year-by-year comparison?
   - Only the most complex ones?

2. **Keep static versions?**
   - Yes for backwards compatibility
   - Yes for embedding in documents/presentations
   - Interactive as primary, static as backup

3. **File naming convention?**
   - `*_interactive.html` suffix?
   - Separate `interactive/` folder?
   - Replace existing outputs entirely?

4. **Hosting preferences?**
   - Local files only
   - GitHub Pages for online viewing
   - Both options available

## Estimated Effort

- **Setup & first chart:** 30-45 minutes
- **Additional charts:** 15-20 minutes each
- **Testing & refinement:** 30 minutes
- **Documentation:** 15 minutes

**Total:** ~2-3 hours for full implementation

## Next Steps

Let me know:
1. Do you want to proceed with Plotly approach?
2. Which visualizations should be interactive (all, or specific ones)?
3. Keep the static PNG versions too?
4. Any specific interactive features you want (beyond legend toggle)?
