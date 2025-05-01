
from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd

# Load data
df = pd.read_csv("data/ocean_climate_dataset.csv")
df['Year'] = pd.to_datetime(df['Date']).dt.year

def create_layout():
    return html.Div([
                html.H2("Coral Reef Health Dashboard", style={'textAlign': 'center', 'marginBottom': 30}),

                html.Div([
                    html.Label("Select a Reef Location:", style={'font-weight': 'bold'}),
                    dcc.Dropdown(
                        id='location-dropdown',
                        options=[{'label': loc, 'value': loc} for loc in sorted(df['Location'].unique())] + [{'label': 'All Locations', 'value': 'All'}],
                        value='All',
                        clearable=False,
                        style={'width': '60%', 'margin': '0 auto', 'marginBottom': 20}
                    )
                ]),

                dcc.RangeSlider(
                    id='year-slider',
                    min=df['Year'].min(),
                    max=df['Year'].max(),
                    value=[2015, 2020],
                    marks={str(year): str(year) for year in sorted(df['Year'].unique())},
                    step=1,
                    tooltip={"placement": "bottom", "always_visible": True}
                ),

                html.Br(),

                dbc.Row([
                    dbc.Col(dbc.Card([
                        dbc.CardHeader("Avg SST (°C)"),
                        dbc.CardBody(html.H4(id='avg-sst', className="card-text"))
                    ], color="primary", inverse=True)),
                    dbc.Col(dbc.Card([
                        dbc.CardHeader(" Bleaching % (Med+High)"),
                        dbc.CardBody(html.H4(id='bleaching-pct', className="card-text"))
                    ], color="danger", inverse=True)),
                    dbc.Col(dbc.Card([
                        dbc.CardHeader(" Avg Species Observed"),
                        dbc.CardBody(html.H4(id='avg-species', className="card-text"))
                    ], color="success", inverse=True)),
                    dbc.Col(dbc.Card([
                        dbc.CardHeader(" Heatwave Events"),
                        dbc.CardBody(html.H4(id='heatwave-count', className="card-text"))
                    ], color="warning", inverse=True)),
                ], className="mb-4"),

                # Graph Type Selection
                dbc.Row([
                    dbc.Col(dcc.Dropdown(
                        id='graph-type-left',
                        options=[
                            {'label': 'SST (°C)', 'value': 'SST (°C)'},
                            {'label': 'pH Level', 'value': 'pH Level'},
                            {'label': 'Species Observed', 'value': 'Species Observed'}
                        ],
                        value='SST (°C)',
                        clearable=False
                    )),
                    dbc.Col(dcc.Dropdown(
                        id='graph-type-right',
                        options=[
                            {'label': 'SST (°C)', 'value': 'SST (°C)'},
                            {'label': 'pH Level', 'value': 'pH Level'},
                            {'label': 'Species Observed', 'value': 'Species Observed'}
                        ],
                        value='pH Level',
                        clearable=False
                    ))
                ], className="mb-3"),

                dbc.Row([
                    dbc.Col(dcc.Graph(id='left-line-graph'), md=6),
                    dbc.Col(dcc.Graph(id='right-line-graph'), md=6)
                ]),

                dbc.Row([
                    dbc.Col(dcc.Graph(id='bleaching-trend'), width=12)
                ])
            ], style={'padding': '20px'})