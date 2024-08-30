# Economic Indicators Dashboard

## Description
This project is an interactive dashboard that displays key economic indicators fetched from the Federal Reserve Economic Data (FRED) API. It provides visualizations for GDP, Unemployment Rate, Inflation Rate, and Federal Funds Rate, allowing users to track economic trends over time.

## Features
- Fetches real-time data from the FRED API
- Displays individual graphs for each economic indicator
- Provides an overview chart with all indicators
- Interactive dropdown to select specific indicators
- Data is stored in a SQLite database for quick access and historical tracking

## Technologies Used
- Python 3.x
- Pandas for data manipulation
- Plotly and Dash for interactive visualizations
- SQLite for data storage
- Requests library for API calls

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/Economic-Dashboard.git
   cd Economic-Dashboard
   ```

2. Install the required packages:
   ```
   pip install numpy==1.23.0
   pip install pandas requests plotly dash
   ```

3. Set up your FRED API key:
   - Sign up for a FRED API key at https://fred.stlouisfed.org/docs/api/api_key.html
   - Replace `"YOUR_API_KEY"` in the script with your actual API key

## Usage

1. Run the script:
   ```
   python economic_dashboard.py
   ```

2. Open a web browser and go to `http://127.0.0.1:8050/` to view the dashboard

## Dashboard Components
- **Indicator Dropdown**: Select a specific economic indicator to view
- **Individual Indicator Graph**: Displays the selected indicator's data over time
- **All Indicators Graph**: Shows all four main indicators in a single view

## Data Update
The dashboard fetches the latest available data each time it's run. The data is then stored in a local SQLite database for faster subsequent access.

## Contributing
Contributions to improve the dashboard are welcome. Please feel free to submit a Pull Request.

## License
This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments
- Data provided by Federal Reserve Economic Data (FRED)
- Built with Plotly Dash
