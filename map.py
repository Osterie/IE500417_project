from data_store import processed_data

import pandas as pd
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px

def create_ghg_layout():


    # Get preprocessed data
    data = processed_data

 
    # We use just the columns that we need for the map. 
    df = data[["year", "country", "total_ghg - Mt"]].dropna()

    # Select a all unique years available in the dataset
    available_years = sorted(df['year'].dropna().unique())

    # For simplicity, we will visulize data for a specific year when the app loads.
    last_year = available_years[-1] # Last year available in the dataset




    layout = html.Div([
        html.H1(children='Global Greenhouse Gas Emissions over time', style={'textAlign':'center'}),

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

# Get the callback to update the map based on the selected year
@callback(
    Output('ghg-map', 'figure'),
    Input('year-slider', 'value')
)
def update_map(selected_year):
    year_to_show = int(selected_year[1])
    filtered_df = processed_data[processed_data['year'] == year_to_show]
    fig = px.choropleth(
        filtered_df,
        locations="country",
        locationmode='country names',
        color="total_ghg",
        hover_name="country",
        projection="natural earth",
        title=f"Total Greenhouse Gas Emissions in {year_to_show}",
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










