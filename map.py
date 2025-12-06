from data_store import processed_data_only_countries

import pandas as pd
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
from dash.exceptions import PreventUpdate


def create_ghg_layout():

    data = processed_data_only_countries

    # Select a all unique years available in the dataset
    available_years = sorted(data['year'].dropna().unique())

    # For simplicity, we will visulize data for a specific year when the app loads.
    last_year = available_years[-1] # Last year available in the dataset




    layout = html.Div([
        html.H1(id ='map-title', children='Y-axis attribute visualized', style={'textAlign':'center'}),

         dcc.Graph(id='ghg-map'),
    
        html.Div([
            html.Label("Select Year:"),
            dcc.RangeSlider(
                id='year-slider',
                min=min(available_years),
                max=max(available_years),
                value=[min(available_years), last_year],
                marks=None,
                step=1,
                tooltip={"placement": "bottom", "always_visible": True},
        
        )
    ])
])
    return layout

@callback(
    Output('map-title', 'children'),
    Input('dropdown-selection-y', 'value')
)
def update_map_title(y_attr):
    if (y_attr is None) or (y_attr in ["country", "year"]):
        return "Y-axis attribute visualized"
    return f"Visualization of {y_attr} across countries (based on attribute selected on Y-axis)"

# Get the callback to update the map based on the selected year
@callback(
    Output('ghg-map', 'figure'),
    Input('year-slider', 'value'),
    Input('dropdown-selection-y', 'value')
)
def update_map(selected_year, y_attr):
    year_to_show = int(selected_year[1])
    filtered_df = processed_data_only_countries[processed_data_only_countries['year'] == year_to_show].copy()
    
    if (y_attr is None) or (y_attr in ["country", "year"]):
        raise PreventUpdate
    
    fig = px.choropleth(
        filtered_df,
        locations="country",
        locationmode='country names',
        color=y_attr,
        hover_name="country",
        projection="natural earth",
        title=f"{y_attr} in {year_to_show}",
)
    fig.update_layout(
        geo=dict(
            showland=True,
            landcolor="lightgreen",
            showcountries=True,
            countrycolor="Black"
        )
    )
    return fig










