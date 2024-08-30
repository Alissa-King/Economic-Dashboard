# Economic Indicator Dashboard

This project is a Dash application that displays key economic indicators using data from the Federal Reserve Economic Database (FRED).

## Setup and Running

1. Clone this repository.
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
3. Replace `"YOUR_FRED_API_KEY"` in `economic_dashboard.py` with your actual FRED API key.
4. Run the script:
   ```
   python economic_dashboard.py
   ```
5. Open a web browser and go to `http://localhost:8050` (or the URL provided in the console output).

## Features

- Data collection from FRED API
- Data processing and storage in SQLite database
- Interactive visualizations using Plotly and Dash
- Single indicator and multi-indicator views

## License

This project is open source and available under the [MIT License](LICENSE).
