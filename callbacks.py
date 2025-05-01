from dash import Input, Output
import plotly.express as px
import pandas as pd

# Load data
df = pd.read_csv("data/ocean_climate_dataset.csv")
df['Year'] = pd.to_datetime(df['Date']).dt.year

def register_callbacks(app):
    @app.callback(
        Output('avg-sst', 'children'),
        Output('bleaching-pct', 'children'),
        Output('avg-species', 'children'),
        Output('heatwave-count', 'children'),
        Output('left-line-graph', 'figure'),
        Output('right-line-graph', 'figure'),
        Output('bleaching-trend', 'figure'),
        Input('location-dropdown', 'value'),
        Input('year-slider', 'value'),
        Input('graph-type-left', 'value'),
        Input('graph-type-right', 'value')
    )
    def update_dashboard(selected_location, year_range, graph_left, graph_right):
        start, end = year_range
        filtered = df[(df['Year'] >= start) & (df['Year'] <= end)]

        if selected_location != 'All':
            filtered = filtered[filtered['Location'] == selected_location]

        avg_sst = round(filtered['SST (°C)'].mean(), 2)
        bleaching_pct = round(
            (filtered['Bleaching Severity'].isin(['Medium', 'High']).sum() / len(filtered)) * 100, 1
        ) if len(filtered) > 0 else 0
        avg_species = round(filtered['Species Observed'].mean(), 1) if len(filtered) > 0 else 0
        heatwave_count = int(filtered['Marine Heatwave'].sum()) if len(filtered) > 0 else 0

        def generate_line_graph(column_name):
            if column_name in filtered.columns:
                data = filtered.groupby('Year')[column_name].mean().reset_index()
                return px.line(data, x='Year', y=column_name, title=f'{column_name} Over Time - {selected_location}',
                               markers=True)
            else:
                return px.line(title=f"{column_name} not found")

        left_fig = generate_line_graph(graph_left)
        right_fig = generate_line_graph(graph_right)

        bleach_counts = filtered.groupby(['Year', 'Bleaching Severity']).size().reset_index(name='Number of Observations')
        bleach_fig = px.bar(
            bleach_counts, x='Year', y='Number of Observations', color='Bleaching Severity',
            title=f'Bleaching Severity Trends - {selected_location}',
            category_orders={'Bleaching Severity': ['None', 'Low', 'Medium', 'High']},
            color_discrete_sequence=['#91c9f7', '#ffe28a', '#ffa15a', '#d9534f']
        )

        return (
            f"{avg_sst} (°C)",
            f"{bleaching_pct}%",
            f"{avg_species}",
            f"{heatwave_count}",
            left_fig,
            right_fig,
            bleach_fig
        )