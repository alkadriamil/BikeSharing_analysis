# Bike Rental Analysis Dashboard

## Description
This Streamlit dashboard provides an interactive analysis of bike rental data. It visualizes various aspects of bike rental patterns, including seasonal trends, weather impacts, and user behavior.

## Features
- Year and season selection filters
- Key performance indicators (KPIs)
- Monthly rental trend visualization
- Seasonal rental pattern analysis
- Weather impact on rentals
- Comparison of weekday vs weekend rentals
- Additional insights and recommendations

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/your-username/bike-rental-dashboard.git
   ```
2. Navigate to the project directory:
   ```
   cd bike-rental-dashboard
   ```
3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the dashboard locally:

```
streamlit run dashboard.py
```

Then, open your web browser and go to `http://localhost:8501`.

## Data

The dashboard uses two CSV files:
- `hour.csv`: Hourly bike rental data
- `day.csv`: Daily bike rental data

Make sure these files are in the correct location as specified in the `load_data()` function.

## Dependencies

- streamlit
- pandas
- matplotlib
- seaborn

See `requirements.txt` for specific versions.

## Author

Amil Al Kadri
