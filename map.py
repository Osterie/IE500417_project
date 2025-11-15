from data_reading import preprocess_data
import pandas as pd
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px


def create_ghg_layout(app):

    # Get preprocessed data
    data = preprocess_data()


    # We use just the columns that we need for the map. 
    df = data[["year", "country", "total_ghg"]].dropna()

    # Select a all unique years available in the dataset
    available_years = sorted(df['year'].dropna().unique())

    # For simplicity, we will visulize data for a specific year when the app loads.
    last_year = available_years[-1] # Last year available in the dataset


    layout = html.Div([
        html.H1(children='Gloabal Greenhouse Gas Emissions over time', style={'textAlign':'center'}),

        dcc.Graph(id='ghg-map'),
        
        html.Div([
            html.Label("Select Year:"),
            dcc.Slider(
                id='year-slider',
                min=min(available_years),
                max=max(available_years),
                value=max(available_years),
                # Viser år hvert 5. år på slideren
                marks={str(year): str(year) for year in available_years[::5]},
                step=1,
                tooltip={"placement": "bottom", "always_visible": True},
            )
        ])
    ])

    # Get the callback to update the map based on the selected year
    @callback(
            Output('ghg-map', 'figure'),
            Input('year-slider', 'value')
    )


    def update_map(selected_year):
        filtered_df = df[df['year'] == selected_year]
        
        # Bruker last_year i tittelen fra det ytre skopet (definisjonen over), 
        # men det er mer nøyaktig å bruke selected_year for å reflektere kartet
        fig = px.scatter_geo(
            filtered_df,
            locations="country",
            locationmode='country names',
            color="total_ghg",
            hover_name="country",
            size="total_ghg",
            projection="natural earth",
            title=f"Total Greenhouse Gas Emissions in {selected_year}", 
        )
        fig.update_layout(geo=dict(showland=True, landcolor="LightGreen"))
        return fig

    return layout