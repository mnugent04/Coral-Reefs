import dash
import pandas as pd
import dash_bootstrap_components as dbc

from callbacks import register_callbacks
from layout import create_layout

# Load data
df = pd.read_csv("data/ocean_climate_dataset.csv")
df['Year'] = pd.to_datetime(df['Date']).dt.year

# Initialize app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SANDSTONE])
app.title = "Coral Reef Health Dashboard"

# Layout
app.layout = create_layout()

# Callbacks
register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)
