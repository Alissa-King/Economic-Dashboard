import requests
import pandas as pd
import sqlite3
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from datetime import datetime

# Configuration
FRED_API_KEY = "YOUR_FRED_API_KEY"  # Replace with your actual API key
INDICATORS = {
    "GDP": "GDP",
    "Unemployment Rate": "UNRATE",
    "Inflation Rate": "CPIAUCSL",
    "Federal Funds Rate": "FEDFUNDS"
}
START_DATE = "2000-01-01"
END_DATE = datetime.now().strftime("%Y-%m-%d")

# Data Collection
class FREDDataCollector:
    def __init__(self, api_key):
        self.base_url = "https://api.stlouisfed.org/fred/series/observations"
        self.api_key = api_key

    def get_data(self, series_id, start_date, end_date):
        params = {
            "series_id": series_id,
            "api_key": self.api_key,
            "file_type": "json",
            "observation_start": start_date,
            "observation_end": end_date
        }
        response = requests.get(self.base_url, params=params)
        data = response.json()
        
        df = pd.DataFrame(data['observations'])
        df['date'] = pd.to_datetime(df['date'])
        df['value'] = pd.to_numeric(df['value'], errors='coerce')
        df = df.set_index('date')
        return df[['value']]

def collect_data(api_key, indicators, start_date, end_date):
    collector = FREDDataCollector(api_key)
    data = {}
    for name, series_id in indicators.items():
        data[name] = collector.get_data(series_id, start_date, end_date)
        print(f"Collected data for {name}")
    return pd.concat(data.values(), axis=1, keys=data.keys())

# Data Processing
def process_data(df):
    df = df.resample('M').last()
    df = df.fillna(method='ffill')
    df['GDP_YoY'] = df['GDP'].pct_change(periods=12)
    df['Inflation_YoY'] = df['Inflation Rate'].pct_change(periods=12)
    df['Unemployment_MA3'] = df['Unemployment Rate'].rolling(window=3).mean()
    return df

# Database Operations
def create_database():
    conn = sqlite3.connect('economic_indicators.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS indicators
                 (date TEXT, indicator TEXT, value REAL)''')
    conn.commit()
    return conn

def insert_data(conn, df):
    for column in df.columns:
        data = df[column].reset_index()
        data.columns = ['date', 'value']
        data['indicator'] = column
        data.to_sql('indicators', conn, if_exists='append', index=False)

def get_data_from_db():
    conn = sqlite3.connect('economic_indicators.db')
    return pd.read_sql_query("SELECT * FROM indicators", conn, parse_dates=['date'])

# Visualization
def create_charts(df):
    fig = make_subplots(rows=2, cols=2, subplot_titles=("GDP", "Unemployment Rate", "Inflation Rate", "Federal Funds Rate"))
    fig.add_trace(go.Scatter(x=df.index, y=df['GDP'], name="GDP"), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['Unemployment Rate'], name="Unemployment Rate"), row=1, col=2)
    fig.add_trace(go.Scatter(x=df.index, y=df['Inflation Rate'], name="Inflation Rate"), row=2, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['Federal Funds Rate'], name="Federal Funds Rate"), row=2, col=2)
    fig.update_layout(height=800, width=1000, title_text="Economic Indicators Dashboard")
    return fig

# Main execution
print("Collecting data...")
all_data = collect_data(FRED_API_KEY, INDICATORS, START_DATE, END_DATE)

print("Processing data...")
processed_data = process_data(all_data)

print("Storing data in database...")
conn = create_database()
insert_data(conn, processed_data)
conn.close()

print("Data collection and storage complete. Starting dashboard...")

# Dash App
app = dash.Dash(__name__)

df = get_data_from_db()

app.layout = html.Div([
    html.H1("Economic Indicators Dashboard"),
    dcc.Dropdown(
        id='indicator-dropdown',
        options=[{'label': i, 'value': i} for i in df['indicator'].unique()],
        value='GDP'
    ),
    dcc.Graph(id='indicator-graph'),
    dcc.Graph(id='all-indicators-graph')
])

@app.callback(
    Output('indicator-graph', 'figure'),
    Input('indicator-dropdown', 'value')
)
def update_graph(selected_indicator):
    filtered_df = df[df['indicator'] == selected_indicator]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=filtered_df['date'], y=filtered_df['value'], mode='lines', name=selected_indicator))
    fig.update_layout(title=f'{selected_indicator} Over Time', xaxis_title='Date', yaxis_title='Value')
    return fig

@app.callback(
    Output('all-indicators-graph', 'figure'),
    Input('indicator-dropdown', 'value')
)
def update_all_indicators_graph(dummy):
    return create_charts(df.pivot(index='date', columns='indicator', values='value'))

if __name__ == '__main__':
    app.run_server(debug=True)
